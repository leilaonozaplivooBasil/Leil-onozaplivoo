# Story único para a figurinha de CONTAGEM REGRESSIVA do Instagram (31/10/2026, pedido da Natália): logo, chamada,
# o notebook real e um espaço livre no meio para ela colar a figurinha. Sem valor de lance (não envelhece) e sem link.
import sys
from PIL import ImageDraw
from arte_do_dia import LIMA, BRANCO, F, produto
from notebook_dia import FOTO, NOME, SPEC
from stories_notebook import fundo, titulo, W
from kit import logo as _logo

b = fundo()
_logo(b, y=150, largura=260)
d = ImageDraw.Draw(b)
d.text((W / 2, 400), 'O MARTELO BATE', font=F('Black', 70), fill=BRANCO, anchor='mm')
titulo(d, 'HOJE', 'ÀS 18H', 520, 130)
# espaço da figurinha: moldura tracejada discreta
x0, y0, x1, y1 = 150, 760, 930, 1010
for x in range(x0, x1, 28) if len(sys.argv) < 3 else []:
    d.line((x, y0, min(x + 14, x1), y0), fill=(190, 242, 60, 110), width=3); d.line((x, y1, min(x + 14, x1), y1), fill=(190, 242, 60, 110), width=3)
for y in range(y0, y1, 28) if len(sys.argv) < 3 else []:
    d.line((x0, y, x0, min(y + 14, y1)), fill=(190, 242, 60, 110), width=3); d.line((x1, y, x1, min(y + 14, y1)), fill=(190, 242, 60, 110), width=3)
produto(b, FOTO, 540, 1440, 380)
d = ImageDraw.Draw(b)
d.text((W / 2, 1520), NOME, font=F('Black', 56), fill=BRANCO, anchor='mm')
d.text((W / 2, 1580), SPEC, font=F('Black', 34), fill=LIMA, anchor='mm')
d.rounded_rectangle((170, 1640, 910, 1740), radius=50, fill=LIMA)
d.text((540, 1690), 'Comenta NOTEBOOK pra dar lance', font=F('Black', 38), fill=(3, 34, 15), anchor='mm')
saida = sys.argv[1]
b.convert('RGB').save(saida, quality=95)
# versão sem a moldura tracejada (se preferir o fundo limpo atrás da figurinha)
