# Handoff: o listening do simulado EMERALD

Escrito em 10/08/2026, para retomar numa sessão nova. O EMERALD está com
**50 das 100 questões prontas** (gramática e leitura). Falta o listening inteiro,
e a decisão que trava tudo é **de onde vem o áudio**.

---

## 1. O que é o EMERALD e por que ele existe

Simulado do MET **escrito pela Fisk**. Os outros quatro oficiais (GREEN, PURPLE,
YELLOW, BLUE) não podem virar treino porque são aplicados presencialmente; o RED
já é usado e sozinho não basta.

Dos oficiais vem só a **estrutura** e o **peso de cada capítulo**, nunca
enunciado, texto ou alternativa. O peso é o motivo de escrever do zero: o RED
traz **uma** questão de conectores, que é o capítulo mais cobrado da prova (13 em
100). O EMERALD traz três, seguindo a distribuição que o MET Study Guide apurou
nos cinco simulados.

**Arquivo:** `questions/emerald.json` · **Como abrir:** `?exame=emerald`

### Ele está FORA DO AR, com três trancas

1. Nenhum card do Portal aponta para ele. Só se chega pelo parâmetro.
2. Com `rascunho: true` no JSON, a home mostra um aviso de simulado em
   construção, dizendo que não é prova oficial da Michigan Language Assessment.
3. Com `rascunho: true`, **nada é enviado**, nem de aluno logado nem solto. E o
   gerador do gabarito no `fisk-hub-backend` pula bancos em rascunho, então o
   servidor nem sabe corrigi-lo.

**Publicar, quando estiver pronto:** tirar o `rascunho` do JSON → rodar
`node scripts/build-gabarito.js` no `fisk-hub-backend` → implantar o backend
(procedimento em `fisk-hub-backend/CLAUDE.md`; **eu publico, o Pedro não**).

---

## 2. O que já está pronto

### Gramática · 20 questões (51–70)

Distribuídas pelos pesos reais do exame:

| Capítulo | No EMERALD | Peso no MET |
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
| 81–90 | escolher uma eletiva: edital, orientação e dois relatos (A/B/C) |
| 91–100 | iniciação científica: chamada, notas ao candidato e ex-bolsista (A/B/C) |

Tipos de pergunta: 12 detalhe, 5 propósito, 5 inferência, 3 vocabulário,
3 referência, 2 ideia principal.

Duas conferências foram rodadas e devem ser repetidas em qualquer texto novo:
**toda palavra citada em negrito existe mesmo no texto**, e nenhuma questão tem
alternativa repetida.

---

## 3. O que falta: 50 questões de listening. DESTRAVADO, a voz foi aprovada

**A decisão que travava tudo foi resolvida em 10/08/2026: edge-TTS, aprovado
pelo Pedro** ("ficou muito melhor"). O que falta agora é só trabalho, e ele
pediu que a próxima sessão comece por ele:

> "pode fazer os 23 roteiros restantes em uma próxima sessão, a partir do
> handoff atualizado"

**Feito em 11/08/2026: o listening está pronto.** Os 27 roteiros, as 50
questões, os 30 MP3s e as unidades no banco. O simulado tem as 100 questões.
Falta só publicar, que é o passo 5 da seção 6.

Na mesma sessão o simulado deixou de se chamar MAGENTA e virou **EMERALD**,
com a cor verde vindo do próprio banco (`"cor"` no JSON).

Estrutura do RED, que o EMERALD deve copiar:

| Parte | Itens | Questões | Duração média | ppm do arquivo | ppm falado |
|---|---|---|---|---|---|
| Part 1 | 19 conversas curtas | 19 | 25s (17s a 70s) | 158 | ~158 |
| Part 2 | 4 conversas longas | 14 (3–4 por conversa) | 110s | 114 | **182** |
| Part 3 | 4 palestras | 17 (4–5 por palestra) | 130s | 113 | **165** |

> **Correção de 11/08: os 121 e 112 ppm não eram velocidade de fala.** Os
> arquivos das Parts 2 e 3 carregam ~12s de silêncio depois de cada pergunta,
> para o aluno responder, e é esse silêncio que derruba a média. Medindo só o
> trecho falado, a conversa longa do MET é falada **mais rápido** que a curta:
> 182 ppm. Quem desacelerasse a voz até 120 ppm produziria um áudio
> irreconhecível. O silêncio de resposta tem que estar *dentro* do MP3.

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

## 4. O que já foi investigado, e não se repete

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

**Onde a VOA ainda cabe:** a Part 3, que são palestras com um locutor só, e o RED
tem lá inclusive uma reportagem de rádio. E de preferência com o site principal
da VOA, que fala em velocidade natural, conferindo caso a caso o material de
terceiros.

### Voz · RESOLVIDA: edge-TTS da Microsoft, aprovado

A primeira tentativa usou o `say` do macOS e o Pedro reprovou na hora
("absolutamente horrorosa"). **O erro foi a ferramenta, não a ideia**, e a
ferramenta certa já estava na casa: a trilha de espanhol do Listening Lab, no
`portal-aluno-fisk`, já usava **edge-TTS** em produção. Refeitas as mesmas duas
conversas com ele, o veredito mudou: "ficou muito melhor".

**A receita aprovada está em `scripts/montar-audio.py`, pronta para rodar.**

| | |
|---|---|
| Motor | edge-TTS (Microsoft): vozes neurais, gratuito, **sem chave de API** |
| Vozes | as **Multilingual**, que são a geração mais natural em diálogo |
| Par do item 1 | Ava + Andrew |
| Par do item 2 | Emma + Brian |
| Narradora | Aria, fixa em todos os itens |
| Formato | mono, 96 kbps, 44,1 kHz, idêntico ao RED |
| Pausas | 0,35s entre falas · 0,9s antes da pergunta |

**RITMO: a parte que exigiu duas rodadas e é a mais fácil de errar.**

A +12% o resultado saiu a 166 e 163 ppm, praticamente no ritmo medido da prova.
O Pedro ouviu e disse: está na velocidade natural, mas **como não é voz humana,
soa rápido demais**. Pediu ~5% mais lento. A recalibragem entregou 164 e 157 ppm.

> **A lição para quem produzir os outros 48: voz sintética no ritmo humano
> PARECE mais rápida que a humana.** O número medido no RED é o piso, não a
> meta. Para TTS, fique um pouco abaixo dele.

E o ritmo **varia por falante** de propósito, porque dois falantes na mesma
velocidade exata soam mecânicos. Hoje: `+8%` e `+5%` num item, invertido no outro. A tabela
`RITMO` do script é por item, então dá para ajustar caso a caso.

Se ele ainda achar corrido, é uma linha: baixar os percentuais dessa tabela.

**Achado que vale para qualquer motor:** o parâmetro de velocidade é promessa,
não medida. No `say`, pedir 165 devolvia 178 ppm. O script imprime o ppm de cada
arquivo para fechar esse laço. **Sempre confira a saída.**

### YouTube · não é caminho

O Pedro perguntou se dá para baixar áudio de canais de ensino de inglês ou de
preparatórios. Não: são obras protegidas, e os Termos do YouTube proíbem
download fora dos recursos da própria plataforma. Isso exporia a escola, que é
justamente o cuidado que ele já tem ao não usar os quatro simulados oficiais.

Existe o filtro Creative Commons do YouTube (CC-BY permite reuso com crédito),
mas o acervo de conversa em cena acadêmica sob essa licença é raro e irregular.

**O Pedro então propôs o caminho certo: incorporar em vez de baixar.** Isso não
serve para o simulado (ver por quê no roadmap do Listening Lab), mas virou uma
frente própria e aprovada: prática de escuta nos estágios avançados, dentro do
Listening Lab do Portal do Aluno. Está registrada em
`../portal-aluno-fisk/docs/roadmap-listening.md`, seção "Vídeos do YouTube
incorporados".

### Corpora abertos · pesquisados, encaixe ruim

- **ELLLO**: conversas naturais de ESL, mas Creative Commons **não comercial**.
- **The People's Speech**: 30 mil horas em CC-BY, reuso comercial permitido,
  porém é base de treino de reconhecimento de fala, não cena curada.
- **LibriVox, Common Voice**: domínio público/CC0, mas leitura em voz alta e
  frases soltas, não conversa.

Nenhum entrega "duas pessoas conversando sobre prorrogação de prazo em ritmo
natural". Escrever a cena e produzir a voz continua sendo o caminho.

---

## 5. Frente separada: o Listening Lab com YouTube

Enquanto se discutia o áudio do simulado, o Pedro propôs incorporar vídeos do
YouTube em vez de baixá-los. **Não serve para o simulado** (o aluno veria quem
fala, controlaria o play, e esconder a imagem é proibido pelos termos), mas
virou frente própria e aprovada: prática de escuta nos estágios avançados,
dentro do Listening Lab do Portal do Aluno.

Registrada em `../portal-aluno-fisk/docs/roadmap-listening.md`, seção "Vídeos do
YouTube incorporados". **É outra frente, não bloqueia esta.**

## 6. O que fazer na próxima sessão

**Publicar.** O conteúdo acabou em 11/08/2026.

| Entregue | Itens | Questões | ppm falado |
|---|---|---|---|
| Part 1 · conversas curtas | 19 | 19 | ~145 |
| Part 2 · conversas longas | 4 | 14 (3–4 cada) | 151 a 159 |
| Part 3 · palestras | 4 | 17 (4–5 cada) | 150 a 151 |

Ficamos de propósito abaixo do RED (182 e 165 falados) pela lição da Part 1:
voz sintética no ritmo humano parece mais rápida que a humana.

> **As vozes não têm o mesmo passo com o mesmo parâmetro.** No `-8%`, a Ava
> entrega 173 ppm e o Andrew 148, uma diferença de 17% que o parâmetro não
> avisa. Por isso o ritmo é calibrado por item, e não por seção. Se entrar
> falante novo, gere um item, meça e só então espalhe.

**Universo:** o acadêmico, o mesmo da leitura. As cenas do RED servem de guia:
monitor corrigindo provas, livro esgotado na livraria, projeto de pesquisa na
biblioteca, professores decidindo proibir laptops, visita de pais à escola,
reportagem de rádio sobre um museu.

**Também ficaram prontos na mesma sessão**, e não são listening:

- **Os 4 mini simulados**, na mesma divisão do RED: cobrem as 100 questões sem
  sobra nem repetição.
- **A ponte para o Quick Practice.** Cada capítulo do Study Guide carrega no
  banco (`qp`) a lista de tópicos equivalentes do In Focus, e a tela de
  resultado leva o aluno ao Custom Practice já marcado. Um nome de tópico
  errado **some lá sem erro nenhum**, então confira contra o `LESSON_MAP` do
  `fisk-simulador/index.html` sempre que mexer. O RED ainda não tem essa ponte.

**Passo a passo, e onde parou:**

1. ~~Escrever os roteiros e as questões~~ · feito, em `data/roteiros-emerald.json`.
   Voz e ritmo de cada item moram lá também; o script só executa.
2. ~~Amostra para o Pedro validar antes de gerar tudo~~ · enviada em 11/08:
   `l1-q03`, `l2-q24-26` e `l3-q38-41`.
3. ~~`python3 scripts/montar-audio.py`~~ · os 30 MP3s estão em `audio/emerald/`,
   e as durações e cues em `data/cues-emerald.json`.
4. ~~`python3 scripts/montar-unidades.py`~~ · as 50 questões entraram no
   `questions/emerald.json`, com os cues que o áudio produziu.
5. **Aqui: publicar.** Tirar o `rascunho` do JSON, rodar
   `node scripts/build-gabarito.js` no `fisk-hub-backend` e implantar o backend.
   Depois disso, apontar um card do Portal para `?exame=emerald`, que hoje não
   existe de propósito.

Se ele achar corrido, é uma linha: baixar o `ritmo` do item no roteiro e
regerar só ele (`python3 scripts/montar-audio.py l3-set2`).

## 7. Onde as coisas moram

| | |
|---|---|
| `questions/emerald.json` | o simulado, 100 questões, a cor, os minis e a ponte `qp` |
| `questions/red.json` | o oficial, referência de estrutura e formato |
| `data/transcripts-red.json` | transcrições do listening do RED, foi daqui que saíram as medições |
| `data/roteiros-emerald.json` | os 27 roteiros e as 50 questões do listening; voz e ritmo por item |
| `data/cues-emerald.json` | duração, ppm e cues, escritos pela geração do áudio |
| `scripts/montar-audio.py` | montagem do áudio, reaproveitável |
| `scripts/montar-unidades.py` | roteiros + cues → as unidades do `emerald.json` |
| `audio/emerald/` | os 30 MP3s do simulado |
| `audio/red/` | os 30 MP3s do RED, referência de formato |
| `../Cadernos-Atividades-Fisk/Focus_Caderno/MET-Study-Guide-original.pdf` | o guia, com os pesos dos 11 capítulos |
| `../fisk-hub-backend/CLAUDE.md` | como publicar no Apps Script |
| `../fisk-simulador/CLAUDE.md` | Quick Practice, o mapa Study Guide × livro |
