// "Enxergar Além" refeito: estilo cinema — fundo noturno, fotos grandes, dourado como destaque, Cambria + Calibri.
const pptxgen = require('pptxgenjs');
const { applyTheme } = require(process.argv[2] + '/scripts/apply_theme.js');
const IMG = __dirname + '/img/';
const THEME = { name: 'Enxergar Além', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '0E1022', lt1: 'F4EFE6', dk2: '1B1C3A', lt2: 'FFFFFF', accent1: 'E9A93A', accent2: '9A9BB5', accent3: '2B2D57', accent4: 'C9573F', accent5: '6E7BD9', accent6: 'D9C9A8', hlink: 'E9A93A', folHlink: '9A9BB5' } };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'Enxergar Além';
const C = pres.SchemeColor; const W = 13.333, H = 7.5;
const num = { x: W - 1.0, y: H - 0.55, w: 0.6, h: 0.3, color: C.accent2, fontSize: 10, align: 'right' };
// layouts
pres.defineSlideMaster({ title: 'Capa', background: { color: '0E1022' }, objects: [
] });
pres.defineSlideMaster({ title: 'Foto a direita', background: { color: '0E1022' }, slideNumber: num, objects: [] });
pres.defineSlideMaster({ title: 'Escuro so titulo', background: { color: '0E1022' }, slideNumber: num, objects: [] });
pres.defineSlideMaster({ title: 'Foto inteira', background: { color: '0E1022' }, slideNumber: num, objects: [] });
const TIT = { 'Foto a direita': { x: 0.7, y: 0.6, w: 6.3, h: 1.2 }, 'Escuro so titulo': { x: 0.7, y: 0.55, w: 11.9, h: 1.0 } };
let ATUAL = '';
const T = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, fontFace: 'Calibri', color: C.background1, fontSize: 16, margin: 0, valign: 'top' }, o));
const { execFileSync } = require('child_process');
const foto = (s, n, o) => { const out = `${IMG}${n}_${Math.round(o.w*100)}x${Math.round(o.h*100)}.jpg`;
  execFileSync('python3', ['-c', `from PIL import Image\nim=Image.open('${IMG}${n}.jpg').convert('RGB'); W,H=im.size; r=${o.w}/${o.h}\nif W/H>r:\n  nw=int(H*r); x=(W-nw)//2; im=im.crop((x,0,x+nw,H))\nelse:\n  nh=int(W/r); y=(H-nh)//2; im=im.crop((0,y,W,y+nh))\nim.save('${out}',quality=86)`]);
  return s.addImage(Object.assign({ path: out, objectName: 'foto ' + n }, o)); };
const veu = (s, o) => s.addShape(pres.shapes.RECTANGLE, Object.assign({ fill: { color: '0E1022', transparency: 35 }, line: { type: 'none' }, objectName: 'véu' }, o));
const circ = (s, x, y, t, o = {}) => { s.addShape(pres.shapes.OVAL, { x, y, w: 0.62, h: 0.62, fill: { color: C.accent1 }, line: { type: 'none' }, objectName: 'círculo ' + t });
  s.addText(t, { isTextBox: true, x, y, w: 0.62, h: 0.62, align: 'center', valign: 'middle', fontFace: 'Cambria', bold: true, fontSize: o.fs || 20, color: C.text1, margin: 0 }); };
const card = (s, x, y, w, h, n) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: '1B1C3A' }, line: { color: '2B2D57', width: 0.75 }, objectName: n });
const fotoDir = (s, n) => { foto(s, n, { x: 7.6, y: 0, w: W - 7.6, h: H }); };
const notas = {};
const HIST = __dirname + '/hist/';
// foto inteira, sem cortar: cabe na caixa e fica centralizada
const inteira = (s, n, x, y, w, h) => { const [iw, ih] = execFileSync('python3', ['-c', `from PIL import Image;print(*Image.open('${HIST}${n}.jpg').size)`]).toString().trim().split(' ').map(Number);
  const k = Math.min(w / iw, h / ih), fw = iw * k, fh = ih * k; return s.addImage({ path: HIST + n + '.jpg', x: x + (w - fw) / 2, y: y + (h - fh) / 2, w: fw, h: fh, objectName: 'foto ' + n }); };
// várias fotos lado a lado, cada uma com legenda pequena embaixo
const fila = (s, itens, y, h) => { const gap = 0.3, w = (W - 1.4 - gap * (itens.length - 1)) / itens.length;
  itens.forEach(([n, leg], i) => { const x = 0.7 + i * (w + gap); inteira(s, n, x, y, w, h - (leg ? 0.5 : 0));
    if (leg) T(s, leg, { x, y: y + h - 0.4, w, h: 0.35, align: 'center', fontSize: 14, color: C.accent2 }); }); };
const rotulo = (s, t) => T(s, t, { x: 0.7, y: 0.45, w: 11.9, h: 0.4, fontSize: 13, bold: true, color: C.accent2, charSpacing: 4 });

// 1 capa
pres.addSection({ title: 'Abertura' });
ATUAL = 'Capa'; let s = pres.addSlide({ masterName: 'Capa', sectionTitle: 'Abertura' });
foto(s, 'olho', { x: 5.2, y: 0, w: W - 5.2, h: H }); s.addShape(pres.shapes.RECTANGLE, { x: 4.6, y: 0, w: 1.6, h: H, fill: { color: '0E1022', transparency: 30 }, line: { type: 'none' }, objectName: 'transição' });
T(s, 'ENXERGAR ALÉM', { x: 0.8, y: 2.6, w: 7.2, h: 1.5, fontFace: 'Cambria', fontSize: 54, bold: true, color: C.accent1, valign: 'bottom' }); T(s, 'Como a mente constrói a realidade que vivemos — e como escolher a que queremos construir', { x: 0.8, y: 4.25, w: 6.6, h: 1.4, fontSize: 18, italic: true });
s.addNotes('ABERTURA (1 min). Agradeça a presença. Diga: hoje a gente vai conversar sobre algo que todo mundo faz o dia inteiro e quase ninguém percebe: interpretar a realidade. A proposta é simples: sair daqui enxergando um pouco além do que enxergava quando entrou.');

// MINHA HISTÓRIA (fotos da palestrante, logo depois da capa)
pres.addSection({ title: 'Minha história' });
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' });
inteira(s, '2015-hospital', 6.9, 0.6, 5.7, 6.3);
T(s, 'MINHA HISTÓRIA', { x: 0.7, y: 2.2, w: 5.8, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 4 });
T(s, 'Antes de falar sobre enxergar além, deixa eu contar o que eu precisei enxergar', { x: 0.7, y: 2.7, w: 5.8, h: 2.4, fontFace: 'Cambria', fontSize: 34, bold: true, color: C.accent1 });
s.addNotes('MINHA HISTÓRIA. Comece contando de onde você veio. Fale com calma, as fotos falam por você.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' }); rotulo(s, 'MINHA HISTÓRIA · 2015');
fila(s, [['2015-hospital', '2015'], ['2015-tipoia', '2015']], 1.0, 6.0);
s.addNotes('2015. Conte o que aconteceu.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' }); rotulo(s, 'MINHA HISTÓRIA');
inteira(s, 'remedios', 0.7, 1.0, 11.9, 6.0);
s.addNotes('Conte essa fase.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' }); rotulo(s, 'MINHA HISTÓRIA · 2020');
fila(s, [['2020-cafe', '2020'], ['2020-piscina', '2020'], ['colagem', '']], 1.0, 6.0);
s.addNotes('2020. Conte como você estava nessa época.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' }); rotulo(s, 'MINHA HISTÓRIA');
fila(s, [['yoga-antes', ''], ['rosto-antes-depois', '']], 1.0, 6.0);
s.addNotes('Conte o começo da mudança.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Minha história' });
inteira(s, 'yoga-antes-depois', 0.7, 0.6, 7.4, 6.3);
T(s, 'A virada', { x: 8.5, y: 2.6, w: 4.2, h: 1.0, fontFace: 'Cambria', fontSize: 44, bold: true, color: C.accent1 });
T(s, 'Quando eu mudei por dentro, tudo por fora começou a mudar.', { x: 8.5, y: 3.7, w: 4.2, h: 1.5, fontSize: 20, italic: true });
s.addNotes('A VIRADA. Conte o que mudou e faça a ponte para o tema: a mesma pessoa, enxergando diferente. Daqui você entra na pergunta do próximo slide.');
// 2 pergunta
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Abertura' });
T(s, 'UMA PERGUNTA ANTES DE COMEÇAR', { x: 1.2, y: 1.5, w: 10.9, h: 0.5, align: 'center', fontSize: 14, bold: true, color: C.accent2, charSpacing: 4 });
T(s, 'Quem aqui tem certeza de que vê o mundo exatamente como ele é?', { x: 1.2, y: 2.3, w: 10.9, h: 2.2, align: 'center', valign: 'middle', fontFace: 'Cambria', fontSize: 44, italic: true, color: C.background1 });
circ(s, W/2 - 0.31, 4.9, '?', { fs: 24 });
T(s, 'Quem só enxerga o óbvio, só alcança o óbvio.', { x: 1.2, y: 5.8, w: 10.9, h: 0.5, align: 'center', fontSize: 18, color: C.accent1 });
s.addNotes('(2 min) Faça a pergunta e espere. Deixe as pessoas levantarem a mão. A maioria vai levantar. Diga: hoje eu vou tentar mostrar que nenhum de nós vê o mundo como ele é. A gente vê o mundo como a gente é.');
// 3 cérebro
pres.addSection({ title: 'Como a mente funciona' });
ATUAL = 'Foto a direita'; s = pres.addSlide({ masterName: 'Foto a direita', sectionTitle: 'Como a mente funciona' }); fotoDir(s, 'cerebro');
T(s, 'O cérebro não é uma câmera', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
T(s, '0,0035%', { x: 0.7, y: 1.95, w: 6.3, h: 1.1, fontFace: 'Cambria', fontSize: 66, bold: true, color: C.accent1 });
T(s, 'é o quanto do espectro de luz que existe os nossos olhos conseguem ver', { x: 0.7, y: 3.05, w: 6.0, h: 0.7, fontSize: 16, color: C.accent2 });
[['Todo o resto existe', 'Só não é captado pelos nossos sentidos.'], ['O cérebro monta a realidade', 'Recebe sinais elétricos, compara com o passado e cria um modelo do mundo em tempo real.'], ['Construtor, não gravador', 'O que chamamos de "mundo" é uma interpretação feita por dentro.']].forEach(([a, b], i) => {
  const y = 4.0 + i * 1.05; circ(s, 0.7, y, String(i + 1), { fs: 16 });
  T(s, [{ text: a, options: { bold: true, color: C.background1, breakLine: true } }, { text: b, options: { color: C.accent2, fontSize: 14 } }], { x: 1.55, y: y - 0.05, w: 5.6, h: 0.95, fontSize: 16 }); });
s.addNotes('(3 min) Fonte: vídeo do Lucas Naves (neurociência). Analogia com maçã: é como olhar o mundo por um buraco de fechadura e achar que viu a casa inteira. O cérebro não fotografa, ele adivinha e corrige o tempo todo (processamento preditivo). Ou seja: a gente não reage ao mundo, reage ao modelo que o cérebro fez do mundo.');
// 4 cartas (foto inteira)
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Como a mente funciona' }); foto(s, 'cartas', { x: 0, y: 0, w: W, h: H }); veu(s, { x: 0, y: 0, w: 7.4, h: H, fill: { color: '0E1022', transparency: 15 } });
T(s, 'As cartas trocadas', { x: 0.7, y: 0.6, w: 6.3, h: 0.9, fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 });
T(s, 'No filme Interstate 60, o médico mostra cartas rápido e o paciente diz o naipe de cada uma.', { x: 0.7, y: 1.75, w: 6.0, h: 0.95, fontSize: 18 });
T(s, 'As copas eram pretas. As espadas, vermelhas. Ele não percebeu.', { x: 0.7, y: 2.85, w: 6.0, h: 0.95, fontSize: 18, bold: true, color: C.accent1 });
T(s, '"A experiência te condicionou a pensar que todas as copas são vermelhas."', { x: 0.7, y: 3.95, w: 6.0, h: 1.1, fontFace: 'Cambria', fontSize: 20, italic: true });
card(s, 0.7, 5.5, 6.0, 1.0, 'dinâmica'); T(s, [{ text: 'Dinâmica: ', options: { bold: true, color: C.accent1 } }, { text: 'mostre cartas de baralho trocadas bem rápido e pergunte o que a sala viu.' }], { x: 0.95, y: 5.62, w: 5.5, h: 0.8, fontSize: 14, valign: 'middle' });
s.addNotes("(3 min) Fonte: Fernando Reis, cena do filme Interstate 60 (2002). DINÂMICA: leve um baralho com cartas trocadas (pinte um 6 de espadas de vermelho, por exemplo) ou mostre a imagem do slide por 2 segundos e pergunte: que cartas vocês viram? A maioria vai dizer 'um copas e um espadas' sem notar a cor errada. Frase do filme: 'Temos o que queremos ver, não necessariamente o que está mesmo lá.' Curiosidade: crianças que nunca jogaram cartas passam no teste.");
// 5 rodovias
ATUAL = 'Escuro so titulo'; s = pres.addSlide({ masterName: 'Escuro so titulo', sectionTitle: 'Como a mente funciona' }); foto(s, 'rodovia', { x: 0, y: 1.7, w: W, h: 2.6 });
T(s, 'O cérebro é um sistema de rodovias', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
T(s, 'É fácil ir de um lugar conhecido para outro. Mas tudo o que fica fora das rodovias, mesmo estando lá, a gente passa batido.', { x: 0.7, y: 1.15, w: 11.9, h: 0.5, fontSize: 16, italic: true, color: C.accent2 });
[['Reagimos igual', 'à mesma objeção, ao mesmo colega, ao mesmo problema'], ['Sentimos igual', 'a mesma irritação, o mesmo medo, a mesma pressa'], ['Decidimos igual', 'e juramos que é a realidade, não condicionamento']].forEach(([a, b], i) => {
  const x = 0.7 + i * 4.05; card(s, x, 4.65, 3.75, 2.0, 'card ' + a);
  T(s, [{ text: a, options: { fontFace: 'Cambria', bold: true, fontSize: 22, color: C.accent1, breakLine: true } }, { text: b, options: { fontSize: 15, color: C.background1 } }], { x: x + 0.3, y: 4.9, w: 3.15, h: 1.6 }); });
s.addNotes("(2 min) Ainda do filme. Pergunte: na empresa, qual é a 'carta virada' que a gente vê todo dia? A mesma objeção de cliente, o mesmo atrito na equipe, a mesma reunião que sempre dá errado. É a realidade ou é a estrada que o cérebro já conhece?");
// 6 projetor
pres.addSection({ title: 'Projeção, tempo e medo' });
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Projeção, tempo e medo' }); foto(s, 'projetor', { x: 0, y: 0, w: W, h: H }); veu(s, { x: 0, y: 0, w: W, h: H, fill: { color: '0E1022', transparency: 40 } });
T(s, 'Você não vê o mundo, você o projeta', { x: 0.7, y: 0.6, w: 11.9, h: 0.9, fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1, align: 'center' });
[['O personagem', 'Está dentro do filme. Se identifica com a história e reage a cada cena.', '1B1C3A', C.background1], ['Quem segura o projetor', 'Lembra quem é. Não briga com a tela: muda o que está sendo projetado.', 'E9A93A', C.text1]].forEach(([a, b, f, c], i) => {
  const x = 1.4 + i * 5.45; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.1, w: 5.05, h: 2.6, rectRadius: 0.12, fill: { color: f, transparency: i ? 0 : 10 }, line: { type: 'none' }, objectName: 'card ' + a });
  T(s, [{ text: a, options: { fontFace: 'Cambria', bold: true, fontSize: 24, breakLine: true } }, { text: b, options: { fontSize: 17 } }], { x: x + 0.35, y: 2.4, w: 4.35, h: 2.1, color: c }); });
T(s, '"A realidade não responde ao que você quer. Ela responde ao que você é."', { x: 1.4, y: 5.3, w: 10.5, h: 1.0, align: 'center', fontFace: 'Cambria', fontSize: 24, italic: true, valign: 'middle' });
s.addNotes('(3 min) Fonte: vídeo do Lucas Naves sobre a projeção. Imagem: um rolo de filme antigo roda quadro a quadro, rápido o suficiente para parecer contínuo. O problema é que a gente se perde no filme e esquece que não está dentro da tela. Tocar na tela não muda o filme; mudar quem está assistindo muda. Então, da próxima vez que a realidade não estiver como você quer, não brigue com a tela: mude o seu estado interno.');
// 7 tempo / tv
ATUAL = 'Foto a direita'; s = pres.addSlide({ masterName: 'Foto a direita', sectionTitle: 'Projeção, tempo e medo' }); fotoDir(s, 'tv');
T(s, 'E se o tempo não existisse?', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
['passado', 'presente', 'futuro'].forEach((t, i) => { const x = 0.7 + i * 2.05; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.85, w: 1.85, h: 0.75, rectRadius: 0.1, fill: { color: i === 1 ? 'E9A93A' : '1B1C3A' }, line: { color: '2B2D57', width: 0.75 }, objectName: 'quadro ' + t });
  T(s, t, { x, y: 1.85, w: 1.85, h: 0.75, align: 'center', valign: 'middle', fontSize: 16, bold: true, color: i === 1 ? C.text1 : C.background1 }); });
T(s, 'Como quadros de um filme passando rápido: a sensação de movimento é criada pela consciência.', { x: 0.7, y: 2.95, w: 6.0, h: 0.9, fontSize: 16 });
T(s, 'Duas pessoas vivem o mesmo evento e contam versões diferentes. O passado também é interpretação.', { x: 0.7, y: 3.95, w: 6.0, h: 0.9, fontSize: 16, color: C.accent2 });
T(s, [{ text: 'Você é a TV ou você é o sinal?', options: { fontFace: 'Cambria', bold: true, fontSize: 26, color: C.accent1, breakLine: true } }, { text: 'Se a TV quebra, o sinal continua.', options: { fontSize: 17, italic: true } }], { x: 0.7, y: 5.2, w: 6.3, h: 1.4 });
s.addNotes("(3 min) Fonte: podcast do Lucas Naves 'E se o tempo não existisse?'. Não precisa convencer ninguém de física. A pergunta útil para a sala é: em qual 'quadro' você está escolhendo viver hoje? Cada escolha, virar à esquerda ou à direita, já muda o próximo quadro. A metáfora da TV: o corpo é o aparelho, quem você é de verdade é o sinal, aquilo que vem de Deus.");
// 8 ponte
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Projeção, tempo e medo' }); foto(s, 'ponte', { x: 0, y: 0, w: W, h: H }); veu(s, { x: 6.4, y: 0, w: W - 6.4, h: H, fill: { color: '0E1022', transparency: 15 } });
T(s, 'A ponte ao futuro… ao contrário', { x: 6.9, y: 0.6, w: 5.9, h: 1.3, fontFace: 'Cambria', fontSize: 34, bold: true, color: C.accent1 });
['E se der errado?', 'E se eu perder o emprego?', 'E se ele(a) me deixar?'].forEach((t, i) => { const x = 6.9 + i * 0.35, y = 2.1 + i * 0.85; card(s, x, y, 4.6, 0.68, 'balão ' + i); T(s, t, { x: x + 0.25, y, w: 4.2, h: 0.68, valign: 'middle', fontSize: 17, italic: true }); });
T(s, [{ text: 'Toda vez que você pergunta isso, está visualizando o futuro. ', options: {} }, { text: 'Só que no negativo.', options: { bold: true, color: C.accent1 } }], { x: 6.9, y: 4.8, w: 5.9, h: 0.8, fontSize: 17 });
T(s, 'A mesma ferramenta que constrói resultados também constrói medo.', { x: 6.9, y: 5.6, w: 5.9, h: 0.6, fontSize: 16, color: C.accent2 });
T(s, 'Nem abra espaço para a possibilidade que você não quer na sua vida.', { x: 6.9, y: 6.3, w: 5.9, h: 0.6, fontSize: 16, italic: true, color: C.accent1 });
s.addNotes("(3 min) Fonte: corte do Lucas Naves (@sonsdo_ser). Peça para a sala lembrar qual 'E se...' cada um ensaiou essa semana. O cérebro não diferencia muito bem ensaio de realidade: a gente sente o medo como se já estivesse acontecendo.");
// 9 resiste persiste
pres.addSection({ title: 'Mudança' });
ATUAL = 'Escuro so titulo'; s = pres.addSlide({ masterName: 'Escuro so titulo', sectionTitle: 'Mudança' }); T(s, 'O que você resiste, persiste', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
[['✕', 'Lutar contra o pensamento', '"Sai da minha cabeça, sai!" Quanto mais você briga, mais ele gruda. Brigar também é dar atenção, e atenção é alimento.', '1B1C3A'], ['✓', 'Tirar a atenção', 'Pare de dar energia. Seja o guarda que deixa o trânsito passar, não o que entra na briga. Foque só na realidade que você quer ver.', '2B2D57']].forEach(([ic, a, b, f], i) => {
  const x = 0.7 + i * 6.05; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.75, w: 5.85, h: 3.6, rectRadius: 0.12, fill: { color: f }, line: { color: '2B2D57', width: 0.75 }, objectName: 'card ' + a });
  circ(s, x + 0.4, 2.1, ic, { fs: 20 }); T(s, a, { x: x + 1.2, y: 2.15, w: 4.4, h: 0.55, fontFace: 'Cambria', bold: true, fontSize: 22, color: C.accent1, valign: 'middle' });
  T(s, b, { x: x + 0.4, y: 3.0, w: 5.05, h: 2.1, fontSize: 17 }); });
T(s, 'Tentar não pensar num elefante rosa só faz ele aparecer mais.', { x: 0.7, y: 5.8, w: 11.9, h: 0.7, align: 'center', fontFace: 'Cambria', fontSize: 22, italic: true, color: C.accent2 });
s.addNotes('(2 min) Fonte: Lucas Naves e Mooji. Analogia: é como tentar não pensar num elefante rosa. Quanto mais você tenta, mais ele aparece. O caminho não é lutar, é trocar o foco.');
// 10 padrões
ATUAL = 'Foto a direita'; s = pres.addSlide({ masterName: 'Foto a direita', sectionTitle: 'Mudança' }); fotoDir(s, 'chave');
T(s, 'De onde vêm os nossos padrões', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
T(s, '3 a 5', { x: 0.7, y: 1.95, w: 6.3, h: 1.2, fontFace: 'Cambria', fontSize: 80, bold: true, color: C.accent1 });
T(s, 'anos de idade: é quando a maioria dos nossos padrões e crenças sobre a vida se forma', { x: 0.7, y: 3.2, w: 6.0, h: 0.8, fontSize: 16, color: C.accent2 });
card(s, 0.7, 4.25, 6.3, 1.5, 'frase Louise Hay'); T(s, '"Estou disposto a mudar o padrão em minha consciência que está criando essa situação."', { x: 1.0, y: 4.4, w: 5.7, h: 1.2, fontFace: 'Cambria', fontSize: 19, italic: true, valign: 'middle' });
T(s, 'A menor mudança na consciência já começa a mudar a experiência. Não estamos presos aos nossos roteiros.', { x: 0.7, y: 6.0, w: 6.3, h: 0.9, fontSize: 15 });
s.addNotes("(2 min) Fonte: Louise Hay. Não precisa saber o 'como' ainda; a chave é a disposição. Convide cada um a pensar num problema e dizer, em silêncio, a frase do slide.");
// 11 resistência
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Mudança' }); foto(s, 'montanha', { x: 0, y: 0, w: W, h: H }); veu(s, { x: 0, y: 0, w: 7.2, h: H, fill: { color: '0E1022', transparency: 15 } });
T(s, 'Toda mudança encontra resistência', { x: 0.7, y: 0.6, w: 6.3, h: 1.3, fontFace: 'Cambria', fontSize: 34, bold: true, color: C.accent1 });
T(s, '"Pra baixo, todo santo ajuda."', { x: 0.7, y: 1.95, w: 6.3, h: 0.6, fontFace: 'Cambria', fontSize: 20, italic: true });
T(s, 'Ela aparece quando você tenta:', { x: 0.7, y: 2.7, w: 6.3, h: 0.4, fontSize: 15, bold: true, color: C.accent2 });
T(s, ['Melhorar um relacionamento', 'Cuidar da saúde ou crescer na fé', 'Empreender ou criar algo', 'Largar um vício', 'Ter coragem e se comprometer', 'Esperar o resultado sem desistir'].map((t, i, a) => ({ text: t, options: { bullet: { indent: 18 }, breakLine: i < a.length - 1 } })), { x: 0.7, y: 3.15, w: 6.0, h: 2.4, fontSize: 16, paraSpaceAfter: 4 });
T(s, [{ text: 'Para subir de patamar, prepare-se: vem artilharia pesada. ', options: {} }, { text: 'O objetivo da resistência é um só: não deixar nada mudar.', options: { bold: true, color: C.accent1 } }], { x: 0.7, y: 5.75, w: 6.2, h: 1.1, fontSize: 16 });
s.addNotes('(3 min) Fonte: Prof. Lúcia Helena Galvão, \'Vença a resistência\'. Mensagem central: se apareceu resistência, é sinal de que você está subindo. Qualquer coisa que te enobreça conta com a resistência, e ela vem com tudo. Ser capaz de persistir por dever, e não só pelo prêmio, é o que rompe o patamar.');
// 12 quebre o ciclo
ATUAL = 'Escuro so titulo'; s = pres.addSlide({ masterName: 'Escuro so titulo', sectionTitle: 'Mudança' }); foto(s, 'trilha', { x: 0, y: 4.35, w: W, h: H - 4.35 }); veu(s, { x: 0, y: 4.35, w: W, h: H - 4.35, fill: { color: '0E1022', transparency: 30 } });
T(s, 'Quebre o ciclo', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
['Eu quero', 'Eu visualizo', 'Eu tento', 'Eu consigo'].forEach((t, i) => { const x = 1.0 + i * 3.0; circ(s, x + 0.75, 1.75, String(i + 1), { fs: 18 });
  T(s, t, { x, y: 2.5, w: 2.1, h: 0.5, align: 'center', fontFace: 'Cambria', bold: true, fontSize: 22, color: C.accent1 });
  if (i < 3) T(s, '→', { x: x + 2.15, y: 1.75, w: 0.8, h: 0.62, align: 'center', valign: 'middle', fontSize: 28, color: C.accent2 }); });
T(s, 'Toda vez que você faz o que achava impossível, o cérebro abre uma estrada nova. Isso é neuroplasticidade: dá para se reinventar.', { x: 1.0, y: 3.2, w: 11.3, h: 0.9, fontSize: 17, align: 'center' });
T(s, '"Transformai-vos pela renovação do vosso entendimento." (Romanos 12:2)', { x: 1.0, y: 6.3, w: 11.3, h: 0.6, fontFace: 'Cambria', fontSize: 20, italic: true, align: 'center', bold: true });
s.addNotes('(2 min) Fonte: vídeo dos neurônios (@quantica_e_espiritualidade). Liga com o slide das rodovias: no começo a estrada nova é uma trilha no mato; a cada repetição vira uma rodovia. Mudar não é virar outra pessoa, é treinar um caminho novo.');
// 13 dia a dia
pres.addSection({ title: 'Na prática' });
ATUAL = 'Escuro so titulo'; s = pres.addSlide({ masterName: 'Escuro so titulo', sectionTitle: 'Na prática' }); T(s, 'Enxergar além no nosso dia a dia', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
[['Vendas', 'Quem vende característica disputa preço. Quem enxerga a necessidade real do cliente constrói valor.'], ['Liderança', 'A "carta virada" sobre alguém da equipe pode estar escondendo o potencial dessa pessoa.'], ['Atendimento', 'O cliente difícil é a realidade, ou é a interpretação de hoje?'], ['Pessoal', 'Qual "E se der errado?" você está ensaiando esta semana?']].forEach(([a, b], i) => {
  const x = 0.7 + (i % 2) * 6.05, y = 1.7 + Math.floor(i / 2) * 2.55; card(s, x, y, 5.85, 2.3, 'card ' + a);
  circ(s, x + 0.35, y + 0.35, a[0], { fs: 18 }); T(s, a, { x: x + 1.15, y: y + 0.38, w: 4.4, h: 0.55, fontFace: 'Cambria', bold: true, fontSize: 22, color: C.accent1, valign: 'middle' });
  T(s, b, { x: x + 0.35, y: y + 1.1, w: 5.15, h: 1.05, fontSize: 16 }); });
s.addNotes('(3 min) Traga um exemplo real da empresa para cada quadrante, se tiver. Pergunte qual deles mais conversa com cada área.');
// 14 exercício
ATUAL = 'Escuro so titulo'; s = pres.addSlide({ masterName: 'Escuro so titulo', sectionTitle: 'Na prática' }); T(s, 'Exercício: troque a carta', Object.assign({ fontFace: 'Cambria', fontSize: 36, bold: true, color: C.accent1 }, TIT[ATUAL]));
['Escreva uma situação da semana que te incomodou', 'Escreva a "carta" que você viu: sua interpretação automática', 'Escreva outra leitura possível da mesma situação', 'Escolha qual delas você vai alimentar a partir de hoje'].forEach((t, i) => {
  const y = 1.75 + i * 1.2; card(s, 0.7, y, 11.9, 0.98, 'passo ' + (i + 1)); circ(s, 0.95, y + 0.18, String(i + 1), { fs: 18 }); T(s, t, { x: 1.85, y, w: 10.5, h: 0.98, valign: 'middle', fontSize: 19 }); });
T(s, '2 minutos em silêncio · papel e caneta', { x: 0.7, y: 6.6, w: 11.9, h: 0.4, fontSize: 13, italic: true, color: C.accent2 });
s.addNotes('(4 min) Distribua papel e caneta antes. Dê 2 minutos em silêncio. Depois peça 1 ou 2 voluntários para compartilhar só o passo 3 e o 4, sem expor a situação inteira.');
// 15 encerramento
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Na prática' }); foto(s, 'pomba', { x: 0, y: 0, w: W, h: H }); veu(s, { x: 0, y: 0, w: W, h: H, fill: { color: '0E1022', transparency: 35 } });
T(s, 'Pare de ser guarda de trânsito da sua mente', { x: 1.2, y: 1.2, w: 10.9, h: 1.4, align: 'center', valign: 'middle', fontFace: 'Cambria', fontSize: 40, bold: true, color: C.accent1 });
T(s, 'Observe sem entrar na briga. Quando perceber que entrou, apenas saia. Aos poucos o barulho vai embora e vem uma calma que ninguém precisa te explicar: você sente. Essa é a presença de Deus em você.', { x: 2.0, y: 2.9, w: 9.3, h: 1.8, align: 'center', fontSize: 19, italic: true });
T(s, 'Enxergar além é escolher, todos os dias, qual realidade você vai alimentar.', { x: 1.2, y: 5.3, w: 10.9, h: 0.9, align: 'center', valign: 'middle', fontFace: 'Cambria', fontSize: 24, bold: true, color: C.accent1 });
s.addNotes('(2 min) Fonte: Mooji. Fale devagar. Retome a pergunta do começo: quem ainda tem certeza de que vê o mundo exatamente como ele é? Agradeça. Se quiser, termine com um minuto de silêncio para cada um sentir essa calma.');

// CAMPO ENERGÉTICO (final)
pres.addSection({ title: 'Campo energético' });
ATUAL = 'Foto inteira'; s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Campo energético' }); rotulo(s, 'CAMPO ENERGÉTICO');
inteira(s, 'emocoes', 0.7, 1.0, 11.9, 6.0);
s.addNotes('CAMPO ENERGÉTICO. Mostre como cada emoção mexe com o corpo.');
s = pres.addSlide({ masterName: 'Foto inteira', sectionTitle: 'Campo energético' }); rotulo(s, 'CAMPO ENERGÉTICO');
fila(s, [['luz', ''], ['toroide', ''], ['aura', '']], 1.0, 6.0);
s.addNotes('Fale do campo de energia que cada um de nós emite.');
(async () => { const f = __dirname + '/Enxergar_Alem_NOVO.pptx'; await pres.writeFile({ fileName: f }); await applyTheme(f, THEME); console.log('ok'); })();
