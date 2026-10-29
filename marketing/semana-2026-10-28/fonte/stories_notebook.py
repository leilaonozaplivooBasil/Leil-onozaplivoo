# Stories (9:16) do leilão do NOTEBOOK no padrão verde aprovado (cópia em pé da "arte do dia").
# Topo e rodapé respeitam a área que o Instagram/WhatsApp cobre; espaço livre embaixo para a figurinha de LINK.
# Uso: python3 stories_notebook.py <lance> <mercado> <saida_dir>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from arte_do_dia import LIMA, BRANCO, ESCURO, F, real, produto
from notebook_dia import FOTO, NOME, SPEC, selo, vidro
from vendedores2 import ic_martelo
from kit import logo as _logo

W, H = 1080, 1920


def fundo():
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W * 0.45) / W) ** 2 + ((yy - H * 0.5) / H) ** 2)
    t = np.clip(d / 0.75, 0, 1)[..., None]
    im = Image.fromarray((np.array([10, 92, 42]) * (1 - t) + np.array([2, 30, 14]) * t).astype('uint8'), 'RGB').convert('RGBA')
    for x0, larg, a in [(0.55, 0.05, 55), (0.68, 0.025, 70), (0.80, 0.08, 35), (0.95, 0.03, 60), (0.30, 0.04, 40)]:
        c = Image.new('L', (W, H), 0)
        ImageDraw.Draw(c).polygon([(x0 * W, 0), ((x0 + larg) * W, 0), ((x0 + larg - 1.3) * W, H), ((x0 - 1.3) * W, H)], fill=a)
        luz = Image.new('RGBA', (W, H), (120, 240, 110, 0))
        luz.putalpha(c.filter(ImageFilter.GaussianBlur(10)))
        im.alpha_composite(luz)
    g = Image.new('L', (W, H), 0)
    ImageDraw.Draw(g).ellipse((140, 1000, 940, 1220), fill=170)
    chao = Image.new('RGBA', (W, H), (110, 230, 90, 0))
    chao.putalpha(g.filter(ImageFilter.GaussianBlur(70)))
    im.alpha_composite(chao)
    v = (np.clip((d - 0.45) / 0.35, 0, 1) * 150).astype('uint8')
    return Image.composite(Image.new('RGBA', (W, H), (0, 14, 5, 255)), im, Image.fromarray(v, 'L'))


def titulo(d, prefixo, tempo, y, tam=124):
    f = F('Black', tam)
    for txt, yy, cor in ((prefixo, y, BRANCO), (tempo, y + tam * 1.02, LIMA)):
        d.text((W / 2 + 5, yy + 7), txt, font=f, fill=(0, 20, 8), anchor='mm')
        d.text((W / 2, yy), txt, font=f, fill=cor, anchor='mm')


def story(lance, mercado, prefixo, tempo, saida):
    b = fundo()
    _logo(b, y=140, largura=230)
    d = ImageDraw.Draw(b)
    titulo(d, prefixo, tempo, 390)
    produto(b, FOTO, 520, 1130, 500)
    selo(b, 880, 790, 112, round(100 * (1 - lance / mercado)))
    vidro(b, (190, 1170, 890, 1400), raio=30)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 330, 1200, 48, LIMA)
    d.text((395, 1226), 'LANCE ATUAL', font=F('Black', 40), fill=LIMA, anchor='lm')
    d.text((540, 1325), real(lance), font=F('Black', 120), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1480), NOME, font=F('Black', 56), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1542), SPEC, font=F('Black', 34), fill=LIMA, anchor='mm')
    # 1600–1700: espaço livre para a figurinha de LINK
    b.convert('RGB').save(saida, quality=95)


DIAS = [
    ('quinta-29-10', 'STORY-1-quinta-faltam-2-dias', 'FALTAM', '2 DIAS'),
    ('sexta-30-10', 'STORY-2-sexta-falta-1-dia', 'FALTA', '1 DIA'),
    ('sabado-31-10', 'STORY-3-sabado-hoje-as-18h', 'É HOJE', 'ÀS 18H'),
    ('sabado-31-10', 'STORY-4-sabado-faltam-3-horas', 'FALTAM', '3 HORAS'),
]

if __name__ == '__main__':
    lance, mercado, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    for pasta, nome, p, t in DIAS:
        os.makedirs(f'{out}/{pasta}', exist_ok=True)
        story(lance, mercado, p, t, f'{out}/{pasta}/{nome}.jpg')
        print(f'{out}/{pasta}/{nome}.jpg')
