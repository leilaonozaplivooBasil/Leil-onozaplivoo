# Carrossel de FEED (1080x1350) com os arrematados, a partir dos 3 stories que trouxeram seguidores (23/11).
# Reaproveita os cards do vitrine_arrematados.py. 1 = pergunta + PCX · 2 = iPhones, MacBook, PS5 · 3 = TV + pedido único.
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ)
src = open(f'{AQ}/vitrine_arrematados.py').read().split("destaque('STORY-1")[0]
g = {'__file__': f'{AQ}/vitrine_arrematados.py', '__name__': 'vitrine'}; exec(compile(src, 'vitrine', 'exec'), g)
F, card, VE, MENTA, BR, NEON = g['F'], g['card'], g['VE'], g['MENTA'], g['BR'], g['NEON']
W, H = 1080, 1350
def fundo():
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 650) * .85) / 1000, 0, 1) ** 1.2
    a = np.array((30, 108, 66))[None, None] * (1 - dd[..., None]) + np.array((12, 62, 38))[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
    b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); r = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(r)
    for i in range(26): yy = 120 + i * 52; d.line((0, yy, W, yy + 40), fill=(255, 255, 255, 12), width=2)
    b.alpha_composite(r); return b
def sombra(b, x, y, c):
    s = Image.new('RGBA', (W, H)); s.paste((0, 0, 0, 90), (x + 8, y + 14, x + c.width + 8, y + c.height + 14), c.split()[3]); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14))); b.alpha_composite(c, (x, y))
def pag(d, n): d.text((W - 50, 52), f'{n}/3', font=F('Bold', 28), fill=MENTA, anchor='rm')
def pil(d, cy, t, f, fu, co, px=34):
    w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - px, cy - f.size * .85, W / 2 + w / 2 + px, cy + f.size * .85), f.size, fill=fu); d.text((W / 2, cy), t, font=f, fill=co, anchor='mm')
# (23/11) Natália: a moto já tem 2 posts no feed → capa com iPhones, MacBook e PS5; a moto na página 2; página 3 chama pra quarta.
# 1 · capa (útil): os 4 arrematados que não são a moto
b = fundo(); d = ImageDraw.Draw(b); pag(d, 1)
d.text((W / 2, 90), 'QUANTO SAIU CADA UM', font=F('Black', 64), fill=BR, anchor='mm'); d.text((W / 2, 162), 'NO LEILÃO?', font=F('Black', 64), fill=NEON, anchor='mm')
sombra(b, 60, 220, card('iphone18', 465, 490)); sombra(b, 555, 220, card('iphone17', 465, 490))
sombra(b, 60, 735, card('macbook', 465, 470)); sombra(b, 555, 735, card('ps5', 465, 470)); d = ImageDraw.Draw(b)
pil(d, 1268, 'valores reais · arrasta pro lado  →', F('Bold', 32), BR, VE, 36)
b.convert('RGB').save(f'{OUT}/CARROSSEL-arrematados-1.jpg', quality=94)
# 2 · a moto (único)
b = fundo(); d = ImageDraw.Draw(b); pag(d, 2)
d.text((W / 2, 95), 'ATÉ MOTO', font=F('Black', 70), fill=BR, anchor='mm'); d.text((W / 2, 170), 'SAIU NO LEILÃO', font=F('Black', 64), fill=NEON, anchor='mm')
sombra(b, 60, 235, card('pcx', 960, 830)); d = ImageDraw.Draw(b)
pil(d, 1180, 'sem preço de etiqueta: quem decide é quem dá o lance', F('Bold', 30), BR, VE, 30)
d.text((W / 2, 1268), 'tudo ao vivo', font=F('Medium', 30), fill=MENTA, anchor='mm')
b.convert('RGB').save(f'{OUT}/CARROSSEL-arrematados-2.jpg', quality=94)
# 3 · TV + chamada da quarta (a versão que a Natália preferiu)
b = fundo(); d = ImageDraw.Draw(b); pag(d, 3)
d.text((W / 2, 85), 'QUARTA, 20H', font=F('Black', 72), fill=NEON, anchor='mm'); d.text((W / 2, 155), 'o próximo pode ser seu', font=F('Black', 44), fill=BR, anchor='mm')   # urgente
sombra(b, 180, 205, card('tv', 720, 545)); d = ImageDraw.Draw(b)
d.rounded_rectangle((90, 820, W - 90, 1130), 40, fill=BR)
d.text((W / 2, 880), 'QUER ENTRAR ANTES DE QUARTA?', font=F('Black', 42), fill=(27, 122, 72), anchor='mm')
d.text((W / 2, 985), 'Comenta LEILÃO', font=F('Black', 92), fill=VE, anchor='mm')
d.text((W / 2, 1075), 'que eu te mando o link no direct', font=F('Medium', 36), fill=(27, 122, 72), anchor='mm')
lg = Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((200, 200)); b.alpha_composite(lg, ((W - lg.width) // 2, 1190))
b.convert('RGB').save(f'{OUT}/CARROSSEL-arrematados-3.jpg', quality=94)
print('ok')
