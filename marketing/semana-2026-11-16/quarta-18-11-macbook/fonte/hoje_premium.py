# Arte "É HOJE · 20h" do MacBook em versão premium (18/11): dourado em degradê, MacBook herói com brilho e reflexo,
# comparação de preço (Apple oficial R$ 8.499 · Mercado Livre a partir de R$ 6.099 · lance atual), regra do 1º lance até 19h.
# Sem %. Uso: hoje_premium.py <lance>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
OURO, OCLARO, OESC, BR, CREME, ESC, VERM = (212, 175, 106), (246, 226, 178), (150, 112, 52), (247, 245, 238), (205, 222, 210), (4, 18, 11), (200, 28, 34)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')

def fundo():
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - 980) * .9) / 1150, 0, 1) ** 1.3
    a = np.array((14, 52, 34))[None, None] * (1 - d[..., None]) + np.array((2, 10, 6))[None, None] * d[..., None]
    a += np.random.default_rng(5).normal(0, 2, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def ouro(b, xy, t, f, anchor='mm', glow=.35):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); bb = m.getbbox()
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        k = abs((y - bb[1]) / max(1, bb[3] - bb[1]) - .38) * 1.6; gd.line((0, y, W, y), fill=tuple(int(a + (z - a) * min(1, k)) for a, z in zip(OCLARO, OESC)) + (255,))
    if glow:
        gl = Image.new('RGBA', (W, H), OURO + (0,)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * glow))); b.alpha_composite(gl)
    b.alpha_composite(Image.composite(g, Image.new('RGBA', (W, H)), m))
def linha_ouro(b, x0, x1, y, a=220):
    l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l)
    for x in range(int(x0), int(x1)):
        k = 1 - abs((x - (x0 + x1) / 2) / ((x1 - x0) / 2)); d.point((x, y), fill=OURO + (int(a * k ** .6),)); d.point((x, y + 1), fill=OURO + (int(a * .5 * k ** .6),))
    b.alpha_composite(l)
def brilho(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def espac(t): return ' '.join(t)

b = fundo()
# facho de luz dourada de cima
cone = Image.new('RGBA', (W, H)); ImageDraw.Draw(cone).polygon([(W / 2 - 60, -20), (W / 2 + 60, -20), (W / 2 + 420, 1260), (W / 2 - 420, 1260)], fill=OCLARO + (30,)); b.alpha_composite(cone.filter(ImageFilter.GaussianBlur(50)))
lg = LOGO.copy(); lg.thumbnail((190, 190)); b.alpha_composite(lg, ((W - lg.width) // 2, 80)); d = ImageDraw.Draw(b)
d.text((W / 2, 250), espac('QUARTA É DIA DE LEILÃO'), font=F('Medium', 32), fill=OCLARO, anchor='mm'); linha_ouro(b, W / 2 - 80, W / 2 + 80, 285)
d.text((W / 2 + 4, 420 + 8), 'É HOJE', font=F('Black', 230), fill=(0, 0, 0, 160), anchor='mm'); d.text((W / 2, 420), 'É HOJE', font=F('Black', 230), fill=BR, anchor='mm')
ouro(b, (W / 2, 575), 'às 20h', F('Bold', 120), glow=.4)
# MacBook herói
mw = 760; mm = MAC.resize((mw, int(MAC.height * mw / MAC.width)), Image.LANCZOS); base = 1175
brilho(b, (W / 2 - 520, base - 420, W / 2 + 520, base + 40), (120, 90, 220), 70, 120); brilho(b, (W / 2 - 560, base - 70, W / 2 + 560, base + 70), OURO, 90, 60)
r = mm.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, mw, int(mm.height * .18))); gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255 - v) * .22))
r.putalpha(ImageChops.multiply(r.split()[3], gm)); b.alpha_composite(r, ((W - mw) // 2, base + 4)); b.alpha_composite(mm, ((W - mw) // 2, base - mm.height))
linha_ouro(b, 110, W - 110, base + 6, 170); d = ImageDraw.Draw(b)
ouro(b, (W / 2, 1245), 'MacBook Neo 13"', F('Bold', 64), glow=.2)
d.text((W / 2, 1310), 'Prateado  ·  Chip A18 Pro  ·  256GB  ·  novo e lacrado', font=F('Regular', 32), fill=CREME, anchor='mm')
# comparação de preço
y0 = 1380; d.rounded_rectangle((70, y0, W - 70, y0 + 330), 30, fill=(4, 20, 12, 235), outline=OURO, width=2)
for i, (rot, val) in enumerate((('na Apple', 'R$ 8.499'), ('no Mercado Livre', 'a partir de R$ 6.099'))):
    cx = 70 + (W - 140) * (.27 + i * .46); d.text((cx, y0 + 50), rot, font=F('Medium', 30), fill=(170, 190, 178), anchor='mm')
    d.text((cx, y0 + 98), val, font=F('Bold', 40 if i == 0 else 34), fill=BR, anchor='mm')
linha_ouro(b, 130, W - 130, y0 + 145, 160)
d.text((W / 2, y0 + 185), espac('NO LEILÃO, O LANCE ESTÁ EM'), font=F('SemiBold', 28), fill=OCLARO, anchor='mm')
fR, fN = F('Medium', 54), F('Black', 120); wr = d.textlength('R$ ', font=fR); wn = d.textlength(real(LANCE), font=fN); x0 = (W - wr - wn) / 2
ouro(b, (x0, y0 + 305), 'R$', fR, anchor='ls', glow=0); ouro(b, (x0 + wr, y0 + 305), real(LANCE), fN, anchor='ls', glow=.35)
# regra
d = ImageDraw.Draw(b); d.rounded_rectangle((70, 1745, W - 70, 1845), 26, fill=VERM)
d.text((W / 2, 1782), '1º LANCE SÓ ATÉ AS 19H', font=F('Black', 46), fill=BR, anchor='mm'); d.text((W / 2, 1825), 'depois disso, fica de fora', font=F('SemiBold', 28), fill=(255, 225, 225), anchor='mm')
b.convert('RGB').save(f'{OUT}/MAC-1-10h-e-hoje-PREMIUM.jpg', quality=95); print('ok')
