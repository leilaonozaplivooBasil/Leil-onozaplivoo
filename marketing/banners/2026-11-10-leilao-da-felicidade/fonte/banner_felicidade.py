# Banner do site "Leilão da Felicidade" no estilo do banner do Leilão dos Centavos. Uso: banner_felicidade.py <cena.png> <saida.jpg>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
cena, out = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1920, 1080; BR, OURO, NEON, ESC = (255,255,255), (245,196,81), (61,220,132), (8,30,24)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
im = Image.open(cena).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA'); d = ImageDraw.Draw(im)
PROB = []
def cabe(t, f, maxw):
    while d.textlength(t, font=f) > maxw: f = ImageFont.truetype(f.path, f.size-2)
    return f
X = 1020; MAXW = 820
# logo no alto, à direita
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((360, 130)); im.alpha_composite(lg, (X+ (MAXW-lg.width)//2 + 60, 70))
# balão de fala (o leiloeiro chamando)
bx0, by0, bx1, by1 = 905, 245, 1560, 455
sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).rounded_rectangle((bx0+6, by0+14, bx1+6, by1+14), 40, fill=(0,0,0,110)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
d.rounded_rectangle((bx0, by0, bx1, by1), 40, fill=BR); d.polygon([(bx0+8, by0+110), (bx0-40, by0+150), (bx0+10, by0+158)], fill=BR)
f = F('Bold', 44); linhas = [[('Eii, vem conhecer o', ESC)], [('Leilão da Felicidade', (27,122,72)), (',', ESC)], [('aqui você ganha ', ESC), ('ou ganha!', (27,122,72))]]
for i, partes in enumerate(linhas):
    x = bx0 + 44; y = by0 + 34 + i*56
    for t, cor in partes: d.text((x, y), t, font=f, fill=cor); x += d.textlength(t, font=f)
    if x > bx1 - 30: PROB.append('balão estoura')
# chamada + título
fk = F('Bold', 30); k = 'SEJA BEM-VINDO AO'
d.text((X+60, 540), ' '.join(k), font=cabe(' '.join(k), fk, MAXW), fill=NEON)
f1 = cabe('LEILÃO DA', F('Black', 150), MAXW); f2 = cabe('FELICIDADE', F('Black', 150), MAXW)
for t, fo, y, cor in (('LEILÃO DA', f1, 590, BR), ('FELICIDADE', f2, 735, OURO)):
    gl = Image.new('RGBA', (W, H)); ImageDraw.Draw(gl).text((X+60, y), t, font=fo, fill=cor+(160,)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
    d.text((X+60, y), t, font=fo, fill=cor)
d.line((X+64, 905, X+230, 905), fill=NEON, width=5)
# botão
fb = F('Black', 42); t = 'QUERO CONHECER  →'; w = d.textlength(t, font=fb)
gl = Image.new('RGBA', (W, H)); ImageDraw.Draw(gl).rounded_rectangle((X+60, 935, X+60+w+110, 1035), 50, fill=NEON+(200,)); im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
d.rounded_rectangle((X+60, 935, X+60+w+110, 1035), 50, fill=NEON); d.text((X+60+55, 985), t, font=fb, fill=ESC, anchor='lm')
if PROB: print('PROBLEMAS', PROB)
im.convert('RGB').save(out, quality=93); print('ok')
