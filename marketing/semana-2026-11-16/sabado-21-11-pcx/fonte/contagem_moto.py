# Contagem do leilão da Honda PCX 160 (sáb 21/11, 20h): 7 artes, cada uma um conceito DE MOTO (nada de repetir o molde de sempre).
# 09h placa Mercosul "É HOJE" · 12h etiqueta de preço (loja ~R$ 20 mil × lance) · 15h velocímetro analógico · 17h painel digital da PCX
# · 19h semáforo amarelo · 19h50 semáforo verde "ACELERA" · 20h bandeira quadriculada "LARGADA". Uso: contagem_moto.py <lance> [so]
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/contagem-sabado'; MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'; SO = sys.argv[2].split(',') if len(sys.argv) > 2 else None
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
W, H = 1080, 1920
BR, OURO, AMA, VERDE, NEON, NOITE, VERM, AZUL = (255, 255, 255), (245, 196, 81), (255, 210, 0), (27, 122, 72), (63, 208, 126), (6, 18, 12), (230, 32, 40), (0, 61, 165)
MOTO = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); MOTO = MOTO.crop(MOTO.getbbox())
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def quer(k): return SO is None or k in SO
def fundo(c1, c0, cy=900, ruido=1.6):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - cy) * .85) / 1150, 0, 1) ** 1.2
    a = np.array(c1)[None, None] * (1 - d[..., None]) + np.array(c0)[None, None] * d[..., None]; a += np.random.default_rng(3).normal(0, ruido, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def glow(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def logo(b, y=70, escuro=True):
    lg = LOGO.copy(); lg.thumbnail((190, 190)); x = (W - lg.width) // 2
    if escuro: ImageDraw.Draw(b).rounded_rectangle((x - 20, y - 12, x + lg.width + 20, y + lg.height + 12), 24, fill=(6, 18, 12, 230))
    b.alpha_composite(lg, (x, y))
def moto(b, larg, cx, base, espelho=False, reflexo=True, sombra=True):
    m = MOTO.resize((larg, int(MOTO.height * larg / MOTO.width)), Image.LANCZOS)
    if espelho: m = ImageOps.mirror(m)
    if sombra:
        s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - larg * .45, base - 18, cx + larg * .45, base + 24), fill=(0, 0, 0, 180)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(20)))
    if reflexo:
        r = m.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, larg, int(m.height * .28))); al = np.array(r.split()[3]).astype(float) * np.linspace(.25, 0, r.height)[:, None]; r.putalpha(Image.fromarray(al.astype('uint8')))
        b.alpha_composite(r, (int(cx - larg / 2), base))
    b.alpha_composite(m, (int(cx - larg / 2), base - m.height))
def cont(d, xy, t, f, cor, w=6, anchor='mm'):
    for dx in range(-w, w + 1, 3):
        for dy in range(-w, w + 1, 3): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0), anchor=anchor)
    d.text(xy, t, font=f, fill=cor, anchor=anchor)
def pilula(d, cx, cy, t, f, fundo_, cor, px=40):
    w = d.textlength(t, font=f); h = f.size * 1.6
    d.rounded_rectangle((cx - w / 2 - px, cy - h / 2, cx + w / 2 + px, cy + h / 2), h / 2, fill=fundo_); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def rodape(d, y=1830, cor=NEON, txt='leilaonozap.net'):
    pilula(d, W / 2, y, txt, F('Black', 42), cor, NOITE)
def caixa_lance(d, y, borda=OURO, rot='LANCE ATUAL'):
    d.rounded_rectangle((170, y, W - 170, y + 190), 32, fill=(0, 0, 0, 215), outline=borda, width=4)
    d.text((W / 2, y + 46), rot, font=F('Bold', 34), fill=borda, anchor='mm'); d.text((W / 2, y + 126), f'R$ {real(LANCE)}', font=AN(96), fill=BR, anchor='mm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=94); print('ok', n)

# 1 · 09h · PLACA MERCOSUL "É HOJE"
if quer('09h'):
    b = fundo((26, 96, 60), NOITE, 950); logo(b); d = ImageDraw.Draw(b)
    for i in range(30):   # asfalto: faixas de velocidade
        y = 220 + i * 52; d.line((0, y, W, y + 40), fill=(255, 255, 255, 10), width=2)
    # placa
    px0, py0, pw, ph = 110, 300, 860, 330
    pl = Image.new('RGBA', (pw, ph)); p = ImageDraw.Draw(pl)
    p.rounded_rectangle((0, 0, pw - 1, ph - 1), 34, fill=(252, 252, 250), outline=(20, 20, 20), width=10)
    p.rounded_rectangle((10, 10, pw - 11, 92), 24, fill=AZUL); p.rectangle((10, 60, pw - 11, 92), fill=AZUL)
    p.text((pw / 2, 52), 'BRASIL', font=F('Black', 46), fill=BR, anchor='mm')
    p.rectangle((34, 26, 84, 74), fill=(0, 150, 60)); p.polygon([(59, 30), (80, 50), (59, 70), (38, 50)], fill=AMA); p.ellipse((50, 41, 68, 59), fill=AZUL)
    p.text((pw - 70, 52), 'BR', font=F('Black', 36), fill=BR, anchor='mm')
    p.text((pw / 2, 218), 'HOJ3·20H', font=AN(190), fill=(20, 20, 20), anchor='mm')
    pl = pl.rotate(-3, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', pl.size, (0, 0, 0, 0)); sh.putalpha(pl.split()[3].point(lambda v: int(v * .55))); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (px0 + 12, py0 + 22)); b.alpha_composite(pl, (px0, py0))
    d = ImageDraw.Draw(b)
    cont(d, (W / 2, 760), 'É HOJE!', AN(190), AMA, 7)
    d.text((W / 2, 880), 'o leilão da moto é hoje às 20h', font=F('SemiBold', 46), fill=BR, anchor='mm')
    glow(b, (W / 2 - 480, 1030, W / 2 + 480, 1600), OURO, 70, 120)
    moto(b, 880, W / 2, 1490)
    d = ImageDraw.Draw(b); d.text((W / 2, 1590), 'HONDA PCX 160 · branca perolizada', font=F('Bold', 40), fill=BR, anchor='mm')
    pilula(d, W / 2, 1690, f'lance atual R$ {real(LANCE)}', F('Black', 50), OURO, NOITE)
    rodape(d); salva(b, 'PCX-1-09h-placa-e-hoje')

# 2 · 12h · ETIQUETA DE PREÇO (vale ~20 mil × começa em 497)
if quer('12h'):
    b = fundo((245, 243, 236), (205, 210, 205), 800, 1.0); logo(b); d = ImageDraw.Draw(b)
    d.text((W / 2, 300), 'QUANTO VALE', font=AN(120), fill=NOITE, anchor='mm'); d.text((W / 2, 420), 'ESSA MOTO?', font=AN(140), fill=VERDE, anchor='mm')
    moto(b, 900, W / 2, 1060, reflexo=False)
    # etiqueta pendurada
    tg = Image.new('RGBA', (560, 470)); t = ImageDraw.Draw(tg)
    t.polygon([(90, 0), (560, 0), (560, 470), (90, 470), (0, 235)], fill=AMA); t.ellipse((44, 215, 84, 255), fill=(245, 243, 236))
    t.text((330, 70), 'NA LOJA', font=F('Black', 40), fill=NOITE, anchor='mm'); t.text((330, 140), 'uns R$ 20 mil', font=F('Bold', 44), fill=NOITE, anchor='mm')
    t.line((120, 200, 540, 200), fill=NOITE, width=3)
    t.text((330, 260), 'NO LEILÃO, O LANCE', font=F('Black', 38), fill=NOITE, anchor='mm'); t.text((330, 300), 'COMEÇA EM', font=F('Black', 38), fill=NOITE, anchor='mm')
    t.text((330, 395), f'R$ {real(LANCE)}', font=AN(130), fill=VERM, anchor='mm')
    tg = tg.rotate(8, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', tg.size); sh.putalpha(tg.split()[3].point(lambda v: int(v * .4))); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (290, 1120)); b.alpha_composite(tg, (270, 1090))
    d = ImageDraw.Draw(b); d.line((320, 1060, 330, 1300), fill=(60, 60, 60), width=4)
    d.text((W / 2, 1700), 'Honda PCX 160 · hoje, às 20h · retirada em mãos', font=F('SemiBold', 38), fill=NOITE, anchor='mm')
    rodape(d, 1810, VERDE); d = ImageDraw.Draw(b); salva(b, 'PCX-2-12h-etiqueta-quanto-vale')

# 3 · 15h · VELOCÍMETRO "FALTAM 5 HORAS"
if quer('15h'):
    b = fundo((30, 30, 34), (4, 4, 6), 700); logo(b); d = ImageDraw.Draw(b); cx, cy, r = W / 2, 760, 400
    glow(b, (cx - 470, cy - 470, cx + 470, cy + 470), NEON, 50, 120); d = ImageDraw.Draw(b)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(14, 14, 16), outline=(70, 70, 76), width=14)
    a0, a1 = 225, -45   # escala de 0 a 8 horas (sentido horário de a0 até a1)
    for i in range(0, 41):
        v = i / 40; an = math.radians(a0 - (a0 - a1) * v); r1 = r - 36; r2 = r - (90 if i % 5 == 0 else 62)
        cor = VERM if v > .74 else BR
        d.line((cx + r1 * math.cos(an), cy - r1 * math.sin(an), cx + r2 * math.cos(an), cy - r2 * math.sin(an)), fill=cor, width=8 if i % 5 == 0 else 3)
        if i % 5 == 0: d.text((cx + (r - 140) * math.cos(an), cy - (r - 140) * math.sin(an)), str(8 - i // 5), font=AN(56), fill=cor, anchor='mm')
    v = 3 / 8; an = math.radians(a0 - (a0 - a1) * v)   # ponteiro em "5 horas restantes"
    d.line((cx, cy, cx + (r - 70) * math.cos(an), cy - (r - 70) * math.sin(an)), fill=VERM, width=16); d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=(40, 40, 44), outline=VERM, width=6)
    d.text((cx, cy + 120), 'HORAS PRO MARTELO', font=F('Black', 34), fill=(200, 200, 205), anchor='mm')
    cont(d, (W / 2, 1250), 'FALTAM 5 HORAS', AN(130), BR); d.text((W / 2, 1345), 'e o ponteiro só vai pra frente', font=F('SemiBold', 44), fill=NEON, anchor='mm')
    moto(b, 540, W / 2, 1720, reflexo=False); d = ImageDraw.Draw(b); pilula(d, W / 2, 1775, f'lance atual R$ {real(LANCE)}', F('Black', 46), OURO, NOITE)
    rodape(d, 1870); salva(b, 'PCX-3-15h-velocimetro-5-horas')

# 4 · 17h · PAINEL DIGITAL DA PCX "03:00:00"
if quer('17h'):
    b = fundo((10, 14, 22), (0, 0, 0), 760); logo(b); d = ImageDraw.Draw(b)
    x0, y0, x1, y1 = 70, 300, W - 70, 980
    d.rounded_rectangle((x0 - 18, y0 - 18, x1 + 18, y1 + 18), 70, fill=(30, 32, 38)); d.rounded_rectangle((x0, y0, x1, y1), 56, fill=(6, 10, 16))
    lcd = Image.new('RGBA', (W, H)); l = ImageDraw.Draw(lcd)
    l.text((W / 2, 560), '03:00:00', font=AN(250), fill=(120, 230, 255, 255), anchor='mm')
    b.alpha_composite(lcd.filter(ImageFilter.GaussianBlur(18))); b.alpha_composite(lcd); d = ImageDraw.Draw(b)
    d.text((W / 2, 400), 'TEMPO PRO MARTELO', font=F('Black', 40), fill=(120, 230, 255), anchor='mm')
    for i in range(12):   # barras de "combustível" quase no fim
        cor = VERM if i < 3 else (40, 50, 60); d.rounded_rectangle((140 + i * 68, 760, 190 + i * 68, 800), 8, fill=cor)
    d.text((140, 850), 'E', font=F('Black', 40), fill=VERM, anchor='lm'); d.text((W - 140, 850), 'F', font=F('Black', 40), fill=(120, 130, 140), anchor='rm')
    d.text((W / 2, 900), 'o tempo tá acabando', font=F('Bold', 38), fill=(200, 210, 220), anchor='mm')
    cont(d, (W / 2, 1120), 'FALTAM 3 HORAS', AN(130), BR); d.text((W / 2, 1215), 'pra essa PCX ter dono', font=F('SemiBold', 46), fill=(120, 230, 255), anchor='mm')
    moto(b, 600, W / 2, 1660, espelho=True); d = ImageDraw.Draw(b); caixa_lance(d, 1690, (120, 230, 255))
    salva(b, 'PCX-4-17h-painel-3-horas')

def semaforo(b, cx, top, acesa):
    d = ImageDraw.Draw(b); w, hh = 330, 900
    d.rounded_rectangle((cx - w / 2, top, cx + w / 2, top + hh), 70, fill=(22, 22, 24), outline=(60, 60, 64), width=8)
    for i, cor in enumerate([(230, 40, 40), (255, 190, 0), (40, 220, 110)]):
        y = top + 160 + i * 290; on = (i == acesa)
        if on: glow(b, (cx - 220, y - 220, cx + 220, y + 220), cor, 200, 60); d = ImageDraw.Draw(b)
        d.ellipse((cx - 115, y - 115, cx + 115, y + 115), fill=cor if on else tuple(int(c * .18) for c in cor))
        if on: d.ellipse((cx - 70, y - 85, cx - 10, y - 45), fill=(255, 255, 255, 120))
    return d

# 5 · 19h · SEMÁFORO AMARELO "1 HORA · ATENÇÃO"
if quer('19h'):
    b = fundo((50, 40, 6), (6, 5, 2), 700); logo(b); d = semaforo(b, 300, 270, 1)
    d.text((780, 470), 'ATENÇÃO', font=AN(100), fill=AMA, anchor='mm')
    d.text((780, 640), '1', font=AN(330), fill=BR, anchor='mm'); d.text((780, 840), 'HORA', font=AN(120), fill=BR, anchor='mm')
    d.text((780, 950), 'pro martelo', font=F('SemiBold', 44), fill=(255, 230, 150), anchor='mm')
    moto(b, 820, W / 2, 1560); d = ImageDraw.Draw(b); caixa_lance(d, 1600, AMA)
    salva(b, 'PCX-5-19h-semaforo-1-hora')

# 6 · 19h50 · SEMÁFORO VERDE "10 MIN · ACELERA"
if quer('19h50'):
    b = fundo((8, 70, 36), (2, 10, 6), 700); logo(b)
    for i in range(18):   # riscos de velocidade
        y = 300 + i * 70; ImageDraw.Draw(b).line((520, y, W, y), fill=(63, 208, 126, 40), width=4)
    d = semaforo(b, 300, 270, 2)
    d.text((780, 470), 'ACELERA!', font=AN(110), fill=NEON, anchor='mm')
    d.text((780, 650), '10', font=AN(330), fill=BR, anchor='mm'); d.text((780, 850), 'MINUTOS', font=AN(110), fill=BR, anchor='mm')
    d.text((780, 950), 'quem já deu lance pode cobrir', font=F('SemiBold', 34), fill=(200, 245, 220), anchor='mm')
    moto(b, 820, W / 2, 1560); d = ImageDraw.Draw(b); caixa_lance(d, 1600, NEON)
    salva(b, 'PCX-6-19h50-semaforo-10-min')

# 7 · 20h · BANDEIRA QUADRICULADA "É AGORA · LARGADA"
if quer('20h'):
    b = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(b); q = 90
    for yy in range(0, H, q):
        for xx in range(0, W, q):
            if ((xx // q) + (yy // q)) % 2 == 0: d.rectangle((xx, yy, xx + q, yy + q), fill=(235, 235, 235))
    ond = np.array(b).astype(float)   # ondula a bandeira
    ys = np.arange(H)[:, None]; xs = np.arange(W)[None, :]; sh = (np.sin(xs / 140 + ys / 300) * 28).astype(int)
    ond = ond[np.clip(ys + sh, 0, H - 1), xs]; shade = (np.sin(xs / 140 + ys / 300) * .25 + .75)[..., None]; ond[..., :3] *= shade
    b = Image.fromarray(np.clip(ond, 0, 255).astype('uint8')).convert('RGBA'); b.alpha_composite(Image.new('RGBA', (W, H), (0, 40, 20, 150)))
    logo(b); d = ImageDraw.Draw(b)
    glow(b, (W / 2 - 520, 500, W / 2 + 520, 1100), AMA, 120, 120); d = ImageDraw.Draw(b)
    cont(d, (W / 2, 420), 'É AGORA!', AN(220), AMA, 8)
    cont(d, (W / 2, 600), 'O MARTELO VAI BATER', F('Black', 70), BR)
    moto(b, 940, W / 2, 1300); d = ImageDraw.Draw(b)
    pilula(d, W / 2, 1400, 'QUEM DÁ MAIS?', F('Black', 64), VERM, BR)
    caixa_lance(d, 1500, AMA); rodape(d)
    salva(b, 'PCX-7-20h-bandeira-e-agora')
