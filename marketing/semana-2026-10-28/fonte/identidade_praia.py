# Proposta de nova identidade (04/11): praia, good vibes, alto padrão, preço baixo. 3 direções com o MESMO post
# (iPhone de sábado) para comparar. Cenário por IA sem produto; produto = foto original recortada.
from PIL import Image, ImageDraw, ImageFilter
from kit import logo, salvar
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/marca/identidade-praia/propostas'
W, H = 1080, 1350
F = lambda p, t: __import__('PIL.ImageFont', fromlist=['x']).truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE = (12, 74, 46); OURO = (201, 162, 77); AREIA = (247, 241, 230); BRANCO = (255, 255, 255)

def cena(n): return Image.open(f'{I}/{n}').convert('RGBA').resize((W, H), Image.LANCZOS)
def produto(b, cx, base, alt, sombra=110):
    p = Image.open(f'{I}/c-iphone.png').convert('RGBA'); p = p.crop(p.getbbox()); p = p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - p.width * .5, base - 18, cx + p.width * .5, base + 18), fill=(0, 0, 0, sombra))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16))); b.alpha_composite(p, (int(cx - p.width / 2), base - alt))
def espaco(d, xy, t, f, fill, track=6, anchor='l'):
    x, y = xy; w = sum(d.textlength(c, font=f) + track for c in t) - track
    if anchor == 'm': x -= w / 2
    for c in t: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + track
def riscado(d, xy, t, f, cor):
    d.text(xy, t, font=f, fill=cor); w = d.textlength(t, font=f); y = xy[1] + f.size * .6; d.line((xy[0] - 2, y, xy[0] + w + 2, y), fill=cor, width=3)

# A · ORLA CLARA — areia, verde-garrafa, um fio de ouro, muito respiro
def A():
    b = cena('id-a.png'); d = ImageDraw.Draw(b); logo(b, y=56, largura=190, x=64)
    espaco(d, (W - 64, 92), 'SÁBADO · 20H', F('SemiBold', 26), VERDE, 5, 'l') if False else espaco(d, (760, 92), 'SÁBADO · 20H', F('SemiBold', 26), VERDE, 5)
    d.text((64, 230), 'iPhone 17', font=F('Light', 118), fill=VERDE); d.text((64, 350), 'Pro Max', font=F('Bold', 118), fill=VERDE)
    d.line((64, 500, 200, 500), fill=OURO, width=3)
    d.text((64, 525), '256 GB · prateado', font=F('Medium', 34), fill=(70, 95, 80))
    produto(b, 540, 1010, 490, 90)
    c = Image.new('RGBA', (W, H)); cd = ImageDraw.Draw(c); cd.rounded_rectangle((600, 1060, 1016, 1286), 28, fill=AREIA + (245,), outline=OURO + (255,), width=2); b.alpha_composite(c)
    d = ImageDraw.Draw(b); espaco(d, (636, 1088), 'LANCE INICIAL', F('SemiBold', 24), (110, 120, 110), 4)
    d.text((632, 1118), 'R$ 197', font=F('Black', 96), fill=VERDE)
    riscado(d, (636, 1236), 'na loja R$ 9.464,78', F('Medium', 28), (130, 130, 125))
    salvar(b, f'{OUT}/A-orla-clara.jpg')

# B · PÔR DO SOL — Dois Irmãos ao fundo, branco + ouro, cartão de vidro escuro
def B():
    b = cena('id-b.png'); d = ImageDraw.Draw(b)
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for y in range(0, 420): gd.line((0, y, W, y), fill=(20, 18, 30, int(150 * (1 - y / 420))))
    b.alpha_composite(g); logo(b, y=56, largura=190, x=W // 2 - 95); d = ImageDraw.Draw(b)
    espaco(d, (W / 2, 220), 'O MARTELO BATE SÁBADO ÀS 20H', F('SemiBold', 26), OURO, 5, 'm')
    d.text((W / 2, 270), 'iPhone 17 Pro Max', font=F('SemiBold', 84), fill=BRANCO, anchor='mt')
    produto(b, 540, 1000, 560, 150)
    c = Image.new('RGBA', (W, H)); ImageDraw.Draw(c).rounded_rectangle((90, 1090, 990, 1280), 36, fill=(10, 20, 16, 175), outline=(255, 255, 255, 90), width=2)
    b.alpha_composite(c.filter(ImageFilter.GaussianBlur(0))); d = ImageDraw.Draw(b)
    espaco(d, (140, 1125), 'LANCE INICIAL', F('SemiBold', 24), (230, 220, 200), 4)
    d.text((136, 1155), 'R$ 197', font=F('Black', 92), fill=OURO)
    d.text((940, 1150), 'na loja', font=F('Medium', 28), fill=(220, 220, 220), anchor='ra')
    w = d.textlength('R$ 9.464,78', font=F('SemiBold', 40)); d.text((940, 1188), 'R$ 9.464,78', font=F('SemiBold', 40), fill=(220, 220, 220), anchor='ra')
    d.line((940 - w, 1212, 940, 1212), fill=(220, 220, 220), width=3)
    salvar(b, f'{OUT}/B-por-do-sol.jpg')

# C · QUIOSQUE — azul do mar, verde da marca, pílulas, alegre mas limpo
def C():
    b = cena('id-c.png'); d = ImageDraw.Draw(b); logo(b, y=56, largura=190, x=64)
    d.rounded_rectangle((64, 230, 470, 290), 30, fill=BRANCO); d.text((267, 260), 'sábado é dia de iPhone', font=F('Bold', 30), fill=VERDE, anchor='mm')
    d.text((64, 320), 'iPhone 17', font=F('Black', 112), fill=BRANCO); d.text((64, 432), 'Pro Max', font=F('Black', 112), fill=BRANCO)
    produto(b, 740, 1070, 470, 120)
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((64, 1090, 520, 1280), 40, fill=(20, 140, 80))
    d.text((100, 1110), 'lance inicial', font=F('Bold', 30), fill=(220, 250, 230))
    d.text((96, 1145), 'R$ 197', font=F('Black', 104), fill=BRANCO)
    d.rounded_rectangle((64, 1000, 470, 1060), 30, fill=(255, 255, 255, 235)); riscado(d, (96, 1012), 'na loja R$ 9.464,78', F('SemiBold', 30), (90, 90, 90))
    salvar(b, f'{OUT}/C-quiosque.jpg')

A(); B(); C(); print('ok')
