# Carrossel "Como funciona o leilão" — explicado como para uma criança de 6 anos — no estilo da arte "É HOJE ÀS 20H"
# (fundo escuro verde/preto com holofote e brilhos dourados, títulos brancos e dourados enormes, pílula com borda dourada).
# Dados reais do PS5 Slim Digital (leilão f11f54a6f4a87eb64112ac0f, 10/11 17h20): começou R$ 197, lances 197 → 247 → 400,
# 3 pessoas disputando, fecha sáb 14/11 às 20h. Nunca nome de quem deu lance. Instagram: sem link e sem %.
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
OUT = sys.argv[1]; F0 = os.path.dirname(os.path.abspath(__file__)); MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1350
NOITE, FLOR, VERDE, NEON, OURO, BR, CINZA = (6,16,11), (16,60,36), (27,122,72), (63,208,126), (245,196,81), (255,255,255), (214,222,214)
OURO_A, OURO_B = (255,232,155), (214,152,44)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
PROB = []

def fundo(tipo='texto', escurecer=0.0):
    sc = Image.open(f'{F0}/fundo-{tipo}.jpg').convert('RGB'); e = max(W/sc.width, H/sc.height)
    sc = sc.resize((round(sc.width*e), round(sc.height*e)), Image.LANCZOS); x = (sc.width-W)//2; y = (sc.height-H)//2
    b = sc.crop((x, y, x+W, y+H))
    if escurecer: b = ImageEnhance.Brightness(b).enhance(1-escurecer)
    return b.convert('RGBA')

def _cabe(d, t, f, maxw):
    while d.textlength(t, font=f) > maxw:
        if f.size < 30: PROB.append(f'não cabe: {t}'); break
        f = ImageFont.truetype(f.path, f.size - 2)
    return f

def T(b, xy, t, f, cor, anchor='mm', maxw=W-120, somb=170):
    d = ImageDraw.Draw(b); f = _cabe(d, t, f, maxw)
    if somb:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+8), t, font=f, fill=(0,0,0,somb), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor); return f

def OUROT(b, xy, t, f, anchor='mm', maxw=W-120):
    d = ImageDraw.Draw(b); f = _cabe(d, t, f, maxw)
    m = Image.new('L', b.size); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); bb = m.getbbox()
    g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3]+1):
        k = (y-bb[1])/max(1, bb[3]-bb[1]); gd.line((0, y, W, y), fill=tuple(int(a+(z-a)*k) for a, z in zip(OURO_A, OURO_B))+(255,))
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+10), t, font=f, fill=(0,0,0,180), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(Image.composite(g, Image.new('RGBA', b.size, (0,0,0,0)), m)); return f

def pil(b, cx, cy, t, f, fundo_=FLOR, cor=OURO, borda=OURO, padx=44, h=None):
    d = ImageDraw.Draw(b); f = _cabe(d, t, f, W-160); w = d.textlength(t, font=f); h = h or f.size + 44
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((cx-w/2-padx, cy-h/2+8, cx+w/2+padx, cy+h/2+8), h/2, fill=(0,0,0,140)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle((cx-w/2-padx, cy-h/2, cx+w/2+padx, cy+h/2), h/2, fill=fundo_, outline=borda, width=4 if borda else 0)
    d.text((cx, cy+2), t, font=f, fill=cor, anchor='mm')

def card(b, box, destaque=False):
    c = Image.new('RGBA', b.size); cd = ImageDraw.Draw(c)
    cd.rounded_rectangle(box, 30, fill=(8,34,22,215) if destaque else (6,20,14,200), outline=OURO+((255,) if destaque else (120,)), width=4 if destaque else 2)
    b.alpha_composite(c)

def luz(b, cx, cy, r, alfa=110, cor=(255,215,140)):
    g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((cx-r, cy-r, cx+r, cy+r), fill=cor+(alfa,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r*0.55)))

def poe(b, p, cx, base):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((cx-p.width*0.42, base-22, cx+p.width*0.42, base+16), fill=(0,0,0,170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(p, (int(cx-p.width/2), int(base-p.height)))

def recorte(path, lim=236):
    im = Image.open(path).convert('RGB'); px = im.load(); w, h = im.size
    m = Image.new('L', (w, h), 255); pm = m.load()
    for y in range(h):
        for x in range(w):
            r, g, bb = px[x, y]
            if r > lim and g > lim and bb > lim: pm[x, y] = 0
    m = m.filter(ImageFilter.GaussianBlur(1.0)); im = im.convert('RGBA'); im.putalpha(m); return im.crop(m.getbbox())

def topo(b, n, total, seta=True):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((210, 78)); b.alpha_composite(lg, ((W-lg.width)//2, 46))
    d = ImageDraw.Draw(b)
    for i in range(total):
        x = W/2 - (total-1)*14 + i*28; d.ellipse((x-6, H-58, x+6, H-46), fill=OURO if i == n-1 else (70,90,78))
    if seta: d.text((W-56, H-52), 'arrasta  →', font=F('Bold', 32), fill=OURO, anchor='rm')

ps5 = recorte(f'{F0}/ps5-1.jpg'); caixa = recorte(f'{F0}/ps5-0.jpg')
leil = Image.open(f'{MK}/marca/leiloeiro-aponta-moeda-recorte.png').convert('RGBA')
TOT = 8; S = []
PODIO_TOPO = 0.765   # altura do tampo do pódio no fundo-podio (fração da altura)

# 1 — capa: R$ 197 NÃO é o preço final
b = fundo('podio'); topo(b, 1, TOT)
T(b, (W/2, 230), 'R$ 197', F('Black', 200), BR)
OUROT(b, (W/2, 420), 'NÃO É O', F('Black', 150))
OUROT(b, (W/2, 560), 'PREÇO FINAL', F('Black', 136))
pil(b, W/2, 700, 'ENTENDA O LEILÃO EM 1 MINUTO', F('Black', 40))
p = ps5.copy(); p.thumbnail((420, 300)); base = int(PODIO_TOPO*H) + 8
luz(b, W/2, base - p.height*0.5, 230); poe(b, p, W/2, base)
S.append(b)

# 2 — o que é um leilão
b = fundo('texto'); topo(b, 2, TOT)
T(b, (W/2, 230), 'O QUE É UM', F('Black', 120), BR)
OUROT(b, (W/2, 370), 'LEILÃO?', F('Black', 170))
for i, t in enumerate(['É uma disputa.', 'Várias pessoas querem', 'a mesma coisa.']):
    T(b, (W/2, 530 + i*74), t, F('Bold', 60), BR)
pil(b, W/2, 800, 'QUEM OFERECE MAIS, LEVA', F('Black', 52), fundo_=OURO, cor=NOITE, borda=None, h=110)
l = leil.copy(); l.thumbnail((360, 400)); luz(b, W/2, 1100, 200, 70); b.alpha_composite(l, ((W-l.width)//2, H-l.height-90))
S.append(b)

# 3 — R$ 197 é só o começo
b = fundo('texto'); topo(b, 3, TOT)
T(b, (W/2, 230), 'R$ 197 É SÓ O', F('Black', 110), BR)
OUROT(b, (W/2, 380), 'COMEÇO', F('Black', 190))
for i, (t, c) in enumerate([('É o primeiro lance.', BR), ('Igual à largada de uma corrida:', CINZA), ('ninguém ganha na largada!', BR)]):
    T(b, (W/2, 560 + i*72), t, F('Bold', 56), c)
card(b, (150, 840, W-150, 1080), True)
T(b, (W/2, 895), 'LANCE INICIAL', F('Bold', 40), CINZA, somb=0)
OUROT(b, (W/2, 995), 'R$ 197', F('Black', 120))
S.append(b)

# 4 — o PS5 de verdade
b = fundo('texto'); topo(b, 4, TOT)
T(b, (W/2, 200), 'OLHA O PS5', F('Black', 120), BR)
OUROT(b, (W/2, 330), 'DE VERDADE', F('Black', 130))
pil(b, W/2, 460, '3 PESSOAS DISPUTANDO', F('Black', 40))
lances = [('1º LANCE', 'R$ 197', False), ('2º LANCE', 'R$ 247', False), ('3º LANCE · AGORA', 'R$ 400', True)]
y = 560
for rot, val, dest in lances:
    card(b, (90, y, W-90, y+150), dest); d = ImageDraw.Draw(b)
    d.text((140, y+75), rot, font=F('Black' if dest else 'Bold', 46), fill=BR if dest else CINZA, anchor='lm')
    if dest: OUROT(b, (W-140, y+75), val, F('Black', 84), anchor='rm')
    else: d.text((W-140, y+75), val, font=F('Black', 70), fill=BR, anchor='rm')
    if not dest: d.polygon([(W/2-20, y+160), (W/2+20, y+160), (W/2, y+184)], fill=OURO)
    y += 195
T(b, (W/2, 1200), 'subiu de R$ 197 para R$ 400', F('Bold', 46), OURO)
S.append(b)

# 5 — e agora? (simulação)
b = fundo('texto'); topo(b, 5, TOT)
OUROT(b, (W/2, 230), 'E AGORA?', F('Black', 170))
T(b, (W/2, 400), 'Cada pessoa que entra', F('Bold', 60), BR); T(b, (W/2, 474), 'dá um lance MAIOR.', F('Bold', 60), BR)
pil(b, W/2, 590, 'EXEMPLO · SIMULAÇÃO', F('Black', 38))
y = 680
for t, v, dest in [('Ana dá', 'R$ 450', False), ('Beto dá', 'R$ 500', False), ('Ana volta e dá', 'R$ 550', True)]:
    card(b, (90, y, W-90, y+130), dest); d = ImageDraw.Draw(b)
    d.text((140, y+65), t, font=F('Bold', 50), fill=BR, anchor='lm')
    if dest: OUROT(b, (W-140, y+65), v, F('Black', 74), anchor='rm')
    else: d.text((W-140, y+65), v, font=F('Black', 66), fill=BR, anchor='rm')
    y += 160
T(b, (W/2, 1180), 'o preço vai subindo, subindo…', F('Bold', 46), OURO)
T(b, (W/2, 1240), '(nomes de mentira, só para explicar)', F('Medium', 30), CINZA, somb=0)
S.append(b)

# 6 — quando o tempo acaba
b = fundo('podio'); topo(b, 6, TOT)
T(b, (W/2, 210), 'QUANDO O TEMPO ACABA…', F('Black', 74), BR)
OUROT(b, (W/2, 400), 'TOC!', F('Black', 260))
T(b, (W/2, 590), 'O martelo bate.', F('Black', 70), BR)
T(b, (W/2, 672), 'Quem deu o lance MAIS ALTO, leva.', F('Black', 54), OURO)
pil(b, W/2, 800, 'O PS5 FECHA SÁBADO (14/11) ÀS 20H', F('Black', 40))
c = caixa.copy(); c.thumbnail((380, 250)); base = int(PODIO_TOPO*H) + 8; luz(b, W/2, base - c.height*0.5, 200); poe(b, c, W/2, base)
S.append(b)

# 7 — como dar seu lance
b = fundo('texto'); topo(b, 7, TOT)
T(b, (W/2, 220), 'COMO DAR', F('Black', 120), BR)
OUROT(b, (W/2, 350), 'SEU LANCE', F('Black', 140))
y = 490
for n, a, c in [('1', 'Faça seu cadastro', 'no site do Leilão no Zap'), ('2', 'Entre na sala', 'do produto que você quer'), ('3', 'Toque em DAR LANCE', 'e escolha o seu valor')]:
    card(b, (90, y, W-90, y+170)); d = ImageDraw.Draw(b)
    d.ellipse((125, y+35, 225, y+135), fill=OURO); d.text((175, y+85), n, font=F('Black', 64), fill=NOITE, anchor='mm')
    T(b, (260, y+60), a, F('Black', 54), BR, anchor='lm', maxw=W-380, somb=0); T(b, (260, y+120), c, F('Medium', 38), CINZA, anchor='lm', maxw=W-380, somb=0)
    y += 200
pil(b, W/2, 1170, 'DÁ PARA ACOMPANHAR TUDO AO VIVO', F('Black', 38))
S.append(b)

# 8 — resumão + CTA
b = fundo('texto'); topo(b, 8, TOT, seta=False)
OUROT(b, (W/2, 230), 'RESUMINDO', F('Black', 160))
y = 370
for t in ['Leilão = quem dá mais, leva', 'R$ 197 é só o 1º lance', 'O preço sobe a cada lance', 'O martelo bate na hora marcada']:
    card(b, (90, y, W-90, y+104)); d = ImageDraw.Draw(b); d.ellipse((128, y+34, 164, y+70), fill=OURO)
    T(b, (190, y+52), t, F('Bold', 50), BR, anchor='lm', maxw=W-300, somb=0); y += 124
T(b, (W/2, y+40), 'Às vezes sai bem abaixo do preço da loja.', F('Medium', 38), CINZA, somb=0)
T(b, (W/2, y+90), 'Às vezes não: depende de quantas pessoas disputam.', F('Medium', 38), CINZA, somb=0)
pil(b, W/2, 1170, 'FICOU DÚVIDA? COMENTA LEILÃO', F('Black', 50), fundo_=OURO, cor=NOITE, borda=None, h=120)
S.append(b)

os.makedirs(OUT, exist_ok=True)
for i, s in enumerate(S, 1): s.convert('RGB').save(f'{OUT}/SLIDE-{i:02d}.jpg', quality=94)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', len(S))
