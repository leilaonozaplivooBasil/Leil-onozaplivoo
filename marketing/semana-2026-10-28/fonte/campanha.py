# 🟢 Molde oficial de campanha do Leilão NoZap (identidade definida pela Natália em 28/10/2026).
# Esmeralda profundo · lima só em números/destaques · branco nas mensagens · dourado-claro só em detalhes.
# Ordem de leitura: urgência → produto → lance atual → valor médio → % de diferença → chamada final.
# Sem barras, setas, faixas ou selos extras. Dados SEMPRE vindos do sistema (nada inventado).
# Uso (exemplo): python3 campanha.py --produto "Máquina de lavar Panasonic" --desc "15 kg · automática" \
#   --linha1 "FALTA MENOS DE" --linha2 "3 HORAS" --medio 904.62 --lance 650 --foto f-000.png --saida a.jpg
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
from vendedores2 import recortar, camada_texto, colar_centro
from kit import AQUI, logo as _logo

W, H = 1080, 1620
ESMERALDA_A, ESMERALDA_B = (6, 78, 40), (2, 34, 18)
LIMA, LIMA_ESC = (196, 244, 66), (150, 210, 40)
DOURADO = (232, 205, 140)
BRANCO = (255, 255, 255)
ESCURO = (3, 36, 16)
FONTE = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'


def F(peso, t):
    return ImageFont.truetype(FONTE % peso, t)


def real(v):
    s = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + (s[:-3] if s.endswith(',00') else s)


def fundo():
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W * 0.38) / W) ** 2 + ((yy - H * 0.58) / H) ** 2)
    t = np.clip(d / 0.8, 0, 1)[..., None]
    img = (np.array(ESMERALDA_A) * (1 - t) + np.array(ESMERALDA_B) * t).astype('uint8')
    im = Image.fromarray(img, 'RGB').convert('RGBA')
    # um único corte diagonal sutil, tom sobre tom (sem poluir)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(c).polygon([(W * 0.62, 0), (W, 0), (W, H * 0.22), (0, H * 0.70), (0, H * 0.52)], fill=(40, 150, 80, 26))
    im.alpha_composite(c.filter(ImageFilter.GaussianBlur(2)))
    # luz verde controlada atrás do produto
    g = Image.new('L', (W, H), 0)
    ImageDraw.Draw(g).ellipse((W * 0.30 - 360, H * 0.62 - 380, W * 0.30 + 360, H * 0.62 + 380), fill=120)
    luz = Image.new('RGBA', (W, H), (70, 200, 100, 0))
    luz.putalpha(g.filter(ImageFilter.GaussianBlur(140)))
    im.alpha_composite(luz)
    return im


def produto(b, foto, cx, base_y, altura, ang=-4):
    p = recortar(foto)
    rgb = ImageEnhance.Contrast(p.convert('RGB')).enhance(1.15)
    gx = np.linspace(1.03, 0.78, rgb.width)[None, :, None]
    gy = np.linspace(1.0, 0.84, rgb.height)[:, None, None]
    rgb = Image.fromarray(np.clip(np.array(rgb).astype(float) * gx * gy * 0.95 + np.array([10, 22, 12]), 0, 255).astype('uint8'))
    a = p.split()[-1]
    p = rgb.convert('RGBA')
    p.putalpha(a)
    p = p.resize((int(p.width * altura / p.height), altura), Image.LANCZOS).rotate(ang, resample=Image.BICUBIC, expand=True)
    x, y = int(cx - p.width / 2), base_y - p.height
    g = Image.new('RGBA', b.size, (120, 230, 110, 0))
    m = Image.new('L', b.size, 0)
    m.paste(p.split()[-1].point(lambda v: 150 if v > 20 else 0), (x, y))
    g.putalpha(m.filter(ImageFilter.GaussianBlur(60)))
    b.alpha_composite(g)
    s = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse((cx - p.width * 0.44, base_y - 24, cx + p.width * 0.44, base_y + 26), fill=(0, 12, 4, 210))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    b.alpha_composite(p, (x, y))


def bloco(b, caixa, fundo_cor, borda=None, raio=30):
    x0, y0, x1, y1 = caixa
    s = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((x0 + 4, y0 + 14, x1 + 4, y1 + 14), radius=raio, fill=(0, 10, 4, 150))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    c = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle(caixa, radius=raio, fill=fundo_cor, outline=borda, width=2 if borda else 0)
    b.alpha_composite(c)


def peca(produto_nome, desc, linha1, linha2, medio, lance, foto, saida, cta='Aproveite antes do encerramento!'):
    b = fundo()
    _logo(b, y=48, largura=210)                                   # 1) logo discreto
    colar_centro(b, camada_texto(linha1, F('Black', 78), BRANCO, relevo=4), 540, 262)   # 2) urgência
    tam = 220
    while tam > 120 and ImageDraw.Draw(b).textlength(linha2, font=F('Black', tam)) > 980:
        tam -= 10
    colar_centro(b, camada_texto(linha2, F('Black', tam), ((222, 255, 120), LIMA_ESC), relevo=10), 540, 410)
    produto(b, foto, 315, 1335, 700)                              # 3) produto protagonista
    d = ImageDraw.Draw(b)
    d.text((315, 1398), produto_nome, font=F('Black', 38), fill=BRANCO, anchor='mm')
    d.text((315, 1442), desc, font=F('Bold', 29), fill=(200, 230, 210), anchor='mm')
    # 4) informações comerciais, à direita
    x0, x1 = 640, 1030
    bloco(b, (x0, 690, x1, 860), (4, 46, 22, 235), borda=(60, 120, 80))
    d = ImageDraw.Draw(b)
    d.text((x0 + 32, 738), 'VALOR MÉDIO DE MERCADO', font=F('Bold', 25), fill=DOURADO, anchor='lm')
    d.text((x0 + 32, 806), real(medio), font=F('Black', 62), fill=BRANCO, anchor='lm')
    bloco(b, (x0, 890, x1, 1090), LIMA + (255,))
    d = ImageDraw.Draw(b)
    d.text((x0 + 32, 940), 'LANCE ATUAL', font=F('Black', 30), fill=ESCURO, anchor='lm')
    fv = F('Black', 104)
    while d.textlength(real(lance), font=fv) > x1 - x0 - 60:
        fv = F('Black', fv.size - 4)
    d.text((x0 + 30, 1026), real(lance), font=fv, fill=ESCURO, anchor='lm')
    # 5) % de diferença: selo independente, abaixo e à direita, com respiro
    pct = round(100 * (1 - lance / medio))
    cx, cy, r = 935, 1225, 82
    s = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(s)
    ds.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(4, 46, 22, 240), outline=LIMA, width=4)
    b.alpha_composite(s)
    d = ImageDraw.Draw(b)
    d.text((cx, cy - 8), f'-{pct}%', font=F('Black', 50), fill=LIMA, anchor='mm')
    d.text((cx, cy + 38), 'de diferença', font=F('Bold', 21), fill=BRANCO, anchor='mm')
    # 6) chamada final, discreta
    d.text((540, 1540), cta, font=F('Bold', 40), fill=DOURADO, anchor='mm')
    b.convert('RGB').save(saida, quality=95)
    return pct


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    for k in ('produto', 'desc', 'linha1', 'linha2', 'foto', 'saida', 'cta'):
        a.add_argument('--' + k)
    a.add_argument('--medio', type=float)
    a.add_argument('--lance', type=float)
    o = a.parse_args()
    print(peca(o.produto, o.desc, o.linha1, o.linha2, o.medio, o.lance, f'{AQUI}/{o.foto}', o.saida, **({'cta': o.cta} if o.cta else {})))


def peca_desejo(produto_nome, desc, linha1, linha2, lance, lances, pessoas, foto, saida,
                sonho=('Imagina essa máquina', '*na* *sua* *casa?*'), prova_foto='murilo-iphone-rosto.jpg',
                prova=None, cta='Aproveite antes do encerramento!'):
    """Versão 'desejo' (28/10): sem valor de mercado nem %, destaca o leilão (tempo + lance + disputa), o sonho e a prova real."""
    b = fundo()
    _logo(b, y=48, largura=210)
    colar_centro(b, camada_texto(linha1, F('Black', 78), BRANCO, relevo=4), 540, 262)
    tam = 220
    while tam > 120 and ImageDraw.Draw(b).textlength(linha2, font=F('Black', tam)) > 980:
        tam -= 10
    colar_centro(b, camada_texto(linha2, F('Black', tam), ((222, 255, 120), LIMA_ESC), relevo=10), 540, 410)
    produto(b, foto, 315, 1290, 670)
    d = ImageDraw.Draw(b)
    d.text((315, 1348), produto_nome, font=F('Black', 38), fill=BRANCO, anchor='mm')
    d.text((315, 1390), desc, font=F('Bold', 29), fill=(200, 230, 210), anchor='mm')
    x0, x1 = 640, 1030
    # lance atual (o destaque) + a disputa real
    dy = 0 if prova else 150  # sem o cartão de prova, o lance desce para o meio da coluna
    bloco(b, (x0, 700 + dy, x1, 920 + dy), LIMA + (255,))
    d = ImageDraw.Draw(b)
    d.text((x0 + 32, 752 + dy), 'LANCE ATUAL', font=F('Black', 32), fill=ESCURO, anchor='lm')
    fv = F('Black', 112)
    while d.textlength(real(lance), font=fv) > x1 - x0 - 60:
        fv = F('Black', fv.size - 4)
    d.text((x0 + 30, 846 + dy), real(lance), font=fv, fill=ESCURO, anchor='lm')
    d.ellipse((x0 + 8, 968 + dy, x0 + 24, 984 + dy), fill=LIMA)
    d.text((x0 + 36, 976 + dy), f'{lances} lances · {pessoas} pessoas disputando', font=F('Bold', 24), fill=BRANCO, anchor='lm')
    # prova real: foto + frase curta (opcional)
    if prova:
      bloco(b, (x0, 1040, x1, 1250), (4, 46, 22, 235), borda=(60, 120, 80))
      ft = Image.open(f'{AQUI}/{prova_foto}').convert('RGB').resize((150, 150), Image.LANCZOS)
      m = Image.new('L', (150, 150), 0)
      ImageDraw.Draw(m).ellipse((0, 0, 149, 149), fill=255)
      ft = ft.convert('RGBA')
      ft.putalpha(m)
      b.alpha_composite(ft, (x0 + 22, 1070))
      d = ImageDraw.Draw(b)
      d.ellipse((x0 + 20, 1068, x0 + 174, 1222), outline=DOURADO, width=3)
      d.text((x0 + 192, 1084), 'QUEM ARREMATA, LEVA', font=F('Black', 19), fill=DOURADO, anchor='lm')
      for i, t in enumerate(prova):
          d.text((x0 + 192, 1124 + i * 34), t, font=F('Bold', 23), fill=BRANCO, anchor='lm')
    # o sonho
    f = F('Black', 46)
    linha_a, linha_b = sonho
    d.text((540, 1472), linha_a, font=f, fill=BRANCO, anchor='mm')
    pal = linha_b.split(' ')
    w = d.textlength(linha_b.replace('*', ''), font=f)
    x = 540 - w / 2
    for i, p in enumerate(pal):
        s = p.replace('*', '') + (' ' if i < len(pal) - 1 else '')
        d.text((x, 1525), s, font=f, fill=LIMA if '*' in p else BRANCO, anchor='lm')
        x += d.textlength(s, font=f)
    d.text((540, 1588), cta, font=F('Bold', 30), fill=DOURADO, anchor='mm')
    b.convert('RGB').save(saida, quality=95)
