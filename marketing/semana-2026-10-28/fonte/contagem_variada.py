# Contagem regressiva do sábado 31/10 com UM VISUAL DIFERENTE por horário (sugestão do time de vendas: arte repetida
# vira "a mesma de antes" e ninguém para). Mesmo texto e mesma marca (verde, lima, logo, notebook real), layouts distintos:
# 15h clássico · 16h número gigante no escuro · 17h fundo lima invertido · 17h30 barra do tempo · 17h50 fita de alerta.
# Uso: python3 contagem_variada.py <lance> <n_lances> <saida_dir>
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from arte_do_dia import LIMA, BRANCO, F, real, produto
from notebook_dia import FOTO, NOME, SPEC, vidro
from stories_notebook import fundo, W, H
from vendedores2 import ic_martelo
from vendedores_sabado import peca
from kit import logo as _logo

ESCURO = (3, 34, 15)
NOITE = (4, 19, 10)


def cta(d, y, fundo_cor=LIMA, cor=ESCURO, texto='DÊ SEU LANCE · leilaonozap.net'):
    d.rounded_rectangle((170, y, 910, y + 100), radius=50, fill=fundo_cor)
    d.text((540, y + 50), texto, font=F('Black', 38), fill=cor, anchor='mm')


def linha_lance(d, lance, n, y, cor_rot=LIMA, cor_val=BRANCO, cor_info=(205, 235, 214)):
    ic_martelo(d, 250, y - 26, 44, cor_rot)
    d.text((310, y), 'LANCE ATUAL', font=F('Black', 38), fill=cor_rot, anchor='lm')
    d.text((900, y), real(lance), font=F('Black', 70), fill=cor_val, anchor='rm')
    d.text((540, y + 70), f'{NOME}  ·  {n} lances', font=F('Black', 30), fill=cor_info, anchor='mm')


def fundo_escuro():
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    t = np.clip(dd / 0.7, 0, 1)[..., None]
    im = Image.fromarray((np.array([12, 52, 26]) * (1 - t) + np.array(NOITE) * t).astype('uint8'), 'RGB').convert('RGBA')
    g = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(g)
    for x in range(0, W, 60):
        dg.line((x, 0, x, H), fill=18)
    for y in range(0, H, 60):
        dg.line((0, y, W, y), fill=18)
    im.alpha_composite(Image.new('RGBA', (W, H), LIMA + (0,)), (0, 0))
    lima = Image.new('RGBA', (W, H), LIMA + (0,)); lima.putalpha(g)
    im.alpha_composite(lima)
    return im


def numero_gigante(lance, n, saida):  # 16h
    b = fundo_escuro(); _logo(b, y=120, largura=220)
    d = ImageDraw.Draw(b)
    d.text((540, 330), 'FALTAM', font=F('Black', 96), fill=BRANCO, anchor='mm')
    brilho = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(brilho).text((540, 700), '2', font=F('Black', 720), fill=LIMA + (160,), anchor='mm')
    b.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(b)
    d.text((540, 700), '2', font=F('Black', 720), fill=LIMA, anchor='mm')
    d.text((540, 1030), 'HORAS', font=F('Black', 120), fill=BRANCO, anchor='mm')
    produto(b, FOTO, 540, 1420, 300)
    d = ImageDraw.Draw(b)
    linha_lance(d, lance, n, 1500)
    cta(d, 1640)
    b.convert('RGB').save(saida, quality=95)


def invertido(lance, n, saida):  # 17h
    b = Image.new('RGBA', (W, H), LIMA + (255,))
    d = ImageDraw.Draw(b)
    for k in range(-H, W, 90):  # listras diagonais sutis
        d.polygon([(k, 0), (k + 40, 0), (k + 40 + H * 0.6, H), (k + H * 0.6, H)], fill=(178, 230, 50, 255))
    lg = Image.open('/home/user/Leil-onozaplivoo/marketing/semana-2026-10-28/fonte/logo.png').convert('RGBA')
    lg = lg.resize((220, int(lg.height * 220 / lg.width))); fundo_logo = Image.new('RGBA', (300, lg.height + 40), (0, 0, 0, 0))
    ImageDraw.Draw(fundo_logo).rounded_rectangle((0, 0, 299, lg.height + 39), radius=30, fill=ESCURO + (255,))
    fundo_logo.alpha_composite(lg, (40, 20)); b.alpha_composite(fundo_logo, (390, 110))
    d = ImageDraw.Draw(b)
    d.text((540, 380), 'FALTA', font=F('Black', 110), fill=ESCURO, anchor='mm')
    d.text((540, 540), '1 HORA', font=F('Black', 190), fill=ESCURO, anchor='mm')
    d.rounded_rectangle((120, 660, 960, 1260), radius=50, fill=BRANCO)
    produto(b, FOTO, 540, 1180, 460)
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((120, 1310, 960, 1560), radius=40, fill=ESCURO)
    linha_lance(d, lance, n, 1390)
    d.text((540, 1505), 'ÚLTIMA HORA PARA DAR LANCE', font=F('Black', 34), fill=LIMA, anchor='mm')
    cta(d, 1620, ESCURO, LIMA)
    b.convert('RGB').save(saida, quality=95)


def barra_do_tempo(lance, n, saida):  # 17h30
    b = fundo(); _logo(b, y=120, largura=220)
    d = ImageDraw.Draw(b)
    d.text((90, 360), 'FALTAM', font=F('Black', 100), fill=BRANCO, anchor='lm')
    d.text((90, 500), '30', font=F('Black', 240), fill=LIMA, anchor='lm')
    d.text((470, 545), 'MINUTOS', font=F('Black', 92), fill=BRANCO, anchor='lm')
    # barra: o leilão até as 18h, faltando 30 minutos
    x0, x1, y = 90, 990, 700
    d.rounded_rectangle((x0, y, x1, y + 44), radius=22, fill=(3, 40, 18), outline=LIMA, width=3)
    fim = x0 + (x1 - x0) * 0.94
    d.rounded_rectangle((x0 + 6, y + 6, fim, y + 38), radius=16, fill=LIMA)
    d.text((x0, y + 80), '17h30', font=F('Black', 34), fill=BRANCO, anchor='lm')
    d.text((x1, y + 80), '18h00 · MARTELO', font=F('Black', 34), fill=LIMA, anchor='rm')
    pr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); produto(pr, FOTO, 540, 1300, 470)
    b.alpha_composite(pr.rotate(-6, resample=Image.BICUBIC, center=(540, 1100)))
    d = ImageDraw.Draw(b)
    vidro(b, (120, 1390, 960, 1580), raio=30); d = ImageDraw.Draw(b)
    linha_lance(d, lance, n, 1460)
    cta(d, 1640)
    b.convert('RGB').save(saida, quality=95)


def fita_alerta(lance, n, saida):  # 17h50
    b = fundo_escuro()
    for y0, ang in ((300, -6), (1270, 5)):
        fita = Image.new('RGBA', (W + 400, 110), LIMA + (255,))
        df = ImageDraw.Draw(fita)
        for k in range(0, W + 400, 70):
            df.polygon([(k, 0), (k + 35, 0), (k + 5, 110), (k - 30, 110)], fill=ESCURO + (255,))
        df.rectangle((0, 25, W + 400, 85), fill=LIMA + (255,))
        for k in range(0, W + 400, 520):
            df.text((k + 20, 55), 'ÚLTIMA CHAMADA', font=F('Black', 44), fill=ESCURO, anchor='lm')
        fita = fita.rotate(ang, expand=True, resample=Image.BICUBIC)
        b.alpha_composite(fita, (-200, y0 - fita.height // 2))
    _logo(b, y=90, largura=200)
    d = ImageDraw.Draw(b)
    d.text((540, 460), 'FALTAM', font=F('Black', 90), fill=BRANCO, anchor='mm')
    brilho = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(brilho).text((540, 720), '10', font=F('Black', 470), fill=(255, 255, 255, 120), anchor='mm')
    b.alpha_composite(brilho.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(b)
    d.text((540, 720), '10', font=F('Black', 470), fill=BRANCO, anchor='mm')
    d.text((540, 990), 'MINUTOS', font=F('Black', 120), fill=LIMA, anchor='mm')
    ic_martelo(d, 470, 1095, 70, LIMA)
    d.text((560, 1130), 'O martelo vai bater!', font=F('Black', 44), fill=BRANCO, anchor='lm')
    produto(b, FOTO, 540, 1560, 230)
    d = ImageDraw.Draw(b)
    d.text((540, 1610), f'Lance atual {real(lance)}  ·  {n} lances', font=F('Black', 40), fill=BRANCO, anchor='mm')
    cta(d, 1680)
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    lance, n, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    os.makedirs(out, exist_ok=True)
    peca(lance, n, 'FALTAM', '3 HORAS', 'O MARTELO BATE ÀS 18H', f'{out}/CONTAGEM-15h-faltam-3-horas.jpg')
    numero_gigante(lance, n, f'{out}/CONTAGEM-16h-faltam-2-horas.jpg')
    invertido(lance, n, f'{out}/CONTAGEM-17h-falta-1-hora.jpg')
    barra_do_tempo(lance, n, f'{out}/CONTAGEM-17h30-faltam-30-minutos.jpg')
    fita_alerta(lance, n, f'{out}/CONTAGEM-17h50-faltam-10-minutos.jpg')
    print('ok')
