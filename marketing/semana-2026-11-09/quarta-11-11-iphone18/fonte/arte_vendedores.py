# Arte dos vendedores (WhatsApp/status) — iPhone 18 Pro Max, quarta 11/11 20h. Cena do Gamma (vertical) + texto nítido.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CENA, OUT, LANCE = sys.argv[1], sys.argv[2], float(sys.argv[3]); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); MENTA=(226,242,232); LIMA=(190,245,90)
W, H = 1080, 1920; PROB = []; caixas = []
real = lambda v: 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
b = Image.open(CENA).convert('RGB'); e = max(W/b.width, H/b.height); b = b.resize((round(b.width*e), round(b.height*e)), Image.LANCZOS)
x = (b.width-W)//2; y = (b.height-H)//2; b = b.crop((x, y, x+W, y+H)).convert('RGBA')
g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
for yy in range(0, 560): gd.line((0, yy, W, yy), fill=(6, 26, 16, int(200*(1-yy/560))))
b.alpha_composite(g)
def T(xy, t, f, cor, anchor='mm'):
    d = ImageDraw.Draw(b); bb = d.textbbox(xy, t, font=f, anchor=anchor); caixas.append((t, bb))
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+6), t, font=f, fill=(0,0,0,170), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor)
def pil(cx, cy, t, f, fundo, cor, padx=36):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2*padx; h = f.size + 30; bb = (cx-w/2, cy-h/2, cx+w/2, cy+h/2)
    d.rounded_rectangle(bb, h/2, fill=fundo); d.text((cx, cy), t, font=f, fill=cor, anchor='mm'); caixas.append((t, bb))
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg = lg.resize((210, int(lg.height*210/lg.width)), Image.LANCZOS)
b.alpha_composite(lg, ((W-210)//2, 70)); caixas.append(('logo', ((W-210)//2, 70, (W+210)//2, 70+lg.height)))
pil(W/2, 238, 'QUARTA 11/11 · MARTELO 20H', F('Black', 40), FOGO, BR)
T((W/2, 350), 'iPHONE 18 PRO MAX', F('Black', 96), BR)
T((W/2, 455), 'ESCOLHA SUA COR', F('Black', 104), OURO)
DADOS = sys.argv[4:]   # posições x dos 3 aparelhos e y da linha dos nomes, medidas na cena
xs = [int(v) for v in DADOS[:3]]; ylab = int(DADOS[3])
for xx, nome, cor in zip(xs, ('GLACIAL', 'BORDÔ', 'SILVER'), ((214,226,234), (122,30,52), (196,198,202))):
    d = ImageDraw.Draw(b); f = F('Black', 30); w = d.textlength(nome, font=f) + 80; h = 54
    d.rounded_rectangle((xx-w/2, ylab-h/2, xx+w/2, ylab+h/2), h/2, fill=(6,30,18,235), outline=(255,255,255,110), width=2)
    d.ellipse((xx-w/2+14, ylab-13, xx-w/2+40, ylab+13), fill=cor, outline=BR, width=3); d.text((xx-w/2+52, ylab), nome, font=f, fill=BR, anchor='lm')
    caixas.append((nome, (xx-w/2, ylab-h/2, xx+w/2, ylab+h/2)))
# cartão do lance, embaixo à direita (a Leila fica embaixo à esquerda, apontando)
cx0, cy0, cx1, cy1 = 565, 1440, 1045, 1820
s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((cx0, cy0, cx1, cy1), 32, fill=(6,30,18,232), outline=(255,255,255,120), width=3); b.alpha_composite(s); d = ImageDraw.Draw(b)
mid = (cx0+cx1)/2
linhas = [('LANCE INICIAL' if LANCE <= 197 else 'LANCE AGORA', F('Black', 34), LIMA, 48), (real(LANCE), F('Black', 88), BR, 126),
          ('lacrado · novo · garantia', F('Bold', 32), MENTA, 208), ('frete grátis', F('Black', 36), OURO, 260), ('dá seu lance no link', F('Black', 32), (255,150,90), 328)]
for t, f, cor, dy in linhas:
    d.text((mid, cy0+dy), t, font=f, fill=cor, anchor='mm')
    if d.textlength(t, font=f) > cx1-cx0-40: PROB.append(f'"{t}" não cabe no cartão')
caixas.append(('cartao', (cx0, cy0, cx1, cy1)))
for i, (n, c) in enumerate(caixas):
    if c[0] < 20 or c[2] > W-20 or c[1] < 20 or c[3] > H-60: PROB.append(f'{n} fora da área {c}')
    for m, e2 in caixas[:i]:
        if not (c[2]+10 < e2[0] or e2[2]+10 < c[0] or c[3]+8 < e2[1] or e2[3]+8 < c[1]): PROB.append(f'{m} e {n} encostam')
b.convert('RGB').save(f'{OUT}/VENDEDORES-iphone18-quarta-escolha-sua-cor.jpg', quality=94)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok')
