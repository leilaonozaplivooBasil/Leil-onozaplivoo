# Carrossel de 3 páginas da PCX (sáb 21/11, 20h), no verde da marca, seguindo o curso Criadores Estratégicos:
# página 1 = GANCHO (pergunta, título grande, moto enorme) · página 2 = MEIO com a VIRADA (loja × leilão) · página 3 = UM pedido só.
# Também gera a versão "slide vídeo" (Reels 1080x1920) a partir das mesmas páginas. Uso: carrossel.py <lance>
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/carrossel'; MK = '/home/user/Leil-onozaplivoo/marketing'
os.makedirs(OUT, exist_ok=True)
LANCE = sys.argv[1] if len(sys.argv) > 1 else '522'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1350
VE, VM, MENTA, M2, M3, BR, NEON = (10, 61, 38), (27, 122, 72), (214, 236, 221), (190, 222, 200), (150, 200, 168), (255, 255, 255), (63, 208, 126)
LADO = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); LADO = LADO.crop(LADO.getbbox())
FRENTE = Image.open(f'{AQ}/fotos/pcx-plataforma-frente.png').convert('RGBA'); FRENTE = FRENTE.crop(FRENTE.getbbox())
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def logo(b, y=H - 110):
    lg = LOGO.copy(); lg.thumbnail((200, 200)); x = (W - lg.width) // 2
    ImageDraw.Draw(b).rounded_rectangle((x - 22, y - 12, x + lg.width + 22, y + lg.height + 12), 34, fill=VE); b.alpha_composite(lg, (x, y))
def moto(b, img, larg, cx, chao, c1, c2):
    m = img.resize((larg, int(img.height * larg / img.width)), Image.LANCZOS); d = ImageDraw.Draw(b)
    pw, ph, pr = larg * .9, 54, 36; x0 = cx - pw / 2
    d.polygon([(x0, chao), (x0 + pw, chao), (x0 + pw + pr, chao - pr), (x0 + pr, chao - pr)], fill=c1); d.rectangle((x0, chao, x0 + pw, chao + ph), fill=c2)
    d.polygon([(x0 + pw, chao), (x0 + pw + pr, chao - pr), (x0 + pw + pr, chao + ph - pr), (x0 + pw, chao + ph)], fill=tuple(int(v * .9) for v in c2))
    chao -= pr / 2; s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - larg * .42, chao - 14, cx + larg * .42, chao + 18), fill=(0, 0, 0, 110)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(m, (int(cx - larg / 2), int(chao - m.height + 6)))
def pilula(d, cx, cy, t, f, fundo, cor, px=30):
    w = d.textlength(t, font=f); h = f.size * 1.75; d.rounded_rectangle((cx - w / 2 - px, cy - h / 2, cx + w / 2 + px, cy + h / 2), h / 2, fill=fundo); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def pagina(d, n, cor):
    d.text((W - 60, 60), f'{n}/3', font=F('Bold', 30), fill=cor, anchor='rm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=94); print('ok', n)

# 1 · GANCHO — pergunta
b = Image.new('RGBA', (W, H), MENTA + (255,)); d = ImageDraw.Draw(b); pagina(d, 1, VE)
pilula(d, W / 2, 95, 'LEILÃO HOJE · 20H', F('Black', 30), VE, MENTA)
d.text((W / 2, 205), 'QUANTO VOCÊ', font=F('Black', 112), fill=VE, anchor='mm')
d.text((W / 2, 320), 'DARIA NESSA', font=F('Black', 112), fill=VE, anchor='mm')
d.text((W / 2, 440), 'MOTO?', font=F('Black', 150), fill=VM, anchor='mm')
moto(b, LADO, 900, W / 2, 1100, M2, M3); d = ImageDraw.Draw(b)
d.text((W / 2, 1165), 'Honda PCX 160 · branca perolizada', font=F('Medium', 36), fill=VE, anchor='mm')
pilula(d, W / 2, 1265, 'arrasta pro lado  →', F('Bold', 32), VM, BR, 40)
salva(b, 'CARROSSEL-1-gancho')

# 2 · MEIO + VIRADA — loja × leilão
b = Image.new('RGBA', (W, H), MENTA + (255,)); d = ImageDraw.Draw(b); pagina(d, 2, VE)
d.text((W / 2, 110), 'NA LOJA, UNS', font=F('Medium', 54), fill=VE, anchor='mm')
d.text((W / 2, 210), 'R$ 20 MIL', font=F('Black', 140), fill=VE, anchor='mm')
moto(b, FRENTE, 700, W / 2, 820, M2, M3); d = ImageDraw.Draw(b)
for i, t in enumerate(['Full LED', 'painel digital', 'freio CBS']):
    pilula(d, 210 + i * 330, 880, t, F('Bold', 30), BR, VE, 26)
d.rounded_rectangle((70, 960, W - 70, 1240), 40, fill=VE)
d.text((W / 2, 1015), 'NO LEILÃO DE HOJE, O LANCE TÁ EM', font=F('Bold', 34), fill=MENTA, anchor='mm')
fr, fn = F('Black', 64), F('Black', 170); n = real(LANCE); wr, wn = d.textlength('R$', font=fr), d.textlength(n, font=fn); x = (W - wr - 12 - wn) / 2
d.text((x, 1080), 'R$', font=fr, fill=NEON, anchor='lm'); d.text((x + wr + 12, 1120), n, font=fn, fill=BR, anchor='lm')
d.text((W / 2, 1290), 'quem decide o preço é quem dá o lance', font=F('Medium', 34), fill=VE, anchor='mm')
salva(b, 'CARROSSEL-2-loja-x-leilao')

# 3 · FINAL — um pedido só
b = Image.new('RGBA', (W, H), VM + (255,)); d = ImageDraw.Draw(b); pagina(d, 3, MENTA)
d.text((W / 2, 130), 'HOJE, ÀS 20H,', font=F('Medium', 64), fill=MENTA, anchor='mm')
d.text((W / 2, 240), 'O MARTELO BATE', font=F('Black', 108), fill=BR, anchor='mm')
moto(b, LADO, 800, W / 2, 860, (22, 104, 61), (17, 88, 51)); d = ImageDraw.Draw(b)
d.rounded_rectangle((90, 900, W - 90, 1130), 40, fill=BR)
d.text((W / 2, 965), 'QUER O LINK PRA DAR LANCE?', font=F('Bold', 38), fill=VM, anchor='mm')
d.text((W / 2, 1060), 'Comenta MOTO', font=F('Black', 96), fill=VE, anchor='mm')
d.text((W / 2, 1180), 'que eu te mando no direct · retirada em mãos', font=F('Medium', 32), fill=MENTA, anchor='mm')
logo(b, 1225)
salva(b, 'CARROSSEL-3-comenta-moto')
