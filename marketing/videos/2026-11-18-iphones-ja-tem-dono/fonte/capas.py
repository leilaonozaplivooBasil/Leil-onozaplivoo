# 3 opções de capa para o vídeo "Esses dois iPhones já têm dono" (18/11)
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'; W, H = 1080, 1920
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
VERDE, OURO, AMA, NOITE, BR, VERM = (27, 122, 72), (245, 196, 81), (255, 214, 10), (10, 20, 16), (255, 255, 255), (222, 30, 38)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((260, 100))
def base(f):
    im = Image.open(f'{S}/{f}').convert('RGBA'); g = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(g)
    for y in range(1000, H): d.line((0, y, W, y), fill=(0, 0, 0, int(225 * min(1, (y - 1000) / 520))))
    im.alpha_composite(g); p = Image.new('RGBA', (W, H)); ImageDraw.Draw(p).rounded_rectangle((W / 2 - LOGO.width / 2 - 20, 110, W / 2 + LOGO.width / 2 + 20, 130 + LOGO.height), 26, fill=(10, 20, 16, 170))
    im.alpha_composite(p); im.alpha_composite(LOGO, (int(W / 2 - LOGO.width / 2), 120)); return im
def cont(d, xy, t, f, cor, w=7):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
def pilula(d, cx, cy, t, f, fundo, cor):
    w = d.textlength(t, font=f); d.rounded_rectangle((cx - w / 2 - 30, cy - f.size * .75, cx + w / 2 + 30, cy + f.size * .75), f.size * .75, fill=fundo); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
# 1 · JÁ TÊM DONO + os dois preços
im = base('f4.3.png'); d = ImageDraw.Draw(im)
cont(d, (W / 2, 1390), 'ESSES 2 IPHONES', F('Black', 96), BR); cont(d, (W / 2, 1530), 'JÁ TÊM DONO', F('Black', 150), AMA)
pilula(d, W / 2 - 230, 1690, 'R$ 6.370', F('Black', 64), BR, NOITE); pilula(d, W / 2 + 230, 1690, 'R$ 7.750', F('Black', 64), BR, NOITE)
im.convert('RGB').save(f'{OUT}/CAPA-1-ja-tem-dono-precos.jpg', quality=94)
# 2 · série JÁ ENCONTROU O DONO · EP. 03
im = base('f5.5.png'); d = ImageDraw.Draw(im)
pilula(d, W / 2, 1280, 'SÉRIE · EP. 03', F('ExtraBold', 44), VERDE, BR)
cont(d, (W / 2, 1420), 'JÁ ENCONTROU', F('Black', 120), BR); cont(d, (W / 2, 1560), 'O DONO', F('Black', 150), OURO)
d.text((W / 2, 1690), 'iPhone 17 Pro Max · iPhone 18 Pro Max', font=F('Bold', 44), fill=(235, 240, 236), anchor='mm')
im.convert('RGB').save(f'{OUT}/CAPA-2-serie-ep03.jpg', quality=94)
# 3 · "É VERDADE?" com carimbo ENTREGUE
im = base('f38.5.png'); d = ImageDraw.Draw(im)
cont(d, (W / 2, 1420), 'É VERDADE?', AN(190), BR, 8); cont(d, (W / 2, 1600), 'TÁ AQUI NA MINHA MÃO', F('Black', 70), AMA)
c = Image.new('RGBA', (620, 210)); k = ImageDraw.Draw(c); k.rounded_rectangle((8, 8, 612, 202), 26, outline=VERM + (240,), width=14); k.text((310, 108), 'ENTREGUE ✓'.replace(' ✓', ''), font=F('Black', 120), fill=VERM + (240,), anchor='mm')
c = c.rotate(-10, resample=Image.BICUBIC, expand=True); im.alpha_composite(c, (int(W / 2 - c.width / 2 + 40), 830))
im.convert('RGB').save(f'{OUT}/CAPA-3-e-verdade-entregue.jpg', quality=94)
print('ok')
