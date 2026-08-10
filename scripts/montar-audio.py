#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta o MP3 de um item de listening a partir de falas soltas.

⚠️  A VOZ SINTÉTICA DAQUI FOI REPROVADA pelo Pedro em 10/08/2026. O `say` do
macOS é TTS de geração antiga e o resultado ficou artificial demais para uma
prova. NÃO refaça por aqui esperando resultado diferente.

O que SOBREVIVE e é o motivo deste arquivo existir: a MONTAGEM. Ela vale para
qualquer origem de voz — locutor humano, TTS neural de API, o que for. Troque
apenas a função que produz o áudio de cada fala; o resto (pausas entre turnos,
concatenação, formato final) já está calibrado contra o simulado oficial:

  · mono, 96 kbps, 44,1 kHz — idêntico aos MP3s do RED
  · 0,35s entre falas da conversa e 0,9s antes da pergunta do narrador
  · três timbres: dois na conversa e um terceiro para o narrador, como no RED

MEDIÇÕES DO RED que valem para calibrar qualquer voz (feitas em 10/08/2026,
palavras da transcrição ÷ duração do MP3):

  Part 1  158 palavras/min · 19 conversas curtas · média 25s (17s a 70s)
  Part 2  121 palavras/min ·  4 conversas longas · média 110s
  Part 3  112 palavras/min ·  4 palestras        · média 130s

ACHADO ÚTIL: o `-r` do `say` NÃO é palavra por minuto de verdade nas vozes
neurais da Apple. A 165 o resultado saiu a ~178 ppm; 146 põe o conjunto (fala
mais pausas) na faixa dos 158 ppm da Part 1. Se um dia outra ferramenta for
usada, meça o resultado em vez de confiar no parâmetro.

FORMATO de cada item da Part 1, copiado do RED: o narrador anuncia o número, vem
a conversa entre duas pessoas e o narrador lê a pergunta no fim.
"""

import subprocess, os, sys, json, re

SAIDA = '/Users/pedroluz/Claude/Projects/met-siele-simulador/audio/magenta'
TMP = '/private/tmp/claude-501/-Users-pedroluz-Claude-Projects/f668cdc2-9b2d-4ee6-b474-9fd4f9bde86c/scratchpad/tts'

VOZ = {'W': 'Ava', 'M': 'Tom', 'N': 'Allison'}
# Calibrado contra a medição: a 165 o resultado saiu a ~178 ppm, então o `-r`
# do `say` não é palavra por minuto de verdade nas vozes neurais. 146 põe o
# conjunto (fala + pausas) na faixa dos 158 ppm que medi na Part 1 do RED.
RITMO = {'W': 146, 'M': 146, 'N': 138}
PAUSA_TURNO = 0.35      # entre falas da conversa
PAUSA_PERGUNTA = 0.9    # antes da pergunta do narrador


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('falhou: %s\n%s' % (' '.join(cmd), r.stderr[:400]))
    return r.stdout


def gera(qid, linhas):
    """linhas: [('N'|'W'|'M', texto), ...]"""
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(SAIDA, exist_ok=True)
    pedacos = []
    for i, (quem, txt) in enumerate(linhas):
        aiff = '%s/%s-%02d.aiff' % (TMP, qid, i)
        sh(['say', '-v', VOZ[quem], '-r', str(RITMO[quem]), '-o', aiff, txt])
        wav = aiff.replace('.aiff', '.wav')
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', aiff, '-ar', '44100', '-ac', '1', wav])
        pedacos.append(wav)
        # silêncio depois da fala: maior antes da pergunta do narrador final
        ultimo = (i == len(linhas) - 2)
        seg = PAUSA_PERGUNTA if ultimo else PAUSA_TURNO
        if i < len(linhas) - 1:
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
    print('%-10s %5.1fs · %3d palavras · %3.0f ppm · %s' %
          (qid, dur, palavras, palavras / dur * 60, mp3))
    return {'id': qid, 'dur': round(dur, 1), 'ppm': round(palavras / dur * 60)}


# ── as duas conversas de teste, no universo acadêmico ────────────────────────
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

if __name__ == '__main__':
    print('voz da mulher: %s · homem: %s · narrador: %s' % (VOZ['W'], VOZ['M'], VOZ['N']))
    print('alvo: 158 palavras por minuto (a Part 1 do RED, medida)\n')
    r = [gera('l1-q01', Q1), gera('l1-q02', Q2)]
    print()
    print(json.dumps(r, ensure_ascii=False))
