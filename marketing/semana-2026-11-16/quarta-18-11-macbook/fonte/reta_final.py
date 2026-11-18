# Reta final do MacBook (qua 18/11): FALTA 1 HORA (19h, entrada fechou: só quem já deu lance segue) e FALTAM 10 MINUTOS (19h50).
# O número do lance é o único que muda na hora. Uso: reta_final.py <lance> [1h|10min]
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/visual'; MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1]; SO = sys.argv[2:] or ['1h', '10min']
MIN = next((x[:-3] for x in SO if x.endswith('min') and x != '10min'), None); PESSOAS = next((x[1:] for x in SO if x.startswith('p')), None)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
W, H = 1080, 1920; BR, OURO, OCL, AMA, VERM, NOITE, NEON = (255, 255, 255), (245, 196, 81), (250, 228, 170), (255, 214, 10), (230, 32, 40), (8, 18, 13), (63, 208, 126)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA'); MAC = MAC.crop(MAC.getbbox())
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def fundo(c1, c0, cy=900):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - cy) * .85) / 1150, 0, 1) ** 1.2
    a = np.array(c1)[None, None] * (1 - d[..., None]) + np.array(c0)[None, None] * d[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def glow(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def logo(b):
    lg = LOGO.copy(); lg.thumbnail((200, 200)); x = (W - lg.width) // 2
    ImageDraw.Draw(b).rounded_rectangle((x - 22, 66, x + lg.width + 22, 94 + lg.height), 26, fill=(10, 20, 16, 235)); b.alpha_composite(lg, (x, 80))
def mac(b, larg, base):
    m = MAC.resize((larg, int(MAC.height * larg / MAC.width)), Image.LANCZOS)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - larg * .46, base - 14, W / 2 + larg * .46, base + 20), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    b.alpha_composite(m, (int(W / 2 - larg / 2), int(base - m.height)))
def cont(d, xy, t, f, cor, w=6, sombra=(0, 0, 0)):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=sombra, anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
def caixa_lance(d, y, cor_borda=OURO):
    d.rounded_rectangle((150, y, W - 150, y + 200), 34, fill=(0, 0, 0, 200), outline=cor_borda, width=4)
    d.text((W / 2, y + 48), 'LANCE ATUAL', font=F('Bold', 34), fill=cor_borda, anchor='mm'); d.text((W / 2, y + 132), f'R$ {real(LANCE)}', font=F('Black', 110), fill=BR, anchor='mm')
def pilula(d, y, t, f, fundo, cor):
    w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - 40, y - 52, W / 2 + w / 2 + 40, y + 52), 52, fill=fundo); d.text((W / 2, y + 2), t, font=f, fill=cor, anchor='mm')

if '1h' in SO:   # relógio-anel quase vazio: 1 hora · a entrada fechou
    b = fundo((22, 84, 54), NOITE, 760); logo(b); cx, cy, r = W / 2, 690, 330
    glow(b, (cx - 430, cy - 430, cx + 430, cy + 430), OURO, 90, 120); d = ImageDraw.Draw(b)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 40), width=34)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * (60 / 720), fill=VERM, width=34)   # só 1 de 12 horas sobrando
    for k in range(60):
        an = k / 60 * 2 * math.pi; r1, r2 = r - 52, r - (78 if k % 5 == 0 else 62)
        d.line((cx + r1 * math.sin(an), cy - r1 * math.cos(an), cx + r2 * math.sin(an), cy - r2 * math.cos(an)), fill=(255, 255, 255, 150 if k % 5 == 0 else 70), width=5 if k % 5 == 0 else 3)
    d.text((cx, cy - 40), '1', font=AN(300), fill=BR, anchor='mm'); d.text((cx, cy + 150), 'HORA', font=AN(110), fill=OURO, anchor='mm')
    cont(d, (W / 2, 1150), 'PRO MARTELO BATER', F('Black', 74), BR)
    pilula(d, 1270, 'ENTRADA FECHADA', F('Black', 58), VERM, BR)
    d.text((W / 2, 1360), 'agora só disputa quem já deu lance', font=F('SemiBold', 40), fill=OCL, anchor='mm')
    caixa_lance(d, 1410); mac(b, 360, 1880)
    b.convert('RGB').save(f'{OUT}/V8-19h-falta-1-hora.jpg', quality=94); print('ok 1h')
for N in (['10'] if '10min' in SO else []) + ([MIN] if MIN else []):   # placar estourando: N MINUTOS, vermelho, raios
    b = fundo((150, 16, 22), (30, 2, 4), 760); logo(b); cx, cy = W / 2, 700; d = ImageDraw.Draw(b)
    for k in range(28):
        an = k / 28 * 2 * math.pi; r1, r2 = 330, 900
        d.polygon([(cx + r1 * math.cos(an - .045), cy + r1 * math.sin(an - .045)), (cx + r2 * math.cos(an), cy + r2 * math.sin(an)), (cx + r1 * math.cos(an + .045), cy + r1 * math.sin(an + .045))], fill=(255, 80, 60, 70))
    glow(b, (cx - 380, cy - 380, cx + 380, cy + 380), AMA, 120, 90); logo(b); d = ImageDraw.Draw(b)
    d.text((cx + 10, cy - 60 + 12), N, font=AN(460), fill=(0, 0, 0, 150), anchor='mm'); d.text((cx, cy - 60), N, font=AN(460), fill=AMA, anchor='mm')
    cont(d, (cx, cy + 250), 'MINUTOS', AN(150), BR, 7)
    cont(d, (W / 2, 1150), 'O MARTELO VAI BATER!', F('Black', 76), BR)
    d.text((W / 2, 1250), (f'{PESSOAS} pessoas na disputa · quem deu lance pode cobrir' if PESSOAS else 'quem já deu lance ainda pode cobrir'), font=F('SemiBold', 40), fill=(255, 225, 225), anchor='mm')
    caixa_lance(d, 1330, AMA); mac(b, 420, 1830)
    nome = 'V9-19h50-faltam-10-minutos' if N == '10' else f'V10-faltam-{N}-minutos'; b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print('ok', nome)
