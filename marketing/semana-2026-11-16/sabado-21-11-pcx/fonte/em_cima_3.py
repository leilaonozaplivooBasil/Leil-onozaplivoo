# Leila em cima da PCX — 3 versões (sáb 21/11), banner do site 1920x1080 que vira vídeo.
# Cada versão sai pronta (FINAL.jpg) e em CAMADAS (foto + cada texto num PNG transparente do tamanho todo) pra animar.
# A PREMIUM (noite + ouro) · B VELOCIDADE (rua à noite + verde neon) · C POP (verde + amarelo-ouro, adesivo)
# Uso: em_cima_3.py <lance> [A,B,C]
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/leila-em-cima-3-versoes'; MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'; SO = sys.argv[2].split(',') if len(sys.argv) > 2 else 'ABC'
FD = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
FI = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{p}.otf', t)
W, H = 1920, 1080
VERDE, NEON, OURO, NOITE, BR, OCLARO, OESC = (27, 122, 72), (63, 208, 126), (245, 196, 81), (10, 20, 16), (255, 255, 255), (250, 230, 170), (170, 120, 40)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def novo(): return Image.new('RGBA', (W, H))
def foto(arq):
    im = Image.open(arq).convert('RGB'); k = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS); x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)).convert('RGBA')
def sombra(cor, ate=.6, forca=235):
    xs = np.arange(W) / W; g = np.tile(np.clip((ate - xs) / (ate * .55), 0, 1) ** 1.2 * forca, (H, 1))
    s = Image.new('RGBA', (W, H), cor + (0,)); s.putalpha(Image.fromarray(g.astype('uint8'))); return s
def logo(x=110, y=80, larg=250):
    c = novo(); lg = LOGO.copy(); lg.thumbnail((larg, larg)); c.alpha_composite(lg, (x, y)); return c
def degrade_txt(xy, t, f, c1, c0, anchor='lm', glow=None):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); bb = m.getbbox()
    g = novo(); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        k = min(1, abs((y - bb[1]) / max(1, bb[3] - bb[1]) - .35) * 1.6); gd.line((0, y, W, y), fill=tuple(int(a + (z - a) * k) for a, z in zip(c1, c0)) + (255,))
    c = novo()
    if glow: gl = Image.new('RGBA', (W, H), glow[0] + (0,)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(glow[2])).point(lambda v: int(v * glow[1]))); c.alpha_composite(gl)
    c.alpha_composite(Image.composite(g, novo(), m)); return c
def txt(xy, t, f, cor, anchor='lm', sombra_=(0, 0, 0, 150), dx=4):
    c = novo(); d = ImageDraw.Draw(c)
    if sombra_: d.text((xy[0] + dx, xy[1] + dx + 3), t, font=f, fill=sombra_, anchor=anchor)
    d.text(xy, t, font=f, fill=cor, anchor=anchor); return c
def juntar(*cs):
    c = novo()
    for x in cs: c.alpha_composite(x)
    return c
def salvar(v, camadas):
    os.makedirs(f'{OUT}/{v}-camadas', exist_ok=True); b = camadas[0][1].copy()
    for i, (n, im) in enumerate(camadas):
        if i: b.alpha_composite(im)
        (im.convert('RGB').save(f'{OUT}/{v}-camadas/{i:02d}-{n}.jpg', quality=93) if i == 0 else im.save(f'{OUT}/{v}-camadas/{i:02d}-{n}.png'))
    b.convert('RGB').save(f'{OUT}/{v}-FINAL-1920x1080.jpg', quality=93); print('ok', v)

# A · PREMIUM — noite verde, ouro em degradê, letras espaçadas, linhas finas
if 'A' in SO and os.path.exists(f'{AQ}/em-cima-A.jpg'):
    X = 120; c = []
    c.append(('foto', foto(f'{AQ}/em-cima-A.jpg'))); c.append(('sombra', sombra(NOITE, .58, 240))); c.append(('logo', logo(X, 80)))
    d0 = novo(); d = ImageDraw.Draw(d0); d.text((X, 300), ' '.join('SÁBADO · 21 DE NOVEMBRO'), font=FD('SemiBold', 30), fill=OURO, anchor='lm'); d.line((X, 335, X + 120, 335), fill=OURO, width=3)
    c.append(('data', d0))
    c.append(('titulo-1', txt((X, 430), 'SUA PCX', FD('Black', 132), BR))); c.append(('titulo-2', degrade_txt((X, 560), 'TE ESPERA', FD('Black', 132), OCLARO, OESC, glow=(OURO, .35, 26))))
    c.append(('sub', txt((X, 670), 'Honda PCX 160  ·  branca perolizada', FD('Medium', 40), (225, 235, 228), sombra_=None)))
    p = novo(); d = ImageDraw.Draw(p); d.rounded_rectangle((X, 740, X + 560, 920), 26, outline=OURO, width=3, fill=(10, 20, 16, 200))
    d.text((X + 36, 785), 'LANCE INICIAL', font=FD('SemiBold', 30), fill=OURO, anchor='lm'); p.alpha_composite(degrade_txt((X + 36, 862), f'R$ {real(LANCE)}', FD('Black', 96), OCLARO, OESC))
    c.append(('preco', p)); c.append(('rodape', txt((X, 1015), 'retirada em mãos com a equipe Leilão no Zap', FD('Medium', 28), (190, 205, 196), sombra_=None)))
    salvar('A-premium-noite-e-ouro', c)

# B · VELOCIDADE — itálico grande, verde neon, riscos de velocidade
if 'B' in SO and os.path.exists(f'{AQ}/em-cima-B.jpg'):
    X = 110; c = []
    c.append(('foto', foto(f'{AQ}/em-cima-B.jpg'))); c.append(('sombra', sombra((5, 11, 8), .6, 235))); c.append(('logo', logo(X, 70)))
    r = novo(); d = ImageDraw.Draw(r)
    for i, (y, l) in enumerate(((360, 520), (392, 380), (950, 600), (978, 420))): d.line((X - 40, y, X - 40 + l, y), fill=NEON + (200 - i * 30,), width=6 - i % 2 * 2)
    c.append(('riscos', r.filter(ImageFilter.GaussianBlur(1))))
    pl = novo(); d = ImageDraw.Draw(pl); f = FI('BlackItalic', 42); w = d.textlength('SÁBADO 21/11', font=f)
    d.polygon([(X + 18, 250), (X + w + 74, 250), (X + w + 56, 326), (X, 326)], fill=NEON); d.text((X + 36, 288), 'SÁBADO 21/11', font=f, fill=NOITE, anchor='lm'); c.append(('data', pl))
    t = txt((X, 470), 'ACELERA', FI('BlackItalic', 190), BR); gl = novo(); ImageDraw.Draw(gl).text((X, 470), 'ACELERA', font=FI('BlackItalic', 190), fill=NEON + (140,), anchor='lm')
    c.append(('titulo-1', juntar(gl.filter(ImageFilter.GaussianBlur(28)), t)))
    c.append(('titulo-2', txt((X + 10, 620), 'pra essa PCX ser sua!', FI('ExtraBoldItalic', 62), NEON)))
    c.append(('sub', txt((X + 10, 710), 'Honda PCX 160 · branca perolizada', FD('Medium', 40), BR, sombra_=(0, 0, 0, 120))))
    p = novo(); d = ImageDraw.Draw(p); d.text((X + 10, 800), 'LANCE INICIAL', font=FI('BoldItalic', 32), fill=NEON, anchor='lm'); d.text((X + 10, 875), f'R$ {real(LANCE)}', font=FI('BlackItalic', 110), fill=BR, anchor='lm')
    c.append(('preco', p)); c.append(('rodape', txt((X + 10, 1020), 'retirada em mãos com a equipe Leilão no Zap', FD('Medium', 28), (200, 215, 205), sombra_=None)))
    salvar('B-velocidade-neon', c)

# C · POP — letras amarelas com contorno escuro, selo de preço girado tipo adesivo
if 'C' in SO and os.path.exists(f'{AQ}/em-cima-C.jpg'):
    X = 110; c = []
    c.append(('foto', foto(f'{AQ}/em-cima-C.jpg'))); c.append(('sombra', sombra((14, 70, 40), .5, 170))); c.append(('logo', logo(X, 70)))
    pl = novo(); d = ImageDraw.Draw(pl); f = FD('Black', 46); w = d.textlength('SÁBADO · 21/11', font=f); d.rounded_rectangle((X, 255, X + w + 60, 335), 40, fill=BR); d.text((X + 30, 296), 'SÁBADO · 21/11', font=f, fill=VERDE, anchor='lm'); c.append(('data', pl))
    def adesivo(xy, t, f, cor):
        k = novo(); d = ImageDraw.Draw(k); d.text((xy[0] + 8, xy[1] + 10), t, font=f, fill=(6, 40, 22, 255), anchor='lm', stroke_width=16, stroke_fill=(6, 40, 22)); d.text(xy, t, font=f, fill=cor, anchor='lm', stroke_width=14, stroke_fill=NOITE); return k
    c.append(('titulo-1', adesivo((X, 440), 'BORA', FD('Black', 150), BR))); c.append(('titulo-2', adesivo((X, 595), 'DE PCX?', FD('Black', 150), OURO)))
    c.append(('sub', txt((X + 6, 715), 'Honda PCX 160 · branca perolizada', FD('Bold', 40), BR, sombra_=(0, 0, 0, 140))))
    s = Image.new('RGBA', (480, 220)); d = ImageDraw.Draw(s); d.rounded_rectangle((10, 10, 470, 210), 36, fill=OURO, outline=NOITE, width=9)
    d.text((240, 62), 'LANCE INICIAL', font=FD('Black', 32), fill=NOITE, anchor='mm'); d.text((240, 142), f'R$ {real(LANCE)}', font=FD('Black', 96), fill=NOITE, anchor='mm')
    s = s.rotate(6, resample=Image.BICUBIC, expand=True); p = novo(); sh = Image.new('RGBA', s.size, (0, 0, 0, 0)); sh.putalpha(s.split()[3].point(lambda v: v * .5))
    p.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (X + 12, 770)); p.alpha_composite(s, (X - 4, 756)); c.append(('preco', p))
    c.append(('rodape', txt((X + 6, 1052), 'retirada em mãos com a equipe Leilão no Zap', FD('SemiBold', 26), BR, sombra_=(0, 0, 0, 120))))
    salvar('C-pop-verde-e-ouro', c)
