# Martelo Batido no padrão da arte do dia (quadrado, verde-escuro, lima nos números). Sem preço de loja:
# o lance final passou do "valor médio" cadastrado, então só o resultado real e a disputa. Nome do arrematante NUNCA aparece.
# Uso: python3 martelo_batido_dia.py <valor_final> <lances> <foto> <saida>
import sys
from PIL import ImageDraw
import arte_do_dia as a
from vendedores2 import ic_martelo
from kit import AQUI, logo as _logo


def arte(valor, lances, foto, saida, nome='MÁQUINA DE LAVAR PANASONIC', spec='15 KG • AUTOMÁTICA'):
    b = a.fundo()
    _logo(b, y=26, largura=150)
    d = ImageDraw.Draw(b)
    f = a.F('Black', 96)
    w1, w2 = d.textlength('MARTELO ', font=f), d.textlength('BATIDO!', font=f)
    x = (a.S - w1 - w2) / 2
    d.text((x + 4, 206), 'MARTELO ', font=f, fill=(0, 20, 8), anchor='lm')
    d.text((x + w1 + 4, 206), 'BATIDO!', font=f, fill=(0, 20, 8), anchor='lm')
    d.text((x, 200), 'MARTELO ', font=f, fill=a.BRANCO, anchor='lm')
    d.text((x + w1, 200), 'BATIDO!', font=f, fill=a.LIMA, anchor='lm')
    a.produto(b, foto, 330, 870, 590)
    from PIL import Image
    c = Image.new('RGBA', b.size, (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((610, 330, 1015, 600), radius=26, fill=(3, 40, 18, 225), outline=a.LIMA + (230,), width=3)
    b.alpha_composite(c)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 640, 362, 46, a.LIMA)
    d.text((702, 388), 'ARREMATADA', font=a.F('Black', 34), fill=a.LIMA, anchor='lm')
    d.text((812, 470), a.real(valor), font=a.F('Black', 100), fill=a.BRANCO, anchor='mm')
    d.text((812, 556), 'lance final', font=a.F('Bold', 28), fill=(200, 230, 210), anchor='mm')
    cx, cy, r = 812, 760, 112
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=a.LIMA)
    d.text((cx, cy - 22), f'{lances}', font=a.F('Black', 84), fill=a.ESCURO, anchor='mm')
    d.text((cx, cy + 48), 'LANCES', font=a.F('Black', 28), fill=a.ESCURO, anchor='mm')
    d.text((a.S / 2, 960), nome, font=a.F('Black', 50), fill=a.BRANCO, anchor='mm')
    d.text((a.S / 2, 1016), spec, font=a.F('Black', 32), fill=a.LIMA, anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    arte(float(sys.argv[1]), int(sys.argv[2]), f'{AQUI}/{sys.argv[3]}', sys.argv[4])
