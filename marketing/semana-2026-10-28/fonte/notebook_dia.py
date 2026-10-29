# Artes do leilão do NOTEBOOK nos 3 modelos quadrados aprovados pela Natália (cópia do padrão da máquina de lavar).
# Números sempre do sistema. Uso: python3 notebook_dia.py <lance> <mercado> <saida_dir>
import os, sys
from PIL import Image, ImageDraw, ImageFilter
from arte_do_dia import S, LIMA, BRANCO, ESCURO, F, real, fundo, produto
from vendedores2 import ic_martelo
from kit import AQUI, logo as _logo

FOTO = f'{AQUI}/f-004.png'
NOME = 'NOTEBOOK DELL CORE I3'
SPEC = '15,6" FULL HD • 8GB • SSD 512GB'


def titulo(d, prefixo, tempo, y, tam=96):
    f = F('Black', tam)
    w1, w2 = d.textlength(prefixo + ' ', font=f), d.textlength(tempo, font=f)
    while w1 + w2 > S - 80:
        tam -= 4; f = F('Black', tam)
        w1, w2 = d.textlength(prefixo + ' ', font=f), d.textlength(tempo, font=f)
    x = (S - w1 - w2) / 2
    d.text((x + 4, y + 6), prefixo + ' ', font=f, fill=(0, 20, 8), anchor='lm')
    d.text((x + w1 + 4, y + 6), tempo, font=f, fill=(0, 20, 8), anchor='lm')
    d.text((x, y), prefixo + ' ', font=f, fill=BRANCO, anchor='lm')
    d.text((x + w1, y), tempo, font=f, fill=LIMA, anchor='lm')


def selo(b, cx, cy, r, pct):
    g = Image.new('RGBA', b.size, LIMA + (0,))
    m = Image.new('L', b.size, 0)
    ImageDraw.Draw(m).ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=140)
    g.putalpha(m.filter(ImageFilter.GaussianBlur(20)))
    b.alpha_composite(g)
    d = ImageDraw.Draw(b)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=LIMA)
    k = r / 112
    d.text((cx, cy - 60 * k), 'ATÉ', font=F('Black', int(30 * k)), fill=ESCURO, anchor='mm')
    d.text((cx, cy + 2 * k), f'-{pct}%', font=F('Black', int(80 * k)), fill=ESCURO, anchor='mm')
    d.text((cx, cy + 62 * k), 'DE DIFERENÇA', font=F('Black', int(21 * k)), fill=ESCURO, anchor='mm')


def vidro(b, caixa, raio=26):
    c = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle(caixa, radius=raio, fill=(3, 40, 18, 225), outline=LIMA + (230,), width=3)
    b.alpha_composite(c)


def valor(d, txt, cx, cy, tam, larg):
    f = F('Black', tam)
    while d.textlength(txt, font=f) > larg:
        f = F('Black', f.size - 4)
    d.text((cx, cy), txt, font=f, fill=BRANCO, anchor='mm')


def modelo1(lance, mercado, prefixo, tempo, saida):
    b = fundo(); _logo(b, y=26, largura=150); d = ImageDraw.Draw(b)
    titulo(d, prefixo, tempo, 200)
    produto(b, FOTO, 310, 860, 470)
    vidro(b, (610, 330, 1015, 560)); d = ImageDraw.Draw(b)
    ic_martelo(d, 640, 362, 46, LIMA)
    d.text((702, 388), 'LANCE ATUAL', font=F('Black', 34), fill=LIMA, anchor='lm')
    valor(d, real(lance), 812, 480, 112, 360)
    selo(b, 812, 715, 112, round(100 * (1 - lance / mercado)))
    d = ImageDraw.Draw(b)
    d.text((S / 2, 960), NOME, font=F('Black', 50), fill=BRANCO, anchor='mm')
    d.text((S / 2, 1016), SPEC, font=F('Black', 32), fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


def modelo2(lance, mercado, prefixo, tempo, saida):
    b = fundo(); _logo(b, y=26, largura=150); d = ImageDraw.Draw(b)
    titulo(d, prefixo, tempo, 185, 84)
    f1, f2 = F('Black', 34), F('Black', 46)
    t1, t2 = 'LANCE ATUAL  ', real(lance)
    w = d.textlength(t1, font=f1) + d.textlength(t2, font=f2)
    vidro(b, ((S - w) / 2 - 40, 250, (S + w) / 2 + 40, 330), raio=40); d = ImageDraw.Draw(b)
    x = (S - w) / 2
    d.text((x, 290), t1, font=f1, fill=BRANCO, anchor='lm')
    d.text((x + d.textlength(t1, font=f1), 290), t2, font=f2, fill=LIMA, anchor='lm')
    produto(b, FOTO, 500, 850, 470)
    selo(b, 900, 760, 88, round(100 * (1 - lance / mercado)))
    vidro(b, (260, 900, 820, 1040), raio=30); d = ImageDraw.Draw(b)
    d.text((S / 2, 945), NOME, font=F('Black', 36), fill=BRANCO, anchor='mm')
    d.text((S / 2, 995), SPEC, font=F('Black', 24), fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


def modelo3(lance, mercado, prefixo, tempo, saida):
    b = fundo(); _logo(b, y=26, largura=150); d = ImageDraw.Draw(b)
    titulo(d, prefixo, tempo, 200, 100)
    produto(b, FOTO, 300, 860, 460)
    vidro(b, (590, 310, 1035, 590)); d = ImageDraw.Draw(b)
    d.text((812, 370), 'LANCE ATUAL', font=F('Black', 38), fill=LIMA, anchor='mm')
    valor(d, real(lance), 812, 490, 124, 400)
    selo(b, 812, 730, 108, round(100 * (1 - lance / mercado)))
    d = ImageDraw.Draw(b)
    d.text((S / 2, 960), NOME, font=F('Black', 54), fill=BRANCO, anchor='mm')
    d.text((S / 2, 1018), SPEC, font=F('Black', 34), fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


DIAS = [  # (pasta, arquivo, modelo, prefixo, tempo)
    ('quinta-29-10', '1-quinta-faltam-2-dias', modelo1, 'FALTAM', '2 DIAS'),
    ('sexta-30-10', '2-sexta-falta-1-dia', modelo2, 'FALTA', '1 DIA'),
    ('sabado-31-10', '3-sabado-hoje-as-18h', modelo3, 'É HOJE', 'ÀS 18H'),
    ('sabado-31-10', '4-sabado-faltam-3-horas', modelo1, 'FALTAM', '3 HORAS'),
]

if __name__ == '__main__':
    lance, mercado, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    for pasta, nome, fn, p, t in DIAS:
        os.makedirs(f'{out}/{pasta}', exist_ok=True)
        fn(lance, mercado, p, t, f'{out}/{pasta}/{nome}.jpg')
        print(f'{out}/{pasta}/{nome}.jpg')
