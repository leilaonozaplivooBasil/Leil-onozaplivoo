# FALTAM N MINUTOS em VERDE da marca + DOURADO (sem vermelho), com o site embaixo. Uso: faltam_verde.py <lance> <min> <pessoas>
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
LANCE, N, PES = sys.argv[1:4]; MK = '/home/user/Leil-onozaplivoo/marketing'; OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-16/quarta-18-11-macbook/visual'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
W, H = 1080, 1920; BR, OURO, OCL, OESC, NOITE, NEON = (255, 255, 255), (245, 196, 81), (252, 232, 175), (165, 115, 40), (6, 26, 16), (63, 208, 126)
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 700) * .85) / 1150, 0, 1) ** 1.2
a = np.array((24, 110, 66))[None, None] * (1 - dd[..., None]) + np.array(NOITE)[None, None] * dd[..., None]
b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); d = ImageDraw.Draw(b); cx, cy = W / 2, 660
for k in range(28):
    an = k / 28 * 2 * math.pi; r1, r2 = 330, 900
    d.polygon([(cx + r1 * math.cos(an - .045), cy + r1 * math.sin(an - .045)), (cx + r2 * math.cos(an), cy + r2 * math.sin(an)), (cx + r1 * math.cos(an + .045), cy + r1 * math.sin(an + .045))], fill=OURO + (45,))
g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx - 380, cy - 380, cx + 380, cy + 380), fill=OURO + (110,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(110)))
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((200, 200)); x0 = (W - lg.width) // 2
d = ImageDraw.Draw(b); d.rounded_rectangle((x0 - 22, 66, x0 + lg.width + 22, 94 + lg.height), 26, fill=(6, 26, 16, 235)); b.alpha_composite(lg, (x0, 80))
d.rounded_rectangle((W / 2 - 150, 250, W / 2 + 150, 330), 40, fill=OURO); d.text((W / 2, 291), 'FALTAM', font=F('Black', 48), fill=NOITE, anchor='mm')
# número em ouro degradê
m = Image.new('L', (W, H)); ImageDraw.Draw(m).text((cx, cy), N, font=AN(440), fill=255, anchor='mm'); bb = m.getbbox()
gr = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(gr)
for yy in range(bb[1], bb[3] + 1):
    k = min(1, abs((yy - bb[1]) / (bb[3] - bb[1]) - .35) * 1.6); gd.line((0, yy, W, yy), fill=tuple(int(p + (q - p) * k) for p, q in zip(OCL, OESC)) + (255,))
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(m.point(lambda v: int(v * .6)).transform((W, H), Image.AFFINE, (1, 0, -10, 0, 1, -14))); b.alpha_composite(sh)
b.alpha_composite(Image.composite(gr, Image.new('RGBA', (W, H)), m)); d = ImageDraw.Draw(b)
def cont(xy, t, f, cor, w=6):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
cont((cx, cy + 300), 'MINUTOS', AN(140), BR)
cont((W / 2, 1150), 'O MARTELO VAI BATER!', F('Black', 76), BR)
d.text((W / 2, 1245), f'{PES} pessoas na disputa · quem deu lance pode cobrir', font=F('SemiBold', 40), fill=(215, 240, 225), anchor='mm')
d.rounded_rectangle((150, 1320, W - 150, 1520), 34, fill=(0, 0, 0, 200), outline=OURO, width=4)
d.text((W / 2, 1368), 'LANCE ATUAL', font=F('Bold', 34), fill=OURO, anchor='mm'); d.text((W / 2, 1452), f'R$ {real(LANCE)}', font=F('Black', 110), fill=BR, anchor='mm')
mac = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA'); mac = mac.crop(mac.getbbox()); mac = mac.resize((400, int(mac.height * 400 / mac.width)), Image.LANCZOS)
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 185, 1795, W / 2 + 185, 1825), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
b.alpha_composite(mac, (int(W / 2 - 200), 1805 - mac.height)); d = ImageDraw.Draw(b)
d.rounded_rectangle((150, 1840, 930, 1900), 30, fill=NEON); d.text((540, 1871), 'leilaonozap.net', font=F('Black', 40), fill=NOITE, anchor='mm')
b.convert('RGB').save(f'{OUT}/V11-faltam-{N}-minutos-VERDE.jpg', quality=94); print('ok')
