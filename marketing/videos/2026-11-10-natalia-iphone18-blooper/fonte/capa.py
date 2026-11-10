# Capa do reel "Espera, espera… para tudo!" — padrão aprovado: texto em cima, a Natália com a caixa do iPhone embaixo.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
q, out = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1920; OURO, NOITE, BR, VERDE = (245,196,81), (10,20,16), (255,255,255), (27,122,72)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
im = Image.open(q).convert('RGB').resize((W, H)).convert('RGBA')
g = Image.new('L', (1, H)); [g.putpixel((0, y), int(225*max(0, 1-y/820)**1.3)) for y in range(H)]
s = Image.new('RGBA', (W, H), NOITE+(0,)); s.putalpha(g.resize((W, H))); im.alpha_composite(s)
d = ImageDraw.Draw(im)
for f, t, y, cor in ((F('Black', 104), 'ESPERA, ESPERA…', 360, BR), (F('Black', 138), 'PARA TUDO!', 490, OURO)):
    while d.textlength(t, font=f) > W-80: f = ImageFont.truetype(f.path, f.size-4)
    d.text((W/2+5, y+6), t, font=f, fill=(0,0,0), anchor='mm'); d.text((W/2, y), t, font=f, fill=cor, anchor='mm')
f3 = F('Bold', 48); sub = 'olha o que vai pro leilão amanhã'; w = d.textlength(sub, font=f3); r = 42
d.rounded_rectangle((W/2-w/2-r, 620-r, W/2+w/2+r, 620+r), r, fill=VERDE); d.text((W/2, 622), sub, font=f3, fill=BR, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 110)); im.alpha_composite(lg, ((W-lg.width)//2, 150))
im.convert('RGB').save(out, quality=93); print('ok')
