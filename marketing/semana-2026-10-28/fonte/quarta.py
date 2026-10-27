# Kit de quarta 28/10/2026 — leilão da Máquina de lavar Panasonic 15 kg, martelo às 18h.
# Roda: python3 quarta.py  → gera ../quarta-28-10/
import os
from PIL import ImageDraw
from kit import *

OUT = os.path.join(AQUI, '..', 'quarta-28-10')
F = lambda n: f'{AQUI}/f-00{n}.png'
TOPO = 'QUARTA · DIA DE LEILÃO'


def previa_video(sob, legenda):
    """Só para o dono enxergar como fica: a sobreposição em cima de um 'vídeo' de mentira."""
    base = fundo()
    d = ImageDraw.Draw(base)
    texto_rico(d, (540, 760), legenda, fonte('Bold', 44), 760, cor=(150, 190, 165))
    base.alpha_composite(sob)
    return base


# 05h00 — equipe correndo na praia (a equipe grava; esta faixa vai por cima)
sob = sobreposicao('Já estamos *aquecendo*', 'Hoje tem leilão. Às 10h o Leiloeiro revela o produto.', topo=TOPO)
salvar(sob, f'{OUT}/stories/01-05h00-praia-FAIXA-cole-no-video.png')
salvar(previa_video(sob, '[ VÍDEO DA EQUIPE CORRENDO NA PRAIA AO NASCER DO SOL ]'), f'{OUT}/previas/01-05h00-praia-como-fica.jpg')

# 05h01 — Leiloeiro fecha o bom dia (arte pronta da Duda)
b = fundo(brilho=(540, 820))
logo(b)
selo(b, TOPO, 330)
p = leiloeiro('a-comemora', 860)
sombra(p, b, ((W - p.width) // 2, 1250 - p.height + 20))
faixa(b, 'Hoje tem *leilão*!', 'Às 10h eu revelo o produto. Ativa o lembrete aqui embaixo.')
salvar(b, f'{OUT}/stories/02-05h01-leiloeiro-bom-dia.jpg')

# 10h00 — Leiloeiro revela o produto principal (arte pronta)
b = fundo(brilho=(420, 760))
logo(b)
selo(b, 'O MARTELO DE HOJE', 330)
cartao_foto(b, F(0), (480, 430, 1010, 1190))
p = leiloeiro('a-apresenta', 820)  # aponta para a máquina (nunca espelhar: o colete tem o nome escrito)
sombra(p, b, (-70, 1240 - p.height))
faixa(b, 'Máquina de lavar *Panasonic* *15* *kg*', 'Na loja: R$ 904,62 · martelo hoje às 18h')
salvar(b, f'{OUT}/stories/03-10h00-leiloeiro-revela.jpg')

# 10h01 — enquete "quanto você daria?" (arte pronta, espaço livre para a figurinha)
b = fundo(brilho=(540, 640))
logo(b)
cartao_foto(b, F(2), (190, 300, 890, 1000))
d = ImageDraw.Draw(b)
d.rounded_rectangle((150, 1030, 930, 1210), radius=30, outline=DOURADO + (120,), width=3)
faixa(b, 'Quanto você *daria* nela?', 'Responde a enquete. O valor real sai às 18h.')
limpo = b.copy()
d.text((540, 1120), 'COLE A ENQUETE AQUI', font=fonte('Black', 36), fill=DOURADO, anchor='mm')
salvar(b, f'{OUT}/previas/04-10h01-enquete-onde-colar.jpg')
ImageDraw.Draw(limpo).rounded_rectangle((150, 1030, 930, 1210), radius=30, fill=None, outline=None)
b = fundo(brilho=(540, 640))
logo(b)
cartao_foto(b, F(2), (190, 300, 890, 1000))
faixa(b, 'Quanto você *daria* nela?', 'Responde a enquete. O valor real sai às 18h.')
salvar(b, f'{OUT}/stories/04-10h01-enquete.jpg')

# 14h00 — produto conferido no galpão (a equipe grava; faixa por cima)
sob = sobreposicao('Conferida e *testada*', 'Antes de ir pra sua casa, passa pela nossa mão. Martelo às 18h.', topo=TOPO)
salvar(sob, f'{OUT}/stories/05-14h00-galpao-FAIXA-cole-no-video.png')
salvar(previa_video(sob, '[ VÍDEO: ALGUÉM DA EQUIPE LIGANDO A MÁQUINA NO GALPÃO ]'), f'{OUT}/previas/05-14h00-galpao-como-fica.jpg')

# 17h00 — falta 1 hora (equipe ao vivo; arte pronta se não der para gravar)
b = fundo(brilho=(540, 820))
logo(b)
selo(b, 'ÚLTIMA HORA', 330)
p = leiloeiro('a-relogio', 860)
sombra(p, b, ((W - p.width) // 2, 1250 - p.height + 20))
faixa(b, 'Falta *1 hora*', 'Martelo às 18h. O lance é no site: toca no link aqui embaixo.')
salvar(b, f'{OUT}/stories/06-17h00-falta-1-hora.jpg')
sob = sobreposicao('Falta *1 hora*', 'Martelo às 18h. O lance é no site: toca no link aqui embaixo.', topo='ÚLTIMA HORA')
salvar(sob, f'{OUT}/stories/06b-17h00-FAIXA-se-gravar-video.png')

# 18h — Martelo Batido (equipe ao vivo). A arte com o valor real é feita pela Duda logo depois do martelo.
sob = sobreposicao('Martelo *batido*!', 'Na loja: R$ 904,62. Olha quanto saiu', topo='LEILÃO DE QUARTA')
salvar(sob, f'{OUT}/stories/07-18h-martelo-batido-FAIXA-cole-no-video.png')

# 12h — feed (carrossel 4:5, 2 cards)
FW, FH = 1080, 1350
b = fundo(FW, FH, brilho=(540, 600))
logo(b, y=60, largura=300)
d = ImageDraw.Draw(b)
texto_rico(d, (540, 300), 'QUANTO VOCÊ *DARIA* NESSA MÁQUINA DE LAVAR?', fonte('Black', 76), 960)
cartao_foto(b, F(1), (250, 450, 830, 1130))
d = ImageDraw.Draw(b)
d.rounded_rectangle((60, 1170, 1020, 1300), radius=34, fill=VERDE_ESCURO, outline=DOURADO, width=3)
texto_rico(d, (540, 1236), 'Na loja: *R$* *904,62* · martelo HOJE às 18h', fonte('Black', 44), 920)
salvar(b, f'{OUT}/feed/feed-12h-card1.jpg')

b = fundo(FW, FH, brilho=(780, 760))
logo(b, y=60, largura=300)
d = ImageDraw.Draw(b)
texto_rico(d, (540, 270), 'QUEM *DECIDE* O PREÇO É VOCÊ', fonte('Black', 76), 960)
p = leiloeiro('a-apresenta', 760)
sombra(p, b, (FW - p.width + 120, FH - p.height - 40))
passos = [('1', 'Comenta *QUARTA* aqui embaixo'), ('2', 'Recebe o link no direct'), ('3', 'Dá seu lance até as *18h*')]
y = 470
for n, t in passos:
    d.ellipse((70, y, 160, y + 90), fill=DOURADO)
    d.text((115, y + 45), n, font=fonte('Black', 54), fill=VERDE_ESCURO, anchor='mm')
    linhas = t.split(' ')
    x = 190
    for i, w_ in enumerate(linhas):
        c = DOURADO if '*' in w_ else BRANCO
        s = w_.replace('*', '') + ' '
        if x + d.textlength(s, font=fonte('Black', 44)) > 600:
            x, y = 190, y + 54
        d.text((x, y + 18), s, font=fonte('Black', 44), fill=c)
        x += d.textlength(s, font=fonte('Black', 44))
    y += 210
d.rounded_rectangle((60, 1170, 640, 1300), radius=34, fill=VERDE_ESCURO, outline=DOURADO, width=3)
texto_rico(d, (350, 1236), 'Comenta *QUARTA*', fonte('Black', 54), 560)
salvar(b, f'{OUT}/feed/feed-12h-card2.jpg')
print('ok', OUT)
