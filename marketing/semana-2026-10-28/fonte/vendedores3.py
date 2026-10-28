# Artes do grupo dos vendedores — versão 3 (28/10/2026): a MESMA sequência da arte do iPhone que o time aprovou
# ("Falta menos de 3 horas"), em 2:3 (1080x1620): fundo verde tom sobre tom com cortes diagonais (planos mais claros e
# mais escuros), cronômetro + "FALTA MENOS DE", número gigante em lima com relevo, faixa curva "PRA VOCÊ ARREMATAR",
# linha curva "UMA MÁQUINA QUE CUSTA EM MÉDIA", produto com brilho à esquerda, cartões de vidro à direita, selo de
# desconto, barra de confiança e a chamada com foguinho.
# Uso: python3 vendedores3.py <lance_agora> <numero> <unidade> <arquivo_saida>   ex.: 600 8 HORAS saida.jpg
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from vendedores2 import (F, real, camada_texto, colar_centro, ic_cronometro, ic_etiqueta, ic_martelo, ic_relogio,
                         ic_raio, ic_escudo, ic_fogo, seta_curva, vidro, selo, produto, etiqueta_produto, cartao_preco,
                         LIMA, LIMA_ESC, CREME, FUNDO_ESC, BRANCO, FOTO, PRODUTO, SUB, LOJA)
from kit import logo as _logo

W, H = 1080, 1620


def fundo_facetado():
    """Verde tom sobre tom: base em degradê e planos com corte reto, uns mais claros, outros mais escuros."""
    y = np.linspace(0, 1, H)[:, None, None]
    base = (np.array([16, 140, 54]) * (1 - y) + np.array([7, 104, 37]) * y).astype('uint8').repeat(W, 1)
    im = Image.fromarray(base, 'RGB').convert('RGBA')

    def plano(pts, cor, alfa):
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(c).polygon([(x * W, y * H) for x, y in pts], fill=cor + (alfa,))
        im.alpha_composite(c.filter(ImageFilter.GaussianBlur(1.2)))

    escuro, claro = (4, 70, 26), (90, 220, 120)
    plano([(0, 0), (0.58, 0), (0, 0.40)], escuro, 120)                          # canto de cima à esquerda, mais escuro
    plano([(0.58, 0), (1, 0), (1, 0.16), (0, 0.66), (0, 0.40)], claro, 62)       # faixa clara em diagonal (atrás do título)
    plano([(1, 0.16), (1, 0.30), (0.12, 0.64), (0, 0.66)], claro, 34)            # corte fino logo abaixo
    plano([(1, 0.30), (1, 0.62), (0.2, 1), (0, 1), (0, 0.66), (0.12, 0.64)], escuro, 75)  # plano do produto, mais fundo
    plano([(1, 0.62), (1, 0.70), (0.36, 1), (0.2, 1)], claro, 45)                # corte claro embaixo à direita
    plano([(1, 0.70), (1, 1), (0.36, 1)], escuro, 100)                            # canto de baixo, escuro
    # brilho atrás do produto e luz no topo
    for cx, cy, r, cor, a in [(0.32, 0.56, 0.42, (120, 255, 120), 120), (0.5, 0.08, 0.5, (150, 255, 170), 50)]:
        g = Image.new('L', (W, H), 0)
        ImageDraw.Draw(g).ellipse(((cx - r) * W, cy * H - r * W, (cx + r) * W, cy * H + r * W), fill=a)
        c = Image.new('RGBA', (W, H), cor + (0,))
        c.putalpha(g.filter(ImageFilter.GaussianBlur(120)))
        im.alpha_composite(c)
    # vinheta nas bordas
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    v = (np.clip((d - 0.42) / 0.35, 0, 1) * 110).astype('uint8')
    im = Image.composite(Image.new('RGBA', (W, H), (0, 30, 12, 255)), im, Image.fromarray(v, 'L'))
    return im


def texto_em_arco(base, texto, fonte, cor, cx, cy, raio, esp=5, sobe=True):
    """Escreve o texto numa curva suave (a 'faixa curva' da arte do iPhone)."""
    d = ImageDraw.Draw(base)
    largs = [d.textlength(c, font=fonte) + esp for c in texto]
    total = sum(largs) - esp
    ang = -total / 2 / raio
    for c, w in zip(texto, largs):
        meio = ang + (w - esp) / 2 / raio
        x = cx + raio * math.sin(meio)
        y = cy - raio * math.cos(meio) + raio if sobe else cy
        letra = Image.new('RGBA', (int(fonte.size * 1.6), int(fonte.size * 1.6)), (0, 0, 0, 0))
        ImageDraw.Draw(letra).text((letra.width / 2, letra.height / 2), c, font=fonte, fill=cor, anchor='mm')
        letra = letra.rotate(-math.degrees(meio), resample=Image.BICUBIC)
        base.alpha_composite(letra, (int(x - letra.width / 2), int(y - letra.height / 2)))
        ang += w / raio


def faixa_curva(base, cx, cy, raio, larg_ang, altura, cor_fundo, cor_borda):
    """Uma pílula curva (pedaço de anel) com pontas arredondadas."""
    c = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    pts_ext, pts_int = [], []
    for t in np.linspace(-larg_ang / 2, larg_ang / 2, 60):
        pts_ext.append((cx + (raio + altura / 2) * math.sin(t), cy + raio - (raio + altura / 2) * math.cos(t)))
        pts_int.append((cx + (raio - altura / 2) * math.sin(t), cy + raio - (raio - altura / 2) * math.cos(t)))
    poly = pts_ext + pts_int[::-1]
    d.polygon(poly, fill=cor_fundo)
    for t in (-larg_ang / 2, larg_ang / 2):  # pontas redondas
        px, py = cx + raio * math.sin(t), cy + raio - raio * math.cos(t)
        d.ellipse((px - altura / 2, py - altura / 2, px + altura / 2, py + altura / 2), fill=cor_fundo)
    contorno = Image.new('L', base.size, 0)
    dm = ImageDraw.Draw(contorno)
    dm.polygon(poly, fill=255)
    for t in (-larg_ang / 2, larg_ang / 2):
        px, py = cx + raio * math.sin(t), cy + raio - raio * math.cos(t)
        dm.ellipse((px - altura / 2, py - altura / 2, px + altura / 2, py + altura / 2), fill=255)
    borda = contorno.filter(ImageFilter.MaxFilter(7))
    anel = Image.new('RGBA', base.size, cor_borda + (0,))
    anel.putalpha(Image.fromarray(np.clip(np.array(borda, int) - np.array(contorno, int), 0, 255).astype('uint8')))
    base.alpha_composite(c)
    base.alpha_composite(anel)


def etiqueta(b, x, y):
    vidro(b, (x, y, x + 500, y + 108), borda=LIMA, raio=26)
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((x + 24, y + 22, x + 66, y + 86), radius=9, outline=CREME, width=5)
    d.line((x + 37, y + 32, x + 53, y + 32), fill=CREME, width=4)
    d.text((x + 88, y + 38), PRODUTO, font=F('Black', 32), fill=BRANCO, anchor='lm')
    d.text((x + 88, y + 76), SUB, font=F('Bold', 27), fill=(210, 240, 218), anchor='lm')


def arte(lance, numero, unidade, saida, topo='FALTA MENOS DE', linha='UMA MÁQUINA QUE CUSTA EM MÉDIA',
         cta='NÃO DEIXA PRA DEPOIS!'):
    b = fundo_facetado()
    _logo(b, y=50, largura=270)
    d = ImageDraw.Draw(b)
    # 1) cronômetro + FALTA MENOS DE
    ic_cronometro(d, 118, 300, 58, LIMA)
    t1 = camada_texto(topo, F('Black', 86), BRANCO, relevo=6)
    colar_centro(b, t1, 600, 300)
    # 2) o número gigante
    txt = f'{numero} {unidade}'
    tam = 270
    while tam > 140 and ImageDraw.Draw(b).textlength(txt, font=F('Black', tam)) > 990:
        tam -= 10
    t2 = camada_texto(txt, F('Black', tam), ((235, 255, 150), LIMA_ESC), relevo=16, brilho=LIMA)
    colar_centro(b, t2, 540, 470)
    # 3) faixa curva + linha curva
    faixa_curva(b, 540, 600, 2200, 0.30, 92, FUNDO_ESC + (215,), LIMA)
    texto_em_arco(b, 'PRA VOCÊ ARREMATAR', F('Black', 46), CREME, 540, 600, 2200, esp=7)
    texto_em_arco(b, linha, F('Black', 30), BRANCO, 540, 690, 2600, esp=6)
    d = ImageDraw.Draw(b)
    seta_curva(d, (900, 700), (1000, 740), (955, 810), LIMA)
    # 4) produto à esquerda, com brilho
    produto(b, FOTO, 320, 1300, 500, ang=-3)
    etiqueta(b, 60, 1225)
    # 5) cartões à direita
    cartao_preco(b, (610, 780, 1030, 985), ic_etiqueta, 'VALOR MÉDIO', 'NA LOJA', real(LOJA))
    cartao_preco(b, (610, 1005, 1030, 1210), ic_martelo, 'LANCE ATUAL', 'DO LEILÃO', real(lance), destaque=True)
    d = ImageDraw.Draw(b)
    seta_curva(d, (1042, 1215), (1055, 1250), (1000, 1268), LIMA)
    off = round(100 * (1 - lance / LOJA))
    selo(b, 860, 1298, 88, ['HOJE', f'-{off}%', 'DA LOJA'])
    # 6) barra de confiança
    vidro(b, (40, 1405, 1040, 1530), borda=LIMA, raio=62)
    d = ImageDraw.Draw(b)
    itens = [(lambda x, y: ic_relogio(d, x, y, 26, CREME), 'LEILÃO TERMINA', 'HOJE ÀS 18H'),
             (lambda x, y: ic_raio(d, x, y, 56, CREME), 'PRODUTO NOVO', 'DE FÁBRICA'),
             (lambda x, y: ic_escudo(d, x, y, 56, CREME), 'LANCES SEGUROS', 'E AO VIVO')]
    for k, (ic, a, c) in enumerate(itens):
        x = 40 + k * 333
        ic(x + 52, 1467)
        d.text((x + 94, 1450), a, font=F('Bold', 24), fill=(225, 245, 230), anchor='lm')
        d.text((x + 94, 1486), c, font=F('Black', 27), fill=BRANCO, anchor='lm')
        if k:
            d.line((x, 1430, x, 1505), fill=(150, 225, 160), width=2)
    # 7) chamada
    d = ImageDraw.Draw(b)
    f = F('Black', 48)
    w = d.textlength(cta, font=f)
    ic_fogo(b, 540 - w / 2 - 22, 1578, 28)
    d.text((540 + 22, 1578), cta, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    arte(float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])


def arte_simples(lance, numero, unidade, saida, cta='NÃO DEIXA PRA DEPOIS!', leiloeiro_pose=None):
    """Versão enxuta (pedido da Natália, 28/10): só o tempo que falta, a máquina grande no centro, o modelo e o lance atual."""
    b = fundo_facetado()
    _logo(b, y=45, largura=250)
    d = ImageDraw.Draw(b)
    ic_cronometro(d, 118, 265, 58, LIMA)
    colar_centro(b, camada_texto('FALTA MENOS DE', F('Black', 86), BRANCO, relevo=6), 600, 265)
    txt = f'{numero} {unidade}'
    tam = 270
    while tam > 140 and ImageDraw.Draw(b).textlength(txt, font=F('Black', tam)) > 990:
        tam -= 10
    colar_centro(b, camada_texto(txt, F('Black', tam), ((235, 255, 150), LIMA_ESC), relevo=16, brilho=LIMA), 540, 430)
    # a máquina, grande e no centro (ou à direita, com o Leiloeiro apresentando)
    if leiloeiro_pose:
        produto(b, FOTO, 690, 1275, 670, ang=0)
        from kit import leiloeiro as _lei, sombra as _sombra
        p = _lei(leiloeiro_pose, 700)
        _sombra(p, b, (10, 1290 - p.height), raio=24, forca=120)
    else:
        produto(b, FOTO, 540, 1275, 690, ang=0)
    # nome do modelo
    d = ImageDraw.Draw(b)
    nome = 'Máquina de lavar Panasonic 15 kg'
    f = F('Black', 44)
    w = d.textlength(nome, font=f)
    vidro(b, (540 - w / 2 - 50, 1300, 540 + w / 2 + 50, 1390), borda=LIMA, raio=45)
    d = ImageDraw.Draw(b)
    d.text((540, 1345), nome, font=f, fill=BRANCO, anchor='mm')
    # lance atual
    f1, f2 = F('Black', 40), F('Black', 92)
    v = real(lance)
    w1, w2 = d.textlength('LANCE ATUAL', font=f1), d.textlength(v, font=f2)
    larg = w1 + w2 + 150
    x0 = 540 - larg / 2
    vidro(b, (x0, 1410, x0 + larg, 1535), borda=LIMA, raio=40)
    d = ImageDraw.Draw(b)
    ic_martelo(d, x0 + 30, 1447, 50, CREME)
    d.text((x0 + 100, 1472), 'LANCE ATUAL', font=f1, fill=CREME, anchor='lm')
    d.rounded_rectangle((x0 + 120 + w1, 1422, x0 + larg - 12, 1523), radius=30, fill=LIMA)
    d.text((x0 + 120 + w1 + (larg - 132 - w1) / 2, 1472), v, font=f2, fill=FUNDO_ESC, anchor='mm')
    # chamada
    f = F('Black', 46)
    w = d.textlength(cta, font=f)
    ic_fogo(b, 540 - w / 2 - 22, 1580, 27)
    d.text((540 + 22, 1580), cta, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


def arte_prompt(lance, topo, grande, barra1, saida, foto=None, linha='UM PRODUTO QUE CUSTA EM MÉDIA', cta='NÃO DEIXA PRA DEPOIS!'):
    """Fiel ao prompt da Natália (28/10, 13h30): valor médio, lance atual, selo 'ATÉ -X% DE DIFERENÇA' e barra de 3 ícones."""
    b = fundo_facetado()
    _logo(b, y=50, largura=270)
    d = ImageDraw.Draw(b)
    ic_cronometro(d, 118, 300, 58, LIMA)
    colar_centro(b, camada_texto(topo, F('Black', 86), BRANCO, relevo=6), 600, 300)
    tam = 270
    while tam > 140 and ImageDraw.Draw(b).textlength(grande, font=F('Black', tam)) > 990:
        tam -= 10
    colar_centro(b, camada_texto(grande, F('Black', tam), ((235, 255, 150), LIMA_ESC), relevo=16, brilho=LIMA), 540, 470)
    faixa_curva(b, 540, 600, 2200, 0.30, 92, FUNDO_ESC + (215,), LIMA)
    texto_em_arco(b, 'PRA VOCÊ ARREMATAR', F('Black', 46), CREME, 540, 600, 2200, esp=7)
    texto_em_arco(b, linha, F('Black', 30), BRANCO, 540, 690, 2600, esp=6)
    d = ImageDraw.Draw(b)
    seta_curva(d, (900, 700), (1000, 740), (955, 810), LIMA)
    produto(b, foto or FOTO, 320, 1300, 540, ang=-6)
    etiqueta(b, 60, 1225)
    cartao_preco(b, (610, 780, 1030, 985), ic_etiqueta, 'VALOR MÉDIO', 'DO PRODUTO', real(LOJA))
    cartao_preco(b, (610, 1005, 1030, 1210), ic_martelo, 'LANCE ATUAL', 'DO LEILÃO', real(lance), destaque=True)
    d = ImageDraw.Draw(b)
    seta_curva(d, (1042, 1215), (1055, 1250), (1000, 1268), LIMA)
    off = round(100 * (1 - lance / LOJA))
    selo(b, 860, 1298, 88, ['ATÉ', f'-{off}%', 'DE DIFERENÇA'])
    vidro(b, (40, 1405, 1040, 1530), borda=LIMA, raio=62)
    d = ImageDraw.Draw(b)
    itens = [(lambda x, y: ic_relogio(d, x, y, 26, CREME), barra1[0], barra1[1]),
             (lambda x, y: ic_raio(d, x, y, 56, CREME), 'PRODUTOS', 'ORIGINAIS'),
             (lambda x, y: ic_escudo(d, x, y, 56, CREME), 'LANCES SEGUROS', 'E TRANSPARENTES')]
    for k, (ic, a, c) in enumerate(itens):
        x = 40 + k * 333
        ic(x + 52, 1467)
        d.text((x + 94, 1450), a, font=F('Bold', 22), fill=(225, 245, 230), anchor='lm')
        fc = F('Black', 25)
        while d.textlength(c, font=fc) > 225:
            fc = F('Black', fc.size - 1)
        d.text((x + 94, 1486), c, font=fc, fill=BRANCO, anchor='lm')
        if k:
            d.line((x, 1430, x, 1505), fill=(150, 225, 160), width=2)
    f = F('Black', 48)
    w = d.textlength(cta, font=f)
    ic_fogo(b, 540 - w / 2 - 22, 1578, 28)
    d.text((540 + 22, 1578), cta, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)
