# 8 capas "modo fofoca" do Ribeiro no galpão (19/11), no molde da Fofoca do escritório (É golpe?): topo escuro, logo, pílula laranja,
# título branco + linha amarela, pílula verde com a frase que dá curiosidade. Uso: capas_fofoca.py <pasta_quadros> <saida>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
IN, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'; F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
LARANJA, AMARELO, VERDE, BRANCO, ESC = (240, 96, 40), (245, 196, 81), (27, 122, 72), (255, 255, 255), (5, 28, 17)
CAPAS = [('q69.0', 'FOFOCA DO GALPÃO', 'FOMOS NO GALPÃO', 'E OLHA O QUE ACHAMOS', 'você não vai acreditar'),
         ('q177', 'EXPOSED', 'TUDO QUE TÁ NO SITE', 'TÁ AQUI MESMO?', 'a gente foi conferir'),
         ('q162', 'FOFOCA DO GALPÃO', 'NOVA, ZERADA', 'E NUNCA USADA?!', 'olha o que ele mostrou'),
         ('q183.2', 'FLAGRA', 'PERGUNTEI O VALOR', 'OLHA A CARA DELE', 'não tem comparação'),
         ('q75.5', 'BASTIDOR', 'O QUE NINGUÉM', 'TE MOSTRA', 'o galpão do Leilão no Zap'),
         ('q129.5', 'FOFOCA DO GALPÃO', 'LEMBRA A CASA', 'DA SUA AVÓ?', 'ele achou isso no galpão'),
         ('q124', 'FOMOS INVESTIGAR', 'EXISTE MESMO', 'ESSE GALPÃO?', 'abrimos as portas'),
         ('q190.5', 'FOFOCA BOMBA', 'ACHOU, LEVOU.', 'PISCOU, PERDEU.', 'ele avisou')]
def cabe(d, t, peso, tam, larg):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 40: tam -= 4
    return F(peso, tam)
def pilula(d, cy, t, f, fundo, cor):
    w = d.textlength(t, font=f); h = f.size + 34
    d.rounded_rectangle((540 - w / 2 - 34, cy - h / 2, 540 + w / 2 + 34, cy + h / 2), h / 2, fill=fundo); d.text((540, cy), t, font=f, fill=cor, anchor='mm')
def contorno(d, xy, t, f, cor):
    for dx, dy in ((0, 7), (3, 5), (-3, 5)): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0, 170), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
grade = []
for i, (q, pil, l1, l2, sub) in enumerate(CAPAS, start=1):
    b = Image.open(f'{IN}/{q}.png').convert('RGBA')
    g = np.zeros((1920, 1080, 4), np.uint8); g[..., :3] = ESC; g[:820, :, 3] = (np.linspace(1, 0, 820) ** 1.2 * 235)[:, None].astype(np.uint8)
    b.alpha_composite(Image.fromarray(g)); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((170, 70)); b.alpha_composite(lg, ((1080 - lg.width) // 2, 70))
    d = ImageDraw.Draw(b); pilula(d, 210, pil, F('Black', 38), LARANJA, BRANCO)
    f1 = cabe(d, l1, 'Black', 120, 990); contorno(d, (540, 335), l1, f1, BRANCO); y = 335 + f1.size * .55
    f2 = cabe(d, l2, 'Black', 120, 990); contorno(d, (540, y + f2.size * .55), l2, f2, AMARELO); y += f2.size * 1.1
    pilula(d, y + 70, sub, F('Bold', 42), VERDE, BRANCO)
    d.text((1040, 1880), f'{i:02d}', font=F('Bold', 34), fill=(255, 255, 255, 160), anchor='rs')
    b.convert('RGB').save(f'{OUT}/capa-{i:02d}.jpg', quality=92); grade.append(b.convert('RGB').resize((270, 480)))
s = Image.new('RGB', (270 * 4, 480 * 2))
for i, im in enumerate(grade): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
s.save(f'{OUT}/TODAS-as-8-capas.jpg', quality=90); print('ok')
