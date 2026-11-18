# Capa "fofoca" com RECORTE (19/11): a foto da Natália falando com o Ribeiro colada inclinada, tipo revista de fofoca,
# sobre o galpão desfocado; título no alto sem cobrir rosto. Uso: capa_recorte.py <quadro_4k.png> <saida.jpg>
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC, OUT = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; W, H = 1080, 1920
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
LARANJA, AMARELO, VERDE, BRANCO, ESC = (240, 96, 40), (245, 196, 81), (27, 122, 72), (255, 255, 255), (5, 28, 17)
q = Image.open(SRC).convert('RGB')
fundo = q.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26)).convert('RGBA'); fundo.alpha_composite(Image.new('RGBA', (W, H), ESC + (170,)))
foto = q.crop((0, 760, 2160, 2980)).resize((900, 924), Image.LANCZOS)          # ela falando + o Ribeiro, do rosto à cintura
card = Image.new('RGBA', (940, 1010), (255, 255, 255, 255)); card.paste(foto, (20, 20))
ImageDraw.Draw(card).text((470, 978), 'flagra no galpão 📸'.replace(' 📸', ''), font=F('Bold', 34), fill=(40, 40, 40), anchor='mm')
card = card.rotate(-4, resample=Image.BICUBIC, expand=True)
sh = Image.new('RGBA', (W, H)); m = card.split()[3]; sh_ = Image.new('RGBA', card.size, (0, 0, 0, 160)); sh_.putalpha(m.point(lambda v: v * .6))
sh.alpha_composite(sh_, (int(W / 2 - card.width / 2) + 14, 640 + 22)); fundo.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
fundo.alpha_composite(card, (int(W / 2 - card.width / 2), 640))
# fita adesiva no canto
fita = Image.new('RGBA', (220, 60), (245, 230, 180, 200)); fita = fita.rotate(30, expand=True); fundo.alpha_composite(fita, (40, 600))
fita2 = Image.new('RGBA', (220, 60), (245, 230, 180, 200)).rotate(-28, expand=True); fundo.alpha_composite(fita2, (W - 260, 620))
d = ImageDraw.Draw(fundo)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((170, 70)); fundo.alpha_composite(lg, ((W - lg.width) // 2, 70))
def pilula(cy, t, f, cor_f, cor):
    w = d.textlength(t, font=f); h = f.size + 34; d.rounded_rectangle((540 - w / 2 - 34, cy - h / 2, 540 + w / 2 + 34, cy + h / 2), h / 2, fill=cor_f); d.text((540, cy), t, font=f, fill=cor, anchor='mm')
def contorno(xy, t, f, cor):
    for dx, dy in ((0, 7), (3, 5), (-3, 5)): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0, 170), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
pilula(205, 'FOFOCA DO GALPÃO', F('Black', 38), LARANJA, BRANCO)
contorno((540, 330), 'FOMOS NO GALPÃO', F('Black', 100), BRANCO); contorno((540, 450), 'E OLHA O QUE ACHAMOS', F('Black', 82), AMARELO)
pilula(1760, 'você não vai acreditar 👀'.replace(' 👀', ''), F('Bold', 48), VERDE, BRANCO)
fundo.convert('RGB').save(OUT, quality=93); print('ok')
