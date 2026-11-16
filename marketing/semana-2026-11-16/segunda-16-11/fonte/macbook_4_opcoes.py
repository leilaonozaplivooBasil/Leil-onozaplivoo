# 4 opções de arte do MacBook Neo PRATEADO (qua 18/11, 20h) para a Natália escolher. Fotos oficiais da Apple do modelo PRATEADO
# (loja e página do MacBook Neo, 16/11), fundo verde da marca.
# Referências dela (16/11): propagandas da Apple, ficha técnica do Mercado Livre, vistas lado a lado. Uso: macbook_4_opcoes.py <lance>
import os, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/opcoes-macbook'; MK = '/home/user/Leil-onozaplivoo/marketing'
os.makedirs(OUT, exist_ok=True); LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
BRANCO, CREME, OURO, OURO2, VERDEC, ESC = (247, 247, 244), (205, 222, 210), (226, 186, 104), (246, 214, 140), (150, 190, 165), (4, 22, 13)
ABERTO = f'{AQ}/fotos/1793811070147_2_macbook-neo-de-13-polegadas-chip-a18-pro-cpu-6-nucleos-gpu-5.jpg'
TAMPA = f'{AQ}/fotos/1793811071242_4_macbook-neo-de-13-polegadas-chip-a18-pro-cpu-6-nucleos-gpu-5.jpg'
W, H = 1080, 1350
DATA = 'quarta-feira, 18/11, às 20h'

def recorta(caminho, larg, ang=0):
    im = Image.open(caminho).convert('RGB'); a = np.asarray(im).astype(float); mn = a.min(axis=2)
    lab, _ = ndimage.label(mn > 246); borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    obj = ndimage.binary_fill_holes(~np.isin(lab, list(borda)))
    alfa = np.where(ndimage.binary_erosion(obj, iterations=2), 1.0, np.where(obj, np.clip((252 - mn) / 7, 0, 1), 0))
    al = Image.fromarray((alfa * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
    p = im.convert('RGBA'); p.putalpha(al); p = p.crop(al.getbbox()); p = p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)
    return p.rotate(ang, resample=Image.BICUBIC, expand=True) if ang else p

def png(nome, larg, ang=0):
    p = Image.open(f'{AQ}/fotos/{nome}').convert('RGBA'); p = p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)
    return p.rotate(ang, resample=Image.BICUBIC, expand=True) if ang else p
FRENTE, TAMPA_A = 'apple-silver-frente.png', 'apple-silver-tampa.png'

def poe(b, p, x, y, dy=34, blur=36, a=.55):
    s = Image.new('RGBA', (W, H)); s.paste((0, 12, 6, 255), (int(x), int(y + dy)), p.split()[3].point(lambda v: int(v * a))); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
    s = Image.new('RGBA', (W, H)); s.paste((0, 10, 5, 255), (int(x), int(y + 8)), p.split()[3].point(lambda v: int(v * .35))); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(8)))
    b.alpha_composite(p, (int(x), int(y)))

def fundo(cx, cy, c1=(28, 92, 60), c0=(5, 26, 16), raio=1.0):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - cx, (y - cy) * .9) / (W * raio), 0, 1) ** 1.3
    a = np.array(c1)[None, None] * (1 - d[..., None]) + np.array(c0)[None, None] * d[..., None]
    a += np.random.default_rng(4).normal(0, 1.6, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')

def logo(b, x, y, larg=150):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((larg, 62)); b.alpha_composite(lg, (int(x if x is not None else (W - lg.width) / 2), int(y)))
def espac(t): return ' '.join(t)
def lance(d, x, y, tam, cor=OURO2, anchor='l'):
    fR, fN = F('Medium', tam * 34 // 100), F('Bold', tam); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN)
    x0 = x - (wr + wn) / 2 if anchor == 'm' else x
    d.text((x0, y), 'R$', font=fR, fill=cor, anchor='ls'); d.text((x0 + wr, y), LANCE, font=fN, fill=cor, anchor='ls')
def pilula(d, cx, cy, t, f, fundo_=ESC, borda=OURO, cor=BRANCO, pad=40):
    wt = d.textlength(t, font=f); h = f.size * .95 + 26
    d.rounded_rectangle((cx - wt / 2 - pad, cy - h / 2, cx + wt / 2 + pad, cy + h / 2), h / 2, fill=fundo_, outline=borda, width=2); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def salvar(b, nome): b.convert('RGB').save(f'{OUT}/{nome}', quality=95); print('ok', nome)

# ícones de linha (dourado), 64 px
def icone(d, tipo, cx, cy, r=34):
    d.ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=(10, 50, 32), outline=OURO, width=2); c = OURO2; w = 4
    if tipo == 'chip':
        d.rounded_rectangle((cx - 20, cy - 20, cx + 20, cy + 20), 6, outline=c, width=w); d.rectangle((cx - 9, cy - 9, cx + 9, cy + 9), fill=c)
        for k in (-10, 0, 10):
            for (x0, y0, x1, y1) in ((cx + k, cy - 30, cx + k, cy - 20), (cx + k, cy + 20, cx + k, cy + 30), (cx - 30, cy + k, cx - 20, cy + k), (cx + 20, cy + k, cx + 30, cy + k)): d.line((x0, y0, x1, y1), fill=c, width=3)
    elif tipo == 'tela':
        d.rounded_rectangle((cx - 26, cy - 22, cx + 26, cy + 12), 4, outline=c, width=w); d.polygon([(cx - 34, cy + 16), (cx + 34, cy + 16), (cx + 28, cy + 24), (cx - 28, cy + 24)], fill=c)
    elif tipo == 'ssd':
        d.rounded_rectangle((cx - 28, cy - 18, cx + 28, cy + 18), 5, outline=c, width=w); d.text((cx, cy + 1), 'SSD', font=F('Bold', 18), fill=c, anchor='mm')
    elif tipo == 'cor':
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=(212, 214, 216), outline=c, width=3); d.ellipse((cx - 14, cy - 16, cx - 2, cy - 4), fill=(245, 246, 247))

# OPÇÃO 1 · FICHA TÉCNICA (referência: arte do Mercado Livre) ------------------------------------------------------------
b = fundo(W * .35, 600); d = ImageDraw.Draw(b); logo(b, 64, 56, 140); d = ImageDraw.Draw(b)
pilula(d, W - 230, 86, 'QUARTA · 20H', F('Bold', 30), fundo_=OURO, borda=OURO, cor=ESC, pad=30)
d.text((64, 170), 'MacBook Neo 13"', font=F('Bold', 96), fill=BRANCO); d.text((66, 290), 'Prateado  ·  Leilão de quarta-feira', font=F('Medium', 36), fill=CREME)
p = png(FRENTE, 560); poe(b, p, 10, 520, dy=26, blur=26); d = ImageDraw.Draw(b)
for i, (ic, t1, t2) in enumerate([('chip', 'Chip A18 Pro', 'CPU 6 núcleos · GPU 5'), ('tela', 'Tela de 13"', 'leve e fino'),
                                  ('ssd', '256GB', 'de armazenamento'), ('cor', 'Prateado', 'cor do produto')]):
    y = 465 + i * 132; icone(d, ic, 640, y); d.text((708, y - 6), t1, font=F('Bold', 40), fill=BRANCO, anchor='ls'); d.text((708, y + 36), t2, font=F('Medium', 30), fill=VERDEC, anchor='ls')
d.rounded_rectangle((40, 1030, W - 40, 1300), 36, fill=ESC, outline=OURO, width=2)
d.text((100, 1095), espac('LANCE ATUAL'), font=F('SemiBold', 30), fill=OURO, anchor='lm'); lance(d, 96, 1255, 150)
d.text((W - 100, 1150), 'quarta-feira', font=F('SemiBold', 40), fill=BRANCO, anchor='rm'); d.text((W - 100, 1205), '18/11 · às 20h', font=F('Medium', 36), fill=CREME, anchor='rm')
salvar(b, 'opcao-1-ficha-tecnica.jpg')

# OPÇÃO 2 · NA LOJA x NO LEILÃO (preço das lojas: Mercado Livre em 16/11, a partir de R$ 6.099) ------------------------------
b = fundo(W / 2, 330, c1=(40, 112, 76), c0=(16, 60, 38), raio=.9); d = ImageDraw.Draw(b)
d.rectangle((0, 760, W, H), fill=ESC); logo(b, None, 50, 140); d = ImageDraw.Draw(b)
d.text((W / 2, 165), 'MacBook Neo 13" · Prateado', font=F('SemiBold', 44), fill=BRANCO, anchor='mm')
d.text((W / 2, 245), espac('NAS LOJAS'), font=F('SemiBold', 30), fill=CREME, anchor='mm')
d.text((W / 2, 330), 'mais de R$ 6 mil', font=F('Bold', 92), fill=BRANCO, anchor='mm')
p = png(FRENTE, 800); poe(b, p, (W - p.width) / 2, 420, dy=30, blur=30, a=.75); d = ImageDraw.Draw(b)
d.text((W / 2, 1020), espac('NO LEILÃO, O LANCE ESTÁ EM'), font=F('SemiBold', 30), fill=OURO, anchor='mm'); lance(d, W / 2, 1200, 190, anchor='m')
pilula(d, W / 2, 1275, DATA, F('SemiBold', 34))
salvar(b, 'opcao-2-loja-x-leilao.jpg')

# OPÇÃO 3 · MINIMALISTA APPLE (tampa com a maçã como herói) --------------------------------------------------------------
b = fundo(W / 2, 640, c1=(22, 78, 50), c0=(3, 16, 9), raio=.85); d = ImageDraw.Draw(b)
d.text((W / 2, 150), 'MacBook Neo', font=F('SemiBold', 120), fill=BRANCO, anchor='mm')
d.text((W / 2, 245), 'Prateado. Leve. Pode ser seu.', font=F('Regular', 40), fill=OURO2, anchor='mm')
p = png(FRENTE, 900); poe(b, p, (W - p.width) / 2, 320, dy=34, blur=34, a=.75); d = ImageDraw.Draw(b)
d.text((W / 2, 900), '13 polegadas  ·  chip A18 Pro  ·  256GB', font=F('Regular', 32), fill=VERDEC, anchor='mm')
d.line((W / 2 - 60, 940, W / 2 + 60, 940), fill=OURO, width=2)
d.text((W / 2, 1000), 'Lance atual', font=F('Medium', 36), fill=CREME, anchor='mm'); lance(d, W / 2, 1160, 150, cor=BRANCO, anchor='m')
d.text((W / 2, 1230), DATA, font=F('Medium', 36), fill=OURO2, anchor='mm'); logo(b, None, 1268, 120)
salvar(b, 'opcao-3-minimalista.jpg')

# OPÇÃO 4 · DUAS VISTAS (referência: fotos lado a lado do Mercado Livre) ------------------------------------------------
b = fundo(W / 2, 520, c1=(30, 98, 64), c0=(6, 30, 18)); d = ImageDraw.Draw(b); logo(b, 64, 56, 140); d = ImageDraw.Draw(b)
d.text((64, 175), 'Ele pode ser seu', font=F('Bold', 84), fill=BRANCO); d.text((64, 272), 'na quarta-feira.', font=F('Bold', 84), fill=OURO2)
t = png(TAMPA_A, 470, 4); k = png(FRENTE, 570)
poe(b, t, 40, 420, dy=36); poe(b, k, 450, 620, dy=26, blur=28, a=.7); d = ImageDraw.Draw(b)
d.ellipse((W - 250, 70, W - 50, 270), fill=OURO); d.text((W - 150, 145), 'QUARTA', font=F('Black', 34), fill=ESC, anchor='mm'); d.text((W - 150, 197), '20H', font=F('Black', 58), fill=ESC, anchor='mm')
d.text((64, 1000), 'MacBook Neo 13" · Prateado · A18 Pro · 256GB', font=F('Medium', 33), fill=CREME)
d.line((64, 1068, W - 64, 1068), fill=OURO, width=2)
d.text((64, 1140), espac('LANCE ATUAL'), font=F('SemiBold', 30), fill=OURO, anchor='lm'); lance(d, 60, 1290, 160)
d.text((W - 64, 1180), 'quarta', font=F('SemiBold', 44), fill=BRANCO, anchor='rm'); d.text((W - 64, 1240), '18/11 · 20h', font=F('Medium', 38), fill=CREME, anchor='rm')
salvar(b, 'opcao-4-duas-vistas.jpg')
