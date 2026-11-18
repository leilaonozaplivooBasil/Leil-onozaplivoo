# Capa do Reels "Ribeiro no galpão" (18/11): os dois com a cafeteira no galpão + TOUR NO GALPÃO + selo TÁ NA LOJA
import sys
from PIL import Image, ImageDraw, ImageFont
BASE, OUT = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; W, H = 1080, 1920
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
BR, OURO, NOITE, VERDE = (255, 255, 255), (245, 196, 81), (10, 20, 16), (46, 196, 110)
im = Image.open(BASE).convert('RGBA'); g = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(g)
for y in range(980, H): d.line((0, y, W, y), fill=(0, 0, 0, int(230 * min(1, (y - 980) / 480))))
im.alpha_composite(g); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((260, 100))
p = Image.new('RGBA', (W, H)); ImageDraw.Draw(p).rounded_rectangle((W / 2 - lg.width / 2 - 20, 110, W / 2 + lg.width / 2 + 20, 130 + lg.height), 26, fill=(10, 20, 16, 170)); im.alpha_composite(p); im.alpha_composite(lg, (int(W / 2 - lg.width / 2), 120))
d = ImageDraw.Draw(im)
def cont(xy, t, f, cor, w=7):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
cont((W / 2, 1300), 'TOUR NO', AN(160), BR); cont((W / 2, 1505), 'GALPÃO', AN(196), OURO)
d.text((W / 2, 1640), 'tudo que tá no site tá aqui', font=F('Bold', 50), fill=BR, anchor='mm')
f = F('Black', 52); t = 'TÁ NA LOJA'; w = d.textlength(t, font=f); larg = 76 + 18 + w + 44; x1 = W / 2 - larg / 2; y1 = 1710
d.rounded_rectangle((x1, y1, x1 + larg, y1 + 92), 46, fill=VERDE); d.ellipse((x1 + 12, y1 + 12, x1 + 80, y1 + 80), fill=BR)
d.line([(x1 + 29, y1 + 47), (x1 + 42, y1 + 61), (x1 + 64, y1 + 32)], fill=VERDE, width=9); d.text((x1 + 80 + 18, y1 + 47), t, font=f, fill=NOITE, anchor='lm')
im.convert('RGB').save(OUT, quality=94); print('ok')
