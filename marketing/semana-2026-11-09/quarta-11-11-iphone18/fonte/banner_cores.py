# Banner "iPhone 18 Pro Max na quarta — escolha sua cor" (256GB: Bordô, Glacial, Silver). Leila apontando + 3 iPhones reais.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
FT, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); FLOR=(12,66,40); MENTA=(226,242,232); LIMA=(190,245,90)
CORES = [('c-bordo.png','BORDÔ',(122,30,52)), ('c-glacial.png','GLACIAL',(214,226,234)), ('c-silver.png','SILVER',(196,198,202))]
PROB = []
def fundo(W, H, cy=.45):
    y, x = np.mgrid[0:H, 0:W]; r = np.clip(((x-W/2)**2 + (y-H*cy)**2)**.5/(H*.62), 0, 1)[..., None]
    return Image.fromarray((np.array([24,98,62])*(1-r) + np.array([5,22,14])*r).astype('uint8')).convert('RGBA')
def recorte(f, alt, ang=0):
    p = Image.open(f'{FT}/{f}').convert('RGBA'); p = p.crop(p.getbbox()); p = p.resize((int(p.width*alt/p.height), alt), Image.LANCZOS)
    return p.rotate(ang, Image.BICUBIC, expand=True) if ang else p
def poe(b, p, x, y, glow=None):
    s = Image.new('RGBA', b.size); sh = Image.new('RGBA', p.size, (0,0,0,255)); sh.putalpha(p.split()[3].point(lambda v: v*.55)); s.alpha_composite(sh, (int(x), int(y+24)))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(22)))
    if glow:
        g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((x-40, y+p.height*.15, x+p.width+40, y+p.height*.95), fill=glow+(70,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(60)))
    b.alpha_composite(p, (int(x), int(y)))
def T(b, xy, t, f, cor, anchor='mm', margem=56):
    d = ImageDraw.Draw(b); bb = d.textbbox(xy, t, font=f, anchor=anchor)
    if bb[0] < margem or bb[2] > b.width-margem: PROB.append(f'"{t}" sai da margem {bb}')
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+7), t, font=f, fill=(0,0,0,150), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor); return bb
def pil(b, cx, cy, t, f, fundo_, cor, padx=36):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2*padx; h = f.size + 30
    d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), h/2, fill=fundo_); d.text((cx, cy), t, font=f, fill=cor, anchor='mm'); return (cx-w/2, cy-h/2, cx+w/2, cy+h/2)
def logo(b, y, larg):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg = lg.resize((larg, int(lg.height*larg/lg.width)), Image.LANCZOS); b.alpha_composite(lg, ((b.width-larg)//2, y))
def leila(alt):
    p = Image.open(f'{FT}/leila-apontando-4x.png').convert('RGBA'); a = p.split()[3].filter(ImageFilter.MinFilter(5)); p.putalpha(a)   # tira a borda branca do recorte
    p = p.crop((0, 0, int(p.width*0.84), p.height))        # corta o pedaço de mão que sobrou na direita do recorte original
    a = np.asarray(p.split()[3]).astype(float); n = 140
    a[:, -n:] *= np.linspace(1, 0, n)[None, :]**1.5         # some suave na beirada (sem linha reta)
    p.putalpha(Image.fromarray(a.astype('uint8')))
    return p.resize((int(p.width*alt/p.height), alt), Image.LANCZOS)
def leque(b, cx, topo, alt, gap):
    xs = [cx-gap, cx, cx+gap]; angs = [8, 0, -8]; caixas = []
    for i in (0, 2, 1):                                   # o do meio por cima
        p = recorte(CORES[i][0], alt, angs[i]); x = xs[i]-p.width/2; y = topo + (0 if i == 1 else 30)
        poe(b, p, x, y, glow=CORES[i][2]); caixas.append((i, x, y, p))
    return xs
def etiquetas(b, xs, y, f):
    for i, (fn, nome, cor) in enumerate(CORES):
        d = ImageDraw.Draw(b); w = d.textlength(nome, font=f) + 92; h = f.size + 28; x0 = xs[i]-w/2
        d.rounded_rectangle((x0, y-h/2, x0+w, y+h/2), h/2, fill=(6,30,18,235), outline=(255,255,255,90), width=2)
        d.ellipse((x0+18, y-15, x0+48, y+15), fill=cor, outline=BR, width=3); d.text((x0+60, y), nome, font=f, fill=BR, anchor='lm')
        if x0 < 30 or x0+w > b.width-30: PROB.append(f'etiqueta {nome} fora')

# ---------- STORY 1080x1920 ----------
W, H = 1080, 1920; b = fundo(W, H); logo(b, 100, 220)
pil(b, W/2, 268, 'QUARTA 11/11 · MARTELO 20H', F('Black', 40), FOGO, BR)
T(b, (W/2, 390), 'iPHONE 18 PRO MAX', F('Black', 90), BR)
T(b, (W/2, 505), 'ESCOLHA SUA COR', F('Black', 96), OURO)
xs = leque(b, W/2, 590, 470, 300)
etiquetas(b, xs, 1120, F('Black', 36))
L = leila(730); poe(b, L, -40, H-L.height)
# cartão que a Leila aponta
x0, y0, x1, y1 = 520, 1400, 1030, 1660
s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((x0, y0, x1, y1), 34, fill=(6,30,18,225), outline=(255,255,255,110), width=3); b.alpha_composite(s); d = ImageDraw.Draw(b)
d.text(((x0+x1)/2, y0+62), 'quem arrematar', font=F('Bold', 40), fill=MENTA, anchor='mm')
d.text(((x0+x1)/2, y0+128), 'ESCOLHE A COR', font=F('Black', 56), fill=LIMA, anchor='mm')
d.text(((x0+x1)/2, y0+200), '256GB · lacrado', font=F('Bold', 40), fill=BR, anchor='mm')
for t, f in (('ESCOLHE A COR', F('Black', 56)), ('quem arrematar', F('Bold', 40))):
    if d.textlength(t, font=f) > x1-x0-40: PROB.append(f'"{t}" não cabe no cartão')
b.convert('RGB').save(f'{OUT}/IPHONE18-STORY-escolha-sua-cor.jpg', quality=94)

# ---------- FEED 1080x1350 ----------
W, H = 1080, 1350; b = fundo(W, H, .5); logo(b, 56, 190)
pil(b, W/2, 196, 'QUARTA 11/11 · MARTELO 20H', F('Black', 36), FOGO, BR)
T(b, (W/2, 300), 'iPHONE 18 PRO MAX', F('Black', 80), BR)
T(b, (W/2, 400), 'ESCOLHA SUA COR', F('Black', 92), OURO)
xs = leque(b, 690, 470, 400, 215)
etiquetas(b, [690-230, 690, 690+230], 945, F('Black', 30))
L = leila(760); poe(b, L, -120, H-L.height)
x0, y0, x1, y1 = 470, 1030, 1030, 1260
s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((x0, y0, x1, y1), 30, fill=(6,30,18,225), outline=(255,255,255,110), width=3); b.alpha_composite(s); d = ImageDraw.Draw(b)
d.text(((x0+x1)/2, y0+55), 'quem arrematar', font=F('Bold', 36), fill=MENTA, anchor='mm')
d.text(((x0+x1)/2, y0+115), 'ESCOLHE A COR', font=F('Black', 50), fill=LIMA, anchor='mm')
d.text(((x0+x1)/2, y0+180), '256GB · lacrado', font=F('Bold', 36), fill=BR, anchor='mm')
b.convert('RGB').save(f'{OUT}/IPHONE18-FEED-escolha-sua-cor.jpg', quality=94)

# ---------- BANNER DO SITE 1920x1080 (mesmo formato dos banners do topo do site) ----------
W, H = 1920, 1080; b = fundo(W, H, .5)
L = leila(1010); poe(b, L, 10, H-L.height)
CX = 1250
cb = pil(b, CX-80, 105, 'QUARTA 11/11 · MARTELO 20H', F('Black', 44), FOGO, BR)
if cb[2] > W-300-60: PROB.append('selo encosta na logo')
T(b, (CX, 225), 'iPHONE 18 PRO MAX', F('Black', 112), BR, margem=40); bbt = ImageDraw.Draw(b).textbbox((CX,225),'iPHONE 18 PRO MAX',font=F('Black',112),anchor='mm'); PROB.extend(['título encosta na Leila'] if bbt[0] < L.width+40 else [])
T(b, (CX, 350), 'ESCOLHA SUA COR', F('Black', 120), OURO, margem=40)
xs = leque(b, CX, 430, 420, 300)
etiquetas(b, xs, 905, F('Black', 36))
bb = pil(b, CX, 1005, 'quem arrematar escolhe a cor  ·  256GB lacrado', F('Bold', 40), (6,30,18,235), BR)
if bb[0] < 600 or bb[2] > W-40: PROB.append('pílula de baixo fora')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg = lg.resize((230, int(lg.height*230/lg.width)), Image.LANCZOS)
d = ImageDraw.Draw(b); d.rounded_rectangle((W-300, 40, W-40, 70+lg.height), 28, fill=(6,30,18,170)); b.alpha_composite(lg, (W-285, 55))
b.convert('RGB').save(f'{OUT}/BANNER-SITE-iphone18-escolha-sua-cor-1920x1080.jpg', quality=94)
b.convert('RGB').resize((390, 219), Image.LANCZOS).save(f'{OUT}/../quarta-11-11-iphone18/fonte/previa-celular-390px.jpg')

if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok')
