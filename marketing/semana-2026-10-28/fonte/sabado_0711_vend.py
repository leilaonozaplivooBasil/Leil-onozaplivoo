# Sábado 07/11 — vendedores + contagem do iPhone: 8 artes, 8 ideias e visuais diferentes (pedido da Natália).
# Sem lance atual (muda o dia todo). Âncoras reais: na loja R$ 9.464,78 · o último saiu por R$ 4.640 (24/10) · lance inicial R$ 197.
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from kit import logo, leiloeiro, sombra, salvar
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-05/sabado-07-11/vendedores'
W, H = 1080, 1920
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE = (27, 122, 72); NEON = (63, 208, 126); FOGO = (243, 91, 18); OURO = (245, 196, 81); NOITE = (10, 20, 16)
FLORESTA = (12, 66, 40); MENTA = (226, 242, 232); AREIA = (246, 239, 226); BRANCO = (255, 255, 255); LIMA = (190, 245, 90)

def cena(n, foco=0.5):
    im = Image.open(f'{I}/{n}').convert('RGB'); e = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * e), round(im.height * e)), Image.LANCZOS); x = int((im.width - W) * foco)
    return im.crop((x, 0, x + W, H)).convert('RGBA')
def chapado(c): return Image.new('RGBA', (W, H), c + (255,))
def iph(alt, ang=0):
    p = Image.open(f'{I}/c-iphone.png').convert('RGBA'); p = p.crop(p.getbbox()); p = p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
    return p.rotate(ang, expand=True, resample=Image.BICUBIC) if ang else p
def pousa(b, p, cx, base, forca=150, brilho=None):
    x, y = int(cx - p.width / 2), int(base - p.height)
    if brilho:
        g = Image.new('RGBA', b.size, brilho + (0,)); m = Image.new('L', b.size, 0); m.paste(p.split()[-1].point(lambda v: 120 if v > 20 else 0), (x, y))
        g.putalpha(m.filter(ImageFilter.GaussianBlur(45))); b.alpha_composite(g)
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((cx - p.width * .42, base - 14, cx + p.width * .42, base + 14), fill=(0, 0, 0, forca))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(12))); b.alpha_composite(p, (x, y))
def sombra_txt(b, xy, txt, f, anchor='mm', alfa=150, r=10):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1] + 6), txt, font=f, fill=(0, 0, 0, alfa), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(r)))
def txt(b, xy, t, f, cor, anchor='mm', somb=True):
    if somb: sombra_txt(b, xy, t, f, anchor)
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor)
def pilula(b, cx, cy, t, f, fundo, cor, padx=40, h=None):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2 * padx; h = h or f.size + 34
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, fill=fundo); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def cta(b, cor=NEON, txtcor=NOITE, y=1745): pilula(b, W / 2, y, 'DÊ SEU LANCE · leilaonozap.net', F('Black', 38), cor, txtcor, h=104)
def topo_logo(b, y=120, larg=230, escuro=False):
    if escuro:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((W / 2 - 150, y - 16, W / 2 + 150, y + 104), 36, fill=(10, 40, 24, 225)); b.alpha_composite(s)
    logo(b, y=y, largura=larg)
def vidro(b, caixa, claro=True, r=34):
    v = b.crop(caixa).filter(ImageFilter.GaussianBlur(18)); v = Image.alpha_composite(v, Image.new('RGBA', v.size, (255, 255, 255, 120) if claro else (6, 30, 18, 150)))
    m = Image.new('L', v.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, v.width - 1, v.height - 1), r, fill=255); b.paste(v, caixa[:2], m)
    ImageDraw.Draw(b).rounded_rectangle(caixa, r, outline=(255, 255, 255, 170), width=2)
def riscado(b, xy, t, f, cor, anchor='mm'):
    d = ImageDraw.Draw(b); d.text(xy, t, font=f, fill=cor, anchor=anchor); bb = d.textbbox(xy, t, font=f, anchor=anchor)
    y = (bb[1] + bb[3]) / 2 + 2; d.line((bb[0] - 4, y, bb[2] + 4, y), fill=FOGO, width=7)

# 1 · 08h — "É HOJE": nascer do sol na praia, iPhone no pedestal de pedra, clima de manhã
def a1():
    b = cena('id-a.png'); topo_logo(b, escuro=True)
    txt(b, (W / 2, 330), 'SÁBADO · 07/11', F('Black', 40), FLORESTA, somb=False)
    txt(b, (W / 2, 470), 'É HOJE', F('Black', 190), FLORESTA, somb=False)
    txt(b, (W / 2, 640), 'o martelo bate às 20h', F('Medium', 64), VERDE, somb=False)
    pousa(b, iph(640), W / 2, 1440, 120)
    vidro(b, (130, 1490, 950, 1650)); d = ImageDraw.Draw(b)
    d.text((W / 2, 1535), 'iPhone 17 Pro Max · 256GB', font=F('Bold', 40), fill=FLORESTA, anchor='mm')
    d.text((W / 2, 1600), 'lance inicial R$ 197', font=F('Black', 44), fill=VERDE, anchor='mm')
    cta(b, VERDE, BRANCO); salvar(b, f'{OUT}/1-08h-e-hoje.jpg')

# 2 · 15h — "FALTAM 5 HORAS": vitrine ouro, número gigante como herói
def a2():
    b = chapado(OURO); d = ImageDraw.Draw(b)
    d.text((W / 2 + 120, 760), '5', font=F('Black', 1100), fill=(228, 176, 58), anchor='mm')
    topo_logo(b, y=110)
    d.text((80, 330), 'FALTAM', font=F('Black', 120), fill=FLORESTA); d.text((80, 455), '5 HORAS', font=F('Black', 120), fill=FLORESTA)
    d.text((80, 600), 'e ainda dá tempo de\nentrar no leilão.', font=F('Medium', 54), fill=FLORESTA, spacing=10)
    d.text((80, 780), 'na loja', font=F('Medium', 44), fill=FLORESTA)
    riscado(b, (80, 860), 'R$ 9.464,78', F('Black', 60), FLORESTA, 'lm')
    pousa(b, iph(700, -8), 740, 1580, 110)
    cta(b, FLORESTA, OURO); salvar(b, f'{OUT}/2-15h-faltam-5-horas.jpg')

# 3 · 17h — "FALTAM 3 HORAS": pódio neon (o visual "anúncio" que ela pediu na quinta)
def a3():
    b = cena('s-verde1.png'); topo_logo(b)
    txt(b, (W / 2, 360), 'FALTAM', F('Black', 120), BRANCO); txt(b, (W / 2, 490), '3 HORAS', F('Black', 160), LIMA)
    txt(b, (W / 2, 610), 'pro martelo bater', F('Medium', 54), MENTA)
    pousa(b, iph(720), W / 2, 1420, 160, brilho=(120, 255, 140))
    vidro(b, (130, 1470, 950, 1640), claro=False); d = ImageDraw.Draw(b)
    d.text((W / 2, 1515), 'O ÚLTIMO SAIU POR', font=F('Bold', 36), fill=MENTA, anchor='mm')
    d.text((W / 2, 1585), 'R$ 4.640', font=F('Black', 84), fill=BRANCO, anchor='mm')
    cta(b); salvar(b, f'{OUT}/3-17h-faltam-3-horas.jpg')

# 4 · 18h — "FALTAM 2 HORAS": o choque de preço (loja x último arremate), fundo areia, tipografia
def a4():
    b = chapado(AREIA); d = ImageDraw.Draw(b); topo_logo(b, y=110)
    pilula(b, W / 2, 320, 'FALTAM 2 HORAS', F('Black', 46), FOGO, BRANCO)
    d.text((W / 2, 440), 'Na loja:', font=F('Medium', 60), fill=FLORESTA, anchor='mm')
    riscado(b, (W / 2, 540), 'R$ 9.464,78', F('Black', 110), (110, 120, 112))
    d.text((W / 2, 680), 'O último saiu por:', font=F('Medium', 60), fill=FLORESTA, anchor='mm')
    d.text((W / 2, 810), 'R$ 4.640', font=F('Black', 190), fill=VERDE, anchor='mm')
    pousa(b, iph(640, 6), W / 2, 1600, 90)
    d = ImageDraw.Draw(b); d.text((W / 2, 1650), 'E esse, vai sair por quanto?', font=F('Bold', 46), fill=FLORESTA, anchor='mm')
    cta(b, VERDE, BRANCO, y=1770); salvar(b, f'{OUT}/4-18h-faltam-2-horas.jpg')

# 5 · 19h — "FALTA 1 HORA": o Leiloeiro com o iPhone, fundo verde da marca, raios de luz
def a5():
    b = chapado(VERDE); d = ImageDraw.Draw(b)
    for k in range(14):
        a0 = math.radians(k * 360 / 14); a1_ = a0 + math.radians(9); cx, cy = W / 2, 1150
        d.polygon([(cx, cy), (cx + 1800 * math.cos(a0), cy + 1800 * math.sin(a0)), (cx + 1800 * math.cos(a1_), cy + 1800 * math.sin(a1_))], fill=(36, 138, 84))
    topo_logo(b)
    txt(b, (W / 2, 370), 'FALTA', F('Black', 130), BRANCO); txt(b, (W / 2, 510), '1 HORA', F('Black', 170), OURO)
    p = leiloeiro('a-apresenta', 900); sombra(p, b, (-60, 1640 - p.height))
    pousa(b, iph(620), 760, 1500, 160, brilho=(255, 230, 150))
    d = ImageDraw.Draw(b); pilula(b, W / 2, 1600, 'martelo às 20h em ponto', F('Bold', 44), FLORESTA, BRANCO)
    cta(b, OURO, NOITE); salvar(b, f'{OUT}/5-19h-falta-1-hora.jpg')

# 6 · 19h30 — "ÚLTIMA CHAMADA": noite + fogo, iPhone inclinado, urgência
def a6():
    b = chapado(NOITE); g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((90, 700, 990, 1600), fill=FOGO + (120,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(140)))
    topo_logo(b)
    txt(b, (W / 2, 360), 'ÚLTIMA', F('Black', 170), BRANCO); txt(b, (W / 2, 530), 'CHAMADA', F('Black', 170), FOGO)
    txt(b, (W / 2, 660), 'fecha às 20h em ponto', F('Medium', 58), (255, 220, 200))
    pousa(b, iph(660, 12), W / 2, 1530, 170, brilho=(255, 140, 60))
    d = ImageDraw.Draw(b); d.text((W / 2, 1590), 'quem der o maior lance leva', font=F('Bold', 48), fill=BRANCO, anchor='mm')
    cta(b, FOGO, BRANCO); salvar(b, f'{OUT}/6-19h30-ultima-chamada.jpg')

# 7 · 19h30 (opção) — "FALTAM 30 MINUTOS": pôr do sol no Dois Irmãos, premium
def a7():
    b = cena('id-b.png'); g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
    for y in range(0, 760): gd.line((0, y, W, y), fill=(20, 16, 30, int(170 * (1 - y / 760))))
    b.alpha_composite(g); topo_logo(b)
    txt(b, (W / 2, 360), 'FALTAM', F('Bold', 90), BRANCO); txt(b, (W / 2, 500), '30 MINUTOS', F('Black', 140), OURO)
    txt(b, (W / 2, 620), 'pro sol se pôr e o martelo bater', F('Medium', 48), (255, 235, 210))
    pousa(b, iph(650), W / 2, 1440, 170)
    vidro(b, (130, 1490, 950, 1640), claro=False); d = ImageDraw.Draw(b)
    d.text((W / 2, 1540), 'iPhone 17 Pro Max', font=F('Bold', 44), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1598), 'na loja R$ 9.464,78', font=F('Medium', 38), fill=(235, 225, 210), anchor='mm')
    cta(b, OURO, NOITE); salvar(b, f'{OUT}/7-19h30-faltam-30-minutos.jpg')

# 8 · 19h50 — "10 MINUTOS": cronômetro digital gigante
def a8():
    b = chapado((4, 14, 10)); d = ImageDraw.Draw(b); topo_logo(b)
    d.ellipse((140, 280, 940, 1080), outline=(30, 60, 44), width=26)
    d.arc((140, 280, 940, 1080), -90, -90 + 60, fill=NEON, width=26)
    txt(b, (W / 2, 640), '10:00', F('Black', 230), BRANCO); txt(b, (W / 2, 800), 'MINUTOS', F('Black', 64), NEON)
    pousa(b, iph(520, -6), W / 2, 1560, 170, brilho=(80, 230, 140))
    d = ImageDraw.Draw(b); d.text((W / 2, 1640), 'é agora ou só no próximo', font=F('Bold', 48), fill=MENTA, anchor='mm')
    cta(b); salvar(b, f'{OUT}/8-19h50-faltam-10-minutos.jpg')

import glob
for f in glob.glob(f'{OUT}/*.jpg'): os.remove(f)
for f in (a1, a2, a3, a4, a5, a6, a7, a8): f()
print('ok')
