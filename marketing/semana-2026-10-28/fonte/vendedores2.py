# Artes do grupo dos vendedores — versão 2 (28/10/2026), no nível das artes do iPhone que o time aprovou:
# fundo verde com luz e raios, título gigante em lima com sombra em relevo, produto recortado com brilho atrás,
# cartões de vidro escuro (preço da loja / lance atual), selo redondo de desconto, barra de confiança e chamada final.
# Uso: python3 vendedores2.py <lance_agora> <pasta_saida>
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from kit import AQUI, logo as _logo

W, H = 1080, 1920
LIMA = (200, 246, 74)
LIMA_ESC = (150, 214, 40)
CREME = (250, 228, 140)
FUNDO_ESC = (4, 52, 24)
VIDRO = (6, 62, 28)
BRANCO = (255, 255, 255)
FONTE = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'

from PIL import ImageFont
def F(peso, t):
    return ImageFont.truetype(FONTE % peso, t)


def real(v):
    s = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + (s[:-3] if s.endswith(',00') else s)


# ---------- recorte do produto (fotos vêm com fundo branco puro)
def recortar(caminho):
    im = Image.open(caminho).convert('RGB')
    base = im.copy()
    for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1),
               (im.width // 2, 0), (0, im.height // 2), (im.width - 1, im.height // 2), (im.width // 2, im.height - 1)]:
        ImageDraw.floodfill(base, xy, (255, 0, 255), thresh=6)
    a = np.array(base)
    m = ~((a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255))
    al = Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.4))
    o = im.convert('RGBA')
    o.putalpha(al)
    return o.crop(o.getbbox())


# ---------- fundo
def fundo():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W * 0.5) / W) ** 2 + ((y - H * 0.42) / H) ** 2)
    t = np.clip(d / 0.75, 0, 1)[..., None]
    c0, c1 = np.array([22, 168, 70]), np.array([3, 58, 26])
    img = (c0 * (1 - t) + c1 * t).astype('uint8')
    im = Image.fromarray(img, 'RGB').convert('RGBA')
    # faixas diagonais de luz (como nas artes do iPhone)
    luz = Image.new('L', (W, H), 0)
    dl = ImageDraw.Draw(luz)
    dl.polygon([(-200, 700), (700, -200), (1000, -200), (-200, 1000)], fill=38)
    dl.polygon([(300, 1920), (1280, 900), (1280, 1150), (550, 1920)], fill=30)
    dl.polygon([(-200, 1500), (300, 1000), (380, 1000), (-200, 1580)], fill=22)
    luz = luz.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new('RGBA', (W, H), (120, 255, 150, 255)), im, luz)
    # vinheta
    v = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v).rectangle((0, 0, W, H), fill=0)
    vig = (np.clip((d - 0.35) / 0.5, 0, 1) * 120).astype('uint8')
    im = Image.composite(Image.new('RGBA', (W, H), (0, 25, 10, 255)), im, Image.fromarray(vig, 'L'))
    # granulado sutil
    ruido = (np.random.default_rng(7).normal(0, 5, (H, W, 1)) + 128).clip(0, 255).astype('uint8').repeat(3, 2)
    r = Image.fromarray(ruido, 'RGB').convert('RGBA')
    r.putalpha(18)
    im.alpha_composite(r)
    return im


# ---------- texto com relevo
def camada_texto(texto, fonte, preench, sombra=FUNDO_ESC, relevo=10, brilho=None, borda=0):
    d0 = ImageDraw.Draw(Image.new('L', (10, 10)))
    x0, y0, x1, y1 = d0.textbbox((0, 0), texto, font=fonte, stroke_width=borda)
    pad = 90 if brilho else 30
    w, h = x1 - x0 + 2 * relevo + 2 * pad, y1 - y0 + 2 * relevo + 2 * pad
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((pad - x0, pad - y0), texto, font=fonte, fill=255, stroke_width=borda, stroke_fill=255)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if brilho:
        g = Image.new('RGBA', (w, h), brilho + (0,))
        g.putalpha(m.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.8)))
        out.alpha_composite(g)
    for k in range(relevo, 0, -1):  # extrusão para baixo/direita
        s = Image.new('RGBA', (w, h), sombra + (255,))
        s.putalpha(ImageChops.offset(m, k // 2, k))
        out.alpha_composite(s)
    if isinstance(preench, tuple) and len(preench) == 2 and isinstance(preench[0], tuple):
        top, bot = preench
        gy = np.linspace(0, 1, h)[:, None, None]
        grad = (np.array(top) * (1 - gy) + np.array(bot) * gy).astype('uint8').repeat(w, 1)
        fill = Image.fromarray(grad, 'RGB').convert('RGBA')
    else:
        fill = Image.new('RGBA', (w, h), preench + (255,))
    fill.putalpha(m)
    out.alpha_composite(fill)
    return out


def colar_centro(base, camada, cx, cy, ang=0):
    if ang:
        camada = camada.rotate(ang, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(camada, (int(cx - camada.width / 2), int(cy - camada.height / 2)))


def texto_espacado(d, xy, texto, fonte, cor, esp=4, ancora='mm'):
    larg = sum(d.textlength(c, font=fonte) for c in texto) + esp * (len(texto) - 1)
    x = xy[0] - larg / 2 if ancora == 'mm' else xy[0]
    for c in texto:
        d.text((x, xy[1]), c, font=fonte, fill=cor, anchor='lm')
        x += d.textlength(c, font=fonte) + esp
    return larg


# ---------- ícones simples (desenhados, nada de imagem de fora)
def ic_cronometro(d, cx, cy, r, cor):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cor, width=max(6, r // 6))
    d.rounded_rectangle((cx - r * 0.25, cy - r - r * 0.42, cx + r * 0.25, cy - r - r * 0.12), radius=4, fill=cor)
    d.line((cx + r * 0.72, cy - r * 0.72, cx + r * 0.95, cy - r * 0.95), fill=cor, width=max(5, r // 7))
    for i in range(12):
        a = i * math.pi / 6
        d.line((cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a), cx + r * 0.84 * math.cos(a), cy + r * 0.84 * math.sin(a)), fill=cor, width=3)
    d.line((cx, cy, cx, cy - r * 0.55), fill=cor, width=max(5, r // 8))
    d.line((cx, cy, cx + r * 0.42, cy + r * 0.18), fill=cor, width=max(5, r // 8))
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=cor)


def ic_etiqueta(d, x, y, s, cor):
    d.polygon([(x, y + s * 0.45), (x + s * 0.45, y), (x + s, y), (x + s, y + s * 0.55), (x + s * 0.55, y + s)], fill=cor)
    d.ellipse((x + s * 0.68, y + s * 0.12, x + s * 0.86, y + s * 0.3), fill=VIDRO)


def ic_martelo(d, x, y, s, cor):
    cab = [(x + s * 0.18, y + s * 0.30), (x + s * 0.48, y), (x + s * 0.72, y + s * 0.24), (x + s * 0.42, y + s * 0.54)]
    d.polygon(cab, fill=cor)
    d.line((x + s * 0.50, y + s * 0.38, x + s * 0.95, y + s * 0.83), fill=cor, width=int(s * 0.14))
    d.rectangle((x, y + s * 0.86, x + s * 0.6, y + s), fill=cor)


def ic_relogio(d, cx, cy, r, cor):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cor, width=6)
    d.line((cx, cy, cx, cy - r * 0.55), fill=cor, width=6)
    d.line((cx, cy, cx + r * 0.45, cy + r * 0.2), fill=cor, width=6)


def ic_raio(d, cx, cy, s, cor):
    d.polygon([(cx + s * 0.12, cy - s * 0.5), (cx - s * 0.32, cy + s * 0.06), (cx - s * 0.02, cy + s * 0.06),
               (cx - s * 0.14, cy + s * 0.5), (cx + s * 0.32, cy - s * 0.08), (cx + s * 0.02, cy - s * 0.08)], fill=cor)


def ic_escudo(d, cx, cy, s, cor):
    d.polygon([(cx, cy - s * 0.5), (cx + s * 0.42, cy - s * 0.32), (cx + s * 0.36, cy + s * 0.18), (cx, cy + s * 0.5),
               (cx - s * 0.36, cy + s * 0.18), (cx - s * 0.42, cy - s * 0.32)], fill=cor)
    d.line((cx - s * 0.18, cy, cx - s * 0.03, cy + s * 0.15, cx + s * 0.2, cy - s * 0.14), fill=FUNDO_ESC, width=int(s * 0.1))


def ic_fogo(base, cx, cy, s):
    f = Image.new('RGBA', (int(s * 2), int(s * 2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)
    c = s
    pts = [(c + s * 0.5 * math.sin(t) * (1 - (t / math.pi) * 0.2), c + s * 0.5 - s * 0.9 * (t / math.pi) ** 1.4) for t in np.linspace(0, math.pi, 30)]
    pts2 = [(2 * c - x, y) for x, y in pts[::-1]]
    d.polygon(pts + pts2, fill=(255, 150, 30, 255))
    d.ellipse((c - s * 0.3, c - s * 0.05, c + s * 0.3, c + s * 0.5), fill=(255, 214, 70, 255))
    base.alpha_composite(f, (int(cx - c), int(cy - c - s * 0.1)))


def seta_curva(d, p0, p1, p2, cor, larg=7):
    pts = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, 40)]
    d.line(pts, fill=cor, width=larg, joint='curve')
    ax, ay = pts[-1]
    bx, by = pts[-4]
    ang = math.atan2(ay - by, ax - bx)
    for da in (2.5, -2.5):
        d.line((ax, ay, ax + 34 * math.cos(ang + da), ay + 34 * math.sin(ang + da)), fill=cor, width=larg)


# ---------- peças
def vidro(base, caixa, borda=(120, 220, 140), raio=34):
    x0, y0, x1, y1 = caixa
    s = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((x0 + 4, y0 + 16, x1 + 4, y1 + 16), radius=raio, fill=(0, 20, 8, 150))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    c = Image.new('RGBA', base.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(c)
    dc.rounded_rectangle(caixa, radius=raio, fill=VIDRO + (232,), outline=borda + (170,), width=3)
    dc.rounded_rectangle((x0 + 3, y0 + 3, x1 - 3, y0 + (y1 - y0) * 0.45), radius=raio, fill=(255, 255, 255, 12))
    base.alpha_composite(c)


def selo(base, cx, cy, r, linhas, ang=-8):
    s = Image.new('RGBA', (r * 2 + 80, r * 2 + 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    c = r + 40
    g = Image.new('RGBA', s.size, LIMA + (0,))
    gm = Image.new('L', s.size, 0)
    ImageDraw.Draw(gm).ellipse((c - r - 10, c - r - 10, c + r + 10, c + r + 10), fill=170)
    g.putalpha(gm.filter(ImageFilter.GaussianBlur(22)))
    s.alpha_composite(g)
    d.ellipse((c - r, c - r, c + r, c + r), fill=LIMA, outline=(235, 255, 170), width=5)
    d.ellipse((c - r + 16, c - r + 16, c + r - 16, c + r - 16), outline=FUNDO_ESC + (90,), width=3)
    tams = [int(r * 0.26), int(r * 0.62), int(r * 0.2)]
    total = sum(tams) + 14
    y = c - total / 2
    for t, tam in zip(linhas, tams):
        d.text((c, y + tam / 2), t, font=F('Black', tam), fill=FUNDO_ESC, anchor='mm')
        y += tam + 7
    s = s.rotate(ang, resample=Image.BICUBIC)
    base.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def produto(base, foto, cx, base_y, altura, ang=-4):
    p = recortar(foto)
    p = p.resize((int(p.width * altura / p.height), altura), Image.LANCZOS)
    if ang:
        p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
    # brilho lima atrás
    g = Image.new('RGBA', base.size, LIMA + (0,))
    gm = Image.new('L', base.size, 0)
    gm.paste(p.split()[-1].point(lambda v: 200 if v > 20 else 0), (int(cx - p.width / 2), base_y - p.height))
    g.putalpha(gm.filter(ImageFilter.GaussianBlur(45)))
    base.alpha_composite(g)
    # sombra no chão
    s = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse((cx - p.width * 0.45, base_y - 30, cx + p.width * 0.45, base_y + 20), fill=(0, 20, 8, 170))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    base.alpha_composite(p, (int(cx - p.width / 2), base_y - p.height))


def etiqueta_produto(base, x, y, nome, sub):
    d = ImageDraw.Draw(base)
    w = max(d.textlength(nome, font=F('Black', 38)), d.textlength(sub, font=F('Bold', 30))) + 150
    vidro(base, (x, y, x + w, y + 120), borda=LIMA, raio=28)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x + 26, y + 26, x + 74, y + 94), radius=10, outline=CREME, width=5)
    d.line((x + 40, y + 36, x + 60, y + 36), fill=CREME, width=4)
    d.text((x + 96, y + 42), nome, font=F('Black', 38), fill=BRANCO, anchor='lm')
    d.text((x + 96, y + 86), sub, font=F('Bold', 30), fill=(210, 240, 218), anchor='lm')


def cartao_preco(base, caixa, icone, rot1, rot2, valor, destaque=False):
    vidro(base, caixa, borda=LIMA if destaque else (120, 220, 140))
    x0, y0, x1, y1 = caixa
    d = ImageDraw.Draw(base)
    icone(d, x0 + 30, y0 + 30, 56, CREME)
    d.text((x0 + 108, y0 + 44), rot1, font=F('Black', 32), fill=CREME, anchor='lm')
    d.text((x0 + 108, y0 + 82), rot2, font=F('Black', 32), fill=CREME, anchor='lm')
    tam = 88
    while tam > 50 and ImageDraw.Draw(base).textlength(valor, font=F('Black', tam)) > (x1 - x0) - (110 if destaque else 60):
        tam -= 4
    f = F('Black', tam)
    if destaque:
        w = d.textlength(valor, font=f)
        d.rounded_rectangle((x0 + 26, y0 + 118, x0 + 26 + w + 50, y0 + 230), radius=26, fill=LIMA)
        d.text((x0 + 51, y0 + 174), valor, font=f, fill=FUNDO_ESC, anchor='lm')
    else:
        d.text((x0 + 30, y0 + 174), valor, font=f, fill=BRANCO, anchor='lm')


def barra_confianca(base, y, itens):
    vidro(base, (50, y, 1030, y + 150), borda=LIMA, raio=75)
    d = ImageDraw.Draw(base)
    larg = 980 / 3
    for k, (ic, a, b) in enumerate(itens):
        x = 50 + k * larg
        ic(d, x + 62, y + 75)
        d.text((x + 112, y + 56), a, font=F('Bold', 26), fill=(225, 245, 230), anchor='lm')
        d.text((x + 112, y + 94), b, font=F('Black', 28), fill=BRANCO, anchor='lm')
        if k:
            d.line((x, y + 35, x, y + 115), fill=(150, 225, 160), width=2)


PRODUTO, SUB, LOJA = 'Máquina de lavar Panasonic', '15 kg · automática', 904.62
FOTO = f'{AQUI}/f-000.png'


def montar(saida, lance, topo1, topo2, sub_pilula, sub_linha, cta_txt, mostrar_cron=True):
    b = fundo()
    _logo(b, y=70, largura=300)
    d = ImageDraw.Draw(b)
    # título
    t1 = camada_texto(topo1, F('Black', 112), BRANCO, relevo=8)
    tam = 240
    while tam > 120 and ImageDraw.Draw(b).textlength(topo2, font=F('Black', tam)) > 960:
        tam -= 10
    t2 = camada_texto(topo2, F('Black', tam), ((232, 255, 140), LIMA_ESC), relevo=16, brilho=LIMA)
    if mostrar_cron:
        ic_cronometro(d, 185, 330, 66, LIMA)
        colar_centro(b, t1, 600, 330)
    else:
        colar_centro(b, t1, 540, 330)
    colar_centro(b, t2, 540, 515)
    d = ImageDraw.Draw(b)
    f = F('Black', 44)
    larg = sum(d.textlength(c, font=f) for c in sub_pilula) + 6 * (len(sub_pilula) - 1)
    d.rounded_rectangle((540 - larg / 2 - 50, 650, 540 + larg / 2 + 50, 740), radius=45, fill=FUNDO_ESC + (220,), outline=LIMA, width=4)
    texto_espacado(d, (540, 695), sub_pilula, f, CREME, esp=6)
    texto_espacado(d, (540, 785), sub_linha, F('Black', 32), BRANCO, esp=5)
    seta_curva(d, (905, 800), (1015, 845), (960, 905), LIMA)
    # produto + etiqueta
    produto(b, FOTO, 320, 1440, 560)
    etiqueta_produto(b, 60, 1395, PRODUTO, SUB)
    # cartões de preço
    cartao_preco(b, (610, 900, 1030, 1130), ic_etiqueta, 'VALOR MÉDIO', 'NA LOJA', real(LOJA))
    cartao_preco(b, (610, 1155, 1030, 1385), ic_martelo, 'LANCE ATUAL', 'DO LEILÃO', real(lance), destaque=True)
    off = round(100 * (1 - lance / LOJA))
    d = ImageDraw.Draw(b)
    seta_curva(d, (1040, 1395), (1055, 1450), (1000, 1480), LIMA)
    selo(b, 880, 1500, 112, ['HOJE', f'-{off}%', 'DA LOJA'])
    barra_confianca(b, 1640, [
        (lambda d, x, y: ic_relogio(d, x, y, 30, CREME), 'MARTELO', 'HOJE ÀS 18H'),
        (lambda d, x, y: ic_raio(d, x, y, 64, CREME), 'PRODUTO NOVO', 'DE FÁBRICA'),
        (lambda d, x, y: ic_escudo(d, x, y, 64, CREME), 'LANCES SEGUROS', 'E AO VIVO'),
    ])
    b = b.convert('RGB')
    b.save(saida, quality=94)


def cta_final(caminho, texto):
    """A chamada final fica abaixo da barra (área livre dos stories)."""
    b = Image.open(caminho).convert('RGBA')
    d = ImageDraw.Draw(b)
    f = F('Black', 50)
    w = d.textlength(texto, font=f)
    ic_fogo(b, 540 - w / 2 - 20, 1845, 30)
    d.text((540 + 25, 1845), texto, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(caminho, quality=94)


if __name__ == '__main__':
    lance = float(sys.argv[1])
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    pecas = [
        ('1-por-quanto-vai-sair.jpg', 'POR QUANTO', 'VAI SAIR?', 'O MARTELO BATE ÀS 18H', 'DEIXA SEU PALPITE PRA MIM', 'ME CHAMA PRA DAR SEU LANCE!', False),
        ('2-faltam-3-horas.jpg', 'FALTAM', '3 HORAS', 'PRA VOCÊ ARREMATAR', 'UMA MÁQUINA QUE CUSTA EM MÉDIA', 'NÃO DEIXA PRA DEPOIS!', True),
        ('3-faltam-1-hora.jpg', 'FALTA', '1 HORA', 'PRA VOCÊ ARREMATAR', 'UMA MÁQUINA QUE CUSTA EM MÉDIA', 'É AGORA OU NUNCA!', True),
        ('4-faltam-30-minutos.jpg', 'FALTAM', '30 MIN', 'PRA VOCÊ ARREMATAR', 'UMA MÁQUINA QUE CUSTA EM MÉDIA', 'CORRE QUE DÁ TEMPO!', True),
    ]
    for nome, a, b_, p, l, c, cron in pecas:
        caminho = f'{out}/{nome}'
        montar(caminho, lance, a, b_, p, l, c, cron)
        cta_final(caminho, c)
    print(out)
