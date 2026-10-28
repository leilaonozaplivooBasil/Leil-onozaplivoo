# Artes para o grupo dos vendedores (status do WhatsApp / stories), no estilo das artes do iPhone que o time já usa:
# verde vivo com raios de luz, destaques em lima e amarelo-claro, foto do produto num cartão branco, preço da loja x lance agora.
# Uso: python3 vendedores.py <lance_agora> <saida_dir>
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
from kit import AQUI, fonte, texto_rico
from kit import logo as _logo

W, H = 1080, 1920
VERDE_A, VERDE_B = (16, 140, 62), (6, 84, 36)
ESCURO = (5, 60, 26)
LIMA = (198, 242, 78)
CREME = (247, 222, 128)
BRANCO = (255, 255, 255)


def real(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').replace(',00', '')


def fundo():
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(VERDE_A, VERDE_B)))
    raios = Image.new('L', (W, H), 0)
    dr = ImageDraw.Draw(raios)
    cx, cy = W // 2, 760
    for i in range(18):
        a = i * math.pi / 9
        dr.polygon([(cx, cy), (cx + 2400 * math.cos(a), cy + 2400 * math.sin(a)), (cx + 2400 * math.cos(a + 0.09), cy + 2400 * math.sin(a + 0.09))], fill=26)
    luz = Image.new('L', (W, H), 0)
    ImageDraw.Draw(luz).ellipse((cx - 520, cy - 520, cx + 520, cy + 520), fill=110)
    luz = luz.filter(ImageFilter.GaussianBlur(170))
    im = Image.composite(Image.new('RGB', (W, H), (60, 200, 100)), im, raios.filter(ImageFilter.GaussianBlur(3)))
    im = Image.composite(Image.new('RGB', (W, H), (90, 215, 110)), im, luz)
    return im.convert('RGBA')


def pilula(d, texto, y, cor=CREME, tam=34, fundo_cor=ESCURO):
    f = fonte('Black', tam)
    w = d.textlength(texto, font=f) + 40
    x = (W - w - 30) / 2
    d.rounded_rectangle((x, y, x + w + 30, y + tam + 34), radius=40, fill=fundo_cor, outline=cor, width=3)
    d.ellipse((x + 22, y + (tam + 34) / 2 - 7, x + 36, y + (tam + 34) / 2 + 7), fill=cor)
    d.text((x + 50, y + (tam + 34) / 2), texto, font=f, fill=cor, anchor='lm')


def cartao(base, foto, caixa, borda=CREME, raio=40):
    x0, y0, x1, y1 = caixa
    w, h = x1 - x0, y1 - y0
    s = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((x0 + 6, y0 + 22, x1 + 6, y1 + 22), radius=raio, fill=(0, 30, 10, 140))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(24)))
    card = Image.new('RGBA', (w, h), BRANCO + (255,))
    ft = Image.open(foto).convert('RGB')
    e = min((w - 60) / ft.width, (h - 60) / ft.height)
    ft = ft.resize((int(ft.width * e), int(ft.height * e)), Image.LANCZOS)
    card.paste(ft, ((w - ft.width) // 2, (h - ft.height) // 2))
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=raio, fill=255)
    card.putalpha(m)
    base.alpha_composite(card, (x0, y0))
    ImageDraw.Draw(base).rounded_rectangle(caixa, radius=raio, outline=borda, width=10)


def selo_redondo(base, centro, linhas, cor=CREME):
    d = ImageDraw.Draw(base)
    cx, cy = centro
    r = 120
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor, outline=ESCURO, width=6)
    tams = [34, 78, 30]
    alt = sum(tams) + 10
    y = cy - alt / 2
    for t, tam in zip(linhas, tams):
        d.text((cx, y + tam / 2), t, font=fonte('Black', tam), fill=ESCURO, anchor='mm')
        y += tam + 5


def caixas_preco(base, y, loja, lance):
    d = ImageDraw.Draw(base)
    larg, gap = 455, 30
    x0 = (W - 2 * larg - gap) / 2
    # na loja (riscado)
    d.rounded_rectangle((x0, y, x0 + larg, y + 190), radius=30, fill=ESCURO + (235,), outline=(120, 200, 140), width=3)
    d.text((x0 + larg / 2, y + 48), 'NA LOJA', font=fonte('Black', 34), fill=(205, 235, 214), anchor='mm')
    fv = fonte('Black', 76)
    tv = real(loja)
    d.text((x0 + larg / 2, y + 125), tv, font=fv, fill=BRANCO, anchor='mm')
    wv = d.textlength(tv, font=fv)
    d.line((x0 + larg / 2 - wv / 2 - 6, y + 130, x0 + larg / 2 + wv / 2 + 6, y + 120), fill=(240, 90, 80), width=8)
    # lance agora
    x1 = x0 + larg + gap
    d.rounded_rectangle((x1, y, x1 + larg, y + 190), radius=30, fill=LIMA, outline=ESCURO, width=4)
    d.text((x1 + larg / 2, y + 48), 'LANCE AGORA', font=fonte('Black', 34), fill=ESCURO, anchor='mm')
    d.text((x1 + larg / 2, y + 125), real(lance), font=fv, fill=ESCURO, anchor='mm')


def cta(base, texto, y):
    d = ImageDraw.Draw(base)
    f = fonte('Black', 50)
    w = d.textlength(texto, font=f)
    d.rounded_rectangle(((W - w) / 2 - 50, y, (W + w) / 2 + 50, y + 110), radius=55, fill=CREME)
    d.text((W / 2, y + 55), texto, font=f, fill=ESCURO, anchor='mm')
    for s in (-1, 1):  # risquinhos de "brilho" dos lados
        xb = W / 2 + s * (w / 2 + 80)
        d.line((xb, y + 30, xb + s * 34, y + 14), fill=CREME, width=7)
        d.line((xb + s * 6, y + 58, xb + s * 44, y + 58), fill=CREME, width=7)
        d.line((xb, y + 86, xb + s * 34, y + 102), fill=CREME, width=7)


def relogio(d, cx, cy, r, cor=LIMA):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cor, width=12)
    d.rectangle((cx - 16, cy - r - 34, cx + 16, cy - r - 8), fill=cor)
    d.line((cx, cy, cx, cy - r * 0.62), fill=cor, width=10)
    d.line((cx, cy, cx + r * 0.45, cy + r * 0.2), fill=cor, width=10)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=cor)


PRODUTO = 'Máquina de lavar Panasonic'
SUB = '15 kg · automática'
LOJA = 904.62
FOTO = f'{AQUI}/f-000.png'


def arte_palpite(lance, saida):
    b = fundo()
    _logo(b, y=90, largura=330)
    d = ImageDraw.Draw(b)
    pilula(d, 'HOJE · O MARTELO BATE ÀS 18H', 300)
    texto_rico(d, (540, 470), 'Por quanto *vai* *sair?*', fonte('Black', 104), 1000, destaque=CREME)
    cartao(b, FOTO, (250, 590, 830, 1250))
    selo_redondo(b, (850, 640), ['', '?', ''])
    d = ImageDraw.Draw(b)
    d.text((540, 1320), PRODUTO, font=fonte('Black', 56), fill=BRANCO, anchor='mm')
    d.text((540, 1382), SUB, font=fonte('Bold', 38), fill=(220, 245, 225), anchor='mm')
    caixas_preco(b, 1440, LOJA, lance)
    cta(b, 'ME CHAMA PRA DAR SEU LANCE', 1700)
    b.convert('RGB').save(saida, quality=93)


def arte_contagem(lance, quanto, unidade, frase, saida):
    b = fundo()
    _logo(b, y=90, largura=330)
    d = ImageDraw.Draw(b)
    pilula(d, 'LEILÃO DA MÁQUINA DE LAVAR', 300, cor=LIMA)
    relogio(d, 210, 520, 82)
    d.text((330, 520), 'FALTAM', font=fonte('Black', 120), fill=BRANCO, anchor='lm')
    texto_rico(d, (540, 700), f'*{quanto}* *{unidade}*', fonte('Black', 190), 1040, destaque=CREME)
    pilula(d, 'PARA O FIM DO LEILÃO', 820, cor=CREME, tam=32)
    cartao(b, FOTO, (230, 930, 850, 1440))
    off = round(100 * (1 - lance / LOJA))
    selo_redondo(b, (860, 980), ['HOJE', f'-{off}%', 'DA LOJA'])
    caixas_preco(b, 1480, LOJA, lance)
    cta(b, frase, 1720)
    b.convert('RGB').save(saida, quality=93)


def arte_arremate(lance, saida):
    b = fundo()
    _logo(b, y=90, largura=330)
    d = ImageDraw.Draw(b)
    relogio(d, 180, 380, 70)
    d.text((290, 380), 'HOJE ÀS 18H', font=fonte('Black', 104), fill=BRANCO, anchor='lm')
    texto_rico(d, (540, 540), 'você pode *arrematar*', fonte('Black', 84), 1000, destaque=LIMA)
    texto_rico(d, (540, 640), 'uma máquina que custa na loja', fonte('Bold', 48), 1000, cor=(225, 245, 230))
    cartao(b, FOTO, (70, 730, 600, 1370))
    d = ImageDraw.Draw(b)
    # coluna da direita: preço da loja e lance agora
    for i, (rot, val, cor_f, cor_t) in enumerate([('NA LOJA', real(LOJA), ESCURO, BRANCO), ('LANCE AGORA', real(lance), LIMA, ESCURO)]):
        y = 760 + i * 250
        d.rounded_rectangle((630, y, 1020, y + 210), radius=30, fill=cor_f, outline=CREME if i == 0 else ESCURO, width=4)
        d.text((825, y + 52), rot, font=fonte('Black', 34), fill=cor_t if i else (205, 235, 214), anchor='mm')
        d.text((825, y + 135), val, font=fonte('Black', 66), fill=cor_t, anchor='mm')
    off = round(100 * (1 - lance / LOJA))
    selo_redondo(b, (825, 1360), ['AGORA', f'-{off}%', 'DA LOJA'])
    d = ImageDraw.Draw(b)
    y = 1500
    d.rounded_rectangle((60, y, 1020, y + 140), radius=40, fill=ESCURO, outline=LIMA, width=3)
    itens = [('Martelo', 'hoje às 18h'), ('Produto', 'novo, de fábrica'), ('Lances', 'ao vivo no site')]
    for k, (a, c) in enumerate(itens):
        cx = 60 + 160 + k * 320
        d.text((cx, y + 48), a.upper(), font=fonte('Black', 32), fill=LIMA, anchor='mm')
        d.text((cx, y + 95), c, font=fonte('Bold', 30), fill=BRANCO, anchor='mm')
        if k:
            d.line((60 + k * 320, y + 30, 60 + k * 320, y + 110), fill=(120, 200, 140), width=3)
    cta(b, 'NÃO DEIXA PRA DEPOIS!', 1710)
    b.convert('RGB').save(saida, quality=93)


if __name__ == '__main__':
    lance = float(sys.argv[1])
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    arte_palpite(lance, f'{out}/1-por-quanto-vai-sair.jpg')
    arte_contagem(lance, '3', 'HORAS', 'NÃO DEIXA PRA DEPOIS!', f'{out}/2-faltam-3-horas.jpg')
    arte_arremate(lance, f'{out}/3-hoje-voce-pode-arrematar.jpg')
    print(out)
