#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta o MP3 de um item de listening a partir de falas soltas.

MOTOR DE VOZ: **edge-TTS da Microsoft** (vozes neurais, gratuito, sem chave de
API). É o mesmo motor que a trilha de espanhol do Listening Lab já usa em
produção, no `portal-aluno-fisk`.

  ⚠️  Histórico, para não se repetir: a primeira tentativa usou o `say` do
  macOS, TTS de geração antiga, e o Pedro reprovou na hora ("absolutamente
  horrorosa"). O erro foi a ferramenta, não a ideia — e a ferramenta certa já
  estava na casa. Se um dia isto falhar, troque só a função `fala()`; a
  montagem abaixo independe de quem dubla.

MONTAGEM, calibrada contra os MP3s do simulado oficial:

  · mono, 96 kbps, 44,1 kHz — idêntico aos arquivos do RED
  · 0,35s entre falas da conversa e 0,9s antes da pergunta do narrador
  · três timbres: dois na conversa e um terceiro no narrador, como no RED

MEDIÇÕES DO RED, para calibrar qualquer voz (10/08/2026, palavras da
transcrição ÷ duração do MP3):

  Part 1  158 palavras/min · 19 conversas curtas · média 25s (17s a 70s)
  Part 2  121 palavras/min ·  4 conversas longas · média 110s
  Part 3  112 palavras/min ·  4 palestras        · média 130s

SEMPRE MEÇA O RESULTADO. O parâmetro de velocidade de qualquer TTS é uma
promessa, não uma medida: no `say`, pedir 165 devolvia 178 palavras por minuto.
Este script imprime o ppm de cada arquivo justamente para fechar esse laço.

FORMATO de cada item da Part 1, copiado do RED: o narrador anuncia o número,
vem a conversa entre duas pessoas e o narrador lê a pergunta no fim.
"""
import asyncio, subprocess, os, sys, json, re
import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'audio', 'magenta')
TMP = '/tmp/fisk-tts'

# As "Multilingual" são a geração mais recente e a mais natural em diálogo.
# Cada item usa um par diferente, como na prova, onde as vozes mudam a cada
# conversa. O narrador é um terceiro timbre, fixo, para o aluno reconhecê-lo.
NARRADOR = 'en-US-AriaNeural'
PARES = {
    'l1-q01': {'W': 'en-US-AvaMultilingualNeural',   'M': 'en-US-AndrewMultilingualNeural'},
    'l1-q02': {'W': 'en-US-EmmaMultilingualNeural',  'M': 'en-US-BrianMultilingualNeural'},
}

# RITMO — calibrado por medição e depois pelo ouvido do Pedro.
#
# A +12% o resultado saiu a 166 e 163 ppm. Ele ouviu e disse: está na velocidade
# natural, mas COMO NÃO É VOZ HUMANA, soa rápido demais. Pediu ~5% mais lento, e
# isso cai justamente nas 158 ppm que medi na Part 1 do RED — o ouvido dele
# chegou no número da prova.
#
# A lição a guardar: voz sintética no ritmo humano PARECE mais rápida que a
# humana. O alvo medido é o piso, não a meta; para TTS convém ficar um pouco
# abaixo dele.
#
# E o ritmo VARIA por falante, de propósito. Duas pessoas na mesma velocidade
# exata soam mecânicas, e na prova real cada um fala no seu tempo.
RITMO_NARRADOR = '+0%'
RITMO = {
    'l1-q01': {'W': '+8%', 'M': '+5%'},   # a aluna, apressada; o professor, calmo
    'l1-q02': {'W': '+5%', 'M': '+8%'},   # invertido, para os itens não se parecerem
}

PAUSA_TURNO = 0.35
PAUSA_PERGUNTA = 0.9


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('falhou: %s\n%s' % (' '.join(cmd), r.stderr[:400]))
    return r.stdout


async def fala(texto, voz, rate, destino):
    """A ÚNICA parte presa ao motor de voz. Trocar aqui troca tudo."""
    await edge_tts.Communicate(texto, voz, rate=rate).save(destino)


async def gera(qid, linhas):
    vozes = dict(PARES[qid]); vozes['N'] = NARRADOR
    ritmo = dict(RITMO[qid]); ritmo['N'] = RITMO_NARRADOR
    os.makedirs(TMP, exist_ok=True); os.makedirs(SAIDA, exist_ok=True)
    pedacos = []
    for i, (quem, txt) in enumerate(linhas):
        bruto = '%s/%s-%02d.mp3' % (TMP, qid, i)
        await fala(txt, vozes[quem], ritmo[quem], bruto)
        wav = bruto.replace('.mp3', '.wav')
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-ar', '44100', '-ac', '1', wav])
        pedacos.append(wav)
        if i < len(linhas) - 1:
            seg = PAUSA_PERGUNTA if i == len(linhas) - 2 else PAUSA_TURNO
            sil = '%s/%s-%02d-sil.wav' % (TMP, qid, i)
            sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi',
                '-i', 'anullsrc=r=44100:cl=mono', '-t', str(seg), sil])
            pedacos.append(sil)

    lista = '%s/%s.txt' % (TMP, qid)
    with open(lista, 'w') as f:
        for p in pedacos:
            f.write("file '%s'\n" % p)
    mp3 = '%s/%s.mp3' % (SAIDA, qid)
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
        '-i', lista, '-ac', '1', '-ar', '44100', '-b:a', '96k', mp3])

    dur = float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'csv=p=0', mp3]).strip())
    palavras = sum(len(re.findall(r"[A-Za-z']+", t)) for _, t in linhas)
    print('%-10s %5.1fs · %3d palavras · %3.0f ppm  (alvo 158)' %
          (qid, dur, palavras, palavras / dur * 60))
    return {'id': qid, 'dur': round(dur, 1), 'ppm': round(palavras / dur * 60)}


# ── as duas conversas, no universo acadêmico ─────────────────────────────────
Q1 = [
  ('N', 'Number one.'),
  ('W', "Professor Hale, I wanted to ask about the essay that's due Friday. My laptop died on Sunday and I lost about half of it."),
  ('M', "That's rough. Had you backed any of it up?"),
  ('W', "Only the outline, unfortunately."),
  ('M', "Then take until Monday. But send me that outline today, so I can see where you got to."),
  ('N', 'What does the professor ask the student to do?'),
]

Q2 = [
  ('N', 'Number two.'),
  ('M', "Are you taking that statistics elective next term?"),
  ('W', "I want to, but it meets at the same time as my chemistry lab."),
  ('M', "Can't you switch to another lab section?"),
  ('W', "I asked. The only other section is Friday at eight in the morning."),
  ('M', "Well, I suppose that tells you how badly you want the elective."),
  ('N', 'What does the man imply about the woman?'),
]


async def main():
    print('motor: edge-TTS (Microsoft) · narrador: %s' % NARRADOR.replace('en-US-', ''))
    for qid, par in PARES.items():
        print('  %s → %s / %s' % (qid, par['W'].replace('en-US-', ''), par['M'].replace('en-US-', '')))
    print()
    r = [await gera('l1-q01', Q1), await gera('l1-q02', Q2)]
    print()
    print(json.dumps(r, ensure_ascii=False))

if __name__ == '__main__':
    asyncio.run(main())
