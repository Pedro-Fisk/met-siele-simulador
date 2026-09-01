# Roteiros do listening · SIELE Modelo 1 (siele-m1)

Roteiros completos da **Comprensión auditiva** do `questions/siele-m1.json`,
para gerar os seis MP3s de `audio/siele-m1/` (`ca-t1.mp3` … `ca-t6.mp3`, os
nomes que o banco já aponta). **Os áudios existem desde 01/09/2026**
(`scripts/montar-siele.py`, edge-TTS); o banco segue em `rascunho: true`
até o Pedro ouvir e aprovar.

## Como gerar

Motor: **edge-TTS** (o mesmo do EMERALD/AMBER, `scripts/montar-audio.py`, e da
trilha de espanhol do Listening Lab no `portal-aluno-fisk`). O
`montar-audio.py` desta casa é do MET (narrador em inglês, "Number seven");
para o SIELE a montagem é outra, a deste arquivo: cada MP3 é a **tarefa
inteira**, com instrução, silêncio de leitura, primeira escuta, pausas e
repetição embutidos, no desenho medido no Modelo 0
(`data/transcripts-siele-m0.json`).

- Concatenar falas e silêncios com ffmpeg, como o `montar-audio.py` faz.
- **Medir o resultado** (regra da casa): o parâmetro de velocidade de TTS é
  promessa, não medida. Voz sintética no ritmo humano parece mais rápida que a
  humana; por isso os ritmos abaixo ficam levemente NEGATIVOS.

### Vozes

| Papel | Voz edge-TTS | Variante | Ritmo |
|---|---|---|---|
| NARRADOR (instruções, "Persona N", "Conteste a la pregunta…") | `es-US-AlonsoNeural` | neutra | `-5%` |
| Tarea 1 · MUJER (vecina) | `es-MX-DaliaNeural` | mexicana | `-38%` |
| Tarea 1 · PABLO | `es-MX-JorgeNeural` | mexicana | `-38%` |
| Tarea 2 · Anuncios 1, 3 e 5 | `es-ES-AlvaroNeural` | peninsular | `-29%` |
| Tarea 2 · Anuncios 2 e 4 | `es-ES-ElviraNeural` | peninsular | `-29%` |
| Tarea 3 · ver tabela da tarefa | mistas | mistas | `-30%` |
| Tarea 4 · PERIODISTA | `es-MX-JorgeNeural` | mexicana | `-15%` |
| Tarea 4 · CAMILA | `es-CO-SalomeNeural` | colombiana | `-15%` |
| Tarea 5 · CONFERENCIANTE | `es-ES-ElviraNeural` | peninsular | `-24%` |
| Tarea 6 · CONFERENCIANTE | `es-MX-JorgeNeural` | mexicana | `-11%` |

⚠️ **Estes ritmos são MEDIDOS, não escolhidos** (01/09/2026). A primeira versão
da tabela trazia `-10%` a `-4%`, escritos no olho: gerado e medido contra o
áudio **oficial** do Modelo 0 (`audio/siele-m0/`, gravação humana), o resultado
saiu de 12% a 46% **mais rápido** que o exame, e pior justamente nos níveis
baixos (A1 a 186 ppm contra 134 do oficial). Com os números acima, as seis
tarefas caem dentro de 0 a 2% do ritmo oficial:

| | A1 | A2 | B1 | B2 | C1 | C1 |
|---|---|---|---|---|---|---|
| oficial (Modelo 0) | 134 | 146 | 139 | 147 | 141 | 157 |
| nosso (Modelo 1) | 134 | 150 | 139 | 148 | 142 | 159 |

Repare que **o exame acelera conforme o nível sobe**: 134 ppm no A1, 157 no C1.
Um ritmo único para as seis tarefas apagaria essa escada, que é parte do que a
prova mede.

⚠️ **A régua é ppm sobre a FALA REAL**, medida no próprio arquivo com o
`silencedetect` do ffmpeg, nunca sobre a duração total nem sobre os colchetes
do roteiro. Colchete é silêncio PLANEJADO, e o TTS acrescenta silêncio próprio
em cada emenda: medindo pelos colchetes, as seis tarefas pareciam certas, e
não estavam.

O narrador é um timbre fixo que não dubla nenhum personagem, regra herdada do
MET. A variante alterna ENTRE tarefas (como o SIELE real), nunca dentro do
mesmo texto.

Marcações: `[N segundos]` é silêncio; `[Repetición]` repete o trecho falado da
tarefa (com as mesmas pausas internas); as falas levam o prefixo do papel.

---

## ca-t1.mp3 · Tarea 1 · Nivel A1

NARRADOR: Usted va a escuchar a un chico, Pablo, que habla sobre su escuela
nueva. Lea las cinco frases y elija la opción correcta para cada hueco. Va a
escuchar la conversación dos veces. Ahora tiene 30 segundos para leer las
frases.

[30 segundos]

MUJER: ¡Hola, Pablo! ¿Qué tal tu escuela nueva?

PABLO: ¡Muy bien! Está al lado de la casa de mi abuela. Mi mamá trabaja cerca,
pero la escuela queda lejos de mi casa.

MUJER: ¿Y cómo vas por las mañanas?

PABLO: Antes iba a la otra escuela en bicicleta, pero ahora voy en autobús.
Paso por la casa de mi amigo Juan y vamos juntos.

MUJER: ¿A qué hora empiezan las clases?

PABLO: Muy temprano: a las siete y media. Salgo de casa a las siete menos
cuarto. Mi hermano tiene más suerte: sus clases empiezan a las nueve.

MUJER: ¿Y qué haces después de las clases?

PABLO: Los amigos y yo jugamos al fútbol en el patio hasta las cinco. Los
martes tengo clase de música y cantamos con la profesora.

MUJER: ¿Cuál es tu materia favorita? ¿La música?

PABLO: ¡No! Me gusta, pero mi materia favorita es historia. La profesora nos
cuenta historias increíbles.

[10 segundos]

[Repetición]

[30 segundos]

---

## ca-t2.mp3 · Tarea 2 · Nivel A2

NARRADOR: Usted va a escuchar cinco anuncios o noticias de radio. Elija la
opción correcta para cada una de las cinco preguntas. Va a escuchar los
anuncios dos veces. Ahora tiene 30 segundos para leer las preguntas.

[30 segundos]

NARRADOR: Anuncio 1.

ÁLVARO: ¿Te gusta el grupo Naranja Eléctrica? Radio Joven regala dos entradas
para su concierto del sábado. Para ganar, solo tienes que contestar a esta
pregunta: ¿cómo se llama el primer disco del grupo? Llama ya al novecientos,
treinta y tres, cuarenta y cuatro, cincuenta y cinco. ¡La décima llamada gana!

[5 segundos]

[Repetición Anuncio 1] + NARRADOR: Conteste a la pregunta número 1.

[10 segundos]

NARRADOR: Anuncio 2.

ELVIRA: ¿Todavía no sabes qué hacer este verano? La piscina municipal abre sus
cursos de natación para chicos y chicas de ocho a dieciséis años. Clases por
las mañanas, de lunes a viernes, en grupos pequeños. Si te apuntas antes del
quince de junio, pagas la mitad. ¡No te quedes en casa!

[5 segundos]

[Repetición Anuncio 2] + NARRADOR: Conteste a la pregunta número 2.

[10 segundos]

NARRADOR: Anuncio 3.

ÁLVARO: Deportes Central cambia de casa: a partir del lunes nos encontrarás en
la avenida del Parque, número doce, en un local dos veces más grande. Para
celebrarlo, durante la primera semana todos los balones y las zapatillas
tienen un veinte por ciento de descuento. Te esperamos.

[5 segundos]

[Repetición Anuncio 3] + NARRADOR: Conteste a la pregunta número 3.

[10 segundos]

NARRADOR: Anuncio 4.

ELVIRA: Llega al cine la película del verano: «Verano en la Patagonia», la
historia de dos hermanos que viajan solos por el sur en busca de su perro
perdido. Una aventura para reír y llorar, con las canciones del grupo Los
Vientos. Desde el jueves, en todas las salas.

[5 segundos]

[Repetición Anuncio 4] + NARRADOR: Conteste a la pregunta número 4.

[10 segundos]

NARRADOR: Noticia 5.

ÁLVARO: Desde ayer, la ciudad tiene una nueva biblioteca en el barrio del Río.
Abre todos los días, de nueve de la mañana a nueve de la noche, y los sábados
hay talleres de lectura para jóvenes. En su primer día recibió más de
quinientas visitas, muchas más de las esperadas.

[5 segundos]

[Repetición Noticia 5] + NARRADOR: Conteste a la pregunta número 5.

---

## ca-t3.mp3 · Tarea 3 · Nivel B1

Vozes por pessoa (alternando variante e timbre):

| Persona | Voz | Variante |
|---|---|---|
| 1 | `es-MX-JorgeNeural` | mexicana |
| 2 | `es-ES-ElviraNeural` | peninsular |
| 3 | `es-ES-AlvaroNeural` | peninsular |
| 4 | `es-MX-DaliaNeural` | mexicana |
| 5 | `es-ES-AlvaroNeural` | peninsular |
| 6 | `es-ES-ElviraNeural` | peninsular |
| 7 | `es-MX-JorgeNeural` | mexicana |
| 8 | `es-CO-SalomeNeural` | colombiana |

NARRADOR: Usted va a escuchar a ocho personas que hablan sobre su primer viaje
sin su familia. Elija la frase que corresponde a cada persona. Va a escuchar a
cada persona dos veces. Ahora tiene 30 segundos para leer las frases.

[30 segundos]

NARRADOR: Persona 1.

HOMBRE: Fui a conocer la capital con dos amigos. El primer día quisimos ir
caminando del hotel al centro, sin mapa y sin internet. ¡Error! Dimos vueltas
durante dos horas por calles que parecían todas iguales, hasta que una señora
nos acompañó casi hasta la puerta del museo. Ahora me río, pero en el momento
pasé nervios.

[5 segundos]

[Repetición Persona 1]

[10 segundos]

NARRADOR: Persona 2.

MUJER: Mis padres me dejaron ir a un campamento internacional en los Pirineos.
Al principio me daba vergüenza hablar en inglés, pero acabé compartiendo
tienda con una francesa y una irlandesa, y todavía hablamos por videollamada
todas las semanas. Del paisaje casi no me acuerdo: lo importante fueron las
personas.

[5 segundos]

[Repetición Persona 2]

[10 segundos]

NARRADOR: Persona 3.

HOMBRE: El viaje fue estupendo hasta el último día. Nos entretuvimos comprando
regalos, llegamos a la estación con el tiempo justo y vimos el autobús salir
delante de nosotros. Tuvimos que esperar cinco horas al siguiente y llamar a
casa para avisar. Mi madre todavía me lo recuerda cada vez que salgo de viaje.

[5 segundos]

[Repetición Persona 3]

[10 segundos]

NARRADOR: Persona 4.

MUJER: Habíamos planeado una semana de playa con mis primas: teníamos lista la
crema, los trajes de baño, todo. Pues llovió los siete días, ¡los siete!
Cambiamos la playa por juegos de mesa en la cabaña. Yo pensé que me iba a
enfermar de tanto frío, pero no: solo me quedé con las ganas de nadar.

[5 segundos]

[Repetición Persona 4]

[10 segundos]

NARRADOR: Persona 5.

HOMBRE: Mi primer viaje solo fue en avión, a los dieciséis años, para pasar
las vacaciones con mi abuelo, que vive en el sur. Estaba nervioso por el
aeropuerto, los papeles, las maletas… pero todo salió bien. Cuando lo vi
esperándome, con el mismo sombrero de siempre, se me olvidaron los nervios.
Fue un mes inolvidable.

[5 segundos]

[Repetición Persona 5]

[10 segundos]

NARRADOR: Persona 6.

MUJER: Aprendí una lección importante: el dinero hay que repartirlo para todos
los días. Yo me emocioné la primera tarde comprando recuerdos y entradas, y el
jueves ya no me quedaba ni para un helado. Menos mal que mis amigas me
prestaron para el billete de metro. Desde entonces viajo con una lista y un
presupuesto.

[5 segundos]

[Repetición Persona 6]

[10 segundos]

NARRADOR: Persona 7.

HOMBRE: Fuimos de campamento a la montaña con el grupo de la escuela.
Caminamos horas, dormimos junto a un lago, vimos miles de estrellas y hasta un
venado. Volví cansado, picado por los mosquitos y con la ropa sucia, pero les
digo la verdad: de todos los viajes que he hecho, ninguno me ha gustado tanto
como ese.

[5 segundos]

[Repetición Persona 7]

[10 segundos]

NARRADOR: Persona 8.

MUJER: Íbamos a estar diez días en casa de la familia de mi amiga, pero a los
cinco días su abuela se puso enferma y decidimos no molestar más. Cambiamos
los pasajes y volvimos el sábado, en lugar del miércoles siguiente. Me dio
tristeza, aunque lo entendí perfectamente. Lo bueno: me quedaron días libres
para ver a mis amigos.

[5 segundos]

[Repetición Persona 8]

---

## ca-t4.mp3 · Tarea 4 · Nivel B2

NARRADOR: Usted va a escuchar, en versión locutada, una entrevista a Camila
Torres, una joven diseñadora de videojuegos colombiana. Elija la opción
correcta para cada una de las ocho preguntas. Va a escuchar la entrevista dos
veces. Ahora tiene 45 segundos para leer las preguntas.

[45 segundos]

PERIODISTA: ¿Qué es Nébula?

CAMILA: Nébula es un estudio de videojuegos que fundé en Medellín con dos
compañeros de la universidad. Cuando empezamos, en la industria nadie nos
tomaba en serio: éramos tres estudiantes haciendo «jueguitos», como decían. No
fuimos el primer estudio de Colombia, ya había varios, pero sí uno de los más
jóvenes. Hoy esa mirada cambió por completo.

PERIODISTA: ¿Cómo nació Nébula?

CAMILA: En la universidad había un concurso anual de creación de videojuegos:
cuarenta y ocho horas para hacer un juego desde cero. Nos presentamos por
diversión y ganamos el segundo lugar. Al recoger el premio pensé: si esto lo
hicimos en un fin de semana, ¿qué haríamos en un año? Muchos creen que fundé
la empresa al graduarme, pero no: seguía estudiando, y así estuvimos dos años,
estudiando de día y creando de noche. Nunca pasé por una empresa grande de
tecnología, como sí hicieron mis socios.

PERIODISTA: ¿Qué se necesita para dedicarse a los videojuegos?

CAMILA: Todo el mundo piensa que hace falta una computadora carísima o conocer
a la gente correcta de la industria. Para mí, eso es secundario. Lo esencial
es terminar cosas: es preferible tener tres juegos pequeños y terminados que
un proyecto gigante que nunca sale del cajón. Un juego terminado, aunque sea
sencillo, demuestra que sabes recorrer el camino completo.

PERIODISTA: ¿Cómo es Nébula hoy?

CAMILA: Somos doce personas: programadores, artistas, una música increíble…
Nuestro último juego superó los dos millones de descargas, la mayoría
gratuitas, así que no, no vendimos dos millones de copias, ¡ojalá! Y aunque
nos han propuesto abrir una sede fuera del país, por ahora seguimos todos en
Medellín.

PERIODISTA: ¿Qué fue lo más difícil del comienzo?

CAMILA: Sin duda, el financiamiento. Los bancos no le prestan a tres muchachos
que hacen videojuegos. Tiempo nos faltaba, claro, y encontrar buenos
programadores tampoco es fácil, pero eso se resuelve; lo que casi nos hace
cerrar dos veces fue no tener con qué pagar los sueldos. Nos salvó un fondo
público para industrias creativas.

PERIODISTA: ¿Qué hace diferentes a sus juegos?

CAMILA: Nuestra marca son las leyendas latinoamericanas: la Llorona, el Mohán,
historias que escuchábamos de nuestras abuelas. Los gráficos no buscan el
realismo, al contrario: parecen dibujados a mano. Y cualquiera puede jugarlos:
los diseñamos para que mi mamá y un jugador experto los disfruten igual.

PERIODISTA: ¿Cómo es ser mujer en este mundo?

CAMILA: Cuando empecé, en los eventos me preguntaban a cuál de mis compañeros
ayudaba. Hoy somos más, pero seguimos siendo pocas: en Nébula somos cinco de
doce, ni siquiera la mitad. Por eso dedico los viernes a un programa de
mentoría: acompaño a chicas que están armando su primer juego, leo sus
proyectos, las conecto con la industria. Es mi manera de abrir la puerta que a
mí me costó tanto empujar.

PERIODISTA: ¿Qué planes tiene para el futuro?

CAMILA: Estamos terminando un juego nuevo, el más ambicioso. Varias empresas
grandes preguntaron si vendemos Nébula, y la respuesta es no: queremos seguir
siendo independientes. ¿Irme del país? Tampoco: aquí están nuestro equipo y
nuestras historias. Mi sueño pendiente es otro: volver a mi universidad, pero
del otro lado del salón, a dar clases de diseño de juegos. El año que viene
empiezo.

[10 segundos]

[Repetición]

[30 segundos]

---

## ca-t5.mp3 · Tarea 5 · Nivel C1

NARRADOR: Usted va a escuchar, en versión locutada, seis fragmentos de una
conferencia de la socióloga española Marina Vidal titulada «Leer en tiempos de
pantallas». Elija, para cada fragmento, la opción que contenga una de las
ideas mencionadas. Va a escuchar los fragmentos de la conferencia dos veces.
Ahora tiene 45 segundos para leer las opciones.

[45 segundos]

MUJER: ¿Leemos menos que antes? Déjenme empezar con un dato incómodo para los
nostálgicos: nunca en la historia se había leído tanto texto como hoy.
Mensajes, subtítulos, publicaciones, comentarios… Un adolescente actual lee
cada día miles de palabras. Lo que ha cambiado no es la cantidad de lectura,
sino su naturaleza: leemos más, pero de otra manera; el papel convive con la
pantalla, no ha sido enterrado por ella.

[2 segundos]

MUJER: Ahora bien, no todas las lecturas son iguales. La lectura en pantalla
nos entrena para saltar: un titular aquí, un enlace allá, tres líneas y
seguimos viaje. Es una habilidad útil, no la desprecio. Pero es una habilidad
distinta de la lectura profunda, esa que exige quedarse en una página aunque
no pase nada. Y cuidado con los diagnósticos apocalípticos: no es que los
jóvenes no puedan concentrarse, es que el entorno les propone, a cada minuto,
no hacerlo.

[2 segundos]

MUJER: ¿Y por qué debería importarnos la lectura de ficción? Algunos estudios
sugieren que quien lee novelas desarrolla más empatía, aunque conviene ser
prudentes: la evidencia todavía se discute. Lo que sí sabemos es que una
novela es un simulador de vidas: nos obliga a mirar el mundo, durante
trescientas páginas, con los ojos de otro. Eso no convierte a los lectores en
mejores personas, conozco lectores insoportables, pero les da un ensayo
general de perspectivas que ninguna otra tecnología ofrece.

[2 segundos]

MUJER: ¿Qué hacemos entonces en las aulas? Veo dos tentaciones igual de
equivocadas: la de prohibir las pantallas, como si el mundo digital fuera a
esperar en la puerta de la escuela, y la de digitalizarlo todo, como si el
papel fuera un estorbo. La escuela inteligente enseña a cambiar de marcha:
este texto se lee saltando, este otro exige silencio y una hora entera.
Alternar entre los dos modos, y saber cuándo corresponde cada uno, es la
verdadera alfabetización de nuestro siglo.

[2 segundos]

MUJER: Me preguntan mucho por los audiolibros: ¿escuchar es leer? Yo respondo
con otra pregunta: ¿qué hacía la humanidad durante los milenios anteriores a
la escritura? Contaba. Alrededor del fuego, en la plaza, junto a la cuna. La
narración oral no es la hermana pobre de la lectura: es su madre. Quien
escucha una novela bien narrada no está haciendo trampa; está volviendo, con
tecnología nueva, al gesto más viejo que tenemos.

[2 segundos]

MUJER: Termino con una apuesta. No sé cómo leeremos dentro de treinta años, y
desconfío de quien diga saberlo. Pero sospecho que, en un mundo diseñado para
interrumpirnos, la capacidad de leer una hora seguida será tan valiosa como
hoy lo es hablar tres idiomas. No por nostalgia, la nostalgia es mala
consejera, sino por pura ventaja: quien domine la atención profunda tendrá
algo que las máquinas reparten cada vez menos: tiempo propio.

[10 segundos]

[Repetición]

[30 segundos]

---

## ca-t6.mp3 · Tarea 6 · Nivel C1

NARRADOR: Usted va a escuchar, en versión locutada, un fragmento de una
conferencia del sociólogo mexicano Andrés Palacios sobre la amistad en los
tiempos de las redes sociales. En ella se mencionan seis de las doce opciones
que aparecen a continuación. Elija las seis opciones que corresponden a esta
conferencia. Para cambiar una opción seleccionada, pulse de nuevo sobre ella.
Va a escuchar la conferencia dos veces. Ahora tiene 50 segundos para leer las
opciones.

[50 segundos]

HOMBRE: Cuando preparaba esta charla, le pregunté a mi hijo de quince años
cuántos amigos tenía. Me contestó sin dudar: setecientos doce. En su teléfono,
claro. La palabra amigo y la palabra contacto se han vuelto prácticamente
intercambiables, y conviene detenerse en esa confusión, porque no es inocente.
Quiero decir desde el principio lo que no vengo a hacer: no vengo a decirles
que las amistades que nacen o viven en internet sean falsas. Conozco amistades
profundas que empezaron en un foro de videojuegos, y amores de cincuenta años
que empezaron por carta, que era el internet de mis abuelos. El medio no
decide la verdad del vínculo. Lo que la decide es otra cosa, y es incómoda: el
tiempo. Una amistad se sostiene con horas compartidas, con presencia, con
estar ahí cuando no pasa nada interesante. Y las horas, a diferencia de los
contactos, no se pueden acumular por millares. Los estudios sobre redes
personales llevan décadas señalando lo mismo: por más grande que sea nuestra
lista, el círculo de vínculos estrechos que un ser humano puede cultivar es
limitado; los números varían según el estudio, pero ninguno pasa de unas
cuantas decenas. Tener setecientos contactos no significa tener con quién
llorar un martes por la noche. Ahora bien, sería injusto quedarnos en la
queja. Las redes hicieron posible algo que las generaciones anteriores no
tenían: conservar. El amigo que se muda de país ya no se pierde; la compañera
del colegio reaparece veinte años después. Antes, las mudanzas eran pequeños
funerales de amistades; hoy son pausas. Y esto importa especialmente en la
adolescencia porque, y aquí me pongo serio, la amistad adolescente no es un
pasatiempo: es el taller donde se construye la identidad. Con los amigos, el
adolescente ensaya quién es, qué opina, hasta dónde llega. Aristóteles, que
pensó sobre la amistad mejor que nadie, distinguía las amistades por lo que
buscamos en ellas: la utilidad, el placer o el bien del otro. Nunca se le
ocurrió medirlas al peso. Y quiero terminar con una imagen que me regaló una
alumna. Me dijo: mi mejor amiga es la única persona con la que puedo estar
callada. Ahí está todo. En un mundo que nos exige comentar, reaccionar y
publicar, compartir un silencio, en persona o incluso cada uno en su pantalla,
sigue siendo la forma más pura de decirle a alguien: contigo no necesito
actuar. Muchas gracias.

[10 segundos]

[Repetición]

[30 segundos] LA PRUEBA HA TERMINADO
