# Quinta 05/11 — kit dos vendedores no estilo "vitrine limpa" (composição inspirada no Mercado Livre, sem copiar),
# com a paleta da Leilão no Zap (docs/GUIA_DE_DESIGN.md). Uma arte e um molde diferente por leilão. Horários do sistema.
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from kit import logo, salvar
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-05/quinta-05-11/kit-vendedores-vitrine'
W, H = 1080, 1350
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE = (27, 122, 72); NEON = (63, 208, 126); FOGO = (243, 91, 18); OURO = (245, 196, 81); NOITE = (10, 20, 16)
FLORESTA = (12, 66, 40); MENTA = (226, 242, 232); AREIA = (246, 239, 226); BRANCO = (255, 255, 255)

def fundo(cor): return Image.new('RGBA', (W, H), cor + (255,))
def prod(nome, alt):
    p = Image.open(f'{I}/{nome}').convert('RGBA'); p = p.crop(p.getbbox()); return p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
def pousa(b, p, x, base, forca=90):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((x + p.width * .1, base - 14, x + p.width * .9, base + 14), fill=(0, 0, 0, forca))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16))); b.alpha_composite(p, (int(x), int(base - p.height)))
def preco(d, x, y, valor, cor, tam=200, rs=None):
    rs = rs or int(tam * .36); d.text((x, y + tam * .2), 'R$', font=F('Black', rs), fill=cor)
    d.text((x + d.textlength('R$', font=F('Black', rs)) + 14, y), valor, font=F('Black', tam), fill=cor)
def pilula(d, x, y, txt, fundo_, cor, tam=32, anc='l'):
    f = F('Black', tam); w = d.textlength(txt, font=f) + 56; h = tam + 30
    if anc == 'r': x -= w
    if anc == 'm': x -= w / 2
    d.rounded_rectangle((x, y, x + w, y + h), h / 2, fill=fundo_); d.text((x + w / 2, y + h / 2), txt, font=f, fill=cor, anchor='mm')
def dagua(b, linhas, cor, alfa=18, tam=300, y0=90):
    m = Image.new('RGBA', b.size); d = ImageDraw.Draw(m)
    for k, t in enumerate(linhas): d.text((W / 2, y0 + k * tam), t, font=F('Black', tam), fill=cor + (alfa,), anchor='mt')
    b.alpha_composite(m)
def rodape(d, txt, cor): d.text((70, H - 62), txt, font=F('SemiBold', 30), fill=cor, anchor='lm')

# 1 · 12h MEDIDOR — fundo verde da marca, "um produto, uma frase"
def a1():
    b = fundo(VERDE); logo(b, y=56, largura=170, x=70); d = ImageDraw.Draw(b)
    pilula(d, W - 70, 70, 'MARTELO 12H', OURO, NOITE, anc='r')
    d.text((70, 230), 'Cuidar de quem', font=F('Black', 84), fill=BRANCO); d.text((70, 322), 'você ama', font=F('Medium', 84), fill=BRANCO)
    d.text((70, 414), 'custa pouco.', font=F('Medium', 84), fill=OURO)
    pousa(b, prod('c-pressao2.png', 470), 360, 1000, 110); d = ImageDraw.Draw(b)
    d.text((70, 1050), 'lance desde', font=F('Medium', 40), fill=MENTA); preco(d, 70, 1090, '7,97', BRANCO, 150)
    d.text((W - 70, 1150), 'Medidor de pressão', font=F('SemiBold', 32), fill=MENTA, anchor='ra'); d.text((W - 70, 1195), 'na loja R$ 56,21', font=F('Medium', 30), fill=MENTA, anchor='ra')
    salvar(b, f'{OUT}/1-12h-medidor-pressao.jpg')

# 2 · 14h TAPETE PET — fundo menta, metade/metade
def a2():
    b = fundo(MENTA); d = ImageDraw.Draw(b); d.rectangle((0, H // 2 + 20, W, H), fill=VERDE)
    d.text((70, 120), 'O que o seu', font=F('Black', 70), fill=FLORESTA); d.text((70, 198), 'pet precisa', font=F('Medium', 70), fill=FLORESTA); d.text((70, 276), 'em casa:', font=F('Medium', 70), fill=FLORESTA)
    pilula(d, 70, 390, '30 UNIDADES · 60 x 60 CM', BRANCO, VERDE, 28)
    pousa(b, prod('c-tapete.png', 380), 650, 700, 80); d = ImageDraw.Draw(b)
    d.text((W - 70, 760), 'Onde o lance', font=F('Black', 72), fill=BRANCO, anchor='ra'); d.text((W - 70, 840), 'começa:', font=F('Medium', 72), fill=BRANCO, anchor='ra')
    preco(d, 70, 960, '7,97', OURO, 230)
    logo(b, y=1215, largura=160, x=W - 230); d = ImageDraw.Draw(b)
    rodape(d, 'Tapete higiênico pet · martelo hoje às 14h', MENTA)
    salvar(b, f'{OUT}/2-14h-tapete-pet.jpg')

# 3 · 16h HEADSET — fundo noite, número herói em verde vivo, pergunta de engajamento
def a3():
    b = fundo(NOITE); dagua(b, ['GAMER'], NEON, 16, 300, 120); logo(b, y=56, largura=170, x=70); d = ImageDraw.Draw(b)
    pilula(d, W - 70, 70, 'MARTELO 16H', FOGO, BRANCO, anc='r')
    d.text((W / 2, 230), 'Quanto você', font=F('Black', 92), fill=BRANCO, anchor='mt'); d.text((W / 2, 330), 'daria nele?', font=F('Medium', 92), fill=NEON, anchor='mt')
    pousa(b, prod('c-headset.png', 500), 290, 990, 160); d = ImageDraw.Draw(b)
    d.text((70, 1060), 'lance desde', font=F('Medium', 40), fill=(190, 214, 200)); preco(d, 70, 1100, '7,97', NEON, 150)
    d.text((W - 70, 1150), 'Headset gamer Flakes', font=F('SemiBold', 32), fill=(190, 214, 200), anchor='ra'); d.text((W - 70, 1195), 'na loja R$ 99,96', font=F('Medium', 30), fill=(190, 214, 200), anchor='ra')
    salvar(b, f'{OUT}/3-16h-headset-gamer.jpg')

# 4 · 18h RELÓGIO — fundo ouro, produto grande à direita, selo "achadinho"
def a4():
    b = fundo(OURO); dagua(b, ['18H'], FLORESTA, 14, 520, 330); logo(b, y=56, largura=170, x=70); d = ImageDraw.Draw(b)
    d.text((70, 250), 'Elegância', font=F('Black', 96), fill=FLORESTA); d.text((70, 350), 'no pulso,', font=F('Medium', 96), fill=FLORESTA)
    d.text((70, 450), 'preço de', font=F('Medium', 96), fill=FLORESTA); d.text((70, 550), 'lance.', font=F('Black', 96), fill=VERDE)
    pousa(b, prod('c-relogio.png', 560), 560, 1040, 90); d = ImageDraw.Draw(b)
    d.ellipse((800, 190, 1020, 410), fill=VERDE); d.text((910, 270), 'ACHADINHO', font=F('Black', 30), fill=BRANCO, anchor='mm'); d.text((910, 320), 'DO DIA', font=F('Black', 38), fill=OURO, anchor='mm')
    d.text((70, 1080), 'lance desde', font=F('Medium', 40), fill=FLORESTA); preco(d, 70, 1120, '7,97', FLORESTA, 150)
    d.text((W - 70, 1170), 'Relógio EYT ouro rosa', font=F('SemiBold', 32), fill=FLORESTA, anchor='ra'); d.text((W - 70, 1215), 'na loja R$ 108,75 · martelo 18h', font=F('Medium', 30), fill=FLORESTA, anchor='ra')
    salvar(b, f'{OUT}/4-18h-relogio.jpg')

# 5 · 20h CÂMERA — fundo areia, "pra que serve?" com 3 etiquetas
def a5():
    b = fundo(AREIA); logo(b, y=56, largura=170, x=70); d = ImageDraw.Draw(b)
    pilula(d, W - 70, 70, 'MARTELO 20H', VERDE, BRANCO, anc='r')
    d.text((70, 220), 'Pra que', font=F('Black', 110), fill=FLORESTA); d.text((70, 330), 'serve?', font=F('Medium', 110), fill=VERDE)
    for k, t in enumerate(['ver o motor', 'achar no ralo', 'olhar na parede']): pilula(d, 70, 500 + k * 90, t, BRANCO, FLORESTA, 34)
    pousa(b, prod('c-camera.png', 640), 580, 1010, 80); d = ImageDraw.Draw(b)
    d.text((70, 1060), 'lance desde', font=F('Medium', 40), fill=VERDE); preco(d, 70, 1100, '7,97', FLORESTA, 150)
    d.text((W - 70, 1150), 'Câmera endoscópica LED', font=F('SemiBold', 32), fill=FLORESTA, anchor='ra'); d.text((W - 70, 1195), 'na loja R$ 96,84', font=F('Medium', 30), fill=FLORESTA, anchor='ra')
    salvar(b, f'{OUT}/5-20h-camera-endoscopica.jpg')

# 6 · SÁBADO iPHONE — fundo floresta, número herói "o último saiu por"
def a6():
    b = fundo(FLORESTA); dagua(b, ['SÁBADO'], OURO, 14, 250, 1040); logo(b, y=56, largura=170, x=70); d = ImageDraw.Draw(b)
    pilula(d, W - 70, 70, 'SÁBADO · 20H', OURO, NOITE, anc='r')
    d.text((70, 220), 'O último iPhone', font=F('Medium', 60), fill=MENTA); d.text((70, 290), 'saiu por', font=F('Medium', 60), fill=MENTA)
    preco(d, 70, 380, '4.640', OURO, 150); d.text((70, 590), 'no leilão de 24/10', font=F('SemiBold', 34), fill=MENTA)
    pousa(b, prod('c-iphone.png', 540), 660, 1000, 150); d = ImageDraw.Draw(b)
    d.line((70, 700, 470, 700), fill=(255, 255, 255, 60), width=2)
    d.text((70, 740), 'Sábado tem outro.', font=F('Black', 56), fill=BRANCO)
    d.text((70, 820), 'lance inicial', font=F('Medium', 38), fill=MENTA); preco(d, 70, 860, '197', BRANCO, 120)
    rodape(d, 'iPhone 17 Pro Max 256GB · na loja R$ 9.464,78', MENTA)
    salvar(b, f'{OUT}/6-sabado-20h-iphone.jpg')

for f in (a1, a2, a3, a4, a5, a6): f()
print('ok')
