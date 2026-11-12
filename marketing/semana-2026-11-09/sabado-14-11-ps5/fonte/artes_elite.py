# 3 artes "elite" do PS5 (sáb 14/11, 20h): minimalistas, verde-escuro + dourado, letra fina, pouco texto.
# 1) MONOLITO — o console sozinho num facho de luz dourada.  2) SUA VEZ — o controle gigante, cortado, com aro de luz.
# 3) O NÚMERO — o lance atual em dourado fino e enorme atrás do console.
# Uso: artes_elite.py <pasta_saida> <lance> <n_pessoas>   (sem link e sem %: servem para Instagram e WhatsApp)
import sys, os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
F0 = os.path.dirname(os.path.abspath(__file__)); MK = '/home/user/Leil-onozaplivoo/marketing'
OUT, LANCE, NP = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
W, H = 1080, 1920
OURO, OCLARO, OESC = (212, 175, 106), (246, 226, 178), (150, 112, 52)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
def real(v): return f'{v:,.0f}'.replace(',', '.')
def fundo(c0=(3, 9, 6), c1=(10, 34, 22), cx=W/2, cy=H*0.45, r=1100):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x-cx, (y-cy)*0.85)/r, 0, 1)**1.4
    a = (np.array(c1)[None, None]*(1-d[..., None]) + np.array(c0)[None, None]*d[..., None])
    a += np.random.default_rng(3).normal(0, 2.2, a.shape)  # grão fino
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def brilho(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor+(a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def espac(t, n=1): return (' '*n).join(t)
def texto(b, xy, t, f, cor, anchor='mm', a=255):
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor+(a,), anchor=anchor)
def ouro_txt(b, xy, t, f, anchor='mm', glow=0.35):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); bb = m.getbbox()
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3]+1):
        k = (y-bb[1])/max(1, bb[3]-bb[1]); k2 = abs(k-0.38)*1.6
        c = [int(a_+(z-a_)*min(1, k2)) for a_, z in zip(OCLARO, OESC)]; gd.line((0, y, W, y), fill=tuple(c)+(255,))
    if glow:
        gl = Image.new('RGBA', (W, H), OURO+(0,)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v*glow))); b.alpha_composite(gl)
    b.alpha_composite(Image.composite(g, Image.new('RGBA', (W, H), (0,0,0,0)), m))
def linha_ouro(b, x0, x1, y, a=200):
    l = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(l)
    for x in range(int(x0), int(x1)):
        k = 1 - abs((x-(x0+x1)/2)/((x1-x0)/2)); d.point((x, y), fill=OURO+(int(a*k**0.6),)); d.point((x, y+1), fill=OURO+(int(a*0.5*k**0.6),))
    b.alpha_composite(l)
def foto(nome, alt=None, larg=None):
    im = Image.open(f'{F0}/fotos/{nome}-recorte.png').convert('RGBA')
    if not alt and not larg: return im
    e = (alt/im.height) if alt else (larg/im.width); return im.resize((round(im.width*e), round(im.height*e)), Image.LANCZOS)
def poe(b, p, x, base, refl=0.22, sombra=True):
    if sombra:
        s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((x-p.width*0.5, base-14, x+p.width*0.5, base+16), fill=(0,0,0,200)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    if refl:
        r = p.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, p.width, int(p.height*0.35)))
        gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255-v)*refl)); r.putalpha(ImageChops.multiply(r.split()[3], gm))
        b.alpha_composite(r, (int(x-p.width/2), int(base+2)))
    b.alpha_composite(p, (int(x-p.width/2), int(base-p.height)))
def tom_quente(p, k=0.10):  # leve banho dourado no branco do console, para casar com a luz
    r, g, bl, a = p.split(); q = Image.merge('RGB', (r, g, bl)); q = Image.blend(q, Image.new('RGB', q.size, (255, 222, 170)), k)
    q = q.convert('RGBA'); q.putalpha(a); return q
def logo(b, y, larg=200):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((larg, 80)); b.alpha_composite(lg, ((W-lg.width)//2, y))
def poeira(b, n=70, seed=5):
    random.seed(seed); p = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(p)
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H*0.8), random.choice([1, 1, 1.5, 2]); d.ellipse((x-r, y-r, x+r, y+r), fill=OCLARO+(random.randint(40, 140),))
    b.alpha_composite(p.filter(ImageFilter.GaussianBlur(0.6)))
console = tom_quente(foto('ps5-console-controle').crop((660, 0, 1204, 1261)))  # só o console
console = console.crop(console.getbbox())
controle = tom_quente(foto('ps5-console-controle').crop((0, 860, 560, 1261))); controle = controle.crop(controle.getbbox())
# ---------- 1) MONOLITO
b = fundo(cy=H*0.55)
cone = Image.new('RGBA', (W, H)); ImageDraw.Draw(cone).polygon([(W/2-60, -20), (W/2+60, -20), (W/2+330, 1420), (W/2-330, 1420)], fill=OCLARO+(48,)); b.alpha_composite(cone.filter(ImageFilter.GaussianBlur(45)))
brilho(b, (W/2-420, 1330, W/2+420, 1470), OURO, 70, 50)
poeira(b, 50)
texto(b, (W/2, 200), espac('SÁBADO · 20H', 1), F('Light', 34), OCLARO)
linha_ouro(b, W/2-60, W/2+60, 240, 220)
c = console.resize((round(console.width*880/console.height), 880), Image.LANCZOS); poe(b, c, W/2, 1400, 0.20)
linha_ouro(b, 140, W-140, 1402, 160)
texto(b, (W/2, 1560), espac('PLAYSTATION 5', 1), F('Thin', 74), (240, 236, 226))
texto(b, (W/2, 1630), espac('SLIM · EDIÇÃO DIGITAL', 1), F('Light', 26), (190, 196, 186))
ouro_txt(b, (W/2, 1735), f'lance atual  R$ {real(LANCE)}', F('Regular', 40), glow=0.2)
logo(b, 1800, 170)
b.convert('RGB').save(f'{OUT}/PS5-ELITE-1-monolito.jpg', quality=95)
# ---------- 2) SUA VEZ (foto de estúdio do controle, gerada no Gamma, com luz dourada de borda)
est = Image.open(f'{F0}/fotos/controle-estudio-gamma.jpg').convert('RGB'); r_ = max(W/est.width, H/est.height)
est = est.resize((round(est.width*r_), round(est.height*r_)), Image.LANCZOS); xo, yo = (est.width-W)//2, (est.height-H)//2
b = est.crop((xo, yo + 40, xo+W, yo+H+40) if est.height-H >= 40 else (xo, yo, xo+W, yo+H)).convert('RGBA')
poeira(b, 40, 9)
texto(b, (W/2, 230), espac('SÁBADO · 20H', 1), F('Light', 34), OCLARO)
linha_ouro(b, W/2-60, W/2+60, 270, 220)
texto(b, (W/2, 410), 'Sua vez', F('Thin', 170), (244, 240, 230))
ouro_txt(b, (W/2, 570), 'de jogar.', F('ExtraLight', 150), glow=0.3)
texto(b, (W/2, 1640), espac('PLAYSTATION 5 SLIM', 1), F('Light', 36), (230, 228, 220))
ouro_txt(b, (W/2, 1720), f'lance atual  R$ {real(LANCE)}', F('Regular', 40), glow=0.2)
logo(b, 1790, 170)
b.convert('RGB').save(f'{OUT}/PS5-ELITE-2-sua-vez.jpg', quality=95)
# ---------- 3) O NÚMERO (lance gigante em ouro fino atrás do console)
b = fundo(cy=H*0.5)
brilho(b, (W/2-480, 380, W/2+480, 1300), (24, 90, 56), 200, 160)
texto(b, (W/2, 210), espac('LANCE ATUAL', 1), F('Light', 32), OCLARO)
linha_ouro(b, W/2-60, W/2+60, 250, 220)
ouro_txt(b, (W/2, 330), 'R$', F('Light', 64), glow=0.15)
num = real(LANCE); fz = 520
while ImageDraw.Draw(b).textlength(num, font=F('Thin', fz)) > W-60: fz -= 10
ouro_txt(b, (W/2, 640), num, F('Thin', fz), glow=0.45)
c = console.resize((round(console.width*760/console.height), 760), Image.LANCZOS); poe(b, c, W/2+20, 1430, 0.2)
linha_ouro(b, 160, W-160, 1432, 150)
texto(b, (W/2, 1560), 'e subindo.', F('ThinItalic', 84), (240, 236, 226))
texto(b, (W/2, 1650), espac(f'{NP} PESSOAS NA DISPUTA · SÁBADO 20H', 1).replace('  ', ' '), F('Light', 26), (196, 200, 190))
logo(b, 1770, 170)
b.convert('RGB').save(f'{OUT}/PS5-ELITE-3-o-numero.jpg', quality=95)
print('ok')
