# Capa da série JÁ ENCONTROU O DONO · EP. 03 (molde dos EP. 01 e 02): foto, pílula SÉRIE · EP. 03, título branco/ouro com contorno.
import sys
from PIL import Image, ImageDraw, ImageFont
BASE, OUT = sys.argv[1:3]; W, H = 1080, 1920
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf' % p, t)
OURO, VERDE, AMA, NOITE = (245, 196, 81), (27, 122, 72), (255, 214, 10), (10, 20, 16)
im = Image.open(BASE).convert('RGBA'); g = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(g)
for y in range(980, H): d.line((0, y, W, y), fill=(0, 0, 0, int(225 * min(1, (y - 980) / 480))))
im.alpha_composite(g); d = ImageDraw.Draw(im)
def cont(xy, t, f, cor, w=6):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0, 200), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
f = F('ExtraBold', 42); t = 'SÉRIE · EP. 03'; w = d.textlength(t, font=f)
d.rounded_rectangle((W / 2 - w / 2 - 32, 1250, W / 2 + w / 2 + 32, 1326), 38, fill=VERDE); d.text((W / 2, 1288), t, font=f, fill=(255, 255, 255), anchor='mm')
cont((W / 2, 1410), 'JÁ ENCONTROU', F('Black', 116), (255, 255, 255)); cont((W / 2, 1540), 'O DONO', F('Black', 146), OURO)
f = F('Black', 48); t = 'iPHONE 18 PRO MAX'; w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - 34, 1630, W / 2 + w / 2 + 34, 1714), 42, fill=AMA); d.text((W / 2, 1672), t, font=f, fill=NOITE, anchor='mm')
d.text((W / 2, 1770), 'arrematado por R$ 7.750', font=F('Bold', 44), fill=(235, 240, 236), anchor='mm')
lg = Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((260, 95))
p = Image.new('RGBA', (W, H)); ImageDraw.Draw(p).rounded_rectangle((W / 2 - lg.width / 2 - 22, 120 - 14, W / 2 + lg.width / 2 + 22, 120 + lg.height + 14), 28, fill=(10, 20, 16, 170)); im.alpha_composite(p); im.alpha_composite(lg, (int(W / 2 - lg.width / 2), 120))
im.convert('RGB').save(OUT, quality=94); print('ok')
