# Artes do grupo — versão 4 (28/10/2026, à tarde): fundo e máquina com acabamento de foto profissional (gerados por IA,
# sem nenhum texto), e por cima SÓ o essencial em letra grande: quanto tempo falta, o modelo e o lance atual (do sistema).
# Uso: python3 vendedores4.py <lance> <topo> <grande> <chamada> <saida.jpg>
import sys
from PIL import Image, ImageDraw
from vendedores2 import F, real, camada_texto, colar_centro, ic_cronometro, ic_martelo, ic_fogo, vidro, LIMA, LIMA_ESC, CREME, FUNDO_ESC, BRANCO
from vendedores3 import faixa_curva, texto_em_arco
from kit import AQUI, logo as _logo

W, H = 1080, 1620


def fundo():
    im = Image.open(f'{AQUI}/fundo-ia-maquina.jpg').convert('RGB')
    im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
    y0 = 70
    return im.crop((0, y0, W, y0 + H)).convert('RGBA')


def arte(lance, topo, grande, cta, saida):
    b = fundo()
    # véu escuro suave no topo para o título "saltar"
    veu = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(veu)
    for y in range(560):
        dv.line([(0, y), (W, y)], fill=(2, 40, 14, int(120 * (1 - y / 560))))
    b.alpha_composite(veu)
    _logo(b, y=40, largura=250)
    d = ImageDraw.Draw(b)
    ic_cronometro(d, 120, 255, 56, LIMA)
    colar_centro(b, camada_texto(topo, F('Black', 84), BRANCO, relevo=6), 600, 255)
    tam = 260
    while tam > 140 and ImageDraw.Draw(b).textlength(grande, font=F('Black', tam)) > 1000:
        tam -= 10
    colar_centro(b, camada_texto(grande, F('Black', tam), ((240, 255, 160), LIMA_ESC), relevo=18, brilho=LIMA), 540, 415)
    faixa_curva(b, 540, 548, 2200, 0.30, 90, FUNDO_ESC + (225,), LIMA)
    texto_em_arco(b, 'PRA VOCÊ ARREMATAR', F('Black', 46), CREME, 540, 548, 2200, esp=7)
    # modelo (embaixo à esquerda, sobre o reflexo)
    d = ImageDraw.Draw(b)
    vidro(b, (50, 1390, 640, 1500), borda=LIMA, raio=30)
    d = ImageDraw.Draw(b)
    d.text((80, 1428), 'Máquina de lavar Panasonic', font=F('Black', 38), fill=BRANCO, anchor='lm')
    d.text((80, 1470), '15 kg · automática', font=F('Bold', 30), fill=(215, 245, 222), anchor='lm')
    # lance atual (à direita)
    vidro(b, (690, 1120, 1045, 1370), borda=LIMA, raio=34)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 718, 1148, 48, CREME)
    d.text((782, 1162), 'LANCE', font=F('Black', 32), fill=CREME, anchor='lm')
    d.text((782, 1198), 'ATUAL', font=F('Black', 32), fill=CREME, anchor='lm')
    v = real(lance)
    fv = F('Black', 84)
    while d.textlength(v, font=fv) > 290:
        fv = F('Black', fv.size - 4)
    d.rounded_rectangle((710, 1240, 1025, 1352), radius=28, fill=LIMA)
    d.text((867, 1296), v, font=fv, fill=FUNDO_ESC, anchor='mm')
    # chamada
    f = F('Black', 50)
    w = d.textlength(cta, font=f)
    ic_fogo(b, 540 - w / 2 - 24, 1570, 30)
    d.text((540 + 24, 1570), cta, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    arte(float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
