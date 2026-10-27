# Arte do Martelo Batido com o valor real (feita logo depois do martelo, com o preço lido do banco).
# Uso: python3 martelo.py "Máquina de lavar Panasonic 15 kg" 904.62 735.00 f-001.png saida.jpg
import sys
from PIL import ImageDraw
from kit import *


def real(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def martelo(produto, loja, saiu, foto, saida):
    b = fundo(brilho=(540, 700))
    logo(b)
    selo(b, 'MARTELO BATIDO', 330)
    cartao_foto(b, f'{AQUI}/{foto}', (70, 430, 600, 930))
    p = leiloeiro('a-comemora', 720)
    sombra(p, b, (W - p.width + 40, 1240 - p.height))
    preco(b, (90, 955), 'Na loja', real(loja), cor_valor=(235, 235, 235), riscado=True, tam=60)
    preco(b, (90, 1075), 'Saiu por', real(saiu), cor_valor=DOURADO, tam=86)
    economia = round(100 * (1 - saiu / loja))
    faixa(b, f'{produto}', f'{economia}% abaixo da loja. Sábado tem mais: comenta SÁBADO.')
    salvar(b, saida)


if __name__ == '__main__':
    martelo(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5])
