# Capas com título de curiosidade (não de propaganda) para o reel de sábado. Uso: capas_titulo.py <pasta-quadros> <pasta-saída>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
Q, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1920; OURO, NOITE, BR, VERDE, FOGO = (245,196,81), (10,20,16), (255,255,255), (27,122,72), (243,91,18)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
OPC = [('D', 'bgA.png', 'OLHA O QUE', 'ROLOU NO SÁBADO', 'a gente conta tudo no vídeo'),
       ('E', 'bgC.png', 'NINGUÉM ACREDITOU', 'NO PREÇO QUE SAIU', 'esse iPhone 17 Pro Max'),
       ('F', 'bgB.png', 'O QUE ACONTECEU', 'NOS ÚLTIMOS 3s', 'ficou todo mundo de boca aberta')]
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 110))
for nome, bg, l1, l2, sub in OPC:
    im = Image.open(f'{Q}/{bg}').convert('RGB').resize((W, H))
    im = ImageEnhance.Contrast(im).enhance(1.05).convert('RGBA')
    g = Image.new('L', (1, H)); [g.putpixel((0, y), int(215*max(0, 1-y/900)**1.4)) for y in range(H)]
    sombra = Image.new('RGBA', (W, H), NOITE+(0,)); sombra.putalpha(g.resize((W, H))); im.alpha_composite(sombra)
    d = ImageDraw.Draw(im)
    f1, f2, f3 = F('Black', 80), F('Black', 112), F('Bold', 46)
    for f, t, y, cor in ((f1, l1, 330, BR), (f2, l2, 440, OURO)):
        w = d.textlength(t, font=f)
        while w > W-90: f = ImageFont.truetype(f.path, f.size-4); w = d.textlength(t, font=f)
        d.text((W/2+4, y+5), t, font=f, fill=(0,0,0), anchor='mm'); d.text((W/2, y), t, font=f, fill=cor, anchor='mm')
    w = d.textlength(sub, font=f3); r = 40
    d.rounded_rectangle((W/2-w/2-r, 560-r+4, W/2+w/2+r, 560+r+4), r, fill=VERDE); d.text((W/2, 562), sub, font=f3, fill=BR, anchor='mm', embedded_color=True)
    im.alpha_composite(lg, ((W-lg.width)//2, 150))
    im.convert('RGB').save(f'{OUT}/CAPA-opcao-{nome}.jpg', quality=93)
print('ok')
