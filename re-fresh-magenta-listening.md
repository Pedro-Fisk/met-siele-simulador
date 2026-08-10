# Handoff — o listening do simulado MAGENTA

Escrito em 10/08/2026, para retomar numa sessão nova. O MAGENTA está com
**50 das 100 questões prontas** (gramática e leitura). Falta o listening inteiro,
e a decisão que trava tudo é **de onde vem o áudio**.

---

## 1. O que é o MAGENTA e por que ele existe

Simulado do MET **escrito pela Fisk**. Os outros quatro oficiais (GREEN, PURPLE,
YELLOW, BLUE) não podem virar treino porque são aplicados presencialmente; o RED
já é usado e sozinho não basta.

Dos oficiais vem só a **estrutura** e o **peso de cada capítulo** — nunca
enunciado, texto ou alternativa. O peso é o motivo de escrever do zero: o RED
traz **uma** questão de conectores, que é o capítulo mais cobrado da prova (13 em
100). O MAGENTA traz três, seguindo a distribuição que o MET Study Guide apurou
nos cinco simulados.

**Arquivo:** `questions/magenta.json` · **Como abrir:** `?exame=magenta`

### Ele está FORA DO AR, com três trancas

1. Nenhum card do Portal aponta para ele. Só se chega pelo parâmetro.
2. Com `rascunho: true` no JSON, a home mostra um aviso de simulado em
   construção, dizendo que não é prova oficial da Michigan Language Assessment.
3. Com `rascunho: true`, **nada é enviado** — nem de aluno logado nem solto. E o
   gerador do gabarito no `fisk-hub-backend` pula bancos em rascunho, então o
   servidor nem sabe corrigi-lo.

**Publicar, quando estiver pronto:** tirar o `rascunho` do JSON → rodar
`node scripts/build-gabarito.js` no `fisk-hub-backend` → implantar o backend
(procedimento em `fisk-hub-backend/CLAUDE.md`; **eu publico, o Pedro não**).

---

## 2. O que já está pronto

### Gramática · 20 questões (51–70)

Distribuídas pelos pesos reais do exame:

| Capítulo | No MAGENTA | Peso no MET |
|---|---|---|
| Connectors | 3 | 13/100 |
| Gerunds & Infinitives | 2 | 12 |
| Phrasal Verbs & Prepositions | 2 | 11 |
| Inversion & Emphasis | 2 | 10 |
| Pronouns & Determiners | 2 | 10 |
| Comparatives & Superlatives | 2 | 10 |
| Embedded Questions & Word Order | 2 | 10 |
| Conditionals & Subjunctive | 2 | 7 |
| Adverbs, Modals & Tags | 1 | 7 |
| Tenses | 1 | 6 |
| Relative Clauses & Passive | 1 | 4 |

### Leitura · 30 questões (71–100)

Quatro textos originais, **no universo acadêmico**, que foi decisão do Pedro
apoiada em medição (ver seção 4):

| Questões | Cena |
|---|---|
| 71–75 | por que os alunos não vão ao *office hours* |
| 76–80 | o que acontece quando o professor flexibiliza o prazo de entrega |
| 81–90 | escolher uma eletiva — edital, orientação e dois relatos (A/B/C) |
| 91–100 | iniciação científica — chamada, notas ao candidato e ex-bolsista (A/B/C) |

Tipos de pergunta: 12 detalhe, 5 propósito, 5 inferência, 3 vocabulário,
3 referência, 2 ideia principal.

Duas conferências foram rodadas e devem ser repetidas em qualquer texto novo:
**toda palavra citada em negrito existe mesmo no texto**, e nenhuma questão tem
alternativa repetida.

---

## 3. O que falta: 50 questões de listening

Estrutura do RED, que o MAGENTA deve copiar:

| Parte | Itens | Questões | Duração média | Velocidade medida |
|---|---|---|---|---|
| Part 1 | 19 conversas curtas | 19 | 25s (17s a 70s) | **158 palavras/min** |
| Part 2 | 4 conversas longas | 14 (3–4 por conversa) | 110s | **121 palavras/min** |
| Part 3 | 4 palestras | 17 (4–5 por palestra) | 130s | **112 palavras/min** |

**33 das 50 questões são conversas entre duas pessoas.** É esse o nó.

Formato de cada item da Part 1: narrador anuncia o número → conversa → narrador
lê a pergunta. O aluno também vê a pergunta escrita.

**Especificação do áudio:** mono, 96 kbps, 44,1 kHz. São 30 MP3s no RED.

O cenário do listening do RED, contado nas transcrições: monitor corrigindo
provas e lançando notas na sala do professor, livro esgotado na livraria antes
da tarefa, projeto de pesquisa na biblioteca da universidade, dois professores
decidindo proibir laptops no próximo semestre, apresentação para a aula de
inglês, visita de pais a uma escola, reportagem de rádio sobre um museu.

---

## 4. O que já foi investigado — não repetir

### VOA · descartada para as Parts 1 e 2

Licença está **ok**: texto, MP3 e vídeo da VOA Learning English são domínio
público, com uso educacional e comercial permitido, exigindo crédito a
`learningenglish.voanews.com`. Ressalva: material de terceiros no site principal
da VOA (fotos e vídeos de AP e Reuters) não é domínio público.

Mas não serve, por dois motivos medidos:

- **Velocidade.** A VOA Learning English usa *Special English*, ~90 palavras por
  minuto, contra 158 da Part 1 do MET. Treinar a 57% da velocidade da prova
  entrega o aluno despreparado justamente na seção com mais questões.
- **Formato.** É quase toda narrador único lendo reportagem. O programa com
  diálogo (*Let's Learn English*, a série da Anna) é nível iniciante.

**Onde a VOA ainda cabe:** a Part 3, que são palestras com um locutor só — o RED
tem lá inclusive uma reportagem de rádio. E de preferência com o site principal
da VOA, que fala em velocidade natural, conferindo caso a caso o material de
terceiros.

### TTS do macOS · REPROVADA pelo Pedro

Gerei duas conversas com `say` (vozes Ava, Tom e Allison), calibradas a 163 e
169 ppm, no formato exato do RED. O Pedro ouviu e reprovou: "absolutamente
horrorosa, não tem como usar".

**O erro foi a ferramenta, não a ideia.** O `say` do macOS é TTS de geração
antiga. Não refaça por ali.

O que sobrou de útil está em **`scripts/montar-audio.py`**: a montagem (pausas
entre turnos, concatenação, formato final) serve para **qualquer origem de voz**.
Troca-se só a função que produz o áudio de cada fala.

**Achado de calibração:** o `-r` do `say` não é palavra por minuto de verdade.
Meça o resultado em vez de confiar no parâmetro — vale para qualquer ferramenta.

### YouTube · não é caminho

O Pedro perguntou se dá para baixar áudio de canais de ensino de inglês ou de
preparatórios. Não: são obras protegidas, e os Termos do YouTube proíbem
download fora dos recursos da própria plataforma. Isso exporia a escola, que é
justamente o cuidado que ele já tem ao não usar os quatro simulados oficiais.

Existe o filtro Creative Commons do YouTube (CC-BY permite reuso com crédito),
mas o acervo de conversa em cena acadêmica sob essa licença é raro e irregular.

### Corpora abertos · pesquisados, encaixe ruim

- **ELLLO** — conversas naturais de ESL, mas Creative Commons **não comercial**.
- **The People's Speech** — 30 mil horas em CC-BY, reuso comercial permitido,
  porém é base de treino de reconhecimento de fala, não cena curada.
- **LibriVox, Common Voice** — domínio público/CC0, mas leitura em voz alta e
  frases soltas, não conversa.

Nenhum entrega "duas pessoas conversando sobre prorrogação de prazo em ritmo
natural". Escrever a cena e produzir a voz continua sendo o caminho.

---

## 5. As opções que restam, em ordem de recomendação

1. **TTS neural moderno via API** (ElevenLabs, OpenAI, Google, Azure). É o que
   "voz sintética hoje" significa de verdade, e para diálogo roteirizado a
   qualidade é outra. **Precisa de uma chave de API — não há nenhuma nesta
   máquina** (conferido). Custo estimado baixo para ~15 minutos de áudio.
2. **Locutor nativo em plataforma de freelancer.** Duas vozes, ~15 minutos de
   áudio no total. Fidelidade perfeita e nenhuma dúvida de licença.
3. **VOA só para a Part 3** (17 questões), com o fluxo invertido: escolher a
   reportagem real, transcrever e escrever as questões em cima dela. Não resolve
   as 33 questões das Parts 1 e 2.

O Pedro descartou gravar ele mesmo com um professor: os dois são brasileiros e
ele quer fidelidade ao falante nativo.

---

## 6. O que fazer na próxima sessão

**Independe da decisão do áudio** e pode começar já: escrever os **23 roteiros**
(19 conversas curtas, 4 longas) e as **4 palestras**, com as 50 questões, no
universo acadêmico e nos ritmos da tabela da seção 3. É onde está o valor
pedagógico, e ele não muda conforme quem dubla.

Duas conversas já foram escritas e aprovadas como conteúdo (só a voz foi
reprovada), e estão em `scripts/montar-audio.py`:

- **Q1 · prorrogação de prazo** — aluna perde metade do trabalho quando o laptop
  morre; o professor dá até segunda e pede o roteiro no mesmo dia.
- **Q2 · a eletiva** — a disciplina choca com o laboratório de química, e a única
  outra turma é sexta às oito da manhã.

**Depois de decidido o áudio:** produzir, montar com `scripts/montar-audio.py`,
conferir duração e ppm contra a tabela, gravar os MP3s em `audio/magenta/`,
acrescentar as unidades `l1`/`l2`/`l3` ao `questions/magenta.json` com os
`topic` já no padrão (`Listening · Detalhe`, `Listening · Inferência`,
`Listening · Ideia principal`, `Listening · Propósito`,
`Listening · Intenção do falante`) e só então publicar.

---

## 7. Onde as coisas moram

| | |
|---|---|
| `questions/magenta.json` | o simulado (50 questões escritas) |
| `questions/red.json` | o oficial, referência de estrutura e formato |
| `data/transcripts-red.json` | transcrições do listening do RED — foi daqui que saíram as medições |
| `scripts/montar-audio.py` | montagem do áudio, reaproveitável |
| `audio/red/` | os 30 MP3s do RED, referência de formato |
| `../Cadernos-Atividades-Fisk/Focus_Caderno/MET-Study-Guide-original.pdf` | o guia, com os pesos dos 11 capítulos |
| `../fisk-hub-backend/CLAUDE.md` | como publicar no Apps Script |
| `../fisk-simulador/CLAUDE.md` | Quick Practice, o mapa Study Guide × livro |
