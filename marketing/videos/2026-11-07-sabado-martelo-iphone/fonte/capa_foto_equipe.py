# Capa do reel de sábado com a foto da equipe na mesa. Uso: capa_foto_equipe.py <foto> <saida.jpg> "<linha1>" "<linha2>" "<faixa>"
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
foto, out, l1, l2, sub = sys.argv[1:6]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1920; OURO, NOITE, BR, VERDE = (245,196,81), (10,20,16), (255,255,255), (27,122,72)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
src = Image.open(foto).convert('RGB')
# fundo: a própria foto ampliada, desfocada e escurecida
e = max(W/src.width, H/src.height); bg = src.resize((round(src.width*e), round(src.height*e)))
bg = bg.crop(((bg.width-W)//2, (bg.height-H)//2, (bg.width-W)//2+W, (bg.height-H)//2+H)).filter(ImageFilter.GaussianBlur(30))
bg = ImageEnhance.Brightness(bg).enhance(0.45).convert('RGBA')
# frente: a equipe inteira, sem cortar ninguém
fr = src.crop((130, 200, 1770, 1520)); fr = fr.resize((W, round(fr.height*W/fr.width)), Image.LANCZOS)
y0 = 800; mf = Image.new('L', fr.size, 255); dm = ImageDraw.Draw(mf)
for i in range(70): dm.line((0, i, fr.width, i), fill=int(255*i/70)); dm.line((0, fr.height-1-i, fr.width, fr.height-1-i), fill=int(255*i/70))
bg.paste(fr, (0, y0), mf)
g = Image.new('L', (1, H)); [g.putpixel((0, y), int(230*max(0, 1-y/860)**1.2)) for y in range(H)]
s = Image.new('RGBA', (W, H), NOITE+(0,)); s.putalpha(g.resize((W, H))); bg.alpha_composite(s)
d = ImageDraw.Draw(bg)
for f, t, y, cor in ((F('Black', 84), l1, 450, BR), (F('Black', 110), l2, 560, OURO)):
    while d.textlength(t, font=f) > W-90: f = ImageFont.truetype(f.path, f.size-4)
    d.text((W/2+4, y+5), t, font=f, fill=(0,0,0), anchor='mm'); d.text((W/2, y), t, font=f, fill=cor, anchor='mm')
f3 = F('Bold', 46); w = d.textlength(sub, font=f3); r = 40
d.rounded_rectangle((W/2-w/2-r, 690-r, W/2+w/2+r, 690+r), r, fill=VERDE); d.text((W/2, 692), sub, font=f3, fill=BR, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 110)); bg.alpha_composite(lg, ((W-lg.width)//2, 260))
bg.convert('RGB').save(out, quality=93); print('ok', fr.size, y0+fr.height)
