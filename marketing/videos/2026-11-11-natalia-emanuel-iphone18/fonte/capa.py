# Capa do reel Natália + Emanuel (take 20): "NINGUÉM DEU LANCE AINDA!" — texto em cima (dentro do recorte 4:5 do perfil), os dois embaixo.
import sys
from PIL import Image, ImageDraw, ImageFont
q, out = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1920; OURO, NOITE, BR, VERDE, FOGO = (245,196,81), (10,20,16), (255,255,255), (27,122,72), (243,91,18)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
im = Image.open(q).convert('RGB').resize((W, H)).convert('RGBA')
g = Image.new('L', (1, H)); [g.putpixel((0, y), int(225 if y < 560 else 225*max(0, 1-(y-560)/330)**1.1)) for y in range(H)]
s = Image.new('RGBA', (W, H), NOITE+(0,)); s.putalpha(g.resize((W, H))); im.alpha_composite(s)
d = ImageDraw.Draw(im)
def pil(t, y, f, fundo, cor, r):
    w = d.textlength(t, font=f); d.rounded_rectangle((W/2-w/2-r, y-r+4, W/2+w/2+r, y+r+4), r, fill=fundo); d.text((W/2, y+4), t, font=f, fill=cor, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((240, 90)); im.alpha_composite(lg, ((W-lg.width)//2, 120))
pil('IPHONE 18 PRO MAX · HOJE 20H', 300, F('Black', 40), FOGO, BR, 36)
for f, t, y, cor in ((F('Black', 118), 'NINGUÉM DEU', 420, BR), (F('Black', 132), 'LANCE AINDA!', 543, OURO)):
    while d.textlength(t, font=f) > W-70: f = ImageFont.truetype(f.path, f.size-4)
    d.text((W/2+5, y+7), t, font=f, fill=(0,0,0), anchor='mm'); d.text((W/2, y), t, font=f, fill=cor, anchor='mm')
pil('o primeiro pode ser o seu 👀'.replace(' 👀', '…'), 650, F('Bold', 44), VERDE, BR, 40)
im.convert('RGB').save(out, quality=93); print('ok')
