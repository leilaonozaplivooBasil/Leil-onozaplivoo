# Capa do reel no PADRÃO aprovado pela Natália (a capa dela com o Emanuel, 07/11): texto em cima com fundo verde-escuro,
# logo, selo laranja, título branco + dourado, linha do produto e o iPhone real à direita; a pessoa embaixo, livre.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
QUADRO, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
IPH = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-09/quarta-11-11-iphone18/fonte/fotos/c-bordo.png'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920; OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); PROB = []
fr = Image.open(QUADRO).convert('RGB').resize((W, H))
ESCALA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85   # o quadro INTEIRO, um pouco menor e preso embaixo: nada é cortado
fundo = fr.resize((round(W*1.2), round(H*1.2))).crop((round(W*0.1), round(H*0.1), round(W*1.1), round(H*1.1))).filter(ImageFilter.GaussianBlur(30))
im = fundo.copy(); pw, ph = round(W*ESCALA), round(H*ESCALA)
pq = fr.resize((pw, ph), Image.LANCZOS); m = Image.new('L', (pw, ph), 0); md = ImageDraw.Draw(m); md.rectangle((30, 30, pw-30, ph+40), fill=255)
m = m.filter(ImageFilter.GaussianBlur(22)); im.paste(pq, ((W-pw)//2, H-ph), m)
im = im.convert('RGBA'); g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
for y in range(0, 1000):
    a = 240 if y < 800 else int(240 * max(0, (1000 - y) / 200)); gd.line([(0, y), (W, y)], fill=(8, 30, 20, a))
im = Image.alpha_composite(im, g); d = ImageDraw.Draw(im)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((250, 94)); im.alpha_composite(lg, (56, 268))
ip = Image.open(IPH).convert('RGBA'); ip = ip.crop(ip.getbbox()); ip.thumbnail((330, 420), Image.LANCZOS)
sx, sy = W - ip.width - 50, 290
glow = Image.new('RGBA', (W, H)); ImageDraw.Draw(glow).ellipse((sx-50, sy+40, sx+ip.width+50, sy+ip.height+30), fill=OURO+(110,))
im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(55))); im.alpha_composite(ip, (sx, sy)); d = ImageDraw.Draw(im)
LIM = sx - 14
def txt(xy, t, f, cor):
    bb = d.textbbox(xy, t, font=f, anchor='ls')
    if bb[2] > LIM or bb[1] < 240: PROB.append(f'"{t}" fora {bb}')
    d.text(xy, t, font=f, fill=cor, anchor='ls'); return bb
f = F('Black', 34); t = 'LEILÃO AO VIVO'; w = d.textlength(t, font=f)
d.rounded_rectangle((60, 392, 60+w+70, 450), 29, fill=FOGO); d.ellipse((80, 411, 100, 431), fill=BR); d.text((112, 421), t, font=f, fill=BR, anchor='lm')
txt((54, 566), 'QUARTA', F('Black', 128), BR)
b = txt((54, 690), 'ÀS 20H', F('Black', 128), OURO)
b2 = txt((60, 748), 'iPhone 18 Pro Max · lacrado', F('Bold', 40), BR)
im.convert('RGB').save(f'{OUT}/CAPA-reel-iphone18-quarta.jpg', quality=93)
im.convert('RGB').crop((0, 240, 1080, 1680)).resize((540, 720)).save(f'{OUT}/fonte/previa-capa-grid.jpg')
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok; texto até', b2[3])
