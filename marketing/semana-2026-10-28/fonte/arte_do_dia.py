# 🟢 ARTE DO DIA — padrão de identidade visual definido pela Natália (28/10/2026, referência quadrada).
# Quadrado 1:1 · verde-escuro com feixes de luz verde na diagonal · logo pequeno no topo · "FALTAM" branco + tempo em lima
# · produto grande à esquerda sobre luz verde no chão · cartão de vidro "LANCE ATUAL" (ícone lima, valor branco)
# · selo lima redondo "ATÉ -X% DE DIFERENÇA" · nome do produto em branco e especificação em lima embaixo.
# Números sempre do sistema. Uso: python3 arte_do_dia.py <lance> <medio> "<tempo>" <foto> <saida.jpg>
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
from vendedores2 import recortar, ic_martelo
from kit import AQUI, logo as _logo

S = 1080
LIMA = (190, 242, 60)
BRANCO = (255, 255, 255)
ESCURO = (3, 34, 15)
FONTE = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'
F = lambda p, t: ImageFont.truetype(FONTE % p, t)


def real(v):
    s = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + (s[:-3] if s.endswith(',00') else s)


def fundo():
    yy, xx = np.mgrid[0:S, 0:S]
    d = np.sqrt(((xx - S * 0.45) / S) ** 2 + ((yy - S * 0.55) / S) ** 2)
    t = np.clip(d / 0.75, 0, 1)[..., None]
    im = Image.fromarray((np.array([10, 92, 42]) * (1 - t) + np.array([2, 30, 14]) * t).astype('uint8'), 'RGB').convert('RGBA')
    # feixes de luz verde na diagonal (de cima à direita para baixo à esquerda)
    for x0, larg, a in [(0.55, 0.05, 55), (0.68, 0.025, 70), (0.80, 0.08, 35), (0.95, 0.03, 60)]:
        c = Image.new('L', (S, S), 0)
        ImageDraw.Draw(c).polygon([(x0 * S, 0), ((x0 + larg) * S, 0), ((x0 + larg - 0.75) * S, S), ((x0 - 0.75) * S, S)], fill=a)
        luz = Image.new('RGBA', (S, S), (120, 240, 110, 0))
        luz.putalpha(c.filter(ImageFilter.GaussianBlur(10)))
        im.alpha_composite(luz)
    # chão de luz verde embaixo do produto
    g = Image.new('L', (S, S), 0)
    ImageDraw.Draw(g).ellipse((40, 760, 640, 960), fill=170)
    chao = Image.new('RGBA', (S, S), (110, 230, 90, 0))
    chao.putalpha(g.filter(ImageFilter.GaussianBlur(60)))
    im.alpha_composite(chao)
    # vinheta
    v = (np.clip((d - 0.45) / 0.35, 0, 1) * 150).astype('uint8')
    return Image.composite(Image.new('RGBA', (S, S), (0, 14, 5, 255)), im, Image.fromarray(v, 'L'))


def produto(b, foto, cx, base_y, altura):
    p = recortar(foto)
    rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.15)
    gx = np.linspace(1.03, 0.80, rgb.width)[None, :, None]
    gy = np.linspace(1.0, 0.86, rgb.height)[:, None, None]
    rgb = Image.fromarray(np.clip(np.array(rgb).astype(float) * gx * gy * 0.95 + np.array([8, 20, 10]), 0, 255).astype('uint8'))
    a = p.split()[-1]
    p = rgb.convert('RGBA')
    p.putalpha(a)
    p = p.resize((int(p.width * altura / p.height), altura), Image.LANCZOS)
    x, y = int(cx - p.width / 2), base_y - p.height
    g = Image.new('RGBA', b.size, (140, 255, 120, 0))
    m = Image.new('L', b.size, 0)
    m.paste(p.split()[-1].point(lambda v: 120 if v > 20 else 0), (x, y))
    g.putalpha(m.filter(ImageFilter.GaussianBlur(40)))
    b.alpha_composite(g)
    s = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse((cx - p.width * 0.48, base_y - 18, cx + p.width * 0.48, base_y + 20), fill=(0, 12, 4, 210))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(12)))
    b.alpha_composite(p, (x, y))


def arte(lance, medio, tempo, foto, saida, nome='MÁQUINA DE LAVAR PANASONIC', spec='15 KG • AUTOMÁTICA', prefixo='FALTAM'):
    b = fundo()
    _logo(b, y=26, largura=150)
    d = ImageDraw.Draw(b)
    # título numa linha: FALTAM (branco) + tempo (lima)
    f = F('Black', 96)
    w1, w2 = d.textlength(prefixo + ' ', font=f), d.textlength(tempo, font=f)
    x = (S - w1 - w2) / 2
    for dx, dy, cor in ((4, 6, (0, 20, 8)),):
        d.text((x + dx, 200 + dy), prefixo + ' ', font=f, fill=cor, anchor='lm')
        d.text((x + w1 + dx, 200 + dy), tempo, font=f, fill=cor, anchor='lm')
    d.text((x, 200), prefixo + ' ', font=f, fill=BRANCO, anchor='lm')
    d.text((x + w1, 200), tempo, font=f, fill=LIMA, anchor='lm')
    # produto
    produto(b, foto, 330, 870, 590)
    # cartão do lance
    c = Image.new('RGBA', b.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(c)
    dc.rounded_rectangle((610, 330, 1015, 560), radius=26, fill=(3, 40, 18, 225), outline=LIMA + (230,), width=3)
    b.alpha_composite(c)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 640, 362, 46, LIMA)
    d.text((702, 388), 'LANCE ATUAL', font=F('Black', 34), fill=LIMA, anchor='lm')
    fv = F('Black', 112)
    while d.textlength(real(lance), font=fv) > 360:
        fv = F('Black', fv.size - 4)
    d.text((812, 480), real(lance), font=fv, fill=BRANCO, anchor='mm')
    # selo lima
    pct = round(100 * (1 - lance / medio))
    cx, cy, r = 812, 715, 112
    g = Image.new('RGBA', b.size, LIMA + (0,))
    m = Image.new('L', b.size, 0)
    ImageDraw.Draw(m).ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=140)
    g.putalpha(m.filter(ImageFilter.GaussianBlur(20)))
    b.alpha_composite(g)
    d = ImageDraw.Draw(b)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=LIMA)
    d.text((cx, cy - 60), 'ATÉ', font=F('Black', 30), fill=ESCURO, anchor='mm')
    d.text((cx, cy + 2), f'-{pct}%', font=F('Black', 80), fill=ESCURO, anchor='mm')
    d.text((cx, cy + 62), 'DE DIFERENÇA', font=F('Black', 21), fill=ESCURO, anchor='mm')
    # nome e especificação
    d.text((S / 2, 960), nome, font=F('Black', 50), fill=BRANCO, anchor='mm')
    d.text((S / 2, 1016), spec, font=F('Black', 32), fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    arte(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], f'{AQUI}/{sys.argv[4]}', sys.argv[5])
