#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta questions/amber.json, a terceira prova do simulador MET.

O esqueleto (seções, CEFR, capítulos de gramática, ponte para o Quick Practice)
é COPIADO do EMERALD: é a mesma prova, com outro banco de itens. O que muda é o
conteúdo, original, e a cor.

Universo, decisão do Pedro: 70% acadêmico, 30% trabalho e vida urbana.

Esta rodada escreve Grammar (51–70) e Reading (71–100). O listening (1–50) entra
na próxima, com roteiro próprio e edge-TTS, como no EMERALD.
"""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
emerald = json.load(open(os.path.join(REPO, 'questions', 'emerald.json')))


def q(n, topic, text, opts, key, expl):
    return {'n': n, 'id': 'amberq%03d' % n, 'topic': topic, 'text': text,
            'opts': opts, 'key': key, 'expl': expl}


# ─────────────────────────────────────────────────────────────────────────────
# GRAMMAR · 51–70, nos pesos que o MET Study Guide apurou nos cinco simulados
# ─────────────────────────────────────────────────────────────────────────────
GR = [
    q(51, 'Connectors',
      'The lab reported no unusual readings; _____, the inspection went ahead as scheduled.',
      ['accordingly', 'nevertheless', 'otherwise', 'meanwhile'], 0,
      'A segunda oração é a CONSEQUÊNCIA da primeira: como nada apareceu, a inspeção seguiu. Accordingly marca resultado. Nevertheless marcaria contraste, otherwise marcaria alternativa e meanwhile só situaria no tempo.'),
    q(52, 'Connectors',
      '_____ the funding was approved late, the team managed to finish the survey on time.',
      ['In spite of', 'Despite', 'Even though', 'Regardless of'], 2,
      'Depois da lacuna vem uma oração completa, com sujeito e verbo ("the funding was approved"). Só EVEN THOUGH aceita oração. In spite of, despite e regardless of pedem substantivo ou gerúndio.'),
    q(53, 'Connectors',
      'The building has no lift, _____ the reading room was moved to the ground floor.',
      ['so that', 'in order to', 'which is why', 'as long as'], 2,
      'A lacuna liga um fato à sua consequência já ocorrida: não há elevador, POR ISSO a sala mudou de andar. Which is why faz exatamente essa ligação. So that e in order to introduziriam finalidade, e as long as, condição.'),
    q(54, 'Gerunds & Infinitives',
      'The committee recommended _____ the deadline by two weeks.',
      ['to extend', 'extending', 'extend', 'that extending'], 1,
      'Recommend é seguido de gerúndio quando não há objeto entre os dois verbos: recommend DOING. Com objeto, a estrutura seria "recommended that the department extend the deadline".'),
    q(55, 'Gerunds & Infinitives',
      'She stopped _____ her notes and looked up at the screen.',
      ['to read', 'reading', 'read', 'having read'], 1,
      'Ela INTERROMPEU a leitura para olhar a tela: stop + gerúndio é parar de fazer aquilo. Stop to read seria parar com a finalidade de ler, o contrário do que a frase descreve.'),
    q(56, 'Phrasal Verbs & Prepositions',
      'The department had to _____ the seminar because the visiting speaker fell ill.',
      ['call off', 'call for', 'call up', 'call on'], 0,
      'Call off é cancelar, que é o que a doença do palestrante provoca. Call for é exigir, call up é telefonar e call on é visitar ou convocar alguém a falar.'),
    q(57, 'Phrasal Verbs & Prepositions',
      'Enrolment figures this term are consistent _____ the forecast published in March.',
      ['to', 'with', 'of', 'for'], 1,
      'Consistent pede WITH quando significa estar de acordo com alguma coisa. As outras preposições não acompanham esse adjetivo nesse sentido.'),
    q(58, 'Inversion & Emphasis',
      'Not until the final week _____ that the two datasets had been swapped.',
      ['the researchers realised', 'did the researchers realise', 'the researchers did realise', 'realised the researchers'], 1,
      'Expressão negativa no começo da frase (not until) obriga a inversão com auxiliar: DID + sujeito + verbo na forma base. A ordem normal só valeria se a frase começasse pelo sujeito.'),
    q(59, 'Inversion & Emphasis',
      '_____ was the response to the survey that the team extended it for another month.',
      ['So strong', 'Such strong', 'Very strong', 'Too strong'], 0,
      'A estrutura é so + adjetivo + that. Such pediria substantivo ("such a strong response that"). Very e too não abrem frase invertida com that consecutivo.'),
    q(60, 'Pronouns & Determiners',
      'Each of the three campuses runs _____ own library system.',
      ['their', 'its', "it's", 'his'], 1,
      'O sujeito é each of, que é singular, então o possessivo é ITS. Their concordaria com um sujeito plural, e it\'s é a contração de it is.'),
    q(61, 'Pronouns & Determiners',
      'There were _____ applicants than places, so the panel interviewed everyone.',
      ['less', 'fewer', 'fewest', 'few'], 1,
      'Applicants é contável no plural, então o comparativo é FEWER. Less acompanha incontáveis, e fewest e few não formam comparação com than.'),
    q(62, 'Comparatives & Superlatives',
      'The revised timetable is _____ than the one it replaced.',
      ['far more practical', 'far practical', 'much practicaler', 'the most practical'], 0,
      'Practical é adjetivo longo, então o comparativo é more practical, e far o intensifica. Practicaler não existe, e o superlativo the most practical não combina com than.'),
    q(63, 'Comparatives & Superlatives',
      'The sooner the samples reach the lab, _____ the results will be.',
      ['the reliable', 'the more reliable', 'more reliable', 'the most reliable'], 1,
      'A estrutura é the + comparativo, the + comparativo, e os dois lados precisam do the: the sooner…, the MORE RELIABLE… O superlativo quebraria o paralelo.'),
    q(64, 'Embedded Questions & Word Order',
      'The porter asked me _____ the parcel had been delivered.',
      ['when had it', 'when it had', 'when did it', 'when was it'], 1,
      'Pergunta embutida em uma frase afirmativa mantém a ordem sujeito + verbo: when IT HAD been delivered. A inversão só valeria numa pergunta direta.'),
    q(65, 'Embedded Questions & Word Order',
      'Could you tell me _____ to submit the form online?',
      ['whether is it possible', 'is it possible', 'whether it is possible', 'that is it possible'], 2,
      'Depois de tell me a pergunta vem embutida, com whether e a ordem normal: whether IT IS possible. Manter "is it" deixaria a pergunta direta dentro da indireta.'),
    q(66, 'Conditionals & Subjunctive',
      'If the sensor _____ calibrated last week, the readings would make sense now.',
      ['was', 'had been', 'would be', 'has been'], 1,
      'A condição está no passado (last week) e o resultado, no presente (now): é a condicional mista, com had been na condição e would + verbo no resultado.'),
    q(67, 'Conditionals & Subjunctive',
      'The board insisted that the report _____ before the end of the quarter.',
      ['is published', 'be published', 'was published', 'will be published'], 1,
      'Insist that pede o subjuntivo, que em inglês é a forma base do verbo, sem concordância: BE published, para qualquer sujeito.'),
    q(68, 'Adverbs, Modals & Tags',
      'You needn\'t have printed the handouts, _____?',
      ['did you', 'needn\'t you', 'had you', 'have you'], 0,
      'Needn\'t have + particípio se comporta como passado, e a tag correspondente usa did. As outras formas não retomam esse tempo.'),
    q(69, 'Tenses',
      'By the time the auditors arrive tomorrow, the team _____ the inventory.',
      ['will finish', 'will have finished', 'finishes', 'has finished'], 1,
      'A ação termina ANTES de um momento futuro (by the time… tomorrow), que é o uso do futuro perfeito: will have finished.'),
    q(70, 'Relative Clauses & Passive',
      'The archive, _____ was damaged by the flood, reopened in March.',
      ['that most of it', 'most of which', 'which most of it', 'that most'], 1,
      'A oração relativa não defensiva, entre vírgulas, não aceita that, e a quantificação se faz com most OF WHICH. As outras opções deixam um pronome sobrando dentro da relativa.'),
]

# ─────────────────────────────────────────────────────────────────────────────
# READING · 71–100. Três blocos acadêmicos e um de trabalho e vida urbana,
# que é a proporção 70/30 pedida.
# ─────────────────────────────────────────────────────────────────────────────
P1 = (
 "<p>Ask a student how they prepare for an examination and the answer is almost always the same: "
 "they read the material again. It feels like the obvious thing to do, and it feels like it is "
 "working. That second impression is the problem.</p>"
 "<p>When a page is read for the third or fourth time, it becomes easy to process. The mind mistakes "
 "that smoothness for knowledge, and the student closes the book confident. The confidence is not "
 "matched by performance. In one well-known comparison, students who reread a text and students who "
 "put it aside and tried to recall it performed almost identically on a test taken ten minutes later. "
 "Two days later, the group that had tried to recall the material was far ahead, and it was the "
 "rereaders who had predicted they would do better.</p>"
 "<p>The explanation is that recall is difficult in a useful way. Retrieving an idea without the page "
 "in front of you strengthens the path back to it; reading it again only strengthens the impression "
 "that you have seen it before. Difficulty here is not an obstacle to learning but a condition of it, "
 "which is why the more comfortable method is the weaker one.</p>"
 "<p>Departments that teach this to first-year students report a familiar objection: recall feels "
 "unpleasant, and students abandon it in the week before an examination, when the pressure is highest "
 "and the temptation to feel prepared is strongest. The technique is not hard to learn. It is hard to "
 "trust.</p>"
)
RD1 = [
 q(71, 'Reading · Ideia principal',
   'What is the main point of the passage?',
   ['Rereading feels effective but teaches less than recalling does',
    'Students should spend more hours preparing for examinations',
    'Examinations taken two days apart give different results',
    'First-year students are given poor advice by their departments'], 0,
   'O texto contrapõe as duas técnicas do começo ao fim: reler dá a sensação de saber, recuperar de memória é que ensina. As outras opções tocam em detalhes que aparecem, mas nenhuma sustenta o texto inteiro.'),
 q(72, 'Reading · Detalhe',
   'What did the two groups of students have in common ten minutes after studying?',
   ['Both predicted the same result', 'Both performed at a similar level',
    'Both had reread the material', 'Both had abandoned the technique'], 1,
   'O texto diz que os dois grupos tiveram desempenho quase idêntico no teste feito dez minutos depois. A diferença só apareceu dois dias mais tarde.'),
 q(73, 'Reading · Vocabulário',
   'In the third paragraph, "retrieving" is closest in meaning to',
   ['bringing back from memory', 'copying by hand', 'reading out loud', 'checking against a source'], 0,
   'O parágrafo explica a técnica de recuperar a ideia sem a página à frente, que é trazer de volta da memória. As outras opções descrevem ações que dependem justamente do texto presente.'),
 q(74, 'Reading · Inferência',
   'What does the passage suggest about the week before an examination?',
   ['It is when students most need to feel prepared',
    'It is when departments stop giving advice',
    'It is when rereading finally becomes effective',
    'It is when most examinations are rescheduled'], 0,
   'O último parágrafo diz que a pressão é máxima e a tentação de se SENTIR preparado é a mais forte, e é por isso que a técnica é abandonada. O texto não sugere nenhuma das outras.'),
 q(75, 'Reading · Propósito',
   'Why does the writer end with "It is hard to trust"?',
   ['To argue that the technique needs more research',
    'To explain why a method that works is still not used',
    'To criticise students who prepare at the last minute',
    'To recommend that departments change their examinations'], 1,
   'A frase fecha o parágrafo que descreve o abandono da técnica: o obstáculo não é a dificuldade de aprender, é a de confiar nela. Não há crítica aos alunos nem proposta de mudar as provas.'),
]

P2 = (
 "<p>When the software company where Nadia works moved to three days in the office, it kept the same "
 "floor and simply removed the name plates. Desks became first come, first served. Management called "
 "the change flexible; within a month the staff had renamed it the seat race.</p>"
 "<p>The arithmetic looked sound. If nobody is in every day, a hundred employees do not need a hundred "
 "desks, and the company was paying for space that stood empty on Mondays and Fridays. What the "
 "arithmetic missed is that people do not arrive at random. Everyone wanted Tuesday and Wednesday, so "
 "the days that were supposed to be quiet were crowded, and the desks nobody wanted sat empty on the "
 "days nobody came.</p>"
 "<p>The second surprise was social. Teams that had sat together for years were now scattered by "
 "whoever booked first, and the informal exchange that made the office worth the commute went with "
 "them. Nadia describes arriving at nine, finding no free desk near her team, and spending the day in "
 "a corner answering the same messages she could have answered at home.</p>"
 "<p>Some employers have since fixed the problem by giving each team a zone rather than each person a "
 "desk, which preserves the saving without scattering the people. Others have concluded that the "
 "office is now for meeting rather than for working, and rebuilt it accordingly. What no longer "
 "convinces anyone is the middle position: asking people to travel in for the sake of a desk that is "
 "no better than the one at home.</p>"
)
RD2 = [
 q(76, 'Reading · Detalhe',
   'Why did the company remove the name plates?',
   ['Because staff no longer came in every day',
    'Because the teams had asked for a change',
    'Because the building was being renovated',
    'Because new employees had been hired'], 0,
   'O texto liga a mudança à passagem para três dias no escritório: se ninguém vem todo dia, cem funcionários não precisam de cem mesas.'),
 q(77, 'Reading · Ideia principal',
   'What is the writer\'s main criticism of the new arrangement?',
   ['It cost more than the company expected',
    'It assumed people would spread evenly across the week',
    'It reduced the number of meetings',
    'It was introduced without telling the staff'], 1,
   'O erro central que o texto aponta é o da conta: as pessoas não chegam ao acaso, todo mundo quer terça e quarta. Os outros itens não são apresentados como problema.'),
 q(78, 'Reading · Referência',
   'In the third paragraph, "them" refers to',
   ['the teams that had sat together', 'the desks near the window',
    'the messages Nadia answered', 'the days nobody came'], 0,
   'A frase diz que a troca informal foi embora COM eles, retomando as equipes que foram espalhadas. Os outros candidatos não cabem na frase.'),
 q(79, 'Reading · Inferência',
   'What can be inferred about Nadia\'s day in the corner?',
   ['It showed the office had lost its advantage over home',
    'It proved she preferred working alone',
    'It was caused by a fault in the booking system',
    'It convinced her to change teams'], 0,
   'Ela passa o dia respondendo as mesmas mensagens que responderia de casa, ou seja, a viagem não entregou nada que a casa não desse. Nada no texto indica preferência, falha de sistema ou mudança de equipe.'),
 q(80, 'Reading · Propósito',
   'What is the purpose of the final paragraph?',
   ['To show that two workable answers exist and one does not',
    'To recommend that companies return to fixed desks',
    'To explain how much money the change saved',
    'To describe what other employees told Nadia'], 0,
   'O parágrafo apresenta duas saídas que funcionam, a zona por equipe e o escritório de reuniões, e recusa a posição do meio. Não há recomendação de voltar às mesas fixas nem números de economia.'),
]

T3 = [
 {'tag': 'A', 'html':
  "<h4>Interlibrary Loans — Main Library</h4>"
  "<p><strong>What the service is for.</strong> If an item you need is not held by this library, we "
  "will request it from another institution at no cost to you.</p>"
  "<ul>"
  "<li>Books usually arrive within <strong>five working days</strong>; journal articles arrive as "
  "scans, normally within 48 hours</li>"
  "<li>Requests are limited to <strong>eight open items</strong> per reader at any time</li>"
  "<li>A borrowed book must be read <em>in the library</em> if the lending institution marks it "
  "reference only, which is the case for roughly one request in five</li>"
  "<li><strong>Renewals are not automatic.</strong> The lending library decides, and a book recalled "
  "by its owner must be returned within three days</li>"
  "</ul>"
  "<p>Undergraduates should note that items already available as e-books through our catalogue will "
  "not be requested. Check the catalogue first.</p>"},
 {'tag': 'B', 'html':
  "<h4>Planning a dissertation: reading — Writing Centre</h4>"
  "<p><strong>How early should I start looking for sources?</strong><br>Earlier than feels necessary. "
  "The students who run into trouble in the final month are almost never the ones who cannot write; "
  "they are the ones who discover in week nine that the book at the centre of their argument takes a "
  "week to arrive.</p>"
  "<p><strong>Should I read everything I request?</strong><br>No, and planning to is a mistake. Read "
  "the introduction and the conclusion of a book before deciding whether the middle is for you. Most "
  "of what you request will be checked, not read.</p>"
  "<p><strong>Is a scanned article as good as the book?</strong><br>For a single chapter, usually. For "
  "an argument you intend to build on, borrow the whole work: chapters written to be read in sequence "
  "rarely survive being read alone.</p>"},
 {'tag': 'C', 'html':
  "<h4>Two students on the same deadline</h4>"
  "<p><strong>Priya, final year:</strong> I requested nine items in one afternoon and the system took "
  "eight. That is how I learned about the limit. Two of them came marked reference only, so I read "
  "them at a desk on the third floor, which I had not planned for at all. It cost me a Saturday, but "
  "the chapter I needed was in one of those two.</p>"
  "<p><strong>Tomás, final year:</strong> I ordered nothing until the middle of term because I assumed "
  "everything would be online. Half of it was. The other half is why I spent the last fortnight "
  "writing around a book instead of from it. If I did it again I would order in week two and accept "
  "that some of it would be wasted.</p>"},
]
RD3 = [
 q(81, 'Reading · Detalhe',
   'According to Text A, how many open requests may a reader have at one time?',
   ['three', 'five', 'eight', 'forty-eight'], 2,
   'O texto A limita a oito itens em aberto por leitor. Cinco são os dias úteis de espera pelos livros, e 48 são as horas dos artigos digitalizados.'),
 q(82, 'Reading · Detalhe',
   'According to Text A, what happens if the owning library recalls a book?',
   ['It must be returned within three days', 'It is renewed automatically',
    'It becomes reference only', 'It is replaced by a scan'], 0,
   'A última regra do texto A diz que o livro chamado de volta pela biblioteca de origem tem de voltar em três dias, e que renovação não é automática.'),
 q(83, 'Reading · Inferência',
   'What does Text A suggest about e-books in the catalogue?',
   ['They take longer to arrive than printed books',
    'They make an interlibrary request unnecessary',
    'They are limited to undergraduates',
    'They must be read in the library'], 1,
   'O texto avisa que itens já disponíveis como e-book não serão solicitados e manda conferir o catálogo primeiro, ou seja, o pedido perde a razão de ser.'),
 q(84, 'Reading · Ideia principal',
   'What is the main advice in Text B?',
   ['Request sources sooner than you think you need to',
    'Read every source you request from beginning to end',
    'Prefer scanned articles to borrowed books',
    'Write the dissertation before choosing the sources'], 0,
   'A primeira resposta do texto B é "earlier than feels necessary", e o exemplo da semana nove reforça. As outras contrariam o que ele diz.'),
 q(85, 'Reading · Detalhe',
   'According to Text B, how should you decide whether to read the middle of a book?',
   ['By reading the introduction and the conclusion first',
    'By checking how long the loan lasts',
    'By asking the Writing Centre',
    'By comparing it with a scanned chapter'], 0,
   'O texto B recomenda ler a introdução e a conclusão antes de decidir se o miolo é para você.'),
 q(86, 'Reading · Vocabulário',
   'In Text B, "checked" is closest in meaning to',
   ['looked at briefly', 'borrowed again', 'corrected for errors', 'returned on time'], 0,
   'A frase opõe checked a read: a maior parte do que se pede é conferida de passagem, não lida inteira.'),
 q(87, 'Reading · Detalhe',
   'What did Priya learn about the limit on requests?',
   ['She learned it when the system accepted only eight of nine',
    'She read about it before ordering',
    'A librarian explained it to her',
    'She learned it from Tomás'], 0,
   'Ela conta que pediu nove itens e o sistema aceitou oito, e que foi assim que soube do limite.'),
 q(88, 'Reading · Inferência',
   'What can be inferred about Priya\'s Saturday in the library?',
   ['It was unplanned but produced the chapter she needed',
    'It was spent waiting for a book to arrive',
    'It replaced a meeting at the Writing Centre',
    'It was required by her department'], 0,
   'Ela diz que não tinha planejado ler na biblioteca, que aquilo custou um sábado, e que o capítulo de que precisava estava justamente ali.'),
 q(89, 'Reading · Ideia principal',
   'What is the main difference between Priya\'s experience and Tomás\'s?',
   ['She ordered early and adapted; he ordered late and wrote around a gap',
    'She used scans and he used printed books',
    'She finished on time and he did not finish',
    'She worked alone and he worked in a group'], 0,
   'Priya pediu cedo, esbarrou no limite e se adaptou; Tomás pediu tarde e passou a última quinzena escrevendo em volta de um livro que não tinha.'),
 q(90, 'Reading · Propósito',
   'Why does Tomás say he would "accept that some of it would be wasted"?',
   ['Because ordering more than you use is better than ordering too late',
    'Because the library charges for unused requests',
    'Because scans are cheaper than books',
    'Because his department limits the number of sources'], 0,
   'A frase vem logo depois de dizer que pediria na semana dois: o desperdício de alguns pedidos é o preço de não ficar sem o livro central. O serviço, aliás, não cobra nada.'),
]

T4 = [
 {'tag': 'A', 'html':
  "<h4>Summer Placement Scheme — City Transport Authority</h4>"
  "<p><strong>Applications close on 28 February.</strong> The scheme runs for eight weeks from early "
  "July and is open to students in their second year or above.</p>"
  "<ul>"
  "<li>Placements are <strong>paid at the standard city rate</strong> and include a travel pass</li>"
  "<li>Applicants choose <strong>one</strong> of three streams: planning, data, or customer operations</li>"
  "<li>A short written task replaces the interview for the data stream</li>"
  "<li><strong>References are not required at application.</strong> We ask for one only after an offer</li>"
  "</ul>"
  "<p>Successful applicants are told by the end of March. We do not keep a waiting list: candidates "
  "who are not selected are encouraged to apply again the following year.</p>"},
 {'tag': 'B', 'html':
  "<h4>Before you apply — notes from last year's supervisors</h4>"
  "<p><strong>Which stream should I choose?</strong><br>The one you can talk about for ten minutes. "
  "Every year we receive applications for planning from candidates whose whole answer is that planning "
  "sounds interesting, and they are the applications we cannot argue for.</p>"
  "<p><strong>Do I need experience?</strong><br>No, and the form does not ask for it. What we look for "
  "is evidence that you finish things. A small project you completed is worth more here than a large "
  "one you describe in the future tense.</p>"
  "<p><strong>What surprises people once they start?</strong><br>How much of the work is explaining. "
  "A recommendation that nobody outside your team can follow will not be adopted, however good it is. "
  "Placements that go badly usually go badly for that reason, not for a technical one.</p>"},
 {'tag': 'C', 'html':
  "<h4>Two former placement students</h4>"
  "<p><strong>Rui:</strong> I applied to the data stream because I had spent a term cleaning a messy "
  "dataset for a society I belonged to, and I could describe every decision I had made. The written "
  "task was three hours and felt harder than an interview, but I preferred it: nobody was watching me "
  "think. The work itself was less about models than about explaining them at meetings, which nobody "
  "had told me.</p>"
  "<p><strong>Amina:</strong> I chose customer operations because the other two sounded more "
  "impressive and I wanted the one I would actually enjoy. I spent the summer with the team that "
  "answers complaints, and I now know more about how the network really runs than any report would "
  "have taught me. I have applied for a graduate post there.</p>"},
]
RD4 = [
 q(91, 'Reading · Detalhe',
   'According to Text A, what do applicants receive besides payment?',
   ['a travel pass', 'a written reference', 'a place on a waiting list', 'a second interview'], 0,
   'O texto A diz que as vagas são pagas pela tarifa padrão da cidade e incluem um passe de transporte.'),
 q(92, 'Reading · Detalhe',
   'According to Text A, what replaces the interview for one of the streams?',
   ['a short written task', 'a group exercise', 'a reference from a tutor', 'a second application'], 0,
   'A terceira regra diz que uma tarefa escrita curta substitui a entrevista no stream de dados.'),
 q(93, 'Reading · Inferência',
   'What does Text A suggest about candidates who are not selected?',
   ['They must apply again to be considered next year',
    'They are contacted when a place becomes free',
    'They are offered a different stream',
    'They may ask for the decision to be reviewed'], 0,
   'Como não há lista de espera e a orientação é candidatar-se de novo no ano seguinte, ninguém é chamado depois sem uma nova inscrição.'),
 q(94, 'Reading · Ideia principal',
   'What is the main advice in Text B about choosing a stream?',
   ['Choose the one you can speak about in detail',
    'Choose the one with the fewest applicants',
    'Choose the one that matches your degree',
    'Choose the one that pays the most'], 0,
   'A resposta do texto B é escolher aquele sobre o qual você consegue falar por dez minutos, e o contraexemplo é quem só diz que a área parece interessante.'),
 q(95, 'Reading · Detalhe',
   'According to Text B, what do the supervisors look for instead of experience?',
   ['evidence that the candidate finishes things',
    'a reference from a previous employer',
    'a degree in a related subject',
    'a large project still in progress'], 0,
   'O texto B diz que não é preciso experiência e que o que conta é a prova de que a pessoa termina o que começa, com o projeto pequeno concluído valendo mais que o grande no futuro.'),
 q(96, 'Reading · Inferência',
   'What does Text B suggest is the most common reason a placement goes badly?',
   ['the student cannot explain the work to others',
    'the student lacks technical training',
    'the team changes supervisor during the summer',
    'the project is too small to matter'], 0,
   'O último parágrafo diz que as vagas que correm mal costumam correr mal por causa da explicação, e não por uma razão técnica.'),
 q(97, 'Reading · Detalhe',
   'Why did Rui choose the data stream?',
   ['He had already cleaned a dataset and could explain his decisions',
    'He wanted to avoid a written task',
    'A supervisor recommended it to him',
    'It was the only stream open to second-year students'], 0,
   'Ele conta que tinha passado um período organizando um conjunto de dados bagunçado e conseguia descrever cada decisão que tomou.'),
 q(98, 'Reading · Referência',
   'In Text C, "it" in "I preferred it" refers to',
   ['the written task', 'the interview', 'the dataset', 'the meeting'], 0,
   'A frase compara a tarefa escrita de três horas com a entrevista e diz que ele preferiu a primeira, porque ninguém o observava pensando.'),
 q(99, 'Reading · Inferência',
   'What did Rui and Text B agree about, without having planned to?',
   ['that much of the work is explaining it to other people',
    'that the written task is easier than an interview',
    'that experience matters more than finishing things',
    'that the planning stream is the most useful'], 0,
   'O texto B avisa que boa parte do trabalho é explicar, e Rui diz que o trabalho tinha menos de modelos e mais de explicá-los em reuniões, e que ninguém tinha avisado.'),
 q(100, 'Reading · Propósito',
   'Why does Amina mention the other two streams?',
   ['To explain that she chose the one she would enjoy rather than the one that sounded better',
    'To show that she was not accepted for them',
    'To argue that all three streams are the same',
    'To recommend the data stream to future applicants'], 0,
   'Ela diz que os outros dois soavam mais impressionantes e que ficou com o que de fato ia curtir. Não há recusa nem recomendação de outro stream.'),
]

# ─────────────────────────────────────────────────────────────────────────────
UNITS = []
for item in GR:
    UNITS.append({'id': 'gr-q%d' % item['n'], 'section': 'gr', 'type': 'single',
                  'questions': [item]})
UNITS.append({'id': 'rd-set1', 'section': 'rd', 'type': 'reading',
              'title': 'Passage 1 · Questions 71–75',
              'passageIntro': 'This passage is about why studying a text again is not the same as learning it.',
              'passage': P1, 'questions': RD1})
UNITS.append({'id': 'rd-set2', 'section': 'rd', 'type': 'reading',
              'title': 'Passage 2 · Questions 76–80',
              'passageIntro': 'This passage is about what happened when an office removed its fixed desks.',
              'passage': P2, 'questions': RD2})
UNITS.append({'id': 'rd-set3', 'section': 'rd', 'type': 'reading-multi',
              'title': 'Texts A, B & C · Questions 81–90', 'texts': T3, 'questions': RD3})
UNITS.append({'id': 'rd-set4', 'section': 'rd', 'type': 'reading-multi',
              'title': 'Texts A, B & C · Questions 91–100', 'texts': T4, 'questions': RD4})

# ─────────────────────────────────────────────────────────────────────────────
# GABARITO ESPALHADO PELAS QUATRO POSIÇÕES.
#
# A tela NÃO embaralha as alternativas (`index.html`: "o índice da tela É o
# índice do banco"), então a posição escrita aqui é a que o aluno vê. Escrever
# item por item empilha a resposta certa na letra A sem ninguém perceber, e um
# aluno que marcasse tudo A passaria. O RED, que é oficial, distribui 24/24/28/24.
#
# O embaralhamento é determinístico (semente fixa): rodar o script de novo dá
# exatamente o mesmo banco, senão o gabarito do backend descasaria a cada build.
# ─────────────────────────────────────────────────────────────────────────────
import random

def espalha_gabarito(units, semente=2026):
    rnd = random.Random(semente)
    todas = [q for u in units for q in u['questions']]
    # uma fila de posições-alvo com as quatro letras igualmente representadas
    alvos = [i % 4 for i in range(len(todas))]
    rnd.shuffle(alvos)
    for q, alvo in zip(todas, alvos):
        certa = q['opts'][q['key']]
        resto = [o for i, o in enumerate(q['opts']) if i != q['key']]
        rnd.shuffle(resto)
        novas = resto[:alvo] + [certa] + resto[alvo:]
        q['opts'] = novas
        q['key'] = alvo
        assert q['opts'][q['key']] == certa

espalha_gabarito(UNITS)

amber = {
    'id': 'amber',
    'name': 'Practice Test · AMBER',
    'examLabel': emerald['examLabel'],
    'cor': '#D97706',
    'toolId': emerald['toolId'],
    'audioBase': 'audio/amber/',
    'secondsPerRGQuestion': emerald['secondsPerRGQuestion'],
    'secondsPerListeningQuestion': emerald['secondsPerListeningQuestion'],
    # Rascunho tranca tudo: aviso na home, nada enviado para a nuvem e o gerador
    # do gabarito no backend pula o banco. Sai quando as 100 estiverem prontas.
    'rascunho': True,
    'cefr': emerald['cefr'],
    'sections': emerald['sections'],
    'units': UNITS,
    'minis': [],          # dependem do listening; entram com ele
    'grammarChapters': emerald['grammarChapters'],
    'quickPractice': emerald['quickPractice'],
}

destino = os.path.join(REPO, 'questions', 'amber.json')
with open(destino, 'w') as f:
    json.dump(amber, f, ensure_ascii=False, indent=1)
    f.write('\n')

n = sum(len(u['questions']) for u in amber['units'])
print('%s · %d questoes em %d unidades' % (destino, n, len(amber['units'])))
