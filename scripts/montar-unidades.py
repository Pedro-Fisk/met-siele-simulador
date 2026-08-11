#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escreve as unidades l1/l2/l3 do questions/emerald.json.

    python3 scripts/montar-unidades.py

Junta duas fontes e não inventa nada:

  data/roteiros-emerald.json  o conteúdo (perguntas, alternativas, explicações)
  data/cues-emerald.json      o que só o áudio pronto sabe (duração e os cues)

Roda DEPOIS de gerar o áudio. Os cues das Parts 2 e 3 são o instante em que o
narrador diz "Number twenty" — é por eles que o simulador acompanha a prova, e
eles só existem depois que o MP3 existe. Rodar antes é erro, e o script avisa.

As unidades de listening entram na frente das de gramática, na ordem da prova.
Qualquer unidade l1/l2/l3 que já estivesse lá é substituída, então dá para
rodar quantas vezes for preciso.
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTEIROS = os.path.join(RAIZ, 'data', 'roteiros-emerald.json')
CUES = os.path.join(RAIZ, 'data', 'cues-emerald.json')
BANCO = os.path.join(RAIZ, 'questions', 'emerald.json')


def questao(q):
    return {
        'n': q['n'],
        'id': 'emeraldq%03d' % q['n'],
        'topic': q['topic'],
        'text': q['text'],
        'opts': q['opts'],
        'key': q['key'],
        'expl': q['expl'],
    }


def main():
    roteiros = json.load(open(ROTEIROS))
    if not os.path.exists(CUES):
        sys.exit('falta data/cues-emerald.json — gere o áudio primeiro '
                 '(python3 scripts/montar-audio.py)')
    cues = json.load(open(CUES))

    novas, faltando = [], []
    for item in roteiros['itens']:
        medido = cues.get(item['id'])
        if not medido:
            faltando.append(item['id'])
            continue
        if item['section'] == 'l1':
            novas.append({
                'id': item['id'],
                'section': 'l1',
                'type': 'audio-single',
                'audio': medido['arquivo'],
                'questions': [questao(q) for q in item['questoes']],
            })
        else:
            novas.append({
                'id': item['id'],
                'section': item['section'],
                'type': 'audio-set',
                'audio': medido['arquivo'],
                'title': item['title'],
                'cues': medido['cues'],
                'questions': [questao(q) for q in item['questoes']],
            })

    if faltando:
        sys.exit('sem áudio (e portanto sem cues): %s' % ', '.join(faltando))

    banco = json.load(open(BANCO))
    resto = [u for u in banco['units'] if u['section'] not in ('l1', 'l2', 'l3')]
    banco['units'] = novas + resto
    with open(BANCO, 'w') as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write('\n')

    ns = [q['n'] for u in banco['units'] for q in u['questions']]
    print('%d unidades de listening · %d questões' %
          (len(novas), sum(len(u['questions']) for u in novas)))
    print('numeração 1–100 completa e sem buraco: %s' % (ns == list(range(1, 101))))


if __name__ == '__main__':
    main()
