# Artes do grupo — versão 5 (28/10/2026): a MÁQUINA e o LANCE BAIXO são o destaque (pedido da Natália).
# O tempo vira uma linha curta no topo; o lance atual (do sistema) é o maior texto da arte.
# Uso: python3 vendedores5.py <lance> "<tempo>" "<chamada>" <saida.jpg>     ex.: 650 "3 HORAS" "NÃO DEIXA PRA DEPOIS!" a.jpg
import sys
from PIL import Image, ImageDraw
from vendedores2 import F, real, camada_texto, colar_centro, ic_cronometro, ic_martelo, ic_fogo, vidro, LIMA, LIMA_ESC, CREME, FUNDO_ESC, BRANCO
from kit import AQUI, logo as _logo

W, H = 1080, 1620


def fundo(y0=290):
    im = Image.open(f'{AQUI}/fundo-ia-maquina.jpg').convert('RGB')
    im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
    return im.crop((0, y0, W, y0 + H)).convert('RGBA')


def arte(lance, tempo, cta, saida, prefixo='FALTA MENOS DE'):
    b = fundo()
    veu = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(veu)
    for y in range(330):
        dv.line([(0, y), (W, y)], fill=(2, 40, 14, int(150 * (1 - y / 330))))
    for y in range(H - 520, H):
        dv.line([(0, y), (W, y)], fill=(2, 36, 12, int(170 * ((y - (H - 520)) / 520) ** 1.4)))
    b.alpha_composite(veu)
    _logo(b, y=36, largura=230)
    # linha do tempo: pílula escura com cronômetro, "FALTA MENOS DE" + tempo em lima
    d = ImageDraw.Draw(b)
    f1, f2 = F('Black', 50), F('Black', 58)
    w1, w2 = d.textlength(prefixo + ' ', font=f1), d.textlength(tempo, font=f2)
    larg = 90 + w1 + w2 + 50
    x0 = (W - larg) / 2
    vidro(b, (x0, 196, x0 + larg, 290), borda=LIMA, raio=47)
    d = ImageDraw.Draw(b)
    ic_cronometro(d, x0 + 52, 246, 26, LIMA)
    d.text((x0 + 92, 243), prefixo + ' ', font=f1, fill=BRANCO, anchor='lm')
    d.text((x0 + 92 + w1, 243), tempo, font=f2, fill=LIMA, anchor='lm')
    # o LANCE: o maior texto da arte, à direita, sobre o reflexo
    colar_centro(b, camada_texto('LANCE ATUAL', F('Black', 54), BRANCO, relevo=5), 800, 1150)
    v = real(lance)
    tam = 190
    while tam > 110 and ImageDraw.Draw(b).textlength(v, font=F('Black', tam)) > 560:
        tam -= 6
    colar_centro(b, camada_texto(v, F('Black', tam), ((245, 255, 170), LIMA_ESC), relevo=16, brilho=LIMA), 790, 1285)
    # modelo
    vidro(b, (50, 1400, 660, 1505), borda=LIMA, raio=30)
    d = ImageDraw.Draw(b)
    d.text((82, 1436), 'Máquina de lavar Panasonic', font=F('Black', 38), fill=BRANCO, anchor='lm')
    d.text((82, 1478), '15 kg · automática · nova', font=F('Bold', 30), fill=(215, 245, 222), anchor='lm')
    # chamada
    f = F('Black', 50)
    w = d.textlength(cta, font=f)
    ic_fogo(b, 540 - w / 2 - 24, 1568, 30)
    d.text((540 + 24, 1568), cta, font=f, fill=LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    arte(float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])
