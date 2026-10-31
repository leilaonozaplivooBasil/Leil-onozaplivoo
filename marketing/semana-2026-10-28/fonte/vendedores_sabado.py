# Stories (9:16) para os VENDEDORES divulgarem o leilão do notebook no sábado 31/10 (8h, 13h e 17h30/18h).
# Padrão verde aprovado, SEM selo de porcentagem (Instagram restringiu a conta por "prática comercial" em 30/10:
# nada de "-9X%" por 30 dias). Lance sempre do sistema. Rodapé com o site, porque status de WhatsApp não tem figurinha.
# Uso: python3 vendedores_sabado.py <lance> <num_lances> <saida_dir>
import os, sys
from PIL import ImageDraw
from arte_do_dia import LIMA, BRANCO, F, real, produto
from notebook_dia import FOTO, NOME, SPEC, vidro
from stories_notebook import fundo, titulo, W
from vendedores2 import ic_martelo
from kit import logo as _logo

PECAS = [  # (arquivo, linha branca, linha lima, faixa de cima)
    ('VENDEDORES-08h-e-hoje', 'É HOJE', 'ÀS 18H', 'O MARTELO BATE HOJE'),
    ('VENDEDORES-13h-faltam-5-horas', 'FALTAM', '5 HORAS', 'AINDA DÁ TEMPO DE DAR LANCE'),
    ('VENDEDORES-17h30-ultima-chamada', 'ÚLTIMA', 'CHAMADA', 'FECHA ÀS 18H EM PONTO'),
]


def faixa(d, texto, y, cor):
    f = F('Black', 34)
    w = d.textlength(texto, font=f)
    d.rounded_rectangle(((W - w) / 2 - 34, y - 30, (W + w) / 2 + 34, y + 30), radius=30, fill=(3, 40, 18), outline=cor, width=3)
    d.text((W / 2, y), texto, font=f, fill=cor, anchor='mm')


def peca(lance, n_lances, linha1, linha2, topo, saida):
    b = fundo()
    _logo(b, y=140, largura=230)
    d = ImageDraw.Draw(b)
    faixa(d, topo, 330, LIMA)
    titulo(d, linha1, linha2, 470, 120)
    produto(b, FOTO, 540, 1172, 470)
    vidro(b, (190, 1190, 890, 1420), raio=30)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 330, 1220, 48, LIMA)
    d.text((395, 1246), 'LANCE ATUAL', font=F('Black', 40), fill=LIMA, anchor='lm')
    d.text((540, 1345), real(lance), font=F('Black', 120), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1490), NOME, font=F('Black', 56), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1550), SPEC, font=F('Black', 34), fill=LIMA, anchor='mm')
    if n_lances:
        d.text((W / 2, 1610), f'{n_lances} lances já dados', font=F('Black', 32), fill=(205, 235, 214), anchor='mm')
    d.rounded_rectangle((190, 1660, 890, 1760), radius=50, fill=LIMA)
    d.text((540, 1710), 'DÊ SEU LANCE · leilaonozap.net', font=F('Black', 38), fill=(3, 34, 15), anchor='mm')
    b.convert('RGB').save(saida, quality=95)


if __name__ == '__main__':
    lance, n, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    os.makedirs(out, exist_ok=True)
    for nome, l1, l2, topo in PECAS:
        peca(lance, n, l1, l2, topo, f'{out}/{nome}.jpg')
        print(f'{out}/{nome}.jpg')
