#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escreve data/roteiros-amber.json: o listening da terceira prova.

Part 1 · 19 conversas curtas de quatro falas, uma pergunta cada (1–19)
Part 2 ·  4 conversas longas, 3 ou 4 perguntas cada (20–33)
Part 3 ·  4 palestras, 4 ou 5 perguntas cada (34–50)

UNIVERSO 70/30, decisão do Pedro: 35 das 50 questões em cena acadêmica e 15 no
trabalho e na vida urbana. A conta é por questão, não por item, porque um set de
Part 3 vale quatro ou cinco.

VOZES: três timbres nos diálogos, mais a narradora (fixa no script). O ritmo
segue a régua medida no RED e anotada no montar-audio.py: a conversa longa da
prova real é falada MAIS RÁPIDO que a curta, e voz sintética no ritmo humano
parece mais rápida que a humana. Ficamos deliberadamente abaixo do original.
"""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W = 'en-US-AvaMultilingualNeural'          # mulher
M = 'en-US-AndrewMultilingualNeural'       # homem
W2 = 'en-GB-SoniaNeural'                   # segunda mulher, para variar timbre
M2 = 'en-GB-RyanNeural'                    # segundo homem

INTROS = {
 'l1-intro': ("Michigan English Test. Practice Test AMBER. Listening Section Instructions. "
   "In this section of the test, you will show your ability to understand spoken English. "
   "There are three parts in this section, with special directions for each part. If you do "
   "not know the answer, you may guess. Try to answer as many questions as possible. Part 1. "
   "In this part of the test, you will hear short conversations between two people. After each "
   "conversation, you will hear a question about it. Choose the best answer to the question from "
   "the choices on the screen. There are 19 questions in Part 1. The conversations and questions "
   "will not be repeated. Please listen carefully."),
 'l2-intro': ("Part 2. In this part of the test, you will hear longer conversations between two "
   "people. After each conversation, you will answer some questions about it. There are 14 "
   "questions in Part 2. The conversations and questions will not be repeated. If you want to, "
   "you may take notes as you listen."),
 'l3-intro': ("Part 3. In this part of the test, you will hear talks given by one speaker. After "
   "each talk, you will answer some questions about it. There are 17 questions in Part 3. The "
   "talks and questions will not be repeated. If you want to, you may take notes as you listen."),
}


def q(n, text, opts, key, expl, topic, quote=None):
    d = {'n': n, 'text': text, 'opts': opts, 'key': key, 'expl': expl, 'topic': topic}
    if quote:
        d['quote'] = quote
    return d


def p1(n, cena, vozes, ritmo, linhas, questao):
    return {'id': 'l1-q%02d' % n, 'section': 'l1', 'cena': cena, 'vozes': vozes,
            'ritmo': ritmo, 'linhas': linhas, 'questoes': [questao]}


DUP = {'W': W, 'M': M}
DUP2 = {'W': W2, 'M': M2}
R1 = {'W': '+8%', 'M': '+5%'}
R2 = {'W': '+5%', 'M': '+8%'}

# ── PART 1 · 19 conversas curtas ────────────────────────────────────────────
ITENS = [
 p1(1, 'a aluna quer trocar de seção do laboratório', DUP, R1, [
   ['W', "Is there any chance of moving to the Thursday lab section? Tuesday clashes with my statistics lecture."],
   ['M', "Thursday's full, I'm afraid. But the Wednesday evening one has space."],
   ['W', "Evening works. Do I need to fill in anything?"],
   ['M', "Just email the coordinator today, before the lists close at five."]],
   q(1, "What does the man tell the woman to do?",
     ["email the coordinator today", "come back on Thursday", "drop her statistics lecture",
      "wait until the lists reopen"], 0,
     "Ele resolve o caso e emenda a instrução: \"Just email the coordinator today, before the lists close at five\". A quinta está cheia, e a estatística é o motivo do pedido, não o que ele manda fazer.",
     "Listening · Detalhe")),

 p1(2, 'o cartão da biblioteca não abre a catraca', DUP2, R2, [
   ['M', "My card won't open the gate downstairs. It worked last week."],
   ['W', "Let me look. Ah, your registration lapsed on the first of the month."],
   ['M', "But I paid my fees in August."],
   ['W', "Fees are separate. Take this form to the registry and they'll reactivate it today."]],
   q(2, "Why is the man's card not working?",
     ["His registration has lapsed.", "He has an unpaid fine.", "The gate is broken.",
      "He is at the wrong entrance."], 0,
     "Ela vê o sistema e diz: \"your registration lapsed on the first of the month\". Ele levanta as mensalidades, e ela separa as duas coisas.",
     "Listening · Detalhe")),

 p1(3, 'ele pede feedback antes de entregar', DUP, R1, [
   ['M', "Would you have time to look at my introduction before Friday?"],
   ['W', "Send it tonight and I'll read it tomorrow morning. Anything later and it waits until next week."],
   ['M', "Tonight's fine. Should I send the whole chapter?"],
   ['W', "Just the introduction. I read better when I'm not skimming."]],
   q(3, "What does the woman ask the man to send?",
     ["only the introduction", "the whole chapter", "his notes from the seminar",
      "a summary of his argument"], 0,
     "Ele pergunta se manda o capítulo inteiro e ela corta: \"Just the introduction. I read better when I'm not skimming\".",
     "Listening · Detalhe")),

 p1(4, 'a impressora da sala de estudos', DUP2, R2, [
   ['W', "Do you know why nothing's coming out of the printer up here?"],
   ['M', "It's been out of toner since Monday. Everyone's using the one in the basement."],
   ['W', "Of course they are. Is there a queue?"],
   ['M', "There was at nine. It's usually clear after lunch."]],
   q(4, "What does the man imply about the basement printer?",
     ["It is less busy later in the day.", "It is also out of toner.",
      "It costs more to use.", "It will be replaced on Monday."], 0,
     "Ela pergunta da fila e ele responde \"There was at nine. It's usually clear after lunch\", ou seja, mais tarde esvazia. Ele não diz nada sobre preço nem troca.",
     "Listening · Inferência")),

 p1(5, 'o seminário mudou de sala', DUP, R1, [
   ['M', "Wasn't the seminar meant to be in room twelve?"],
   ['W', "They moved us. There's a lecture in there until four."],
   ['W', "We're in the annexe now, across the courtyard."],
   ['M', "Nobody told me. I've been sitting outside twelve for twenty minutes."]],
   q(5, "How does the man feel?",
     ["annoyed that he was not informed", "pleased with the new room",
      "worried about the lecture", "confused about the time"], 0,
     "A última fala é a queixa: \"Nobody told me. I've been sitting outside twelve for twenty minutes\". Ele não comenta a sala nova nem a hora.",
     "Listening · Intenção do falante")),

 p1(6, 'devolver um livro emprestado entre bibliotecas', DUP2, R2, [
   ['W', "I'd like to return this, and renew it if that's possible."],
   ['M', "This one came from another library, so the renewal isn't ours to give."],
   ['W', "How long does asking take?"],
   ['M', "Two days, usually. Keep the book meanwhile, and I'll write to them now."]],
   q(6, "What will the man do next?",
     ["contact the other library", "renew the book himself",
      "put the book back on the shelf", "charge the woman a fee"], 0,
     "Ele explica que a renovação não é dele para dar e fecha com \"I'll write to them now\", que é escrever para a biblioteca de origem.",
     "Listening · Detalhe")),

 p1(7, 'trabalho em grupo com um integrante sumido', DUP, R1, [
   ['M', "Have you heard anything from Daniel? He hasn't sent his section."],
   ['W', "He messaged me on Sunday saying he'd been ill all week."],
   ['M', "That's the first I've heard of it. We present on Thursday."],
   ['W', "I know. I've started writing his part, just in case."]],
   q(7, "What has the woman already done?",
     ["begun writing Daniel's section", "cancelled the presentation",
      "spoken to the professor", "asked for an extension"], 0,
     "A última fala dela é \"I've started writing his part, just in case\". Nada indica cancelamento, professor nem prorrogação.",
     "Listening · Detalhe")),

 p1(8, 'reservar sala de estudo em grupo', DUP2, R2, [
   ['W', "Can I book a group room for four of us tomorrow afternoon?"],
   ['M', "Group rooms go to bookings of five or more after two o'clock."],
   ['W', "Four is all we are."],
   ['M', "Then take one before two, or use the open tables at the back. Those are free."]],
   q(8, "What is the woman's problem?",
     ["Her group is too small for the afternoon rule.", "She has booked the wrong day.",
      "The rooms are all reserved.", "She does not have a library card."], 0,
     "A regra que ele cita é de cinco pessoas ou mais depois das duas, e o grupo dela tem quatro. Ele nem diz que está tudo reservado, oferece alternativas.",
     "Listening · Ideia principal")),

 p1(9, 'a nota da prova parcial saiu diferente do esperado', DUP, R1, [
   ['M', "I was surprised by my mark. I thought that essay was my best work."],
   ['W', "The argument was strong. You lost points on the referencing, which is a quarter of the sheet."],
   ['M', "A quarter? I hadn't looked at the sheet."],
   ['W', "Look at it before the next one. It costs you nothing to follow."]],
   q(9, "Why did the man lose marks?",
     ["because of his referencing", "because his argument was weak",
      "because he submitted the essay late", "because he wrote too little"], 0,
     "Ela elogia o argumento e localiza a perda: \"You lost points on the referencing, which is a quarter of the sheet\".",
     "Listening · Detalhe")),

 p1(10, 'estágio: primeiro dia e crachá', DUP2, R2, [
   ['W', "You'll need a pass for the sixth floor. Reception takes your photo."],
   ['M', "Should I do that now, before the induction?"],
   ['W', "Do it now. The queue after eleven is half an hour."],
   ['M', "Right. I'll go straight down."]],
   q(10, "What does the woman advise?",
     ["going to reception immediately", "attending the induction first",
      "coming back after eleven", "bringing a photo from home"], 0,
     "Ela é direta: \"Do it now. The queue after eleven is half an hour\". Depois das onze é justamente o que ela recomenda evitar.",
     "Listening · Detalhe")),

 p1(11, 'devolver um casaco na loja', DUP, R1, [
   ['M', "I'd like to return this coat. It's the wrong size."],
   ['W', "Do you have the receipt? Without it I can only exchange."],
   ['M', "It was a present, so no receipt."],
   ['W', "Then an exchange it is. Anything in the shop, same value or more."]],
   q(11, "What can the man do?",
     ["exchange the coat for something else", "get his money back",
      "order the correct size online", "keep the coat and pay less"], 0,
     "Sem recibo ela só pode trocar, e fecha com \"Then an exchange it is. Anything in the shop, same value or more\".",
     "Listening · Detalhe")),

 p1(12, 'o ônibus mudou de itinerário', DUP2, R2, [
   ['W', "Does the forty-one still stop at the hospital?"],
   ['M', "Not since the roadworks started. It turns before the bridge now."],
   ['W', "So how do I get there?"],
   ['M', "Stay on to the market and walk up. It's five minutes, no more."]],
   q(12, "What does the man suggest the woman do?",
     ["get off at the market and walk", "take a different bus",
      "wait for the roadworks to finish", "cross the bridge on foot"], 0,
     "A instrução é \"Stay on to the market and walk up. It's five minutes, no more\".",
     "Listening · Detalhe")),

 p1(13, 'ela hesita em falar no seminário', DUP, R1, [
   ['W', "I had the same point in my head for ten minutes and never said it."],
   ['M', "And then someone else said it and everyone nodded."],
   ['W', "Exactly. That happens to me every week."],
   ['M', "Say it in the first ten minutes next time. It gets harder the longer you wait."]],
   q(13, "What does the man mean when he says the point gets harder the longer you wait?",
     ["Speaking early in the seminar is easier.", "The seminar should be shorter.",
      "The woman's point was not important.", "He also stays quiet in seminars."], 0,
     "Ele acabou de recomendar falar nos dez primeiros minutos, e a frase justifica o conselho: quanto mais se espera, mais custa. Não há julgamento sobre a ideia dela.",
     "Listening · Intenção do falante",
     quote="Say it in the first ten minutes next time. It gets harder the longer you wait.")),

 p1(14, 'a bolsa exige carga horária mínima', DUP2, R2, [
   ['M', "If I drop this module I'd be down to ten credits."],
   ['W', "Careful. Your scholarship needs twelve to stay active."],
   ['M', "Nobody mentioned that when I applied."],
   ['W', "It's in the conditions. Add something small before you drop anything."]],
   q(14, "What does the woman warn the man about?",
     ["losing his scholarship", "failing the module", "missing the deadline",
      "paying a higher fee"], 0,
     "Ela liga os dez créditos à condição: \"Your scholarship needs twelve to stay active\". A ordem que ela dá é acrescentar antes de largar.",
     "Listening · Ideia principal")),

 p1(15, 'consulta com o orientador antes das férias', DUP, R1, [
   ['W', "Are you around in the last week of term?"],
   ['M', "I'm at a conference from Wednesday. Monday or Tuesday, then."],
   ['W', "Monday suits me better."],
   ['M', "Monday at two. Bring whatever you have, even if it's rough."]],
   q(15, "When will they meet?",
     ["Monday at two", "Tuesday at two", "Wednesday morning", "after the conference"], 0,
     "Ele fecha em \"Monday at two\". A quarta é a viagem dele, e a terça era a outra opção que ela recusou.",
     "Listening · Detalhe")),

 p1(16, 'reclamação sobre barulho no prédio', DUP2, R2, [
   ['M', "The building work starts at seven, and my window faces it."],
   ['W', "Have you told the housing office, or just complained to me?"],
   ['M', "Only to you, so far."],
   ['W', "Then tell them. They moved someone last term for exactly this."]],
   q(16, "What does the woman imply?",
     ["Complaining to the office can produce a result.",
      "The noise will stop by itself.", "The man should close his window.",
      "She has already spoken to the office."], 0,
     "Ela manda avisar o setor e sustenta com um precedente: \"They moved someone last term for exactly this\".",
     "Listening · Inferência")),

 p1(17, 'o café da esquina fechou', DUP, R1, [
   ['W', "The place on the corner has closed. I went this morning."],
   ['M', "For good, or is it the refurbishment they announced?"],
   ['W', "There was a sign saying back in September."],
   ['M', "Then it's the refurbishment. That's a relief, actually."]],
   q(17, "What does the man conclude?",
     ["The café will reopen.", "The café has closed permanently.",
      "The sign was wrong.", "The woman went to the wrong street."], 0,
     "A placa dizendo \"back in September\" o faz concluir que é a reforma anunciada, e ele comemora. Fechar de vez era a outra hipótese, descartada.",
     "Listening · Inferência")),

 p1(18, 'entrega do relatório no estágio', DUP2, R2, [
   ['M', "Does the report go to you or straight to the client?"],
   ['W', "To me first, always. I check the numbers before anything leaves the building."],
   ['M', "Even the short weekly one?"],
   ['W', "Especially that one. It's the one people read."]],
   q(18, "What is the woman's rule?",
     ["Everything goes through her before the client sees it.",
      "Only long reports need checking.", "The weekly report can go directly.",
      "The client checks the numbers."], 0,
     "\"To me first, always\", e quando ele tenta abrir exceção para o relatório curto ela reforça: \"Especially that one\".",
     "Listening · Ideia principal")),

 p1(19, 'ela perdeu o prazo da matrícula', DUP, R1, [
   ['W', "I missed registration. The portal shut at eight and I got there at ten past."],
   ['M', "Late registration opens tomorrow, with a fee."],
   ['W', "Is the fee waived for anything?"],
   ['M', "Illness with a note. Otherwise everyone pays it, including me last year."]],
   q(19, "What does the man say about the fee?",
     ["It is waived only for documented illness.", "It applies to nobody this term.",
      "It doubles after tomorrow.", "It is waived for first-year students."], 0,
     "Ele responde à pergunta dela com a única exceção, \"Illness with a note\", e reforça que os demais pagam, ele inclusive.",
     "Listening · Detalhe")),
]

# ── PART 2 · 4 conversas longas (20–33) ─────────────────────────────────────
ITENS.append({
 'id': 'l2-set1', 'section': 'l2', 'audio': 'l2-q20-23.mp3',
 'title': 'Conversation 1 · Questions 20–23',
 'cena': 'a aluna escolhe entre um semestre fora e o projeto de laboratório',
 'intro': "Now, turn the page. Numbers 20 to 23. Listen to a conversation between a student and her tutor.",
 'vozes': DUP, 'ritmo': {'W': '-13%', 'M': '-3%'},
 'linhas': [
   ['W', "I've been offered a place on the exchange in Lisbon for the spring, and I can't decide."],
   ['M', "What's holding you back? Most people take it without thinking twice."],
   ['W', "The lab project. If I go, I'd have to hand it to someone else halfway through."],
   ['M', "Whose project is it, formally? Yours, or the group's?"],
   ['W', "The group's. But the sampling design is mine, and nobody else has run it."],
   ['M', "Then write the design down properly before you go. That is worth doing whether you travel or not."],
   ['W', "You think it's transferable?"],
   ['M', "If it isn't, that's a problem with the project, not with the exchange. A method only one person can run isn't a method yet."],
   ['W', "That's a hard way to put it."],
   ['M', "It's meant to be useful, not comfortable. Now, the other side: what does Lisbon give you that here doesn't?"],
   ['W', "Fieldwork in a system I've only read about. And the language, eventually."],
   ['M', "Both of those take a term to be worth anything. Two weeks of it would be tourism."],
   ['W', "So you're saying go."],
   ['M', "I'm saying the project is a reason to prepare, not a reason to stay. Decide by Friday, and tell the group before you tell the office."]],
 'questoes': [
   q(20, "What are the speakers mainly discussing?",
     ["whether the woman should go on an exchange", "a project the woman has already finished",
      "the woman's application for funding", "a language course in Lisbon"], 0,
     "A conversa inteira gira em torno da decisão sobre o intercâmbio na primavera, e o projeto entra como o que a segura.",
     "Listening · Ideia principal"),
   q(21, "Why does the woman hesitate to accept the place?",
     ["She would have to hand over her part of the lab project.",
      "She has already promised the term to another group.",
      "She does not speak the language.",
      "The exchange lasts only two weeks."], 0,
     "Ela diz que teria de passar o projeto a outra pessoa no meio do caminho, e que o desenho de amostragem é dela.",
     "Listening · Detalhe"),
   q(22, "What does the tutor mean when he says a method only one person can run is not a method yet?",
     ["The design should be written so that others can use it.",
      "The woman should not share her work with the group.",
      "The project is too difficult for the group.",
      "The method needs to be tested again."], 0,
     "A frase responde à dúvida dela sobre ser transferível, e ele já tinha mandado escrever o desenho direito antes de viajar.",
     "Listening · Intenção do falante",
     quote="If it isn't, that's a problem with the project, not with the exchange. A method only one person can run isn't a method yet."),
   q(23, "What does the tutor advise the woman to do first?",
     ["tell the group before telling the office", "book her flights before Friday",
      "ask the office for more time", "finish the sampling herself"], 0,
     "A última instrução é a ordem das conversas: \"tell the group before you tell the office\".",
     "Listening · Detalhe")],
})

ITENS.append({
 'id': 'l2-set2', 'section': 'l2', 'audio': 'l2-q24-26.mp3',
 'title': 'Conversation 2 · Questions 24–26',
 'cena': 'aluguel: a caução não voltou inteira',
 'intro': "Now, turn the page. Numbers 24 to 26. Listen to a conversation between a tenant and a letting agent.",
 'vozes': DUP2, 'ritmo': {'W': '-8%', 'M': '-6%'},
 'linhas': [
   ['M', "I'm calling about my deposit. Two hundred was taken off and the letter just says cleaning."],
   ['W', "Let me open the file. Yes, there's a cleaning charge and a note about the oven."],
   ['M', "I cleaned the oven. I have photographs from the day I left, with the date on them."],
   ['W', "Then send those to me today. Photographs from the day of departure are what settles this."],
   ['M', "And if the landlord disagrees with the photographs?"],
   ['W', "Then it goes to the deposit scheme, which is independent of us and of him. They look at the inventory from when you moved in and at what you send."],
   ['M', "How long does that take?"],
   ['W', "Four weeks, sometimes six. Most cases don't get that far, because the photographs are usually enough."],
   ['M', "I'd rather not wait six weeks for two hundred pounds."],
   ['W', "Nobody would. That's exactly why I'm asking for them today rather than at the end of the month."]],
 'questoes': [
   q(24, "Why is the man calling?",
     ["Money was deducted from his deposit.", "He wants to end his contract early.",
      "The oven in his flat is broken.", "He has lost his inventory."], 0,
     "A primeira fala é a razão: duzentos foram descontados e a carta só diz limpeza.",
     "Listening · Ideia principal"),
   q(25, "What does the agent ask the man to do?",
     ["send his dated photographs today", "arrange a second cleaning",
      "speak to the landlord directly", "wait for the end of the month"], 0,
     "\"Then send those to me today. Photographs from the day of departure are what settles this.\"",
     "Listening · Detalhe"),
   q(26, "What does the agent suggest about the deposit scheme?",
     ["Most disputes are resolved before reaching it.", "It always takes six weeks.",
      "It is run by the landlord.", "It does not accept photographs."], 0,
     "Ela diz que a maioria dos casos não chega lá, porque as fotos costumam bastar, e que o esquema é independente dela e do proprietário.",
     "Listening · Inferência")],
})

ITENS.append({
 'id': 'l2-set3', 'section': 'l2', 'audio': 'l2-q27-30.mp3',
 'title': 'Conversation 3 · Questions 27–30',
 'cena': 'dois alunos dividem a apresentação e discordam do formato',
 'intro': "Now, turn the page. Numbers 27 to 30. Listen to a conversation between two students.",
 'vozes': DUP, 'ritmo': {'W': '-10%', 'M': '-5%'},
 'linhas': [
   ['W', "We've got fifteen minutes on Thursday and about forty minutes of material."],
   ['M', "We could talk faster."],
   ['W', "We could, and nobody would follow a word. I'd rather cut the second case study."],
   ['M', "That's the one I spent the weekend on."],
   ['W', "I know, and it's good. It's also the one that needs ten minutes to make sense."],
   ['M', "What if we put it in the handout instead? People can read it afterwards."],
   ['W', "That works. Then we use the time for the first case and the comparison."],
   ['M', "The comparison is the part they'll ask about anyway."],
   ['W', "Which is why it can't be the part we rush. Shall I redo the slides tonight?"],
   ['M', "Send them to me when they're done and I'll time myself reading them out."],
   ['W', "Time yourself slowly. Everyone speeds up in front of people."],
   ['M', "That's not been my experience, but fine."]],
 'questoes': [
   q(27, "What is the main problem the students are discussing?",
     ["They have more material than time.", "They disagree about the topic.",
      "One of them has not prepared.", "The presentation has been moved."], 0,
     "A primeira fala fecha o problema: quinze minutos na quinta e quarenta minutos de material.",
     "Listening · Ideia principal"),
   q(28, "What do they decide to do with the second case study?",
     ["put it in the handout", "present it first", "cut it completely",
      "give it to another group"], 0,
     "A saída é dele: \"What if we put it in the handout instead?\", e ela aceita.",
     "Listening · Detalhe"),
   q(29, "Why does the woman refuse to talk faster?",
     ["The audience would not be able to follow.", "The room has poor acoustics.",
      "She has been told off for it before.", "The handout would be unnecessary."], 0,
     "\"We could, and nobody would follow a word.\" A recusa é sobre quem escuta.",
     "Listening · Propósito"),
   q(30, "What does the man agree to do before Thursday?",
     ["time himself reading the slides", "rewrite the comparison",
      "print the handouts", "book a larger room"], 0,
     "Ele fecha em \"Send them to me when they're done and I'll time myself reading them out\".",
     "Listening · Detalhe")],
})

ITENS.append({
 'id': 'l2-set4', 'section': 'l2', 'audio': 'l2-q31-33.mp3',
 'title': 'Conversation 4 · Questions 31–33',
 'cena': 'entrevista de estágio de verão numa empresa de dados',
 'intro': "Now, turn the page. Numbers 31 to 33. Listen to a conversation between a student and an interviewer.",
 'vozes': DUP2, 'ritmo': {'W': '-6%', 'M': '-8%'},
 'linhas': [
   ['W', "You've put a student society at the top of your form, above your coursework. Was that deliberate?"],
   ['M', "It was. The society is where I actually finished something. The coursework is graded, but it ends whether I finish it well or not."],
   ['W', "Tell me what you finished."],
   ['M', "We had four years of membership records in three different spreadsheets, none of them agreeing. I merged them and wrote down the rules I used, so the next person wouldn't have to guess."],
   ['W', "How long did that take?"],
   ['M', "Six weeks, most of it deciding what counted as the same person. The merging itself was an afternoon."],
   ['W', "That ratio is the whole job, more or less. What did you do about the cases you couldn't decide?"],
   ['M', "Left them in a separate list and marked them. About sixty of them."],
   ['W', "Good. People who guess in those cases are the ones we have to correct later."]],
 'questoes': [
   q(31, "Why did the man list the society above his coursework?",
     ["Because it is where he completed something himself.",
      "Because his coursework marks were low.",
      "Because the form required it.",
      "Because the society was more recent."], 0,
     "Ele explica que a sociedade é onde de fato terminou alguma coisa, enquanto o trabalho de curso acaba de qualquer jeito.",
     "Listening · Propósito"),
   q(32, "What took most of the six weeks?",
     ["deciding which records referred to the same person",
      "merging the spreadsheets", "learning new software",
      "waiting for the society's approval"], 0,
     "\"Six weeks, most of it deciding what counted as the same person. The merging itself was an afternoon.\"",
     "Listening · Detalhe"),
   q(33, "What does the interviewer approve of?",
     ["that he marked the uncertain cases instead of guessing",
      "that he finished ahead of schedule", "that he worked alone",
      "that he deleted the duplicate records"], 0,
     "Ela responde ao \"left them in a separate list and marked them\" com \"Good\", e completa que quem chuta nesses casos dá trabalho depois.",
     "Listening · Inferência")],
})

# ── PART 3 · 4 palestras (34–50) ────────────────────────────────────────────
ITENS.append({
 'id': 'l3-set1', 'section': 'l3', 'audio': 'l3-q34-37.mp3',
 'title': 'Lecture 1 · Questions 34–37',
 'cena': 'orientação sobre integridade acadêmica para calouros',
 'intro': "Now, turn the page. Numbers 34 to 37. Listen to a talk given to new students.",
 'vozes': {'S': W}, 'ritmo': {'S': '-20%'},
 'linhas': [
   ['S', "Good morning. I'm here to talk about academic honesty, and I'd like to start by admitting that the way we usually talk about it is unhelpful. We hand you a document, you tick a box, and everyone assumes the matter is settled. Then in March someone is sitting in my office in tears, and it turns out nobody had ever explained the part that actually catches people."],
   ['S', "The cases that reach me are almost never about buying an essay. That happens, and it is dealt with quickly. The ordinary case is a student who took notes from three sources in November, came back to them in February, and could no longer tell which sentences were theirs. That is not dishonesty. It is a filing problem that becomes a disciplinary one."],
   ['S', "So the advice is procedural, not moral. When you take a note, mark it: quotation, paraphrase, or your own thought. Three letters in the margin. Do it while you have the source open, because in February you will not remember, and the version of you that remembers is not available for consultation."],
   ['S', "The second thing worth knowing is that collaboration is allowed far more often than students think, and forbidden in more specific ways than they expect. Working through a problem set at the same table is usually fine. Sending your finished file to someone who is stuck is usually not, even if they only look at it. The line is not the room; it is the document."],
   ['S', "And if you are unsure, ask before, not after. An email asking whether something is allowed has never once got a student into trouble. I have kept the ones I have received, and the honest answer is that most of them describe things that were perfectly fine."]],
 'questoes': [
   q(34, "What is the talk mainly about?",
     ["how ordinary note-taking habits lead to academic misconduct",
      "the penalties for buying an essay",
      "how to write better paraphrases",
      "why collaboration is forbidden at the university"], 0,
     "Ela descarta o caso da compra de trabalho logo no começo e dedica o resto ao aluno que perdeu o controle das próprias anotações.",
     "Listening · Ideia principal"),
   q(35, "According to the speaker, what causes most of the cases she sees?",
     ["students losing track of which words were their own",
      "students deliberately copying from friends",
      "students misunderstanding the deadline",
      "students using sources that are not allowed"], 0,
     "Ela descreve o caso comum: anotações de novembro retomadas em fevereiro, sem saber quais frases eram de quem.",
     "Listening · Detalhe"),
   q(36, "What does the speaker recommend doing while taking notes?",
     ["marking each note as quotation, paraphrase or original thought",
      "writing only in your own words", "copying the full source into the file",
      "keeping all notes in a single document"], 0,
     "\"When you take a note, mark it: quotation, paraphrase, or your own thought. Three letters in the margin.\"",
     "Listening · Detalhe"),
   q(37, "What does the speaker mean when she says the line is not the room but the document?",
     ["Sharing a finished file is the problem, not studying together.",
      "Students should not work in the same room.",
      "Documents must be submitted from the library.",
      "Each room has a different rule."], 0,
     "A frase resume os dois exemplos que ela acabou de dar: sentar-se à mesma mesa costuma ser permitido, mandar o arquivo pronto não.",
     "Listening · Intenção do falante",
     quote="Working through a problem set at the same table is usually fine. Sending your finished file to someone who is stuck is usually not, even if they only look at it. The line is not the room; it is the document.")],
})

ITENS.append({
 'id': 'l3-set2', 'section': 'l3', 'audio': 'l3-q38-41.mp3',
 'title': 'Lecture 2 · Questions 38–41',
 'cena': 'aula sobre por que as cidades ficam mais quentes que o campo',
 'intro': "Now, turn the page. Numbers 38 to 41. Listen to a talk given in a geography class.",
 'vozes': {'S': M}, 'ritmo': {'S': '-18%'},
 'linhas': [
   ['S', "Last week you measured temperature at six points across the city, and your results probably surprised you. The park was four degrees cooler than the street two hundred metres away. Today I want to explain why, and then complicate the explanation, because the simple version is where most reporting stops."],
   ['S', "The standard account is about materials. Asphalt and brick absorb heat during the day and release it slowly at night, while soil and leaves do not store it in the same way. That is true, and it explains why the gap between city and countryside is widest at three in the morning rather than at noon, which is the detail people find counterintuitive."],
   ['S', "But materials are only part of it. A city also removes water. Rain that would have soaked into ground and evaporated over the following days instead runs into a drain within minutes. Evaporation is a cooling process, and we have engineered it out of the landscape. That is why a city with the same materials but with permeable surfaces runs measurably cooler."],
   ['S', "The third factor is shape. Narrow streets between tall buildings trap heat by reflecting it between the walls instead of letting it escape upwards. This means two districts with identical materials can differ by two degrees purely because of how they are laid out, which is a planning decision, not a construction one."],
   ['S', "Why this matters is straightforward. Heat kills more people in most European countries than floods do, and it kills them indoors at night. So the design question is not how to cool a street at midday for people walking through it. It is how to let a building lose its heat by three in the morning, when the people who die are asleep."]],
 'questoes': [
   q(38, "What is the main purpose of the talk?",
     ["to explain why cities are hotter than surrounding areas",
      "to describe how to measure temperature accurately",
      "to compare European and other cities",
      "to argue against building tall buildings"], 0,
     "Ele anuncia no começo que vai explicar o resultado que os alunos mediram e depois complicar a explicação.",
     "Listening · Ideia principal"),
   q(39, "According to the speaker, why is the difference greatest at three in the morning?",
     ["because built surfaces release stored heat slowly",
      "because traffic is heaviest at that time",
      "because the wind drops at night",
      "because parks close at night"], 0,
     "O material absorve de dia e devolve devagar de madrugada, e é isso que abre a diferença às três da manhã e não ao meio-dia.",
     "Listening · Detalhe"),
   q(40, "What does the speaker say about water in cities?",
     ["Draining it away removes a cooling process.",
      "Cities use more of it than the countryside.",
      "It makes narrow streets more dangerous.",
      "It is stored in building materials."], 0,
     "A chuva que evaporaria ao longo dos dias vai para o ralo em minutos, e a evaporação é o processo de resfriamento que se perde.",
     "Listening · Detalhe"),
   q(41, "What does the speaker suggest about the design of cities?",
     ["Layout matters as much as the materials used.",
      "Materials are the only factor that can be changed.",
      "Narrow streets are cooler than wide ones.",
      "Planning decisions have little effect on temperature."], 0,
     "Dois bairros com materiais idênticos podem diferir em dois graus só pelo traçado, que é decisão de planejamento.",
     "Listening · Inferência")],
})

ITENS.append({
 'id': 'l3-set3', 'section': 'l3', 'audio': 'l3-q42-46.mp3',
 'title': 'Lecture 3 · Questions 42–46',
 'cena': 'palestra sobre por que dados de pesquisa se perdem',
 'intro': "Now, turn the page. Numbers 42 to 46. Listen to a talk given at a research methods seminar.",
 'vozes': {'S': W2}, 'ritmo': {'S': '-16%'},
 'linhas': [
   ['S', "I want to talk about something that sounds administrative and is in fact scientific: what happens to data after a study is published. The short answer is that it disappears, and it disappears at a rate you can measure."],
   ['S', "A group of researchers tried to obtain the raw data behind five hundred papers, chosen across two decades. For papers published in the previous two years, they got the data about half the time. For papers twenty years old, the figure was under seven per cent. The odds of the data still being available fell by roughly seventeen per cent for every year that had passed."],
   ['S', "The reasons are almost comically mundane. Email addresses expire when people change institutions. The student who ran the analysis has left. The files are on a machine that was replaced, or in a format that nothing now opens. Very few of these are refusals. When the authors could be reached, most were willing and simply could not find it."],
   ['S', "Notice what this means for the claim we make about science being self-correcting. Self-correction requires that someone can check the work, and checking requires the data. If the material has evaporated by the time a result is influential enough to be worth checking, then the correction mechanism is running on a resource that is no longer there."],
   ['S', "The remedy is not heroic. Deposit the data in a repository when the paper is accepted, with a licence and a description written for a stranger. This takes an afternoon, it is now required by most funders, and its whole purpose is that it does not depend on you being reachable in fifteen years."]],
 'questoes': [
   q(42, "What is the talk mainly about?",
     ["the disappearance of research data over time",
      "how to choose a data repository",
      "why researchers refuse to share their work",
      "the cost of storing scientific files"], 0,
     "Ela anuncia o assunto na primeira fala: o que acontece com os dados depois que o artigo sai, e que eles somem a uma taxa mensurável.",
     "Listening · Ideia principal"),
   q(43, "What did the study of five hundred papers find?",
     ["Data was much harder to obtain for older papers.",
      "Half of all authors refused to cooperate.",
      "Older papers had better documentation.",
      "Most data was stored in the wrong format."], 0,
     "Cerca de metade nos artigos recentes contra menos de sete por cento nos de vinte anos.",
     "Listening · Detalhe"),
   q(44, "According to the speaker, why is the data usually unavailable?",
     ["because of practical problems such as lost files and old addresses",
      "because authors are unwilling to share it",
      "because journals forbid its release",
      "because the analyses were never done"], 0,
     "Ela lista endereço que expirou, aluno que saiu, máquina trocada, formato que ninguém abre, e diz que quase nenhuma recusa.",
     "Listening · Detalhe"),
   q(45, "What does the speaker suggest about the idea that science corrects itself?",
     ["It depends on material that often no longer exists.",
      "It works better for older papers.",
      "It has been proved by this study.",
      "It applies only to influential results."], 0,
     "Ela diz que a autocorreção exige conferir, conferir exige o dado, e o dado evaporou justamente quando o resultado passa a valer a conferência.",
     "Listening · Inferência"),
   q(46, "What does the speaker recommend?",
     ["depositing data in a repository when the paper is accepted",
      "keeping personal copies for fifteen years",
      "publishing only in journals that require data",
      "contacting authors before their addresses expire"], 0,
     "\"Deposit the data in a repository when the paper is accepted, with a licence and a description written for a stranger.\"",
     "Listening · Detalhe")],
})

ITENS.append({
 'id': 'l3-set4', 'section': 'l3', 'audio': 'l3-q47-50.mp3',
 'title': 'Lecture 4 · Questions 47–50',
 'cena': 'apresentação da equipe de transporte sobre a faixa de ônibus',
 'intro': "Now, turn the page. Numbers 47 to 50. Listen to a talk given at a public meeting.",
 'vozes': {'S': M2}, 'ritmo': {'S': '-15%'},
 'linhas': [
   ['S', "Thank you for coming. I'm from the transport authority, and I'm here about the bus lane on Bridge Road, which has now been running for a year. I'd like to give you the numbers before we take questions, because the numbers are more interesting than either side of the argument has been."],
   ['S', "The lane was predicted to cut bus journey times by four minutes. It cut them by eleven. That is a larger effect than we expected, and the reason is not the lane itself but the junction at the north end, where buses used to wait through two or three light cycles. Removing one queue removed the whole delay."],
   ['S', "Car journey times on the same road rose by two minutes on average, which is less than opponents predicted and more than we told you it would be. I want to be clear that we got that estimate wrong, and I would rather say so than argue about the definition of average."],
   ['S', "The part nobody predicted is what happened on the side streets. Some drivers now avoid Bridge Road entirely and cut through the residential grid to the east, where traffic is up by about a fifth. Those streets have schools on them. That is the problem we are now working on, and it was created by our own scheme."],
   ['S', "So the proposal tonight is not to remove the lane, which is working, but to close two of the side streets to through traffic while keeping them open to residents. I expect disagreement about which two, and that is a reasonable thing to disagree about. What I would ask is that we argue about the streets and not about whether the traffic moved, because on that last point we now have counts."]],
 'questoes': [
   q(47, "What is the main purpose of the talk?",
     ["to report the results of the bus lane and propose a next step",
      "to announce that the bus lane will be removed",
      "to explain why the meeting was called late",
      "to compare Bridge Road with other cities"], 0,
     "Ele abre dizendo que vai dar os números de um ano da faixa e fecha com a proposta das ruas laterais.",
     "Listening · Ideia principal"),
   q(48, "Why did bus journey times improve more than predicted?",
     ["because the lane removed a queue at a junction",
      "because fewer people travelled by bus",
      "because the buses were replaced",
      "because the road was resurfaced"], 0,
     "Ele credita ao cruzamento do lado norte, onde os ônibus esperavam dois ou três ciclos de semáforo.",
     "Listening · Detalhe"),
   q(49, "What does the speaker admit?",
     ["that the authority's estimate for car journeys was wrong",
      "that the bus lane has failed", "that the counts were never made",
      "that the schools were not consulted"], 0,
     "\"I want to be clear that we got that estimate wrong, and I would rather say so than argue about the definition of average.\"",
     "Listening · Intenção do falante",
     quote="Car journey times on the same road rose by two minutes on average, which is less than opponents predicted and more than we told you it would be. I want to be clear that we got that estimate wrong."),
   q(50, "What is being proposed?",
     ["closing two side streets to through traffic",
      "removing the bus lane at the north end",
      "building a new junction", "reducing the speed limit near the schools"], 0,
     "A proposta da noite é fechar duas ruas laterais ao tráfego de passagem, mantendo-as abertas a moradores, e não tirar a faixa.",
     "Listening · Detalhe")],
})

roteiro = {
 '_leia_me': [
   "Roteiros ORIGINAIS do listening do AMBER, a terceira prova do Treino MET.",
   "",
   "Estrutura e pesos vêm do MET; enunciado, fala e alternativa são da Fisk.",
   "Universo 70/30 (decisão do Pedro): 35 das 50 questões em cena acadêmica e",
   "15 no trabalho e na vida urbana.",
   "",
   "O NARRADOR NÃO ESTÁ AQUI. O 'Number seven.' e a leitura da pergunta são",
   "montados pelo script a partir do campo `text` da própria questão, para o que",
   "o aluno ouve e o que ele lê saírem da mesma string.",
   "",
   "Gerar o áudio:   python3 scripts/montar-audio.py --prova amber",
   "Escrever as unidades: python3 scripts/montar-unidades.py --prova amber",
   "",
   "⚠️ A ORDEM DAS ALTERNATIVAS AQUI É PROVISÓRIA. Depois de montar as unidades,",
   "rode scripts/espalhar-gabarito.py questions/amber.json --gravar: ele espalha",
   "o gabarito e realinha este arquivo. Sem isso o banco vira teste de marcar A.",
 ],
 'intros': INTROS,
 'itens': ITENS,
}

destino = os.path.join(REPO, 'data', 'roteiros-amber.json')
with open(destino, 'w') as f:
    json.dump(roteiro, f, ensure_ascii=False, indent=2)
    f.write('\n')
qs = [q for i in ITENS for q in i['questoes']]
print('%s · %d itens · %d questões (%s)' % (destino, len(ITENS), len(qs),
      ' '.join('%s=%d' % (s, sum(1 for i in ITENS for _ in i['questoes'] if i['section'] == s))
               for s in ('l1', 'l2', 'l3'))))
