#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carimba `id` estavel nas questoes dos bancos do SIELE.

POR QUE PRECISOU EXISTIR (01/09/2026). As tres provas do MET (red, emerald,
amber) tinham `id` nas 100 questoes; os DOIS bancos do SIELE nao tinham em
NENHUMA. Consequencia, achada ao liberar o Modelo 1:

  · o gerador do Gabarito pula questao sem id ("banco ainda sem id estavel");
  · o front so monta `respostas[q.id]`, entao para o SIELE o objeto saia vazio;
  · com o objeto vazio, o proprio front desiste com "Nenhuma resposta para
    enviar" e NAO manda nada.

Ou seja: desde que o Modelo 0 entrou no ar, aluno logado terminava o SIELE e o
resultado nao ia para lugar nenhum. Nao aparecia no historico dele, nao pagava
Fisk Dolar, nao chegava ao Dossie do professor. Ninguem viu porque a tela do
aluno mostra a nota normalmente: quem some e o registro.

⚠️ O ID E PARA SEMPRE. Ele e a chave da questao no Gabarito e no historico do
aluno; renomear apaga o que ja foi respondido. Por isso ele sai da POSICAO
(`n`), que e estavel no banco, e nao da ordem do arquivo.

    python3 scripts/dar-ids-siele.py           # aplica
    python3 scripts/dar-ids-siele.py --check   # so acusa (exit 1 se faltar)

Idempotente: questao que ja tem `id` nao e tocada.
"""
import json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SO_CHECAR = '--check' in sys.argv
falta = 0

for nome in sorted(os.listdir(os.path.join(RAIZ, 'questions'))):
    if not nome.endswith('.json'):
        continue
    caminho = os.path.join(RAIZ, 'questions', nome)
    with open(caminho, encoding='utf-8') as h:
        texto = h.read()
    d = json.loads(texto)
    # prefixo tirado do id do banco: "siele-m1" -> "sielem1", como "red" -> "red"
    pref = re.sub(r'[^a-z0-9]', '', str(d.get('id', '')).lower())
    if not pref:
        continue
    novos = 0
    for u in d.get('units', []):
        for q in u.get('questions', []):
            if q.get('id') or q.get('n') is None:
                continue
            novos += 1
            if SO_CHECAR:
                continue
            # reescreve a questao PELO TEXTO, para o resto do arquivo (ordem das
            # chaves, acentuacao, indentacao) ficar exatamente como estava
            alvo = '"n": %d,' % q['n']
            marca = '"n": %d, "id": "%sq%03d",' % (q['n'], pref, q['n'])
            assert texto.count(alvo) == 1, '%s: "n": %d aparece %d vezes' % (nome, q['n'], texto.count(alvo))
            texto = texto.replace(alvo, marca)
    if novos:
        falta += novos
        print('%-16s %3d questoes sem id%s' % (nome, novos, '' if SO_CHECAR else ' → carimbadas'))
        if not SO_CHECAR:
            json.loads(texto)          # nao grava JSON quebrado
            with open(caminho, 'w', encoding='utf-8') as h:
                h.write(texto)

if not falta:
    print('todas as questoes ja tem id')
elif SO_CHECAR:
    sys.exit(1)
