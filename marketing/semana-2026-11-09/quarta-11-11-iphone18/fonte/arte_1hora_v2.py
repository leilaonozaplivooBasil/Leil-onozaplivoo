# Arte "60 MINUTOS" (19h) do iPhone 18 Pro Max — estilo lançamento: fundo escuro com holofote, "60" gigante dourado atrás,
# anel de relógio com 60 marcas, iPhone Bordô inclinado na frente com reflexo, cartão de vidro com o lance.
# Uso: arte_1hora_v2.py <saida.jpg> <lance> <n_lances> <stories|vendedores>
import sys, os, math, random, importlib.util
from PIL import Image, ImageDraw, ImageFilter, ImageChops
F0 = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('A', f'{F0}/artes_hoje_lib.py'); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
out, LANCE, NL, VER = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W, H = A.W, A.H; F = A.F; OURO, BR = A.OURO, A.BR
CX, CY = W/2, 1090
# fundo: preto-esverdeado com holofote dourado de cima e brilho verde atrás do anel
b = Image.new('RGBA', (W, H), (4, 10, 7, 255))
def brilho(cx, cy, rx, ry, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx-rx, cy-ry, cx+rx, cy+ry), fill=cor+(a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
brilho(CX, CY, 520, 520, (18, 80, 48), 255, 160)
brilho(CX, -150, 420, 700, (255, 214, 140), 95, 140)
cone = Image.new('RGBA', (W, H)); ImageDraw.Draw(cone).polygon([(CX-90, -40), (CX+90, -40), (CX+520, 1500), (CX-520, 1500)], fill=(255, 220, 150, 38)); b.alpha_composite(cone.filter(ImageFilter.GaussianBlur(60)))
random.seed(11); pt = Image.new('RGBA', (W, H)); dp = ImageDraw.Draw(pt)
for _ in range(260):
    x, y, r = random.uniform(0, W), random.uniform(0, H*0.85), random.choice([1, 1, 2, 2, 3, 4]); dp.ellipse((x-r, y-r, x+r, y+r), fill=(255, 215, 130, random.randint(60, 200)))
b.alpha_composite(pt.filter(ImageFilter.GaussianBlur(0.8))); b.alpha_composite(pt.filter(ImageFilter.GaussianBlur(5)))
# "60" gigante em degradê dourado, atrás do celular
def ouro_grande(t, cy, size, alfa=255):
    f = F('Black', size); m = Image.new('L', (W, H)); ImageDraw.Draw(m).text((CX, cy), t, font=f, fill=alfa, anchor='mm'); bb = m.getbbox()
    gr = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(gr)
    for y in range(bb[1], bb[3]+1):
        k = (y-bb[1])/max(1, bb[3]-bb[1]); c = [int(a+(z-a)*k) for a, z in zip((255, 238, 180), (176, 116, 30))]; gd.line((0, y, W, y), fill=tuple(c)+(255,))
    gl = Image.new('RGBA', (W, H), (255, 200, 90, 0)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v*0.55))); b.alpha_composite(gl)
    b.alpha_composite(Image.composite(gr, Image.new('RGBA', (W, H), (0,0,0,0)), m))
ouro_grande('60', 468, 390)
# anel de relógio: 60 marcas + arco dourado completo com ponto brilhante no topo
R = 370; an = Image.new('RGBA', (W, H)); da = ImageDraw.Draw(an)
da.ellipse((CX-R, CY-R, CX+R, CY+R), outline=(255, 215, 130, 70), width=4)
for i in range(60):
    ang = math.radians(i*6 - 90); r1, r2 = (R-34, R-6) if i % 5 == 0 else (R-20, R-6); w_ = 7 if i % 5 == 0 else 3
    da.line((CX+r1*math.cos(ang), CY+r1*math.sin(ang), CX+r2*math.cos(ang), CY+r2*math.sin(ang)), fill=(255, 222, 150, 230 if i % 5 == 0 else 150), width=w_)
da.arc((CX-R-18, CY-R-18, CX+R+18, CY+R+18), -90, 268, fill=OURO+(255,), width=12)
gl = an.filter(ImageFilter.GaussianBlur(10)); b.alpha_composite(gl); b.alpha_composite(an)
pk = Image.new('RGBA', (W, H)); ImageDraw.Draw(pk).ellipse((CX-26, CY-R-18-26, CX+26, CY-R-18+26), fill=(255, 250, 225, 255)); b.alpha_composite(pk.filter(ImageFilter.GaussianBlur(14))); b.alpha_composite(pk.filter(ImageFilter.GaussianBlur(3)))
# iPhones: Glacial e Silver discretos atrás (meio escuros), Bordô grande inclinado na frente + reflexo no chão
def fone(nome, alt, rot=0, escuro=0):
    im = Image.open(f'{F0}/fotos/c-{nome}.png').convert('RGBA'); im = im.crop(im.getbbox()); e = alt/im.height
    im = im.resize((round(im.width*e), alt), Image.LANCZOS)
    if escuro: im = Image.composite(Image.blend(im, Image.new('RGBA', im.size, (6, 14, 10, 255)), escuro), Image.new('RGBA', im.size, (0,0,0,0)), im.split()[3])
    return im.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else im
CHAO = 1395
def poe(p, cx, base, refl=0.28):
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx-p.width*0.42, base-16, cx+p.width*0.42, base+20), fill=(0,0,0,210)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    r = p.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, p.width, int(p.height*0.4)))
    gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255-v)*refl)); r.putalpha(ImageChops.multiply(r.split()[3], gm))
    b.alpha_composite(r, (int(cx-p.width/2), int(base+4))); b.alpha_composite(p, (int(cx-p.width/2), int(base-p.height)))
poe(fone('glacial', 400, 9, 0.35), CX-290, CHAO-30, 0.15)
poe(fone('silver', 400, -9, 0.35), CX+290, CHAO-30, 0.15)
brilho(CX, CHAO-380, 260, 360, (255, 190, 170), 40, 90)
poe(fone('bordo', 630, -6), CX+10, CHAO, 0.30)
# topo: logo + chamada
A.logo(b, 80)
A.T(b, (CX, 240), 'O MARTELO BATE EM', F('Black', 50), BR, somb=150)
A.T(b, (CX, 650), 'M I N U T O S', F('Black', 46), (255, 222, 150), somb=120)
# nome + cores
A.T(b, (CX, 1505), 'iPhone 18 Pro Max', F('Black', 76), BR)
d = ImageDraw.Draw(b); fc = F('Bold', 34); itens = [((128, 40, 52), 'Bordô'), ((214, 222, 226), 'Glacial'), ((196, 198, 200), 'Silver')]
larg = sum(44 + d.textlength(t, font=fc) + 50 for _, t in itens) - 50; x = CX - larg/2
for cor, t in itens:
    d.ellipse((x, 1570, x+32, 1602), fill=cor, outline=OURO, width=3); d.text((x+44, 1587), t, font=fc, fill=(230, 232, 228), anchor='lm'); x += 44 + d.textlength(t, font=fc) + 50
# cartão de vidro com o lance
cx0, cy0, cx1, cy1 = 90, 1640, W-90, 1770
vid = b.crop((cx0, cy0, cx1, cy1)).filter(ImageFilter.GaussianBlur(18)); b.paste(vid, (cx0, cy0))
cart = Image.new('RGBA', (W, H)); dc = ImageDraw.Draw(cart); dc.rounded_rectangle((cx0, cy0, cx1, cy1), 36, fill=(255, 255, 255, 26), outline=(255, 222, 150, 150), width=3); b.alpha_composite(cart)
d = ImageDraw.Draw(b)
d.text((cx0+44, cy0+44), 'LANCE AGORA', font=F('Bold', 30), fill=(255, 222, 150), anchor='lm')
d.text((cx0+44, cy0+92), A.real(LANCE), font=F('Black', 58), fill=BR, anchor='lm')
d.ellipse((cx1-330, cy0+52, cx1-308, cy0+74), fill=(255, 80, 60)); d.text((cx1-294, cy0+63), 'DISPUTA ABERTA', font=F('Black', 30), fill=BR, anchor='lm')
d.text((cx1-44, cy0+100), f'{NL} lances até agora', font=F('Bold', 30), fill=(210, 216, 210), anchor='rm')
rod = 'DÁ SEU LANCE · leilaonozap.net' if VER == 'vendedores' else 'CHAMA NO DIRECT: IPHONE'
A.pil(b, CX, 1846, rod, F('Black', 44), fundo=OURO, cor=A.NOITE, borda=None, h=100)
b.convert('RGB').save(out, quality=95); print('ok', A.PROB)
