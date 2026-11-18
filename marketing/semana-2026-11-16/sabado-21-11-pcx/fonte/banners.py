# Banners do site (1920x1080) do leilão da Honda PCX 160 — sábado 21/11. Leila (IA, Gamma) com a moto à direita,
# texto à esquerda. 1 em cima da moto · 2 apontando · 3 acabou de arrematar. Uso: banners.py <lance>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1920, 1080
BR, OURO, AMA, ESC, VERM = (255, 255, 255), (246, 214, 140), (255, 210, 0), (4, 22, 13), (214, 26, 34)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def base(foto):
    im = Image.open(foto).convert('RGB'); k = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS); x = (im.width - W) // 2; y = (im.height - H) // 2
    b = im.crop((x, y, x + W, y + H)).convert('RGBA')
    g = np.zeros((H, W), 'float32'); xs = np.arange(W) / W; g[:] = np.clip((0.62 - xs) / 0.32, 0, 1) ** 1.1 * 235   # sombra verde à esquerda p/ ler o texto
    t = Image.new('RGBA', (W, H), ESC + (0,)); t.putalpha(Image.fromarray(g.astype('uint8'))); b.alpha_composite(t); return b
def pilula(d, x, y, t, f, fundo, cor):
    w = d.textlength(t, font=f); d.rounded_rectangle((x, y, x + w + 56, y + f.size + 34), (f.size + 34) / 2, fill=fundo); d.text((x + 28, y + 17 + f.size / 2), t, font=f, fill=cor, anchor='lm')
def texto(b, titulo, sub, cor_t=BR):
    d = ImageDraw.Draw(b); X = 110
    lg = LOGO.copy(); lg.thumbnail((260, 260)); b.alpha_composite(lg, (X, 80)); d = ImageDraw.Draw(b)
    pilula(d, X, 270, 'SÁBADO · 21/11', F('Black', 46), AMA, ESC)
    y = 410
    for linha in titulo:
        d.text((X + 4, y + 7), linha, font=F('Black', 108), fill=(0, 0, 0, 150), anchor='lm'); d.text((X, y), linha, font=F('Black', 108), fill=cor_t, anchor='lm'); y += 116
    d.text((X, y + 10), sub, font=F('Bold', 54), fill=OURO, anchor='lm'); y += 100
    d.text((X, y), 'Honda PCX 160 · branca perolizada', font=F('SemiBold', 40), fill=BR, anchor='lm'); y += 80
    d.text((X, y), 'LANCE INICIAL', font=F('SemiBold', 32), fill=OURO, anchor='lm')
    d.text((X, y + 75), f'R$ {real(LANCE)}', font=F('Black', 110), fill=BR, anchor='lm')
    d.text((X, H - 45), 'retirada em mãos com a equipe Leilão no Zap', font=F('Medium', 30), fill=(210, 225, 215), anchor='lm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=93); print('ok', n)
FT = f'{AQ}/'
if os.path.exists(FT + 'leila-em-cima.jpg'):
    b = base(FT + 'leila-em-cima.jpg'); texto(b, ['SUA PCX', 'TE ESPERA'], 'leilão da moto neste sábado'); salva(b, 'BANNER-1-leila-em-cima-da-pcx-1920x1080')
if os.path.exists(FT + 'leila-apontando.jpg'):
    b = base(FT + 'leila-apontando.jpg'); texto(b, ['OLHA ESSA', 'MOTO!'], 'vai a leilão neste sábado'); salva(b, 'BANNER-2-leila-apontando-pcx-1920x1080')
if os.path.exists(FT + 'leila-arrematou.jpg'):
    b = base(FT + 'leila-arrematou.jpg'); texto(b, ['ARREMATEI!'], 'no sábado pode ser você'); salva(b, 'BANNER-3-leila-arrematou-pcx-1920x1080')
