# Contagem regressiva do MacBook Neo (qua 18/11, martelo 20h) + REGRA NOVA do 1º lance até as 19h.
# 6 artes de story/status (1080x1920), verde da marca + dourado; o vermelho só no aviso da regra.
# 10h É HOJE · 14h FALTAM 6 HORAS · 17h 1º LANCE ATÉ 19H · 18h30 ÚLTIMOS 30 MIN PRO 1º LANCE · 19h50 ÚLTIMOS 10 · 20h É AGORA
# Uso: contagem.py <lance> <n_pessoas> [só: 10h,14h,...]
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE, NP = sys.argv[1], int(sys.argv[2]); SO = sys.argv[3].split(',') if len(sys.argv) > 3 else None
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
BR, OURO, OURO2, VERDE2, ESC, CREME, VERM, AMA = (255, 255, 255), (245, 196, 81), (246, 214, 140), (27, 122, 72), (5, 28, 17), (214, 230, 218), (214, 26, 34), (255, 210, 0)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')

def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def fundo(cy=900, c1=(24, 88, 56)):
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - cy) * .85) / 1150, 0, 1) ** 1.2
    a = np.array(c1)[None, None] * (1 - dd[..., None]) + np.array(ESC)[None, None] * dd[..., None]
    a += np.random.default_rng(3).normal(0, 1.5, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def cabe(d, t, peso, tam, larg=W * .9):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 20: tam -= 2
    return F(peso, tam)
def txt(d, y, t, peso, tam, cor, sombra=True):
    f = cabe(d, t, peso, tam)
    if sombra: d.text((W / 2, y + 7), t, font=f, fill=(0, 0, 0, 150), anchor='mm')
    d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def pil(d, y, t, f, fundo_, cor):
    w = d.textlength(t, font=f); h = f.size + 30
    d.rounded_rectangle((W / 2 - w / 2 - 34, y - h / 2, W / 2 + w / 2 + 34, y + h / 2), h / 2, fill=fundo_); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def brilho(b, cx, cy, r, cor=OURO, a=80):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * .5)))
def mac(b, larg, base):
    mm = MAC.resize((larg, int(MAC.height * larg / MAC.width)), Image.LANCZOS)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - larg * .47, base - 18, W / 2 + larg * .47, base + 22), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(20)))
    b.alpha_composite(mm, (int((W - larg) / 2), int(base - mm.height)))
def logo(b, y=110, larg=180):
    lg = LOGO.copy(); lg.thumbnail((larg, larg)); b.alpha_composite(lg, ((W - lg.width) // 2, y))
def rodape(b, y=1640, sub=None):
    d = ImageDraw.Draw(b); d.text((W / 2, y), 'LANCE ATUAL', font=F('SemiBold', 34), fill=OURO, anchor='mm')
    fR, fN = F('Medium', 56), F('Black', 150); wr = d.textlength('R$ ', font=fR); wn = d.textlength(real(LANCE), font=fN); x0 = (W - wr - wn) / 2
    d.text((x0, y + 170), 'R$', font=fR, fill=OURO2, anchor='ls'); d.text((x0 + wr, y + 170), real(LANCE), font=fN, fill=OURO2, anchor='ls')
    d.text((W / 2, y + 225), sub or 'MacBook Neo 13" · prateado · novo e lacrado', font=F('Medium', 34), fill=CREME, anchor='mm')
def tarja_regra(d, y, t1='1º LANCE SÓ ATÉ AS 19H', t2='depois disso, fica de fora'):
    d.rounded_rectangle((W * .07, y, W * .93, y + 150), 28, fill=VERM); d.text((W / 2, y + 52), t1, font=F('Black', 56), fill=BR, anchor='mm'); d.text((W / 2, y + 112), t2, font=F('SemiBold', 36), fill=(255, 225, 225), anchor='mm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=94); print('ok', n)
def quer(h): return SO is None or h in SO

if quer('10h'):
    b = fundo(950); logo(b); d = ImageDraw.Draw(b); pil(d, 320, 'QUARTA É DIA DE LEILÃO', F('Black', 40), OURO, ESC)
    txt(d, 520, 'É HOJE!', 'Black', 240, BR); txt(d, 700, 'às 20h', 'Black', 130, OURO)
    brilho(b, W / 2, 1020, 300, a=60); mac(b, 560, 1210); d = ImageDraw.Draw(b); tarja_regra(d, 1260); rodape(b, 1500); salva(b, 'MAC-1-10h-e-hoje')
if quer('14h'):
    b = fundo(800); logo(b); d = ImageDraw.Draw(b); pil(d, 320, 'O MARTELO BATE EM', F('Black', 40), OURO, ESC)
    txt(d, 560, '6', 'Black', 420, OURO); txt(d, 820, 'HORAS', 'Black', 140, BR)
    mac(b, 440, 1215); d = ImageDraw.Draw(b); tarja_regra(d, 1240); rodape(b, 1500); salva(b, 'MAC-2-14h-faltam-6-horas')
if quer('17h'):
    b = fundo(700, (120, 20, 26)); logo(b); d = ImageDraw.Draw(b); pil(d, 320, '⚠ ATENÇÃO'.replace('⚠ ', ''), F('Black', 44), AMA, ESC)
    txt(d, 500, 'FALTAM 2 HORAS', 'Black', 110, BR); txt(d, 640, 'PRO 1º LANCE', 'Black', 110, AMA)
    d.text((W / 2, 760), 'quem não der lance até as 19h fica de fora', font=F('SemiBold', 42), fill=(255, 225, 225), anchor='mm')
    mac(b, 640, 1240); rodape(b, 1460); salva(b, 'MAC-3-17h-faltam-2h-pro-1o-lance')
if quer('18h30'):
    b = fundo(700, (130, 18, 24)); logo(b); d = ImageDraw.Draw(b); pil(d, 320, 'ÚLTIMA CHAMADA', F('Black', 44), AMA, ESC)
    txt(d, 560, '30', 'Black', 400, AMA); txt(d, 800, 'MINUTOS', 'Black', 130, BR)
    d.text((W / 2, 920), 'pra dar o seu 1º lance (até as 19h)', font=F('Bold', 46), fill=BR, anchor='mm')
    mac(b, 520, 1340); rodape(b, 1460); salva(b, 'MAC-4-18h30-ultimos-30-pro-1o-lance')
if quer('19h50'):
    b = fundo(800); logo(b); d = ImageDraw.Draw(b); pil(d, 320, 'RETA FINAL', F('Black', 44), OURO, ESC)
    txt(d, 560, '10', 'Black', 400, OURO); txt(d, 800, 'MINUTOS', 'Black', 130, BR)
    d.text((W / 2, 920), 'pro martelo bater no MacBook', font=F('Bold', 46), fill=CREME, anchor='mm')
    mac(b, 520, 1340); rodape(b, 1460, 'quem deu lance ainda pode cobrir · vai até as 20h'); salva(b, 'MAC-5-19h50-ultimos-10')
if quer('20h'):
    b = fundo(850); logo(b); d = ImageDraw.Draw(b); pil(d, 320, 'O MARTELO VAI BATER', F('Black', 44), OURO, ESC)
    txt(d, 560, 'É AGORA!', 'Black', 220, BR); brilho(b, W / 2, 1000, 360, a=80)
    mac(b, 760, 1280); rodape(b, 1400, 'MacBook Neo 13" · últimos segundos'); salva(b, 'MAC-6-20h-e-agora')
