# Treino MET: decisões e roadmap

## O que é

Simulador do **MET (Michigan English Test)** do Fisk Hub, publicado por GitHub
Pages em `https://pedro-fisk.github.io/met-siele-simulador/`. Uma página só
(`index.html`, autocontida, vanilla JS) que carrega um **banco de itens** por
prova de `questions/*.json`. O SIELE mora no mesmo repositório por herança do
nome, mas é outro exame e não divide nada com o MET além do motor.

Dois modos:

- **aluno** (padrão): pré-página de instruções em português, depois cinco
  seções independentes com timer próprio e sem volta (L1, L2, L3, Grammar,
  Reading). Durante a prova a interface é toda em inglês, regra do Pedro.
- **professor** (`?modo=professor`): questão a questão, com revelar resposta e
  player completo. Sem timer, sem pré-página, sem tranca.

## As três provas

| | RED | EMERALD | AMBER |
|---|---|---|---|
| Origem | MET Practice Test #5, transcrito | escrita pela Fisk | escrita pela Fisk |
| Cor | `#d81f26` | `#059669` | `#D97706` |
| Listening | áudio original | edge-TTS | edge-TTS |
| No ar desde | 23/07/2026 | 11/08/2026 | 12/08/2026 |
| Tranca | nenhuma | nenhuma | exige RED e EMERALD |

As três dividem **uma home só** (`FAMILIAS` no `index.html`) e aparecem lado a
lado: o aluno escolhe a prova sem trocar de página. Cada uma tem 100 questões,
4 mini simulados e 5 seções, sempre na ordem oficial da prova.

Os outros quatro simulados oficiais (GREEN, PURPLE, YELLOW, BLUE) **não** viram
treino: são aplicados presencialmente. Dos oficiais vem só a estrutura e o peso
de cada capítulo, nunca enunciado, texto ou alternativa.

### Por que o EMERALD e o AMBER existem

Peso. O RED traz **uma** questão de conectores, que é o capítulo mais cobrado da
prova (13 em 100). As provas escritas pela Fisk seguem a distribuição que o MET
Study Guide apurou nos cinco simulados, então treinam o que a prova cobra.

O AMBER ainda equilibra o universo: 70% acadêmico e 30% trabalho e vida urbana,
decisão do Pedro em 12/08/2026, contra o EMERALD, que é todo acadêmico.

## Linha de produção de uma prova nova

Quatro scripts, nesta ordem. **Todos são idempotentes**: rodar de novo, ou fora
de ordem, produz o mesmo arquivo.

```bash
python3 scripts/montar-audio.py --prova amber        # roteiro → MP3 + cues
python3 scripts/montar-unidades.py --prova amber     # roteiro + cues → unidades l1/l2/l3
python3 scripts/montar-amber.py                      # gramática e leitura + minis
python3 scripts/espalhar-gabarito.py questions/amber.json --gravar
cd ../fisk-hub-backend && node scripts/build-gabarito.js   # e implantar
```

- O **roteiro** (`data/roteiros-<prova>.json`) é a fonte do listening: falas,
  vozes, ritmo, perguntas. O narrador não está lá: o "Number seven." e a leitura
  da pergunta são montados a partir do campo `text` da própria questão, para o
  que o aluno ouve e o que ele lê saírem da mesma string.
- Os **cues** (`data/cues-<prova>.json`) só existem depois do áudio: são o
  instante em que o narrador diz "Number twenty", e é por eles que a tela
  acompanha a prova.
- `montar-unidades.py` escreve as unidades de listening dentro do banco;
  `montar-<prova>.py` cuida de gramática e leitura e **preserva** o listening.

### Ritmo do listening, medido e não prometido

O parâmetro de velocidade de qualquer TTS é promessa; o script mede o resultado
e imprime duas contas: o ppm do arquivo (comparável com o RED item a item) e o
ppm só do trecho falado.

| | RED (original) | EMERALD/AMBER (alvo) |
|---|---|---|
| Part 1 | ~158 ppm de fala | 112 a 162 |
| Part 2 | 182 | 141 a 156 |
| Part 3 | 165 | 138 a 161 |

Ficamos deliberadamente **abaixo** do original: voz sintética no ritmo humano
parece mais rápida que a humana. A conversa longa da prova real é falada mais
rápido que a curta, ao contrário do que o instinto sugere. Quem desacelerasse
até 120 ppm produziria um áudio irreconhecível.

## O gabarito mora no servidor

`Gabarito.js`, no `fisk-hub-backend`, é **gerado** a partir destes JSONs e
guarda, por questão, a resposta certa e o tópico. Quem corrige é o servidor: o
aluno manda as respostas, não o placar. Desde 03/08/2026 mentir deixou de ser
digitar um número e passou a exigir acertar as questões.

Duas chaves reservadas:

- `__provas__`: indexada pelo **id da questão** (`amberq001`).
- `__escopos__`: quantas questões tem cada bloco (`amber:mini:mini1` → 23). É o
  que permite pagar Fisk Dólar só com a atividade inteira respondida.

Banco em `rascunho: true` é pulado pelo gerador e não envia nada: é a tranca de
quem está em construção.

## Progresso do aluno

Cada card mostra uma **barra por questão respondida**: azul no que foi feito,
cinza no que falta, "37 de 100", "concluído · 78%". A cor da prova diz de qual
simulado o card é; a barra diz quanto dele o aluno fez, e por isso ela **não**
usa a cor da prova.

- **Retomar** já existia: respostas e fase ficam no `localStorage` e voltam ao
  reabrir. Esse registro é apagado no envio.
- **A memória de ter feito** é outra coisa, e sobrevive ao envio.
- **A chave leva o RAF.** Sem isso, numa máquina da escola o segundo aluno
  retomava as respostas do primeiro.
- **A nuvem** (rotas `progGet`/`progSet`, aba `_progsim`) guarda **uma linha por
  aluno**, sobrescrita: ~30 blocos cabem num JSON de 2 KB numa célula, e 300
  alunos dão 300 linhas. A fusão é do servidor, pelo MAIOR número de questões
  feitas de cada bloco, e concluído nunca volta atrás.
- **A tela nunca espera a rede**: a home desenha com o que o navegador sabe e
  repinta quando a resposta chega. Lê uma vez por abertura, grava uma vez por
  bloco entregue. O teto medido em 30/07/2026 é de ~25 chamadas simultâneas.

Sem RAF não há nuvem: o progresso é do navegador. O RAF chega na URL quando o
aluno entra pelo Portal, que já o acrescenta em toda ferramenta.

## Fisk Dólares

Participação 2 por questão respondida, acerto 8 por questão, conclusão 30 na
primeira vez, e 1 por ponto percentual de melhora ao refazer. O card mostra o
teto (`10 × questões + 30`).

**Só paga com o bloco inteiro respondido** (decisão do Pedro, 12/08/2026). O
servidor só enxerga as respostas que chegam, então quem mandasse 5 de 23
entregaria uma "atividade de cinco" e receberia por ela. O cliente manda o
`escopo` e o gabarito diz o tamanho. Tentativa incompleta continua registrada,
porque aconteceu e o professor precisa dela; o que não sai é o crédito.

## A tranca por pré-requisito

O banco declara `requer: ["met","emerald"]`. A home tranca os cinco cards da
prova (completo, minis e seções): cinza, cadeado no lugar do ícone, sem abrir ao
clique, e o card treme em vez de ficar mudo, no mesmo idioma do Movie Program.

"Fez a prova" quer dizer a prova **inteira**, por qualquer um dos três caminhos:
o simulado completo, **ou** as cinco seções, **ou** os quatro minis. São
recortes das mesmas 100 questões; exigir os três seria cobrar a mesma prova três
vezes. O professor nunca é barrado.

Quando a nuvem responde com conclusões que aquele navegador não conhecia, a home
é redesenhada e a tranca cai sozinha.

## Etiqueta da prova

Pílula arredondada com o nome dentro, fundo na cor da prova. O `#red` que existia
antes era jargão de arquivo na tela do aluno.

⚠️ **O rótulo interno continua sendo `Mini Simulado 1 #red`, em texto.** Ele
viaja para a nuvem, nomeia a tentativa no painel do professor e é a chave que
agrupa "a mesma prova" na comparação de evolução. Renomear isso renomearia o
histórico de quem já fez. O que muda é só o desenho, em `rotuloComTag`.

## Armadilhas já pagas

- **Gabarito empilhado na letra A.** O EMERALD nasceu com 99 das 100 respostas
  em A, e a tela **não embaralha alternativa**: o índice do banco é a letra que
  o aluno vê. Quem marcasse A em tudo tirava 99. `espalhar-gabarito.py` conserta,
  com semente derivada do id do banco e dos números das questões, para rodar
  duas vezes dar o mesmo arquivo. O RED, que é oficial, distribui 24/24/28/24.
- **Espalhar só o banco não basta.** As unidades de listening são geradas do
  roteiro, então o roteiro precisa ser alinhado junto, senão a próxima geração
  desfaz metade do conserto. O script faz isso sozinho desde 12/08/2026.
- **Id de questão com prefixo escrito à mão.** `montar-unidades.py` batizava
  tudo de `emeraldq%03d`: as 50 questões de escuta do AMBER nasceram com os ids
  do EMERALD, e o gabarito é indexado por id, então uma prova seria corrigida pelo
  gabarito da outra. O prefixo vem da prova.
- **Nome de aba repetido.** A rota de progresso foi batizada de `_progresso`,
  que já era o livro-caixa dos Fisk Dólares, e passou a gravar dentro dele.
  Antes de batizar aba, `grep` o nome no `Code.js`. Hoje é `_progsim`.
- **Prova em construção dentro da família.** Enquanto for rascunho, a prova fica
  fora de `FAMILIAS`: dentro dela, o card e o aviso de obra apareceriam na home
  de todo aluno que abre o Treino MET.
- **Funções de desenho presas ao escopo da home.** As telas de prova quebravam
  ao tentar desenhar a etiqueta. Helper que toda tela usa mora no escopo de cima.
- **`--help` não existe nestes scripts.** `montar-unidades.py --help` roda o
  script e reescreve o banco.

## O que o aluno vê fora daqui

Dois cards no Portal, os dois levando a esta home: **Treino MET** (três provas e
doze minis) e **Treino MET · AMBER**, cujo texto já avisa da tranca. Mesma régua
`desdeBook: 'Fluency 2'`, porque é o mesmo exame. Quem libera é o simulador,
pelo `requer`; o card é só a porta.

O aviso de que **isto é treino** fica na home do simulador: o simulado oficial só
conta feito presencialmente na escola, uma vez por mês, e é pré-requisito da
inscrição no exame. Sem esse parágrafo o aluno sai daqui achando que já cumpriu
a exigência.

## Próximos passos

- **Tabela CEFR própria.** A conversão de acertos para scaled score é linear
  (×1,6), uma aproximação. As faixas oficiais por scaled score (C1 ≥ 64, B2
  53–63, B1 40–52, A2 27–39, de 80) já estão certas; o que é aproximado é o
  caminho até lá. Trocar é editar `cefr` no banco.
- **Os tópicos não chegam ao painel do professor.** O payload enviado à nuvem
  não os leva; mexer nele altera as colunas da planilha e exige publicar o
  backend junto.
- **A barra de progresso não aparece no card do Portal.** Decisão do Pedro em
  12/08/2026: não agora.
- **Quarta prova.** É escrever o roteiro e o banco e declarar o `requer`. A
  linha de produção já serve qualquer prova por `--prova`.

## Histórico

`re-fresh-emerald-listening.md`, na raiz, é o handoff da sessão que fez o
listening do EMERALD, em 10/08/2026. Está cumprido, e fica como registro de como
aquela frente foi decidida.
