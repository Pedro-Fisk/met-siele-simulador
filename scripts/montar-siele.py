#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta os MP3s da Comprensión auditiva do SIELE a partir do roteiro em markdown.

    python3 scripts/montar-siele.py                  # os seis
    python3 scripts/montar-siele.py ca-t1 ca-t4      # só esses
    python3 scripts/montar-siele.py --dry            # só o plano, sem gerar

POR QUE NAO E O montar-audio.py. Aquele monta o MET: um MP3 por questao ou por
set, com "Number seven" e silencio de resposta, a partir de um JSON. O SIELE e
outro objeto: **cada MP3 e a TAREFA INTEIRA** — instrucao, tempo de leitura,
primeira escuta, pausa, repeticao e tempo de resposta, tudo dentro do arquivo,
como no exame de verdade. E a fonte aqui e o proprio markdown que a pessoa
escreve e revisa (docs/roteiros-siele-m1.md), nao um JSON: duplicar aquele
texto num JSON criaria duas versoes do mesmo roteiro, e um dia elas
discordariam.

MOTOR: edge-TTS, o mesmo do EMERALD/AMBER e da trilha de espanhol do Listening
Lab. Trocar de motor e trocar so a funcao `fala()`.

⚠️ MEDIR O RESULTADO, sempre. O parametro de velocidade de TTS e promessa, nao
medida, e voz sintetica no ritmo humano PARECE mais rapida que a humana. Por
isso os ritmos da tabela do roteiro sao negativos, e por isso este script
imprime a duracao e o ppm de fala de cada tarefa.

GRAMATICA DO ROTEIRO (o que o parser entende):

  ## ca-tN.mp3 · Tarea N · Nivel X   abre uma tarefa
  PAPEL: texto                        uma fala (o papel casa com a tabela de vozes)
  [N segundos]                        silencio
  [Repetición]                        repete a fala da tarefa inteira
  [Repetición Anuncio 1]              repete so o trecho daquele rotulo
  [Repetición Persona 1] + NARRADOR: …  repeticao seguida de outra fala
  | Persona | Voz | Variante |        tabela de vozes por rotulo, dentro da tarefa

A REPETICAO NAO E UM SEGUNDO TTS: e o mesmo audio concatenado de novo, entao
sai identica a primeira escuta, como no exame. Repetir chamando o TTS outra vez
daria duas leituras diferentes do mesmo texto.
"""
import asyncio, subprocess, os, sys, re
import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTEIRO = os.path.join(RAIZ, 'docs', 'roteiros-siele-m1.md')
SAIDA = os.path.join(RAIZ, 'audio', 'siele-m1')
TMP = '/tmp/fisk-tts/siele-m1'

NARRADOR = 'es-US-AlonsoNeural'   # timbre fixo que nao dubla personagem nenhum
RITMO_NARRADOR = '-5%'

# Voz e ritmo por PAPEL, tarefa a tarefa (a tabela do cabecalho do roteiro).
# A variante alterna ENTRE tarefas, como no SIELE real, nunca dentro do texto.
#
# ⚠️ OS RITMOS SAO MEDIDOS, NAO ESCOLHIDOS (01/09/2026). A tabela do roteiro
# trazia -10%/-8%/-6%/-5%/-4%, escritos no olho. Gerado e medido contra o
# audio OFICIAL do Modelo 0 (`audio/siele-m0/`, gravacao humana), o resultado
# foi 12% a 46% MAIS RAPIDO que o oficial, e pior justamente nos niveis
# baixos: A1 a 186 ppm contra 134 do exame. Os numeros abaixo sao o que
# reencaixa cada tarefa na faixa do oficial, medido de novo depois.
#
# A regua e ppm sobre a FALA REAL (silencedetect no proprio arquivo), nunca
# sobre a duracao total nem sobre os colchetes do roteiro: colchete e silencio
# PLANEJADO, e o TTS acrescenta silencio proprio em cada emenda. Medir pelos
# colchetes dizia que estava tudo bem, e nao estava.
#
#   nivel   A1   A2   B1   B2   C1   C1
#   oficial 134  146  139  147  141  157   ppm (o exame acelera com o nivel)
#
VOZES = {
 'ca-t1': {'MUJER':   ('es-MX-DaliaNeural',  '-38%'),
           'PABLO':   ('es-MX-JorgeNeural',  '-38%')},
 'ca-t2': {'ÁLVARO':  ('es-ES-AlvaroNeural', '-29%'),
           'ELVIRA':  ('es-ES-ElviraNeural', '-29%')},
 'ca-t4': {'PERIODISTA': ('es-MX-JorgeNeural',  '-15%'),
           'CAMILA':     ('es-CO-SalomeNeural', '-15%')},
 'ca-t5': {'MUJER':   ('es-ES-ElviraNeural', '-24%')},
 'ca-t6': {'HOMBRE':  ('es-MX-JorgeNeural',  '-11%')},
}
# A tarefa 3 e a excecao: o papel escrito e HOMBRE/MUJER, mas quem manda na voz
# e a PERSONA, porque sao oito depoimentos de oito pessoas diferentes. A tabela
# vem do proprio roteiro (o parser le), e o ritmo e um so.
RITMO_T3 = '-30%'

PAUSA_TURNO = 0.4      # entre falas seguidas de uma conversa
PAUSA_ROTULO = 0.6     # depois de "Anuncio 1." / "Persona 3.", antes da fala
PAUSA_INSTRUCAO = 1.0  # depois de uma instrucao do narrador


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit('falhou: %s\n%s' % (' '.join(cmd), r.stderr[:400]))
    return r.stdout


def dur(caminho):
    return float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'csv=p=0', caminho]).strip())


def palavras(txt):
    return len(re.findall(r"[\wÁÉÍÓÚÜÑáéíóúüñ']+", txt))


async def fala(texto, voz, rate, destino):
    """A UNICA parte presa ao motor de voz. Trocar aqui troca tudo."""
    await edge_tts.Communicate(texto, voz, rate=rate).save(destino)


# ── leitura do roteiro ──────────────────────────────────────────────────────

RE_TAREFA = re.compile(r'^##\s+(ca-t\d)\.mp3\s+·\s+(Tarea \d)\s+·\s+Nivel\s+(\S+)')
RE_FALA = re.compile(r'^([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]*):\s*(.*)$')
RE_SILENCIO = re.compile(r'^\[(\d+)\s+segundos\](.*)$')
RE_REPETE = re.compile(r'^\[Repetición(?:\s+([^\]]+))?\](.*)$')
RE_LINHA_TAB = re.compile(r'^\|\s*(\d+)\s*\|\s*`([^`]+)`')


def ler_roteiro(caminho):
    """Devolve [{'id','tarea','nivel','eventos':[...],'vozes3':{...}}].

    Evento: ('fala', papel, texto) · ('sil', segundos) · ('rep', rotulo|None)
    """
    tarefas, atual, papel, buf = [], None, None, []

    def fecha_fala():
        nonlocal papel, buf
        if papel is not None:
            atual['eventos'].append(('fala', papel, ' '.join(buf).strip()))
        papel, buf = None, []

    for linha in open(caminho, encoding='utf-8'):
        linha = linha.rstrip('\n')
        m = RE_TAREFA.match(linha)
        if m:
            if atual:
                fecha_fala()
            atual = {'id': m.group(1), 'tarea': m.group(2), 'nivel': m.group(3),
                     'eventos': [], 'vozes3': {}}
            tarefas.append(atual)
            papel, buf = None, []
            continue
        if atual is None:
            continue
        if linha.startswith('---'):
            fecha_fala()
            continue
        m = RE_LINHA_TAB.match(linha)
        if m:                      # tabela de vozes por persona (tarefa 3)
            atual['vozes3'][m.group(1)] = m.group(2)
            continue
        if linha.startswith('|') or not linha.strip():
            fecha_fala()
            continue
        m = RE_SILENCIO.match(linha)
        if m:
            fecha_fala()
            atual['eventos'].append(('sil', int(m.group(1))))
            # "[30 segundos] LA PRUEBA HA TERMINADO": o texto solto depois do
            # colchete e o fecho que o narrador diz, como no exame real.
            resto = m.group(2).strip()
            if resto:
                atual['eventos'].append(('fala', 'NARRADOR', resto.capitalize() + '.'))
            continue
        m = RE_REPETE.match(linha)
        if m:
            fecha_fala()
            atual['eventos'].append(('rep', (m.group(1) or '').strip() or None))
            resto = m.group(2).strip()
            if resto.startswith('+'):        # "+ NARRADOR: Conteste a la…"
                mm = RE_FALA.match(resto[1:].strip())
                if mm:
                    atual['eventos'].append(('fala', mm.group(1).strip(), mm.group(2)))
            continue
        m = RE_FALA.match(linha)
        if m:
            fecha_fala()
            papel, buf = m.group(1).strip(), [m.group(2)]
            continue
        if papel is not None:       # continuacao da fala, quebrada em varias linhas
            buf.append(linha.strip())
    if atual:
        fecha_fala()
    return tarefas


# ── expansao das repeticoes ─────────────────────────────────────────────────

def expande(eventos):
    """Troca cada ('rep', rotulo) pelos eventos que ela repete.

    Bare `[Repetición]`  → tudo desde a primeira fala que NAO e instrucao do
    narrador ate a ultima fala antes do marcador, com os silencios que caem
    ENTRE falas (os [2 segundos] da palestra) e sem o silencio de resposta que
    vem logo antes do marcador.

    `[Repetición Persona 3]` → da fala do narrador que anuncia esse rotulo ate
    a ultima fala antes do marcador. O rotulo entra na repeticao de proposito:
    o aluno precisa saber qual das oito esta ouvindo de novo.
    """
    saida = []
    for i, ev in enumerate(eventos):
        if ev[0] != 'rep':
            saida.append(ev)
            continue
        rotulo = ev[1]
        # onde comeca
        if rotulo:
            ini = None
            for j in range(i - 1, -1, -1):
                e = eventos[j]
                if e[0] == 'fala' and e[1] == 'NARRADOR' and \
                   e[2].strip().rstrip('.').lower() == rotulo.lower():
                    ini = j
                    break
            if ini is None:
                sys.exit('rotulo de repeticao nao encontrado: %r' % rotulo)
        else:
            # a primeira fala depois da ULTIMA instrucao longa do narrador
            ini = 0
            for j in range(i - 1, -1, -1):
                e = eventos[j]
                if e[0] == 'fala' and e[1] == 'NARRADOR' and len(e[2].split()) > 12:
                    ini = j + 1
                    break
            # ...e ela e a primeira FALA, nao o silencio de leitura que vem
            # logo depois da instrucao: repetir aquele meio minuto no meio da
            # tarefa seria um buraco mudo onde o aluno espera a segunda escuta.
            while ini < i and eventos[ini][0] != 'fala':
                ini += 1
        # onde termina: a ultima fala antes do marcador
        fim = None
        for j in range(i - 1, ini - 1, -1):
            if eventos[j][0] == 'fala':
                fim = j
                break
        if fim is None:
            sys.exit('repeticao sem fala para repetir')
        saida.extend(eventos[ini:fim + 1])
    return saida


# ── montagem ────────────────────────────────────────────────────────────────

def voz_de(tarefa, papel, persona):
    if tarefa['id'] == 'ca-t3' and papel != 'NARRADOR':
        v = tarefa['vozes3'].get(persona)
        if not v:
            sys.exit('sem voz para a Persona %s' % persona)
        return v, RITMO_T3
    if papel == 'NARRADOR':
        return NARRADOR, RITMO_NARRADOR
    par = VOZES.get(tarefa['id'], {}).get(papel)
    if not par:
        sys.exit('sem voz para %s na %s' % (papel, tarefa['id']))
    return par


async def gera(tarefa, seco=False):
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(SAIDA, exist_ok=True)
    eventos = expande(tarefa['eventos'])
    pedacos, t, faladas, silencio = [], 0.0, 0, 0.0
    persona = None
    cache = {}          # (texto, voz, ritmo) -> wav, e e ele que faz a
                        # repeticao sair IDENTICA a primeira escuta
    anterior = None

    for i, ev in enumerate(eventos):
        if ev[0] == 'sil':
            seg = float(ev[1])
            if not seco:
                wav = '%s/%s-%03d-sil.wav' % (TMP, tarefa['id'], i)
                sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi',
                    '-i', 'anullsrc=r=44100:cl=mono', '-t', str(seg), wav])
                pedacos.append(wav)
            t += seg
            silencio += seg
            anterior = 'sil'
            continue
        _, papel, texto = ev
        m = re.match(r'^(Persona|Anuncio|Noticia)\s+(\d+)', texto)
        if papel == 'NARRADOR' and m:
            persona = m.group(2)
        # pausa implicita entre falas seguidas, sem colchete no roteiro
        if anterior == 'fala':
            p = PAUSA_ROTULO if (eventos[i - 1][1] == 'NARRADOR' and papel != 'NARRADOR'
                                 and len(eventos[i - 1][2].split()) <= 4) else \
                PAUSA_INSTRUCAO if eventos[i - 1][1] == 'NARRADOR' else PAUSA_TURNO
            if not seco:
                wav = '%s/%s-%03d-p.wav' % (TMP, tarefa['id'], i)
                sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi',
                    '-i', 'anullsrc=r=44100:cl=mono', '-t', str(p), wav])
                pedacos.append(wav)
            t += p
            silencio += p
        voz, ritmo = voz_de(tarefa, papel, persona)
        chave = (texto, voz, ritmo)
        if not seco:
            if chave not in cache:
                bruto = '%s/%s-%03d.mp3' % (TMP, tarefa['id'], i)
                await fala(texto, voz, ritmo, bruto)
                wav = bruto.replace('.mp3', '.wav')
                sh(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto,
                    '-ar', '44100', '-ac', '1', wav])
                cache[chave] = wav
            pedacos.append(cache[chave])
            t += dur(cache[chave])
        if papel != 'NARRADOR':
            faladas += palavras(texto)
        anterior = 'fala'

    if seco:
        return {'id': tarefa['id'], 'eventos': len(eventos), 'silencio': silencio,
                'faladas': faladas, 'dur': None}

    lista = '%s/%s.txt' % (TMP, tarefa['id'])
    with open(lista, 'w') as f:
        for p in pedacos:
            f.write("file '%s'\n" % p)
    mp3 = os.path.join(SAIDA, tarefa['id'] + '.mp3')
    sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
        '-i', lista, '-ac', '1', '-ar', '44100', '-b:a', '96k', mp3])
    d = dur(mp3)
    return {'id': tarefa['id'], 'dur': d, 'silencio': silencio, 'faladas': faladas,
            'ppm_fala': round(faladas / (d - silencio) * 60) if d > silencio else 0,
            'eventos': len(eventos)}


async def main():
    seco = '--dry' in sys.argv
    alvos = [a for a in sys.argv[1:] if not a.startswith('--')]
    tarefas = ler_roteiro(ROTEIRO)
    print('motor: edge-TTS · narrador: %s (%s)\n' % (NARRADOR, RITMO_NARRADOR))
    print('%-8s %-8s %8s %9s %8s %10s' %
          ('tarefa', 'nivel', 'blocos', 'duracao', 'silencio', 'ppm fala'))
    for tf in tarefas:
        if alvos and tf['id'] not in alvos:
            continue
        r = await gera(tf, seco)
        print('%-8s %-8s %8d %8s %7ds %10s' %
              (r['id'], tf['nivel'], r['eventos'],
               '%.0fs' % r['dur'] if r['dur'] else '-',
               r['silencio'], r.get('ppm_fala', '-')))


if __name__ == '__main__':
    asyncio.run(main())
