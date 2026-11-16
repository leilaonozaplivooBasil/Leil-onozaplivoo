# MacBook Neo PRATEADO (foto oficial da Apple, real) montado numa mesa de madeira perto da janela (cenário gerado no Gamma,
# SEM produto). O produto nunca é desenhado por IA: é a foto oficial, com sombra de contato e luz da janela. Uso:
#   macbook_na_mesa.py <cenario.png> <saida.jpg> <cx 0-1> <base_y 0-1> <largura 0-1> <inclinação graus> <luz: esq|dir>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
AQ = os.path.dirname(os.path.abspath(__file__))
cen, out, cx, by, lw, ang, luz = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
bg = Image.open(cen).convert('RGBA'); W, H = bg.size
p = Image.open(f'{AQ}/fotos/apple-silver-frente.png').convert('RGBA'); larg = int(W * lw); p = p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)

def perspectiva(im, graus):
    """vira o MacBook um pouco de lado: o lado mais longe fica menor (perspectiva simples)"""
    if abs(graus) < .5: return im
    w, h = im.size; k = np.tan(np.radians(abs(graus))) * .22; enc = h * k
    if graus > 0: quad = (0, 0, 0, h, w, h - enc, w, enc)      # lado direito mais longe
    else: quad = (0, enc, 0, h - enc, w, h, w, 0)
    novo_w = int(w * np.cos(np.radians(abs(graus)))); tmp = im.transform((w, h), Image.QUAD, quad, Image.BICUBIC)
    return tmp.resize((novo_w, h), Image.LANCZOS)

p = perspectiva(p, ang)
# casa a cor do produto com a cena: um pouco mais quente e menos contraste (luz do dia)
rgb = p.convert('RGB'); rgb = ImageEnhance.Brightness(ImageEnhance.Contrast(rgb).enhance(.9)).enhance(.9); r, g, b = rgb.split()
rgb = Image.merge('RGB', (r.point(lambda v: min(255, int(v * 1.03))), g, b.point(lambda v: int(v * .96)))); q = rgb.convert('RGBA'); q.putalpha(p.split()[3]); p = q
x = int(W * cx - p.width / 2); base = int(H * by); y = base - p.height
# brilho da janela num lado do alumínio
gl = Image.new('L', p.size, 0); gd = ImageDraw.Draw(gl)
for i in range(p.width):
    t = i / p.width; t = (1 - t) if luz == 'esq' else t; gd.line((i, 0, i, p.height), fill=int(26 * t ** 2))
br = Image.new('RGBA', p.size, (255, 248, 235, 0)); br.putalpha(Image.fromarray(np.minimum(np.asarray(gl), np.asarray(p.split()[3]))))
# sombras: contato (bem escura e fina) + projetada para o lado oposto da janela
s = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(s)
d.ellipse((x + p.width * .02, base - 10, x + p.width * .98, base + 12), fill=(20, 12, 6, 200)); bg.alpha_composite(s.filter(ImageFilter.GaussianBlur(6)))
s = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(s); dx = p.width * (.10 if luz == 'esq' else -.10)
d.polygon([(x + dx, base - 6), (x + p.width + dx, base - 6), (x + p.width * .95 + dx * 2.2, base + p.height * .10), (x + p.width * .05 + dx * 2.2, base + p.height * .10)], fill=(30, 18, 8, 120))
bg.alpha_composite(s.filter(ImageFilter.GaussianBlur(26)))
s = Image.new('RGBA', (W, H)); s.paste((25, 15, 8, 255), (x + int(dx * .6), y + 18), p.split()[3].point(lambda v: int(v * .35))); bg.alpha_composite(s.filter(ImageFilter.GaussianBlur(30)))
bg.alpha_composite(p, (x, y)); bg.alpha_composite(br, (x, y))
# reflexo bem leve da tela colorida na madeira, logo à frente
tela = p.crop((0, 0, p.width, int(p.height * .9))).transpose(Image.FLIP_TOP_BOTTOM).resize((p.width, int(p.height * .18)))
m = Image.linear_gradient('L').resize(tela.size).point(lambda v: int((255 - v) * .10)); tela.putalpha(Image.fromarray(np.minimum(np.asarray(tela.split()[3]), np.asarray(m))))
bg.alpha_composite(tela.filter(ImageFilter.GaussianBlur(6)), (x, base + 4))
bg.convert('RGB').save(out, quality=94); print('ok', out, bg.size)
