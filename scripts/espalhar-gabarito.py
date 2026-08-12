#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Espalha o gabarito de um banco pelas quatro posições.

    python3 scripts/espalhar-gabarito.py questions/emerald.json          # confere
    python3 scripts/espalhar-gabarito.py questions/emerald.json --gravar # aplica

POR QUE EXISTE. A tela **não embaralha alternativa**: o índice escrito no banco
é a letra que o aluno vê (o comentário do envio, no `index.html`, diz isso com
todas as letras). Quem escreve questão a questão põe a resposta certa em cima
sem perceber, e o banco vira um teste de marcar A. Foi o que aconteceu com o
EMERALD, que nasceu com 99 das 100 respostas na letra A: um aluno que marcasse
tudo A tirava 99. O RED, que é oficial, distribui 24/24/28/24.

A ordem é sorteada com **semente fixa**, derivada do id do banco: rodar de novo
dá exatamente o mesmo resultado. Isso não é capricho — o `Gabarito.js` do
`fisk-hub-backend` é gerado a partir destes arquivos, e um embaralhamento
diferente a cada rodada faria o servidor corrigir por um gabarito e a tela
mostrar outro.

⚠️ DEPOIS DE GRAVAR, o gabarito do servidor precisa ser refeito e implantado,
senão a correção da nuvem fica apontando para as posições velhas:

    cd ../fisk-hub-backend && node scripts/build-gabarito.js && clasp push
    (e uma implantação nova — quem publica o Apps Script sou eu, não o Pedro)

⚠️ NÃO RODE em banco cujo `expl` cite a POSIÇÃO da alternativa ("a letra B", "a
primeira opção"). O script confere isso e recusa.
"""
import json, os, random, re, sys

POSICAO = re.compile(r'\b(letra [A-D]\b|alternativa [A-D]\b|op[çc][ãa]o [A-D]\b|'
                     r'a (primeira|segunda|terceira|quarta|última) op[çc][ãa]o|'
                     r'as duas (primeiras|últimas) op[çc][õo]es)', re.I)


def questoes(banco):
    return [q for u in banco['units'] for q in u['questions']]


def distribuicao(qs):
    d = {}
    for q in qs:
        d[q['key']] = d.get(q['key'], 0) + 1
    return {k: d.get(k, 0) for k in range(4)}


def espalha(banco):
    qs = questoes(banco)
    presas = [q['n'] for q in qs if POSICAO.search(q.get('expl', ''))]
    if presas:
        sys.exit('estas explicações citam a posição da alternativa e seriam '
                 'invalidadas: %s' % presas)

    # SEMENTE FIXA, e o resultado NÃO depende da ordem em que as alternativas
    # estão agora: as posições-alvo saem do id do banco e dos números das
    # questões, e os distratores partem sempre da mesma ordem canônica (a
    # alfabética). Sem isso o script embaralharia o embaralhado e rodar duas
    # vezes daria dois bancos, que é o oposto do que o Gabarito.js precisa.
    base = sum(ord(c) for c in banco['id']) * 1000 + len(qs)
    alvos = [i % 4 for i in range(len(qs))]
    random.Random(base).shuffle(alvos)
    for q, alvo in zip(sorted(qs, key=lambda x: x['n']), alvos):
        certa = q['opts'][q['key']]
        resto = sorted(o for i, o in enumerate(q['opts']) if i != q['key'])
        random.Random(base + q['n']).shuffle(resto)
        q['opts'] = resto[:alvo] + [certa] + resto[alvo:]
        q['key'] = alvo
        assert q['opts'][q['key']] == certa, q['n']
    return qs


def main():
    caminho = sys.argv[1]
    gravar = '--gravar' in sys.argv
    banco = json.load(open(caminho))
    qs = questoes(banco)
    antes = distribuicao(qs)
    gabarito_antes = {q['n']: q['opts'][q['key']] for q in qs}

    espalha(banco)
    depois = distribuicao(questoes(banco))

    # a resposta CERTA tem de ser a mesma frase de antes; só mudou de lugar
    for q in questoes(banco):
        assert q['opts'][q['key']] == gabarito_antes[q['n']], q['n']

    print('%s · %d questões' % (caminho, len(qs)))
    print('  antes:  %s' % antes)
    print('  depois: %s' % depois)
    if not gravar:
        print('\n(nada gravado; rode com --gravar para aplicar)')
        return
    with open(caminho, 'w') as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('gravado: %s' % caminho)

    # O LISTENING NÃO MORA SÓ AQUI. As unidades l1/l2/l3 são geradas por
    # `montar-unidades.py` a partir de `data/roteiros-<prova>.json`. Espalhar só
    # o banco deixa o roteiro com a ordem velha, e a próxima geração desfaz
    # metade do conserto sem avisar ninguém. Aconteceu em 12/08/2026, com o
    # EMERALD já publicado.
    roteiro = os.path.join(os.path.dirname(os.path.dirname(caminho)),
                           'data', 'roteiros-%s.json' % banco['id'])
    if not os.path.exists(roteiro):
        print('\n(sem roteiro de listening para este banco)')
    else:
        r = json.load(open(roteiro))
        porn = {q['n']: q for q in questoes(banco)}
        n = 0
        for item in r['itens']:
            for q in item['questoes']:
                b = porn[q['n']]
                assert sorted(b['opts']) == sorted(q['opts']), q['n']
                if q['opts'] != b['opts']:
                    q['opts'], q['key'] = list(b['opts']), b['key']
                    n += 1
        with open(roteiro, 'w') as f:
            json.dump(r, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print('roteiro alinhado: %s (%d questões)' % (roteiro, n))

    print('\nAgora refaça o gabarito do servidor e implante.')


if __name__ == '__main__':
    main()
