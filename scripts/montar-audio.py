#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta os MP3s do listening do EMERALD a partir de data/roteiros-emerald.json.

    python3 scripts/montar-audio.py                # tudo
    python3 scripts/montar-audio.py l1-q03 l2-set1 # só esses
    python3 scripts/montar-audio.py --intros       # só as três aberturas

MOTOR DE VOZ: **edge-TTS da Microsoft** (vozes neurais, gratuito, sem chave de
API). É o mesmo motor que a trilha de espanhol do Listening Lab já usa em
produção, no `portal-aluno-fisk`.

  ⚠️  Histórico, para não se repetir: a primeira tentativa usou o `say` do
  macOS, TTS de geração antiga, e o Pedro reprovou na hora ("absolutamente
  horrorosa"). O erro foi a ferramenta, não a ideia — e a ferramenta certa já
  estava na casa. Se um dia isto falhar, troque só a função `fala()`; a
  montagem abaixo independe de quem dubla.

O NARRADOR NÃO ESTÁ NO ROTEIRO. O "Number seven." e a leitura da pergunta são
montados aqui, a partir do campo `text` da própria questão. É de propósito: o
que o aluno ouve e o que ele lê saem da mesma string, e não têm como divergir.

────────────────────────────────────────────────────────────────────────────
MEDIÇÕES DO RED (10/08/2026) — e a correção de 11/08

Medir palavras ÷ duração do arquivo inteiro dá:

    Part 1  158 ppm  ·  Part 2  114 ppm  ·  Part 3  113 ppm

Mas Parts 2 e 3 **não são faladas mais devagar**. Os arquivos delas carregam
~12s de silêncio depois de cada pergunta, para o aluno responder, e é esse
silêncio que derruba a média. Medindo só o trecho falado:

    Part 1  ~158 ppm  ·  Part 2  182 ppm  ·  Part 3  165 ppm

Ou seja: a conversa longa do MET é falada MAIS RÁPIDO que a curta. Quem
desacelerasse a voz até 120 ppm produziria um áudio irreconhecível.

Por isso este script imprime **as duas medidas**: `ppm` do arquivo (comparável
com o RED item a item) e `fala` do trecho falado (a velocidade de verdade).

ALVO. Vale a lição que o ouvido do Pedro deu na Part 1: voz sintética no ritmo
humano PARECE mais rápida que a humana, então o número do RED é piso, não meta.
Ficamos deliberadamente abaixo: ~160 ppm de fala nas conversas longas e ~150
nas palestras, contra 182 e 165 do original.

SEMPRE MEÇA O RESULTADO. O parâmetro de velocidade de qualquer TTS é promessa,
não medida: no `say`, pedir 165 devolvia 178 ppm.
"""
import asyncio, subprocess, os, sys, json, re
import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTEIROS = os.path.join(RAIZ, 'data', 'roteiros-emerald.json')
CUES = os.path.join(RAIZ, 'data', 'cues-emerald.json')
SAIDA = os.path.join(RAIZ, 'audio', 'emerald')
TMP = '/tmp/fisk-tts'

# Terceiro timbre, fixo em todos os itens, para o aluno reconhecer o narrador.
# As vozes dos diálogos vivem no roteiro, item a item.
NARRADOR = 'en-US-AriaNeural'
RITMO_NARRADOR = '+0%'

PAUSA_TURNO = 0.35       # entre falas da conversa
PAUSA_PERGUNTA = 0.9     # antes da pergunta, na Part 1
PAUSA_INTRO = 1.2        # depois do "Listen to a conversation between..."
PAUSA_NUMERO = 0.5       # entre "Number twenty." e a pergunta
PAUSA_CITACAO = 0.6      # antes do trecho repetido, nas questões de intenção
PAUSA_RESPOSTA = 11.5    # o silêncio para responder — o RED usa ~12s
PAUSA_FINAL = 1.0        # depois da última pergunta do set

ALVO = {'l1': 158, 'l2': 114, 'l3': 113}   # ppm de arquivo, medido no RED

UNID = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen']
DEZ = {20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty'}


def porextenso(n):
    """1..50 por extenso — o TTS lê números soltos com entonação de lista."""
    if n < 20:
        return UNID[n]
    d, u = divmod(n, 10)
    base = DEZ[d * 10]
    return base if not u else '%s-%s' % (base, UNID[u])


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('falhou: %s\n%s' % (' '.join(cmd), r.stderr[:400]))
    return r.stdout


def dur(caminho):
    return float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'csv=p=0', caminho]).strip())


def palavras(txt):
    return len(re.findall(r"[A-Za-z']+", txt))


async def fala(texto, voz, rate, destino):
    """A ÚNICA parte presa ao motor de voz. Trocar aqui troca tudo."""
    await edge_tts.Communicate(texto, voz, rate=rate).save(destino)


# ── montagem ────────────────────────────────────────────────────────────────
# Um roteiro vira uma lista de blocos: ('fala', quem, texto) ou ('pausa', s) ou
# ('marca', rótulo) — a marca não vira áudio, só anota o instante para os cues.

def blocos_part1(item):
    q = item['questoes'][0]
    b = [('fala', 'N', 'Number %s.' % porextenso(q['n'])), ('pausa', PAUSA_TURNO)]
    b.append(('marca', 'Conversation'))
    for i, (quem, txt) in enumerate(item['linhas']):
        if i:
            b.append(('pausa', PAUSA_TURNO))
        b.append(('fala', quem, txt))
    b += [('pausa', PAUSA_PERGUNTA), ('fala', 'N', q['text'])]
    return b


def blocos_set(item):
    rotulo = 'Lecture' if item['section'] == 'l3' else 'Conversation'
    b = [('fala', 'N', item['intro']), ('pausa', PAUSA_INTRO), ('marca', rotulo)]
    for i, (quem, txt) in enumerate(item['linhas']):
        if i:
            b.append(('pausa', PAUSA_TURNO))
        b.append(('fala', quem, txt))
    ultimas = len(item['questoes']) - 1
    for i, q in enumerate(item['questoes']):
        b.append(('pausa', PAUSA_INTRO))
        b.append(('marca', q['n']))
        b.append(('fala', 'N', 'Number %s.' % porextenso(q['n'])))
        b += [('pausa', PAUSA_NUMERO), ('fala', 'N', q['text'])]
        if q.get('quote'):
            b += [('pausa', PAUSA_CITACAO), ('fala', 'N', q['quote'])]
        b.append(('pausa', PAUSA_FINAL if i == ultimas else PAUSA_RESPOSTA))
    return b


async def gera(qid, blocos, vozes, ritmo, arquivo):
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(SAIDA, exist_ok=True)
    pedacos, cues, t = [], [], 0.0
    faladas = 0          # palavras ditas por quem não é o narrador
    fim_da_fala = None   # instante em que a conversa/palestra acaba

    for i, bloco in enumerate(blocos):
        if bloco[0] == 'marca':
            rot = bloco[1]
            cues.append({'label': rot, 't': round(t, 1)} if isinstance(rot, str)
                        else {'n': rot, 't': round(t, 1)})
            if not isinstance(rot, str) and fim_da_fala is None:
                fim_da_fala = t
            continue
        if bloco[0] == 'pausa':
            seg = bloco[1]
            wav = '%s/%s-%03d-sil.wav' % (TMP, qid, i)
            sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi',
                '-i', 'anullsrc=r=44100:cl=mono', '-t', str(seg), wav])
            pedacos.append(wav)
            t += seg
            continue
        _, quem, txt = bloco
        bruto = '%s/%s-%03d.mp3' % (TMP, qid, i)
        await fala(txt, vozes[quem], ritmo[quem], bruto)
        wav = bruto.replace('.mp3', '.wav')
        sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto,
            '-ar', '44100', '-ac', '1', wav])
        pedacos.append(wav)
        t += dur(wav)
        if quem != 'N':
            faladas += palavras(txt)

    lista = '%s/%s.txt' % (TMP, qid)
    with open(lista, 'w') as f:
        for p in pedacos:
            f.write("file '%s'\n" % p)
    mp3 = os.path.join(SAIDA, arquivo)
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
        '-i', lista, '-ac', '1', '-ar', '44100', '-b:a', '96k', mp3])

    d = dur(mp3)
    todas = sum(palavras(b[2]) for b in blocos if b[0] == 'fala')
    inicio = next((c['t'] for c in cues if 'label' in c), 0.0)
    fim = fim_da_fala if fim_da_fala is not None else d
    ppm_fala = faladas / (fim - inicio) * 60 if fim > inicio else 0
    return {'id': qid, 'arquivo': arquivo, 'dur': round(d, 1),
            'palavras': todas, 'ppm': round(todas / d * 60),
            'ppm_fala': round(ppm_fala), 'cues': cues}


async def main():
    roteiros = json.load(open(ROTEIROS))
    alvos = [a for a in sys.argv[1:] if not a.startswith('--')]
    so_intros = '--intros' in sys.argv

    print('motor: edge-TTS (Microsoft) · narradora: %s\n' % NARRADOR.replace('en-US-', ''))
    saida = []

    if so_intros or not alvos:
        for nome, txt in roteiros['intros'].items():
            r = await gera(nome, [('fala', 'N', txt)], {'N': NARRADOR},
                           {'N': RITMO_NARRADOR}, nome + '.mp3')
            print('%-10s %6.1fs · %3d palavras' % (nome, r['dur'], r['palavras']))
        if so_intros:
            return

    for item in roteiros['itens']:
        if alvos and item['id'] not in alvos:
            continue
        vozes = dict(item['vozes']); vozes['N'] = NARRADOR
        ritmo = dict(item['ritmo']); ritmo['N'] = RITMO_NARRADOR
        if item['section'] == 'l1':
            blocos = blocos_part1(item)
            arquivo = '%s.mp3' % item['id']
        else:
            blocos = blocos_set(item)
            arquivo = item['audio']
        r = await gera(item['id'], blocos, vozes, ritmo, arquivo)
        alvo = ALVO[item['section']]
        print('%-10s %6.1fs · %3d palavras · %3d ppm (alvo %d) · fala %3d ppm'
              % (item['id'], r['dur'], r['palavras'], r['ppm'], alvo, r['ppm_fala']))
        saida.append(r)

    if saida:
        antigo = json.load(open(CUES)) if os.path.exists(CUES) else {}
        antigo.update({r['id']: r for r in saida})
        with open(CUES, 'w') as f:
            json.dump(antigo, f, ensure_ascii=False, indent=1)
        print('\ncues e durações → %s' % os.path.relpath(CUES, RAIZ))


if __name__ == '__main__':
    asyncio.run(main())
