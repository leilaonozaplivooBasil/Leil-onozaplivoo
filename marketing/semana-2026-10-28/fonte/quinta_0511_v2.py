# Quinta 05/11 v2: 6 artes de feed, cada uma com um layout diferente (inspiração: como Amazon e Mercado Livre
# mostram produto — achadinho, benefícios, "pra que serve", foto de uso, engajamento e prova de preço).
# Fotos: produto real com fundo trocado (Magnific). Dados do sistema. Sem selo de %, sem link.
import sys
from PIL import Image, ImageDraw, ImageFilter
from kit import fundo, logo, fonte, texto_rico, leiloeiro, sombra, salvar, DOURADO, VERDE_ESCURO, VERDE, VERDE_CLARO, BRANCO
from pecas import real
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-05/quinta-05-11/feed-v2'
W, H = 1080, 1350
HORA = sys.argv[1] if len(sys.argv) > 1 else '8H'
LANCE0 = 7.97

def cobre(caminho, w, h, foco=(0.5, 0.5)):
    im = Image.open(caminho).convert('RGB'); e = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * e), round(im.height * e)), Image.LANCZOS)
    x = int((im.width - w) * foco[0]); y = int((im.height - h) * foco[1])
    return im.crop((x, y, x + w, y + h)).convert('RGBA')

def arred(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    im = im.copy(); im.putalpha(m); return im

def degrade(b, y0, y1, cor=VERDE_ESCURO, a0=0, a1=255):
    g = Image.new('RGBA', (W, y1 - y0)); d = ImageDraw.Draw(g)
    for y in range(y1 - y0):
        a = int(a0 + (a1 - a0) * (y / (y1 - y0)) ** 1.3); d.line((0, y, W, y), fill=cor + (a,))
    b.alpha_composite(g, (0, y0))

def pilula(d, xy, txt, f, fundo_=DOURADO, cor=VERDE_ESCURO, pad=(28, 14), anc='l'):
    w = d.textlength(txt, font=f); x, y = xy
    if anc == 'm': x -= (w + 2 * pad[0]) / 2
    hh = f.size + 2 * pad[1]
    d.rounded_rectangle((x, y, x + w + 2 * pad[0], y + hh), hh / 2, fill=fundo_)
    d.text((x + pad[0], y + hh / 2), txt, font=f, fill=cor, anchor='lm'); return x + w + 2 * pad[0]

def riscado(d, xy, txt, f, cor=(225, 225, 225)):
    d.text(xy, txt, font=f, fill=cor); w = d.textlength(txt, font=f)
    yy = xy[1] + f.size * 0.62; d.line((xy[0] - 4, yy, xy[0] + w + 4, yy), fill=(230, 80, 70), width=6)

def logo_canto(b, x=60, y=50, larg=230): logo(b, y=y, largura=larg, x=x)

def check(d, x, y, r=26):
    d.ellipse((x, y, x + 2 * r, y + 2 * r), fill=VERDE)
    d.line((x + r * .5, y + r * 1.05, x + r * .9, y + r * 1.45, x + r * 1.55, y + r * .65), fill=BRANCO, width=7, joint='curve')

# 1 · RELÓGIO — "achadinho do dia": foto cheia, etiqueta de oferta, preço de loja riscado x lance inicial
def a1():
    b = cobre(f'{I}/bg-relogio.jpg', W, H, (0.35, 0.4)); degrade(b, 620, H, a1=250); degrade(b, 0, 260, a0=200, a1=0)
    logo_canto(b); d = ImageDraw.Draw(b)
    pilula(d, (W - 60 - 410, 70), 'ACHADINHO DO DIA', fonte('Black', 38), anc='l')
    d.text((60, 900), 'Relógio EYT', font=fonte('Black', 88), fill=BRANCO)
    d.text((60, 1000), 'caixa ouro rosa · pulseira de couro marrom', font=fonte('Bold', 36), fill=VERDE_CLARO)
    riscado(d, (60, 1075), f'Na loja {real(108.75)}', fonte('Bold', 44))
    d.text((60, 1150), 'lance começa em', font=fonte('Bold', 40), fill=BRANCO)
    d.text((410, 1128), real(LANCE0), font=fonte('Black', 84), fill=DOURADO)
    pilula(d, (60, 1255), f'MARTELO HOJE ÀS {HORA}', fonte('Black', 32), fundo_=(255, 255, 255), cor=VERDE_ESCURO, pad=(24, 10))
    salvar(b, f'{OUT}/01-relogio-achadinho.jpg')

# 2 · MEDIDOR — jeito Amazon: título de benefício, foto de uso, "o que vem na caixa" com checks
def a2():
    b = Image.new('RGBA', (W, H), (246, 248, 245, 255)); d = ImageDraw.Draw(b)
    d.rectangle((0, 0, W, 150), fill=VERDE_ESCURO); logo(b, y=28, largura=230)
    ft = arred(cobre(f'{I}/bg-pressao.jpg', 960, 620, (0.5, 0.45)), 34); b.alpha_composite(ft, (60, 190))
    d.text((60, 850), 'Pressão medida em casa,', font=fonte('Black', 60), fill=VERDE_ESCURO)
    d.text((60, 920), 'sem fila de farmácia', font=fonte('Black', 60), fill=VERDE)
    for k, t in enumerate(['Digital, de pulso', 'Vem com 2 pilhas AAA', 'Manual de instruções']):
        y = 1015 + k * 70; check(d, 60, y); d.text((130, y + 26), t, font=fonte('Bold', 40), fill=(30, 40, 34), anchor='lm')
    d.rounded_rectangle((620, 1010, 1020, 1220), 30, fill=VERDE_ESCURO)
    riscado(d, (650, 1030), f'Na loja {real(56.21)}', fonte('Bold', 32))
    d.text((650, 1080), 'lance desde', font=fonte('Bold', 32), fill=VERDE_CLARO)
    d.text((650, 1120), real(LANCE0), font=fonte('Black', 72), fill=DOURADO)
    d.text((W / 2, 1290), f'Martelo hoje às {HORA} · Leilão no Zap', font=fonte('Black', 34), fill=VERDE_ESCURO, anchor='mm')
    salvar(b, f'{OUT}/02-medidor-beneficios.jpg')

# 3 · CÂMERA — "pra que serve?": pergunta grande, foto, 3 usos numerados
def a3():
    b = fundo(W, H, brilho=(700, 620)); logo_canto(b); d = ImageDraw.Draw(b)
    d.text((60, 190), 'PRA QUE', font=fonte('Black', 110), fill=BRANCO)
    d.text((60, 300), 'SERVE?', font=fonte('Black', 110), fill=DOURADO)
    ft = arred(cobre(f'{I}/bg-camera.jpg', 420, 760, (0.5, 0.3)), 34)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).rounded_rectangle((610, 210, 1040, 990), 34, fill=(0, 0, 0, 160))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(24))); b.alpha_composite(ft, (600, 190))
    d = ImageDraw.Draw(b); d.rounded_rectangle((600, 190, 1020, 950), 34, outline=DOURADO, width=4)
    for k, (t1, t2) in enumerate([('Ver dentro', 'do motor'), ('Achar o que', 'caiu no ralo'), ('Olhar atrás', 'da parede')]):
        y = 470 + k * 165
        d.ellipse((60, y, 140, y + 80), fill=DOURADO); d.text((100, y + 40), str(k + 1), font=fonte('Black', 48), fill=VERDE_ESCURO, anchor='mm')
        d.text((165, y + 4), t1, font=fonte('Black', 42), fill=BRANCO); d.text((165, y + 50), t2, font=fonte('Bold', 38), fill=VERDE_CLARO)
    d.text((60, 1010), 'Câmera endoscópica com LED', font=fonte('Black', 52), fill=BRANCO)
    riscado(d, (60, 1085), f'Na loja {real(96.84)}', fonte('Bold', 42))
    x = pilula(d, (60, 1160), f'LANCE DESDE {real(LANCE0)}', fonte('Black', 44))
    pilula(d, (x + 20, 1166), f'HOJE ÀS {HORA}', fonte('Black', 36), fundo_=VERDE_ESCURO, cor=DOURADO, pad=(24, 12))
    salvar(b, f'{OUT}/03-camera-pra-que-serve.jpg')

# 4 · TAPETE PET — foto de casa, título emocional, adesivo redondo de preço
def a4():
    b = Image.new('RGBA', (W, H), VERDE_ESCURO + (255,))
    ft = Image.open(f'{I}/bg-tapete.jpg').convert('RGBA').resize((1080, 1115), Image.LANCZOS); b.alpha_composite(ft, (0, 235))
    degrade(b, 235, 420, a0=255, a1=0); degrade(b, 1000, H, a1=245)
    logo_canto(b, x=W - 290, y=40); d = ImageDraw.Draw(b)
    d.text((60, 40), 'Seu pet', font=fonte('Black', 84), fill=BRANCO)
    d.text((60, 130), 'agradece', font=fonte('Black', 84), fill=DOURADO)
    x = pilula(d, (W - 60 - 250, 160), '60 x 60 cm', fonte('Black', 32), fundo_=BRANCO)
    pilula(d, (W - 60 - 250 - 16 - 268, 160), '60 UNIDADES', fonte('Black', 32), fundo_=BRANCO)
    cx, cy, r = 880, 1020, 160
    s_ = Image.new('RGBA', (W, H)); ImageDraw.Draw(s_).ellipse((cx - r + 8, cy - r + 20, cx + r + 8, cy + r + 20), fill=(0, 0, 0, 150))
    b.alpha_composite(s_.filter(ImageFilter.GaussianBlur(20))); d = ImageDraw.Draw(b)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=DOURADO, outline=BRANCO, width=6)
    d.text((cx, cy - 70), 'lance desde', font=fonte('Bold', 32), fill=VERDE_ESCURO, anchor='mm')
    d.text((cx, cy), real(LANCE0), font=fonte('Black', 64), fill=VERDE_ESCURO, anchor='mm')
    d.text((cx, cy + 66), f'hoje às {HORA.lower()}', font=fonte('Black', 32), fill=VERDE_ESCURO, anchor='mm')
    d.text((60, 1180), 'Tapete higiênico pet', font=fonte('Black', 56), fill=BRANCO)
    riscado(d, (60, 1255), f'Na loja {real(68.71)}', fonte('Bold', 42))
    salvar(b, f'{OUT}/04-tapete-pet-casa.jpg')

# 5 · HEADSET — engajamento: "quanto você daria?" + caixa de comentário
def a5():
    b = cobre(f'{I}/bg-headset.jpg', W, H, (0.5, 0.4)); degrade(b, 0, 380, cor=(5, 10, 8), a0=230, a1=0); degrade(b, 820, H, cor=(5, 10, 8), a1=250)
    logo_canto(b); d = ImageDraw.Draw(b)
    pilula(d, (W - 60 - 330, 66), 'SETUP GAMER', fonte('Black', 36), fundo_=(230, 60, 60), cor=BRANCO)
    d.text((60, 860), 'Quanto você', font=fonte('Black', 96), fill=BRANCO)
    d.text((60, 965), 'daria nele?', font=fonte('Black', 96), fill=DOURADO)
    d.rounded_rectangle((60, 1095, 1020, 1185), 45, fill=(255, 255, 255, 255))
    d.text((105, 1140), 'Comenta seu lance aqui embaixo...', font=fonte('Bold', 38), fill=(120, 120, 120), anchor='lm')
    d.text((60, 1225), f'Headset gamer Flakes · na loja', font=fonte('Bold', 36), fill=VERDE_CLARO)
    d.text((630, 1222), real(99.96), font=fonte('Black', 40), fill=BRANCO)
    d.text((60, 1275), f'lance desde {real(LANCE0)} · martelo hoje às {HORA}', font=fonte('Black', 36), fill=DOURADO)
    salvar(b, f'{OUT}/05-headset-quanto-voce-daria.jpg')

# 6 · iPHONE SÁBADO — prova de preço: quanto saiu o último (24/10, dado do sistema) x preço de loja de agora
def a6():
    b = Image.new('RGBA', (W, H), (6, 14, 10, 255)); b.alpha_composite(fundo(W, H, brilho=(760, 560)).point(lambda v: int(v * 0.85)))
    logo_canto(b); d = ImageDraw.Draw(b)
    pilula(d, (W - 60 - 330, 66), 'SÁBADO · 20H', fonte('Black', 38))
    ft = arred(cobre(f'{I}/bg-iphone.jpg', 440, 800, (0.5, 0.5)), 34)
    sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).rounded_rectangle((590, 200, 1040, 1010), 34, fill=(0, 0, 0, 170))
    b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26))); b.alpha_composite(ft, (580, 190))
    ImageDraw.Draw(b).rounded_rectangle((580, 190, 1020, 990), 34, outline=DOURADO, width=4)
    d = ImageDraw.Draw(b)
    d.text((60, 230), 'O último', font=fonte('Black', 70), fill=BRANCO)
    d.text((60, 310), 'saiu por', font=fonte('Black', 70), fill=BRANCO)
    d.text((60, 400), 'R$ 4.640', font=fonte('Black', 104), fill=DOURADO)
    d.text((60, 525), 'iPhone 17 Pro Max', font=fonte('Bold', 38), fill=VERDE_CLARO)
    d.text((60, 572), 'no leilão de 24/10', font=fonte('Bold', 38), fill=VERDE_CLARO)
    d.rounded_rectangle((60, 1050, 1020, 1290), 34, fill=(8, 38, 25, 235), outline=DOURADO, width=3)
    d.text((100, 1080), 'Sábado tem outro: iPhone 17 Pro Max 256GB', font=fonte('Black', 40), fill=BRANCO)
    riscado(d, (100, 1145), f'Na loja {real(9464.78)}', fonte('Bold', 40))
    d.text((100, 1205), 'lance inicial', font=fonte('Bold', 40), fill=VERDE_CLARO)
    d.text((345, 1192), real(197), font=fonte('Black', 62), fill=DOURADO)
    salvar(b, f'{OUT}/06-sabado-iphone-o-ultimo-saiu-por.jpg')

for f in (a1, a2, a3, a4, a5, a6): f()
print('ok')
