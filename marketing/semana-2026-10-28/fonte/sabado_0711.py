# Sábado 07/11 — kit do leilão do iPhone 17 Pro Max (martelo 20h), mesma grade de horários do sábado 31/10.
# Sem "lance atual" nas artes (o lance muda o dia todo): âncora = preço de loja e o último iPhone (R$ 4.640, 24/10).
import os
from PIL import Image, ImageDraw, ImageFilter
from pecas import personagem, overlay, revela, enquete, feed_foto, feed_passos, AQUI
from stories_notebook import fundo, titulo, W, H
from notebook_dia import vidro
from arte_do_dia import LIMA, BRANCO, F
from vendedores2 import ic_martelo
from kit import logo as _logo, salvar

B = os.path.join(AQUI, '..', '..', 'semana-2026-11-05', 'sabado-07-11')
FT = 'iphone17pm.webp'
T = 'SÁBADO · DIA DE IPHONE'
LOJA = 'R$ 9.464,78'

# ---- stories da página (mesma grade do sábado passado)
overlay(f'{B}/stories/01-05h00-praia-FAIXA-cole-no-video.png', f'{B}/previas/01-05h00-praia-como-fica.jpg',
        'Hoje tem *iPhone* no martelo', 'Às 10h o Leiloeiro revela tudo. Martelo às 20h.', T,
        '[ VÍDEO DA EQUIPE NA PRAIA AO NASCER DO SOL ]')
personagem(f'{B}/stories/02-05h01-leiloeiro-bom-dia.jpg', T, 'leiloeiro', 'a-comemora',
           'Dou-lhe uma, dou-lhe duas… *bom dia*!', 'Hoje tem iPhone 17 Pro Max. O martelo bate às 20h.')
revela(f'{B}/stories/03-10h00-leiloeiro-revela.jpg', 'O MARTELO DE HOJE', FT,
       'iPhone *17* *Pro* *Max*', f'256GB prateado · na loja {LOJA} · martelo às 20h')
enquete(f'{B}/stories/04-10h01-enquete.jpg', f'{B}/previas/04-10h01-enquete-onde-colar.jpg', None, FT,
        'Quanto você *daria* nele?', 'Responde a enquete. O valor real sai às 20h.')
overlay(f'{B}/stories/05-14h00-ta-rolando-agora-FAIXA.png', f'{B}/previas/05-14h00-ta-rolando-como-fica.jpg',
        'Tá *rolando* agora!', 'O último saiu por R$ 4.640. E esse, vai sair por quanto?', 'LEILÃO AO VIVO',
        '[ VÍDEO: TELA DO LEILÃO DO IPHONE COM OS LANCES ]')
personagem(f'{B}/stories/06-19h00-falta-1-hora.jpg', 'ÚLTIMA HORA', 'leiloeiro', 'a-relogio',
           'Falta *1 hora*', 'Martelo às 20h. O lance é no site: toca no link aqui embaixo.')
overlay(f'{B}/stories/06b-19h00-FAIXA-se-gravar-video.png', f'{B}/previas/06b-19h00-como-fica.jpg',
        'Falta *1 hora*', 'Martelo às 20h. O lance é no site: toca no link aqui embaixo.', 'ÚLTIMA HORA',
        '[ VÍDEO: LANCE ATUAL NA TELA DO SITE ]')
overlay(f'{B}/stories/07-20h-martelo-batido-FAIXA-cole-no-video.png', f'{B}/previas/07-20h-martelo-como-fica.jpg',
        'Martelo *batido*!', f'Na loja: {LOJA}. Olha quanto saiu', 'IPHONE DE SÁBADO',
        '[ VÍDEO: TELA DO LEILÃO NOS ÚLTIMOS SEGUNDOS ]')
# ---- feed 12h (carrossel de 2)
feed_foto(f'{B}/feed/feed-12h-card1.jpg', 'HOJE O MARTELO BATE ÀS *20H*', FT, f'iPhone 17 Pro Max · na loja *R$* *9.464,78*')
feed_passos(f'{B}/feed/feed-12h-card2.jpg', 'QUEM *DECIDE* O PREÇO É VOCÊ',
            ['Comenta *IPHONE* aqui embaixo', 'Recebe o link no direct', 'Dá seu lance até as *20h*'], 'Comenta *IPHONE*')

# ---- vendedores + contagem (molde dos vendedores de sábado, com o iPhone recortado)
def faixa(d, texto, y, cor):
    f = F('Black', 34); w = d.textlength(texto, font=f)
    d.rounded_rectangle(((W - w) / 2 - 34, y - 30, (W + w) / 2 + 34, y + 30), radius=30, fill=(3, 40, 18), outline=cor, width=3)
    d.text((W / 2, y), texto, font=f, fill=cor, anchor='mm')

def iphone(b, cx, base, alt):
    p = Image.open(f'{AQUI}/iphone17pm-recorte.png').convert('RGBA'); p = p.crop(p.getbbox()); p = p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
    x, y = int(cx - p.width / 2), base - p.height
    g = Image.new('RGBA', b.size, (140, 255, 120, 0)); m = Image.new('L', b.size, 0); m.paste(p.split()[-1].point(lambda v: 110 if v > 20 else 0), (x, y))
    g.putalpha(m.filter(ImageFilter.GaussianBlur(40))); b.alpha_composite(g)
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((cx - p.width * .45, base - 16, cx + p.width * .45, base + 16), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(p, (x, y))

def peca(l1, l2, topo, saida):
    b = fundo(); _logo(b, y=140, largura=230); d = ImageDraw.Draw(b)
    faixa(d, topo, 330, LIMA); titulo(d, l1, l2, 470, 120)
    iphone(b, 540, 1176, 490)
    vidro(b, (190, 1190, 890, 1420), raio=30); d = ImageDraw.Draw(b)
    ic_martelo(d, 330, 1220, 48, LIMA)
    d.text((395, 1246), 'O ÚLTIMO SAIU POR', font=F('Black', 38), fill=LIMA, anchor='lm')
    d.text((540, 1345), 'R$ 4.640', font=F('Black', 120), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1490), 'IPHONE 17 PRO MAX', font=F('Black', 56), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1550), f'256GB PRATEADO • NA LOJA {LOJA}', font=F('Black', 32), fill=LIMA, anchor='mm')
    d.text((W / 2, 1610), 'lance inicial R$ 197 · confira o lance agora no link', font=F('Black', 30), fill=(205, 235, 214), anchor='mm')
    d.rounded_rectangle((190, 1660, 890, 1760), radius=50, fill=LIMA)
    d.text((540, 1710), 'DÊ SEU LANCE · leilaonozap.net', font=F('Black', 38), fill=(3, 34, 15), anchor='mm')
    os.makedirs(os.path.dirname(saida), exist_ok=True); b.convert('RGB').save(saida, quality=95)

V = f'{B}/vendedores'
for nome, l1, l2, topo in [
    ('VENDEDORES-08h-e-hoje', 'É HOJE', 'ÀS 20H', 'O MARTELO BATE HOJE'),
    ('VENDEDORES-15h-faltam-5-horas', 'FALTAM', '5 HORAS', 'AINDA DÁ TEMPO DE DAR LANCE'),
    ('VENDEDORES-19h30-ultima-chamada', 'ÚLTIMA', 'CHAMADA', 'FECHA ÀS 20H EM PONTO'),
    ('CONTAGEM-17h-faltam-3-horas', 'FALTAM', '3 HORAS', 'O MARTELO BATE ÀS 20H'),
    ('CONTAGEM-18h-faltam-2-horas', 'FALTAM', '2 HORAS', 'O MARTELO BATE ÀS 20H'),
    ('CONTAGEM-19h-falta-1-hora', 'FALTA', '1 HORA', 'ÚLTIMA HORA PARA DAR LANCE'),
    ('CONTAGEM-19h30-faltam-30-minutos', 'FALTAM', '30 MINUTOS', 'FECHA ÀS 20H EM PONTO'),
    ('CONTAGEM-19h50-faltam-10-minutos', 'FALTAM', '10 MINUTOS', 'ÚLTIMA CHAMADA')]:
    peca(l1, l2, topo, f'{V}/{nome}.jpg')
print('ok')
