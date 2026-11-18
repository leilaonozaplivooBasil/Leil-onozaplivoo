# Capa da série "JÁ ENCONTROU O DONO" · EP. 02 (vídeo de prova social de 11/11), no mesmo molde da capa do EP. 01:
# foto do cliente do notebook Dell no alto, 4 entregas em miniatura, pílula SÉRIE · EP. 02, título branco/ouro com contorno.
# Os quadros saem do próprio vídeo (sem print com nome de cliente). Uso: capa_ep02.py <pasta-dos-quadros>
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
S = sys.argv[1]; D = '/home/user/Leil-onozaplivoo/marketing/videos/2026-11-11-prova-social'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf' % p, t)
W, H = 1080, 1920; OURO = (245, 196, 81); VERDE = (27, 122, 72)
guy = Image.open(f'{S}/f21.0.png').convert('RGB').crop((6, 504, 1034, 1400))           # foto do notebook Dell, sem o rótulo
bg = ImageOps.fit(guy, (W // 4, H // 4)).filter(ImageFilter.GaussianBlur(8)).resize((W, H)); bg = Image.blend(bg, Image.new('RGB', (W, H), (10, 20, 16)), .35).convert('RGBA')
top = ImageOps.fit(guy, (W, 1180), centering=(0.42, 0.5)).convert('RGBA')
m = np.ones((1180, W), 'float32'); m[900:] = np.linspace(1, 0, 280)[:, None]; top.putalpha(Image.fromarray((m * 255).astype('uint8')))
im = bg.copy(); im.alpha_composite(top, (0, 0))
g = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(g)
for y in range(860, H): d.line((0, y, W, y), fill=(0, 0, 0, int(215 * min(1, (y - 860) / 520))))
im.alpha_composite(g); d = ImageDraw.Draw(im)
def cont(xy, t, f, cor, w=6):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0, 200), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
th = []
for nome, box in (('f6.0', (230, 560, 830, 1160)), ('f11.0', (260, 640, 860, 1240)), ('f13.6', (180, 420, 900, 1140)), ('f18.5', (90, 560, 990, 1160))):
    t = ImageOps.fit(Image.open(f'{S}/{nome}.png').convert('RGB').crop(box), (190, 190))
    mk = Image.new('L', (190, 190), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, 189, 189), 36, fill=255)
    c = Image.new('RGBA', (202, 202), (255, 255, 255, 255)); mm = Image.new('L', (202, 202), 0); ImageDraw.Draw(mm).rounded_rectangle((0, 0, 201, 201), 40, fill=255); c.putalpha(mm)
    c.paste(t, (6, 6), mk); th.append(c)
x0 = (W - (4 * 202 + 3 * 22)) // 2
for i, c in enumerate(th): im.alpha_composite(c, (x0 + i * 224, 1010))
d = ImageDraw.Draw(im)
f = F('ExtraBold', 42); t = 'SÉRIE · EP. 02'; w = d.textlength(t, font=f)
d.rounded_rectangle((W / 2 - w / 2 - 32, 1250, W / 2 + w / 2 + 32, 1326), 38, fill=VERDE + (255,)); d.text((W / 2, 1288), t, font=f, fill=(255, 255, 255), anchor='mm')
cont((W / 2, 1410), 'JÁ ENCONTROU', F('Black', 116), (255, 255, 255, 255))
cont((W / 2, 1540), 'O DONO', F('Black', 146), OURO + (255,))
f = F('Bold', 44); t = 'notebook, PS5, iPhone, TV…'; d.text((W / 2, 1660), t, font=f, fill=(235, 240, 236), anchor='mm')
lg = Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((260, 95))
pill = Image.new('RGBA', (W, H)); ImageDraw.Draw(pill).rounded_rectangle((W / 2 - lg.width / 2 - 22, 120 - 14, W / 2 + lg.width / 2 + 22, 120 + lg.height + 14), 28, fill=(10, 20, 16, 170)); im.alpha_composite(pill); im.alpha_composite(lg, (int(W / 2 - lg.width / 2), 120))
im.convert('RGB').save(f'{D}/CAPA-ja-encontrou-o-dono-ep02.jpg', quality=94); print('ok')
