# met-siele-simulador: Treino MET e Treino SIELE

Simuladores do MET (inglês) e do SIELE (espanhol), servidos pelo GitHub Pages
em `pedro-fisk.github.io/met-siele-simulador`. **HTML estático, sem build.**
Todo o app é o `index.html`; os bancos moram em `questions/*.json` (`red`,
`emerald`, `amber` do MET; `siele-m0` e `siele-m1` do SIELE), escolhidos por
`?exame=` (`met` é o padrão). Decisões e histórico: `docs/roadmap-met.md`.

## Portas de entrada

| Como entra | URL | O que muda |
|---|---|---|
| Aluno, pelo Portal | `?exame=…#raf=&nome=&book=` | nome travado; resultado vai para a nuvem com o RAF; progresso e tranca por aluno |
| Aluno solto | `?exame=…` | digita o nome; resultado só gera código |
| Professor, pelo Portal do Aluno (visão do professor, RAF `0000-000` ou Direção) | `?exame=…&modo=professor#raf=…` | uma questão por vez, para projetar na TV; sem nome, sem timer, sem tour, sem tranca, sem envio; teclado/passador |

⚠️ **O professor chega pelo card do Portal do Aluno** (tabela `TEACHER_MODE`
em `portal-aluno-fisk/assets/portal-app.js`, `met` e `siele` com
`query: 'modo=professor'`). A identidade vem no fragmento, nunca na query.

Modo professor (desde 17/09/2026, o mesmo desenho do Quick Practice,
`fisk-simulador` commit `5b30f54`):

- **Tamanho encaixado**: todo o CSS de TV depende de `body.prof-mode`; as
  fontes usam `min(vw, vh)` vezes o fator `--pf`, e `profEncaixa()` reduz o
  fator (passo 0,05, mínimo 0,55) até o cartão `#prof-card` (texto, player,
  questão, explicação aberta) terminar acima da barra `#prof-bar`. Roda ao
  desenhar, ao revelar, no resize e quando as fontes carregam. Leitura vai em
  duas colunas (`.prof-leitura`). Abaixo de 0,55 a página rola: a questão
  não coube, e isso é conteúdo a dividir, não fator a baixar.
- **Teclado/passador**: → e PageDown avançam, ← e PageUp voltam, Espaço e
  Enter revelam, A–D (e as letras seguintes do banco do SIELE) e 1–9 marcam a
  resposta da turma. Só na tela da questão, e nunca com o foco num campo (a
  barra de tempo do player é um input: ali as setas mexem no áudio).
- **Troca de modo**: quem chega com `modo` na URL (professor ou aluno) vê o
  botão "Switch to Student/Teacher Mode" (no SIELE, "Pasar al Modo
  Alumno/Profesor"), que troca `modo` e preserva o resto da query e o
  fragmento. O aluno comum, sem `modo`, não vê.
- A barra e a linha de atalhos ficam em inglês no MET e em espanhol no SIELE
  (`PROF_TXT`); os botões da barra continuam em português.

## PEARL: prova oficial CIFRADA (desde 24/09/2026)

A PEARL é a MET 2603 A, forma **oficial** e "SECURE TEST" da Michigan. Este
repositório é público, então ela mora aqui **cifrada** (AES-256-GCM):

- `questions/pearl.json` é só o esqueleto que a home precisa (cor, seções,
  minis, a contagem de questões) mais `cifra`, o banco inteiro cifrado;
- `audio/pearl/*.mp3.enc` são os áudios oficiais, cifrados.

Ao abrir, `abreCofre()` pede a chave ao backend (rota `provaChave`), decifra
o banco no mesmo objeto e os áudios viram blobs locais (`audioCifrado`). A
chave só sai para RAF do roster a partir de `liberaEm` (01/11/2026; até lá o
card é "Soon"), ou antes disso para quem tem a chave do professor salva no
aparelho. **A fonte em claro e o cifrador não moram aqui**: estão em
`fisk-hub-backend/provas-privadas/pearl/` (repositório privado). Nunca
commitar o `pearl.json` em claro, os MP3 da PEARL ou os scripts que os montam
neste repositório.

A PEARL **não tem `expl`** (decisão do Pedro): o Teacher Mode revela só a
letra.
