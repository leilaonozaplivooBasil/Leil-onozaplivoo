# Artes do MacBook Neo PRATEADO na mesa (foto oficial montada no cenário de mesa): feed 1080x1350 e story 1080x1920.
# Faixa verde da marca em cima (nome) e embaixo (lance + data). Uso: artes_macbook_mesa.py <lance>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
BRANCO, CREME, OURO, OURO2, VERDE, ESC = (247, 247, 244), (214, 230, 218), (226, 186, 104), (246, 214, 140), (14, 58, 37), (5, 28, 17)
FOTO = Image.open(f'{OUT}/macbook-na-mesa-1.jpg').convert('RGBA')

def degrade(b, y0, y1, cor, a0, a1):
    W = b.width; g = np.zeros((y1 - y0, W, 4), np.uint8); g[..., :3] = cor
    g[..., 3] = np.linspace(a0, a1, y1 - y0)[:, None].astype(np.uint8); b.alpha_composite(Image.fromarray(g), (0, y0))
def logo(b, y, larg=150):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((larg, 62)); b.alpha_composite(lg, ((b.width - lg.width) // 2, y))
def centro(d, W, y, t, f, cor): d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def lance(d, W, y, tam):
    fR, fN = F('Medium', tam * 34 // 100), F('Bold', tam); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
    d.text((x0, y), 'R$', font=fR, fill=OURO2, anchor='ls'); d.text((x0 + wr, y), LANCE, font=fN, fill=OURO2, anchor='ls')
def pilula(d, W, cy, t, f):
    wt = d.textlength(t, font=f); h = f.size + 30
    d.rounded_rectangle((W / 2 - wt / 2 - 40, cy - h / 2, W / 2 + wt / 2 + 40, cy + h / 2), h / 2, fill=ESC, outline=OURO, width=2); d.text((W / 2, cy), t, font=f, fill=BRANCO, anchor='mm')

def arte(W, H, nome, y_foto, cfg):
    b = Image.new('RGBA', (W, H), VERDE + (255,)); f = FOTO.resize((W, int(FOTO.height * W / FOTO.width)), Image.LANCZOS); b.alpha_composite(f, (0, y_foto))
    degrade(b, 0, cfg['topo'], VERDE, 250, 0) if y_foto <= 0 else degrade(b, y_foto, y_foto + 260, VERDE, 255, 0)
    degrade(b, cfg['base'] - 220, cfg['base'], VERDE, 0, 255); ImageDraw.Draw(b).rectangle((0, cfg['base'], W, H), fill=VERDE)
    d = ImageDraw.Draw(b); logo(b, cfg['logo']); d = ImageDraw.Draw(b)
    centro(d, W, cfg['kicker'], ' '.join('LEILÃO DE QUARTA · 20H'), F('SemiBold', 30), OURO)
    centro(d, W, cfg['nome'], 'MacBook Neo 13"', F('Bold', cfg['tam']), BRANCO)
    centro(d, W, cfg['sub'], 'Prateado  ·  Chip A18 Pro  ·  256GB', F('Medium', 36), CREME)
    centro(d, W, cfg['rot'], ' '.join('LANCE ATUAL'), F('SemiBold', 30), OURO); lance(d, W, cfg['lance'], cfg['tl'])
    pilula(d, W, cfg['data'], 'quarta-feira, 18/11, às 20h', F('SemiBold', 36))
    b.convert('RGB').save(f'{OUT}/{nome}', quality=95); print('ok', nome)

arte(1080, 1350, 'arte-macbook-mesa-feed.jpg', -150, dict(topo=520, base=1150, logo=40, kicker=140, nome=225, tam=104, sub=305,
     rot=1095, lance=1225, tl=120, data=1295))
arte(1080, 1920, 'arte-macbook-mesa-story.jpg', 330, dict(base=1600, logo=110, kicker=240, nome=330, tam=112, sub=420,
     rot=1560, lance=1745, tl=170, data=1835))
