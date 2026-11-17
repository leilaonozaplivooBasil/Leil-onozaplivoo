# 3 artes de story (17/11) com ESPAÇO LIVRE para a figurinha do Instagram: enquete do MacBook, caixinha de perguntas e
# contagem regressiva para o leilão de amanhã. Verde da marca + dourado + logo. Sem link e sem %.
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
BR, OURO, OURO2, VERDE2, ESC, CREME = (255, 255, 255), (245, 196, 81), (246, 214, 140), (27, 122, 72), (5, 28, 17), (214, 230, 218)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')

def fundo(cy=800):
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - cy) * .85) / 1150, 0, 1) ** 1.2
    a = np.array((24, 88, 56))[None, None] * (1 - dd[..., None]) + np.array(ESC)[None, None] * dd[..., None]
    a += np.random.default_rng(2).normal(0, 1.5, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def cabe(d, t, peso, tam, larg=W * .88):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 20: tam -= 2
    return F(peso, tam)
def txt(d, y, t, peso, tam, cor, sombra=True):
    f = cabe(d, t, peso, tam)
    if sombra: d.text((W / 2, y + 6), t, font=f, fill=(0, 0, 0, 150), anchor='mm')
    d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def pil(d, y, t, f, fundo_, cor):
    w = d.textlength(t, font=f); h = f.size + 30
    d.rounded_rectangle((W / 2 - w / 2 - 34, y - h / 2, W / 2 + w / 2 + 34, y + h / 2), h / 2, fill=fundo_); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def logo(b, y=120, larg=190):
    lg = LOGO.copy(); lg.thumbnail((larg, larg)); b.alpha_composite(lg, ((W - lg.width) // 2, y))
def seta(d, y):
    d.text((W / 2, y), '⌄', font=F('Black', 10), fill=OURO)  # (reserva)
    d.polygon([(W / 2 - 34, y), (W / 2 + 34, y), (W / 2, y + 40)], fill=OURO)
def brilho(b, cx, cy, r, a=90):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=OURO + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * .5)))
def salvar(b, n): b.convert('RGB').save(f'{OUT}/{n}', quality=94); print('ok', n)

# 1 · ENQUETE do MacBook (espaço livre: y 1250–1600)
b = fundo(720); logo(b); d = ImageDraw.Draw(b)
pil(d, 330, 'CHUTA AÍ 👀'.replace(' 👀', ''), F('Black', 44), OURO, ESC)
txt(d, 470, 'POR QUANTO SAI', 'Black', 104, BR); txt(d, 590, 'O MACBOOK AMANHÃ?', 'Black', 104, OURO)
brilho(b, W / 2, 960, 300, 60); mw = 660; mm = MAC.resize((mw, int(MAC.height * mw / MAC.width)), Image.LANCZOS)
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 320, 1130, W / 2 + 320, 1170), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(20)))
b.alpha_composite(mm, ((W - mw) // 2, 1150 - mm.height)); d = ImageDraw.Draw(b)
d.text((W / 2, 1225), f'lance atual: R$ {LANCE}  ·  quarta, 20h', font=F('SemiBold', 40), fill=CREME, anchor='mm')
seta(d, 1275)
d.text((W / 2, 1740), 'MacBook Neo 13" · prateado · novo e lacrado', font=F('Medium', 36), fill=CREME, anchor='mm')
salvar(b, 'STORY-enquete-macbook.jpg')

# 2 · CAIXINHA DE PERGUNTAS (espaço livre: y 1000–1450)
b = fundo(1100); logo(b); d = ImageDraw.Draw(b)
d.ellipse((W / 2 - 120, 300, W / 2 + 120, 540), fill=OURO); d.text((W / 2, 425), '?', font=F('Black', 200), fill=ESC, anchor='mm')
txt(d, 660, 'QUAIS SÃO', 'Black', 120, BR); txt(d, 790, 'SUAS DÚVIDAS?', 'Black', 120, OURO)
d.text((W / 2, 900), 'leilão, cadastro, lance, entrega… pergunta aqui 👇'.replace(' 👇', ''), font=cabe(d, 'leilão, cadastro, lance, entrega… pergunta aqui', 'SemiBold', 42), fill=CREME, anchor='mm')
seta(d, 950)
pil(d, 1640, 'a gente responde tudo nos stories', F('Black', 40), VERDE2, BR)
salvar(b, 'STORY-caixinha-de-perguntas.jpg')

# 3 · CONTAGEM REGRESSIVA (espaço livre: y 1080–1450)
b = fundo(760); logo(b); d = ImageDraw.Draw(b)
pil(d, 330, 'CONTAGEM REGRESSIVA', F('Black', 44), OURO, ESC)
txt(d, 470, 'AMANHÃ ÀS', 'Black', 110, BR); txt(d, 640, '20H', 'Black', 240, OURO)
mw = 480; mm = MAC.resize((mw, int(MAC.height * mw / MAC.width)), Image.LANCZOS); b.alpha_composite(mm, ((W - mw) // 2, 1110 - mm.height)); d = ImageDraw.Draw(b)
d.text((W / 2, 1160), 'o martelo bate no MacBook Neo', font=F('SemiBold', 42), fill=CREME, anchor='mm')
seta(d, 1205)
d.rounded_rectangle((W * .08, 1560, W * .92, 1700), 30, fill=(150, 20, 28)); d.text((W / 2, 1605), '⚠ 1º LANCE SÓ ATÉ AS 19H'.replace('⚠ ', ''), font=F('Black', 52), fill=BR, anchor='mm')
d.text((W / 2, 1662), 'depois disso, fica de fora', font=F('SemiBold', 36), fill=(255, 220, 220), anchor='mm')
salvar(b, 'STORY-contagem-regressiva.jpg')
