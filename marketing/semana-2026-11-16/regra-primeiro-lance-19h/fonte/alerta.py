# ESTILO C · ALERTA (17/11, pedido da Natália: "bem chamativo para ninguém reclamar"): faixas de perigo amarelo/preto,
# triângulo de alerta, vermelho para a regra. Mesmo conteúdo (vale no leilão do MacBook de qua 18/11, fecha 20h).
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AMA, PRETO, VERM, BR, ESC, OURO = (255, 205, 0), (18, 18, 18), (220, 30, 38), (255, 255, 255), (5, 28, 17), (245, 196, 81)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')

def cabe(d, t, peso, tam, larg):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 18: tam -= 2
    return F(peso, tam)
def faixa(b, y, h):
    W = b.width; s = Image.new('RGBA', (W + 2 * h, h), AMA); d = ImageDraw.Draw(s); w = int(h * .9)
    for x in range(-h, W + 2 * h, 2 * w): d.polygon([(x, h), (x + w, h), (x + w + h, 0), (x + h, 0)], fill=PRETO)
    b.alpha_composite(s.crop((h, 0, h + W, h)), (0, int(y)))
def triangulo(d, cx, cy, r):
    p = [(cx, cy - r), (cx + r * .95, cy + r * .72), (cx - r * .95, cy + r * .72)]
    d.polygon(p, fill=AMA); d.line(p + [p[0]], fill=PRETO, width=max(6, int(r * .1)), joint='curve')
    d.text((cx, cy + r * .2), '!', font=F('Black', int(r * 1.15)), fill=PRETO, anchor='mm')
def logo(b, cx, y, larg):
    lg = LOGO.copy(); lg.thumbnail((larg, larg)); b.alpha_composite(lg, (int(cx - lg.width / 2), int(y)))
def centro(d, W, y, t, peso, tam, cor, larg=None):
    f = cabe(d, t, peso, tam, larg or W * .9); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm'); return f.size

def alerta(W, H, nome, u, ys):
    b = Image.new('RGBA', (W, H), PRETO + (255,)); fh = int(70 * u); faixa(b, 0, fh); faixa(b, H - fh, fh); d = ImageDraw.Draw(b)
    triangulo(d, W / 2, ys['tri'], int(120 * u))
    centro(d, W, ys['atencao'], 'ATENÇÃO!', 'Black', int(150 * u), AMA)
    centro(d, W, ys['mudou'], 'A REGRA DO LEILÃO MUDOU', 'Black', int(62 * u), BR)
    # bloco vermelho com a regra
    d.rounded_rectangle((W * .05, ys['bloco'], W * .95, ys['bloco'] + ys['bloco_h']), int(30 * u), fill=VERM)
    centro(d, W, ys['bloco'] + ys['bloco_h'] * .28, 'PRIMEIRO LANCE', 'Black', int(84 * u), BR, W * .82)
    centro(d, W, ys['bloco'] + ys['bloco_h'] * .68, 'SÓ ATÉ AS 19H', 'Black', int(120 * u), AMA, W * .82)
    y = ys['corpo']
    for t, peso, cor in (('Quem não der o primeiro lance até as 19h', 'Bold', BR), ('NÃO PARTICIPA do leilão.', 'Black', AMA),
                          ('Vale para TODOS: clientes novos e antigos.', 'Bold', BR)):
        s_ = centro(d, W, y, t, peso, int(46 * u), cor, W * .88); y += s_ * 1.35
    d.rounded_rectangle((W * .08, ys['box'], W * .92, ys['box'] + ys['box_h']), int(26 * u), outline=AMA, width=max(3, int(4 * u)))
    centro(d, W, ys['box'] + ys['box_h'] * .33, 'JÁ VALE AMANHÃ', 'Black', int(46 * u), AMA, W * .78)
    centro(d, W, ys['box'] + ys['box_h'] * .70, 'MacBook Neo · quarta, 18/11 · fecha às 20h', 'SemiBold', int(38 * u), BR, W * .78)
    if ys.get('logo'): logo(b, W / 2, ys['logo'], int(150 * u))
    b.convert('RGB').save(f'{OUT}/{nome}', quality=94); print('ok', nome)

alerta(1080, 1920, 'C-ALERTA-story-status-1080x1920.jpg', 1.0, dict(tri=250, atencao=470, mudou=590, bloco=680, bloco_h=330, corpo=1110, box=1370, box_h=200, logo=1640))
alerta(1080, 1350, 'C-ALERTA-feed-1080x1350.jpg', .82, dict(tri=180, atencao=335, mudou=430, bloco=490, bloco_h=270, corpo=830, box=1040, box_h=165))
alerta(1080, 1080, 'C-ALERTA-whatsapp-1080x1080.jpg', .68, dict(tri=150, atencao=275, mudou=350, bloco=395, bloco_h=225, corpo=680, box=860, box_h=135))

# site: faixa de alerta 1920x500
W, H = 1920, 500; b = Image.new('RGBA', (W, H), PRETO + (255,)); faixa(b, 0, 46); faixa(b, H - 46, 46); d = ImageDraw.Draw(b)
triangulo(d, 210, 250, 130)
d.text((400, 140), 'ATENÇÃO: A REGRA MUDOU!', font=F('Black', 70), fill=AMA, anchor='lm')
d.rounded_rectangle((390, 195, 1520, 285), 20, fill=VERM); d.text((415, 240), 'PRIMEIRO LANCE SÓ ATÉ AS 19H', font=F('Black', 64), fill=BR, anchor='lm')
d.text((400, 330), 'Quem não der o primeiro lance até as 19h NÃO PARTICIPA do leilão. Vale para todos.', font=cabe(d, 'Quem não der o primeiro lance até as 19h NÃO PARTICIPA do leilão. Vale para todos.', 'Bold', 40, 1460), fill=BR, anchor='lm')
d.text((400, 395), 'Já vale amanhã: MacBook Neo · quarta, 18/11 · fecha às 20h', font=F('Black', 38), fill=AMA, anchor='lm')
b.convert('RGB').save(f'{OUT}/C-ALERTA-site-faixa-1920x500.jpg', quality=94); print('ok faixa')
