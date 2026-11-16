# MacBook Neo (qua 18/11, 20h) — estilo "elite" das artes do PS5: verde-escuro profundo, facho de luz dourada,
# produto real com reflexo no chão, nome e lance em dourado. Sem link e sem %. Uso: artes_macbook_elite.py <lance>
import os, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
OURO, OCLARO, OESC = (212, 175, 106), (246, 226, 178), (150, 112, 52); CREME = (236, 232, 220); CINZA = (170, 186, 176)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W = H = 0

def fundo(cy):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - cy) * 0.85) / (W * 1.05), 0, 1) ** 1.4
    a = np.array((12, 40, 27))[None, None] * (1 - d[..., None]) + np.array((3, 9, 6))[None, None] * d[..., None]
    a += np.random.default_rng(3).normal(0, 2.2, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def brilho(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def facho(b, x, y0, y1, larg):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).polygon([(x - 60, y0), (x + 60, y0), (x + larg, y1), (x - larg, y1)], fill=OCLARO + (34,))
    b.alpha_composite(g.filter(ImageFilter.GaussianBlur(50)))
def ouro_txt(b, xy, t, f, anchor='mm', glow=0.35):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); bb = m.getbbox()
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        k = abs((y - bb[1]) / max(1, bb[3] - bb[1]) - 0.38) * 1.6
        gd.line((0, y, W, y), fill=tuple(int(a + (z - a) * min(1, k)) for a, z in zip(OCLARO, OESC)) + (255,))
    if glow:
        gl = Image.new('RGBA', (W, H), OURO + (0,)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * glow))); b.alpha_composite(gl)
    b.alpha_composite(Image.composite(g, Image.new('RGBA', (W, H), (0, 0, 0, 0)), m)); return bb
def texto(b, xy, t, f, cor, anchor='mm'): ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor)
def espac(t, n=1): return (' ' * n).join(t)
def linha_ouro(b, x0, x1, y, a=200):
    l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l)
    for x in range(int(x0), int(x1)):
        k = 1 - abs((x - (x0 + x1) / 2) / ((x1 - x0) / 2)); d.point((x, y), fill=OURO + (int(a * k ** 0.6),)); d.point((x, y + 1), fill=OURO + (int(a * .5 * k ** 0.6),))
    b.alpha_composite(l)
def poeira(b, n=70, seed=5):
    random.seed(seed); p = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(p)
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H * .8), random.choice([1, 1, 1.5, 2]); d.ellipse((x - r, y - r, x + r, y + r), fill=OCLARO + (random.randint(40, 140),))
    b.alpha_composite(p.filter(ImageFilter.GaussianBlur(.6)))
def logo(b, y, larg=190):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((larg, 80)); b.alpha_composite(lg, ((W - lg.width) // 2, y))
def macbook(larg):
    # foto oficial do site: o aberto fica na frente do fechado; a base é simétrica, então o lado direito dela é o espelho do esquerdo
    a = np.asarray(Image.open(f'{AQ}/fotos/macbook-neo-foto-c.webp').convert('RGB')).copy(); cx = 453
    a[712:830, cx:cx + 440] = a[712:830, cx - 440:cx][:, ::-1]
    a = a[235:830, 12:890]; f = a.astype(float)
    al = Image.fromarray((np.clip((238 - f.min(axis=2)) / 16, 0, 1) * 255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    from PIL import ImageEnhance
    p = ImageEnhance.Brightness(Image.fromarray(a)).enhance(0.88).convert('RGBA'); p.putalpha(al.filter(ImageFilter.MinFilter(3))); p = p.crop(al.getbbox()); return p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)
def poe(b, p, x, base, refl=0.22):
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((x - p.width * .52, base - 16, x + p.width * .52, base + 18), fill=(0, 0, 0, 210)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(20)))
    r = p.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, p.width, int(p.height * .3)))
    gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255 - v) * refl)); r.putalpha(ImageChops.multiply(r.split()[3], gm))
    b.alpha_composite(r, (int(x - p.width / 2), int(base + 2))); b.alpha_composite(p, (int(x - p.width / 2), int(base - p.height)))

def arte(w, h, nome, y):
    global W, H; W, H = w, h
    b = fundo(y['prod'] - 120); facho(b, W / 2, 0, y['prod'], 430)
    brilho(b, (W / 2 - 420, y['prod'] - 470, W / 2 + 420, y['prod'] + 60), (150, 110, 210), 70, 120)   # luz da tela
    brilho(b, (W / 2 - 520, y['prod'] - 120, W / 2 + 520, y['prod'] + 120), OURO, 60, 90)               # brilho dourado no chão
    poeira(b); logo(b, y['logo'])
    texto(b, (W / 2, y['kicker']), espac('LEILÃO DE QUARTA · 20H'), F('Medium', 30), OURO + (255,))
    ouro_txt(b, (W / 2, y['nome']), 'MacBook Neo', F('Bold', y['tam_nome']))
    texto(b, (W / 2, y['sub']), '13 polegadas  ·  chip A18 Pro  ·  256GB', F('Regular', 34), CREME + (230,))
    p = macbook(y['larg']); poe(b, p, W / 2, y['prod'])
    texto(b, (W / 2, y['rotulo']), espac('LANCE ATUAL'), F('Medium', 32), CINZA + (255,))
    fR = F('Light', y['tam_lance'] // 3); fN = F('Bold', y['tam_lance'])
    d = ImageDraw.Draw(b); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
    ouro_txt(b, (x0, y['lance']), 'R$', fR, anchor='ls', glow=0); ouro_txt(b, (x0 + wr, y['lance']), LANCE, fN, anchor='ls', glow=.4)
    linha_ouro(b, W / 2 - 260, W / 2 + 260, y['linha'])
    texto(b, (W / 2, y['data']), 'quarta-feira, 18/11, às 20h', F('Medium', 40), CREME + (255,))
    b.convert('RGB').save(f'{OUT}/{nome}', quality=94); print('ok', nome)

arte(1080, 1920, 'arte-macbook-story.jpg', dict(logo=140, kicker=330, nome=455, tam_nome=150, sub=575, larg=860, prod=1180,
     rotulo=1330, lance=1590, tam_lance=250, linha=1680, data=1745))
arte(1080, 1350, 'arte-macbook-feed.jpg', dict(logo=60, kicker=190, nome=290, tam_nome=124, sub=385, larg=700, prod=880,
     rotulo=965, lance=1170, tam_lance=200, linha=1215, data=1270))
