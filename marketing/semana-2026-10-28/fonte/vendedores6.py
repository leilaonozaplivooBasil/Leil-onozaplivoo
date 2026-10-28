# Artes do grupo — versão 6 (28/10/2026): cópia fiel do layout da arte do iPhone, em VERDE ESCURO, com a máquina em evidência.
# Uso: python3 vendedores6.py <lance> <tempo ex.: "3 HORAS"> <saida.jpg>
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import vendedores3 as v3
from kit import AQUI

W, H = 1080, 1620


def fundo_escuro():
    y = np.linspace(0, 1, H)[:, None, None]
    base = (np.array([8, 92, 36]) * (1 - y) + np.array([3, 52, 20]) * y).astype('uint8').repeat(W, 1)
    im = Image.fromarray(base, 'RGB').convert('RGBA')

    def plano(pts, cor, alfa):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(c).polygon([(x * W, y * H) for x, y in pts], fill=cor + (alfa,))
        im.alpha_composite(c.filter(ImageFilter.GaussianBlur(1.2)))

    escuro, claro = (1, 30, 11), (30, 140, 60)
    plano([(0, 0), (0.58, 0), (0, 0.40)], escuro, 110)
    plano([(0.58, 0), (1, 0), (1, 0.16), (0, 0.66), (0, 0.40)], claro, 55)
    plano([(1, 0.16), (1, 0.30), (0.12, 0.64), (0, 0.66)], claro, 28)
    plano([(1, 0.30), (1, 0.62), (0.2, 1), (0, 1), (0, 0.66), (0.12, 0.64)], escuro, 70)
    plano([(1, 0.62), (1, 0.70), (0.36, 1), (0.2, 1)], claro, 35)
    plano([(1, 0.70), (1, 1), (0.36, 1)], escuro, 110)
    for cx, cy, r, cor, a in [(0.32, 0.56, 0.38, (90, 230, 90), 115), (0.5, 0.05, 0.5, (60, 180, 90), 40)]:
        g = Image.new('L', (W, H), 0)
        ImageDraw.Draw(g).ellipse(((cx - r) * W, cy * H - r * W, (cx + r) * W, cy * H + r * W), fill=a)
        c = Image.new('RGBA', (W, H), cor + (0,))
        c.putalpha(g.filter(ImageFilter.GaussianBlur(120)))
        im.alpha_composite(c)
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    v = (np.clip((d - 0.38) / 0.35, 0, 1) * 140).astype('uint8')
    return Image.composite(Image.new('RGBA', (W, H), (0, 18, 6, 255)), im, Image.fromarray(v, 'L'))


v3.fundo_facetado = fundo_escuro
from PIL import ImageEnhance
from vendedores2 import recortar, LIMA


def produto_destaque(b, foto, cx=320, base_y=1395, altura=615, ang=-5):
    """A máquina em evidência: grande, com contraste de foto de anúncio, halo lima forte e sombra no chão."""
    p = recortar(foto)
    rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.18)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.96)
    # volume: luz vindo da esquerda/cima, sombra suave à direita e embaixo (o branco deixa de ficar "chapado")
    gx = np.linspace(1.04, 0.74, rgb.width)[None, :, None]
    gy = np.linspace(1.0, 0.82, rgb.height)[:, None, None]
    arr = np.clip(np.array(rgb).astype(float) * gx * gy, 0, 255)
    verde = np.array([150, 235, 150]) * 0.10  # um reflexo verde de leve, como luz do ambiente
    rgb = Image.fromarray(np.clip(arr * 0.92 + verde, 0, 255).astype('uint8'))
    a = p.split()[-1]
    p = rgb.convert('RGBA')
    p.putalpha(a)
    p = p.resize((int(p.width * altura / p.height), altura), Image.LANCZOS).rotate(ang, resample=Image.BICUBIC, expand=True)
    x, y = int(cx - p.width / 2), base_y - p.height
    for raio, forca in ((90, 230), (35, 200)):
        g = Image.new('RGBA', b.size, LIMA + (0,))
        m = Image.new('L', b.size, 0)
        m.paste(p.split()[-1].point(lambda v: forca if v > 20 else 0), (x, y))
        g.putalpha(m.filter(ImageFilter.GaussianBlur(raio)))
        b.alpha_composite(g)
    s = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse((cx - p.width * 0.42, base_y - 26, cx + p.width * 0.42, base_y + 22), fill=(0, 15, 5, 200))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    b.alpha_composite(p, (x, y))


v3.produto = lambda b, foto, cx, base_y, altura, ang=-6: produto_destaque(b, foto)

if __name__ == '__main__':
    lance, tempo, saida = float(sys.argv[1]), sys.argv[2], sys.argv[3]
    v3.arte_prompt(lance, 'FALTA MENOS DE', tempo, ('LEILÃO TERMINA EM', f'MENOS DE {tempo}'), saida, foto=f'{AQUI}/f-000.png')
