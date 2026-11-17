# ESTILO D · ALERTA CURTO (17/11, "as pessoas estão com preguiça de ler": claro, urgente, útil e único).
# Fundo vermelho, faixas de perigo, poucas palavras: o 19H gigante. Urgente = prazo; útil = o que fazer; único = MacBook amanhã.
import os
from PIL import Image, ImageDraw, ImageFont
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AMA, PRETO, VERM, VERM2, BR = (255, 210, 0), (15, 15, 15), (214, 22, 32), (150, 8, 16), (255, 255, 255)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')

def cabe(d, t, tam, larg, peso='Black'):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 18: tam -= 2
    return F(peso, tam)
def faixa(b, y, h):
    W = b.width; s = Image.new('RGBA', (W + 2 * h, h), AMA); d = ImageDraw.Draw(s); w = int(h * .9)
    for x in range(-h, W + 2 * h, 2 * w): d.polygon([(x, h), (x + w, h), (x + w + h, 0), (x + h, 0)], fill=PRETO)
    b.alpha_composite(s.crop((h, 0, h + W, h)), (0, int(y)))
def tri(d, cx, cy, r):
    p = [(cx, cy - r), (cx + r * .95, cy + r * .72), (cx - r * .95, cy + r * .72)]; d.polygon(p, fill=AMA)
    d.line(p + [p[0]], fill=PRETO, width=max(6, int(r * .1)), joint='curve'); d.text((cx, cy + r * .2), '!', font=F('Black', int(r * 1.15)), fill=PRETO, anchor='mm')
def txt(d, W, y, t, tam, cor, peso='Black', sombra=True):
    f = cabe(d, t, tam, W * .92, peso)
    if sombra: d.text((W / 2 + 6, y + 8), t, font=f, fill=VERM2, anchor='mm')
    d.text((W / 2, y), t, font=f, fill=cor, anchor='mm'); return f.size
def fundo(W, H):
    b = Image.new('RGBA', (W, H), VERM + (255,)); d = ImageDraw.Draw(b)
    for i in range(0, max(W, H) * 2, 90): d.line((i, 0, i - H, H), fill=(200, 18, 28), width=40)   # textura diagonal sutil
    return b

def peca(W, H, nome, u, y):
    b = fundo(W, H); fh = int(80 * u); faixa(b, 0, fh); faixa(b, H - fh, fh); d = ImageDraw.Draw(b)
    tri(d, W / 2, y['tri'], int(110 * u))
    txt(d, W, y['at'], 'ATENÇÃO!', int(130 * u), AMA)
    txt(d, W, y['l1'], '1º LANCE ATÉ AS', int(96 * u), BR)
    txt(d, W, y['h'], '19H', int(400 * u), AMA)
    # tarja preta: a consequência
    d.rounded_rectangle((W * .05, y['tarja'], W * .95, y['tarja'] + y['tarja_h']), int(24 * u), fill=PRETO)
    txt(d, W, y['tarja'] + y['tarja_h'] / 2, 'OU FICA DE FORA DO LEILÃO', int(66 * u), BR, sombra=False)
    txt(d, W, y['quando'], 'MACBOOK · AMANHÃ (QUA) · FECHA 20H', int(54 * u), AMA, sombra=False)
    if y.get('logo'):
        lg = LOGO.copy(); lg.thumbnail((int(150 * u), int(150 * u))); d.rounded_rectangle((W / 2 - lg.width / 2 - 20, y['logo'] - 10, W / 2 + lg.width / 2 + 20, y['logo'] + lg.height + 10), 18, fill=PRETO)
        b.alpha_composite(lg, (int(W / 2 - lg.width / 2), y['logo']))
    b.convert('RGB').save(f'{OUT}/{nome}', quality=94); print('ok', nome)

peca(1080, 1920, 'D-URGENTE-story-status-1080x1920.jpg', 1.0, dict(tri=270, at=470, l1=640, h=900, tarja=1150, tarja_h=150, quando=1400, logo=1600))
peca(1080, 1350, 'D-URGENTE-feed-1080x1350.jpg', .8, dict(tri=200, at=350, l1=475, h=680, tarja=880, tarja_h=125, quando=1100, logo=1150 + 20))
peca(1080, 1080, 'D-URGENTE-whatsapp-1080x1080.jpg', .66, dict(tri=165, at=290, l1=390, h=560, tarja=715, tarja_h=105, quando=900))

# site: faixa 1920x500
W, H = 1920, 500; b = fundo(W, H); faixa(b, 0, 44); faixa(b, H - 44, 44); d = ImageDraw.Draw(b); tri(d, 190, 250, 120)
d.text((350, 165), 'ATENÇÃO! 1º LANCE ATÉ AS', font=F('Black', 76), fill=BR, anchor='lm')
d.text((1640, 250), '19H', font=F('Black', 230), fill=AMA, anchor='mm')
d.rounded_rectangle((340, 225, 1330, 315), 18, fill=PRETO); d.text((835, 270), 'OU FICA DE FORA DO LEILÃO', font=F('Black', 56), fill=BR, anchor='mm')
d.text((350, 380), 'MACBOOK · AMANHÃ (QUARTA) · FECHA 20H', font=F('Black', 44), fill=AMA, anchor='lm')
b.convert('RGB').save(f'{OUT}/D-URGENTE-site-faixa-1920x500.jpg', quality=94); print('ok faixa')
