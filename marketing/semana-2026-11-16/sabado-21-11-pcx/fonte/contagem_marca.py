# Contagem da PCX (sáb 21/11, 20h), versão 2 — pedido do João Ale (21/11 10h07): "manter a identidade visual, as paletas de cores
# e deixar a moto maior e em mais destaque". A Natália pediu branding fixo, como o roxo do Nubank e o amarelo do Mercado Livre.
# Sistema: FUNDO OURO chapado (#F5C451) + texto VERDE-ESCURO (#0A3D26) + selo MENTA + uma família de letra só (Inter Display).
# (21/11) Natália: nada de fundo quase preto — a reta final usa o VERDE DA MARCA #1B7A48, não o verde-escuro.
# O ouro é a "nossa cor": as 5 primeiras artes são ouro. Na reta final (19h50 e 20h) a arte INVERTE (verde-escuro com ouro),
# que é o "alarme" da marca sem sair da paleta. O que muda de uma arte para outra é o elemento de moto (placa, etiqueta,
# velocímetro, painel, semáforo, bandeira) — a cor fica. Uso: contagem_marca.py <lance> [09h,12h,...]
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/contagem-marca'; MK = '/home/user/Leil-onozaplivoo/marketing'
os.makedirs(OUT, exist_ok=True)
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'; SO = sys.argv[2].split(',') if len(sys.argv) > 2 else None
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
# (21/11) Natália: "tira esse amarelo, testa verde claro e verde escuro". O nome OURO ficou, mas agora é o VERDE CLARO da marca.
OURO, OURO2, OURO3 = (214, 236, 221), (190, 222, 200), (150, 200, 168)
AMBAR = (245, 196, 81)
VE, VM, MENTA, AREIA, NEON, BR = (10, 61, 38), (27, 122, 72), (214, 236, 221), (246, 239, 226), (63, 208, 126), (255, 255, 255)
VE2 = (16, 78, 50)
MOTO = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); MOTO = MOTO.crop(MOTO.getbbox())
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def quer(k): return SO is None or k in SO
def base(cor): return Image.new('RGBA', (W, H), cor + (255,))
def agua(b, linhas, cor, y0=250, tam=330, passo=330):
    return  # marca-d'água tirada: ficava espiando atrás da moto e poluía
    d = ImageDraw.Draw(b)
    for i, t in enumerate(linhas): d.text((W / 2, y0 + i * passo), t, font=F('Black', tam), fill=cor, anchor='mm')
def logo(b, y=1790):
    lg = LOGO.copy(); lg.thumbnail((250, 250)); x = (W - lg.width) // 2
    if sum(b.getpixel((10, H - 10))[:3]) > 500:   # fundo claro: o texto branco do logo some, então vai numa pílula verde-escura
        ImageDraw.Draw(b).rounded_rectangle((x - 26, y - 14, x + lg.width + 26, y + lg.height + 14), 40, fill=VE)
    b.alpha_composite(lg, (x, y))
def moto(b, larg, cx, chao, podio=None):
    m = MOTO.resize((larg, int(MOTO.height * larg / MOTO.width)), Image.LANCZOS)
    if podio:   # bloco liso da mesma cor, um tom mais escuro (regra 4 do estilo vitrine)
        c1, c2 = podio; d = ImageDraw.Draw(b); pw, ph, prof = larg * .92, 70, 46
        x0 = cx - pw / 2; d.polygon([(x0, chao), (x0 + pw, chao), (x0 + pw + prof, chao - prof), (x0 + prof, chao - prof)], fill=c1)
        d.rectangle((x0, chao, x0 + pw, chao + ph), fill=c2); d.polygon([(x0 + pw, chao), (x0 + pw + prof, chao - prof), (x0 + pw + prof, chao + ph - prof), (x0 + pw, chao + ph)], fill=tuple(int(v * .9) for v in c2))
        chao = chao - prof / 2
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - larg * .44, chao - 16, cx + larg * .44, chao + 22), fill=(0, 0, 0, 120)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    b.alpha_composite(m, (int(cx - larg / 2), int(chao - m.height + 6)))
def lance(d, y, cor_txt=VE, cor_rot=VE, rot=('LANCE', 'ATUAL')):
    fr, fn, fl = F('Black', 74), F('Black', 260), F('Medium', 52)
    n = real(LANCE); wr, wn = d.textlength('R$', font=fr), d.textlength(n, font=fn); wl = max(d.textlength(t, font=fl) for t in rot)
    tot = wl + 40 + wr + 14 + wn; x = (W - tot) / 2
    d.text((x, y - 34), rot[0], font=fl, fill=cor_rot, anchor='lm'); d.text((x, y + 30), rot[1], font=fl, fill=cor_rot, anchor='lm')
    x += wl + 40; d.text((x, y - 60), 'R$', font=fr, fill=cor_txt, anchor='lm'); x += wr + 14; d.text((x, y), n, font=fn, fill=cor_txt, anchor='lm')
def selo(b, cx, cy, r, linhas, fundo=MENTA, cor=VE):
    d = ImageDraw.Draw(b); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fundo); f = F('Black', int(r * .36)); n = len(linhas)
    for i, t in enumerate(linhas): d.text((cx, cy + (i - (n - 1) / 2) * r * .44), t, font=f, fill=cor, anchor='mm')
def rotulo(d, y, t, cor=VE):
    d.text((W / 2, y), t, font=F('Medium', 40), fill=cor, anchor='mm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=94); print('ok', n)
def girar(b, camada, xy, ang, sombra=60):
    c = camada.rotate(ang, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', c.size); sh.putalpha(c.split()[3].point(lambda v: int(v * sombra / 255))); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (xy[0] + 8, xy[1] + 14))
    b.alpha_composite(c, xy)

# 1 · 09h · É HOJE (placa no estilo Mercosul, na cor da marca)
if quer('09h'):
    b = base(OURO); agua(b, ['HOJE', 'PCX'], OURO2, 900, 400, 420); d = ImageDraw.Draw(b)
    d.text((W / 2, 230), 'É HOJE!', font=F('Black', 190), fill=VE, anchor='mm'); d.text((W / 2, 370), 'o leilão da moto é às 20h', font=F('Medium', 56), fill=VE, anchor='mm')
    pl = Image.new('RGBA', (560, 210)); p = ImageDraw.Draw(pl)
    p.rounded_rectangle((0, 0, 559, 209), 26, fill=BR, outline=VE, width=8); p.rounded_rectangle((8, 8, 551, 62), 18, fill=VE); p.rectangle((8, 40, 551, 62), fill=VE)
    p.text((280, 36), 'BRASIL', font=F('Black', 32), fill=OURO, anchor='mm'); p.text((280, 138), 'HOJ3·20H', font=F('Black', 92), fill=VE, anchor='mm')
    girar(b, pl, (470, 470), -4)
    moto(b, 1040, W / 2, 1360, (OURO2, OURO3))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'Honda PCX 160 · branca perolizada'); lance(d, 1640); logo(b)
    salva(b, 'PCX-1-09h-e-hoje')

# 2 · 12h · QUANTO VALE ESSA MOTO? (etiqueta de preço verde)
if quer('12h'):
    b = base(OURO); agua(b, ['20', 'MIL'], OURO2, 820, 460, 440); d = ImageDraw.Draw(b)
    d.text((W / 2, 210), 'QUANTO VALE', font=F('Black', 120), fill=VE, anchor='mm'); d.text((W / 2, 340), 'ESSA MOTO?', font=F('Black', 120), fill=VE, anchor='mm')
    moto(b, 1040, W / 2, 1180, (OURO2, OURO3))
    tg = Image.new('RGBA', (500, 230)); t = ImageDraw.Draw(tg)
    t.polygon([(70, 0), (500, 0), (500, 230), (70, 230), (0, 115)], fill=VE); t.ellipse((30, 100, 60, 130), fill=OURO)
    t.text((285, 65), 'NA LOJA', font=F('Medium', 44), fill=MENTA, anchor='mm'); t.text((285, 145), 'uns R$ 20 mil', font=F('Black', 62), fill=BR, anchor='mm')
    girar(b, tg, (500, 395), 5)
    d = ImageDraw.Draw(b); rotulo(d, 1290, 'no leilão, quem decide o preço é você'); lance(d, 1480, rot=('O LANCE', 'TÁ EM'))
    rotulo(d, 1680, 'Honda PCX 160 · hoje, às 20h'); logo(b)
    salva(b, 'PCX-2-12h-quanto-vale')

# 3 · 15h · FALTAM 5 HORAS (velocímetro atrás da moto)
if quer('15h'):
    b = base(OURO); d = ImageDraw.Draw(b)
    d.text((W / 2, 210), 'FALTAM', font=F('Medium', 80), fill=VE, anchor='mm'); d.text((W / 2, 350), '5 HORAS', font=F('Black', 190), fill=VE, anchor='mm')
    cx, cy, r = W / 2, 1060, 470; a0, a1 = 200, -20
    d.arc((cx - r, cy - r, cx + r, cy + r), -a0, -a1, fill=OURO2, width=60)
    for i in range(0, 41):
        v = i / 40; an = math.radians(a0 - (a0 - a1) * v); r1, r2 = r - 60, r - (120 if i % 5 == 0 else 90)
        d.line((cx + r1 * math.cos(an), cy - r1 * math.sin(an), cx + r2 * math.cos(an), cy - r2 * math.sin(an)), fill=VE if i % 5 == 0 else OURO3, width=9 if i % 5 == 0 else 4)
    an = math.radians(a0 - (a0 - a1) * 3 / 8); d.line((cx, cy, cx + (r - 80) * math.cos(an), cy - (r - 80) * math.sin(an)), fill=VE, width=18)
    d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=VE)
    for i in range(0, 41, 5):   # números por cima do ponteiro, numa bolinha, para o ponteiro não tampar
        an2 = math.radians(a0 - (a0 - a1) * i / 40); px, py = cx + (r - 175) * math.cos(an2), cy - (r - 175) * math.sin(an2)
        d.ellipse((px - 36, py - 36, px + 36, py + 36), fill=OURO); d.text((px, py), str(8 - i // 5), font=F('Black', 54), fill=VE, anchor='mm')
    moto(b, 1040, W / 2, 1370, (OURO2, OURO3))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'e o ponteiro só vai pra frente'); lance(d, 1640); logo(b)
    salva(b, 'PCX-3-15h-5-horas')

# 4 · 17h · FALTAM 3 HORAS (painel digital, verde-escuro)
if quer('17h'):
    b = base(OURO); agua(b, ['17H'], OURO2, 1000, 520); d = ImageDraw.Draw(b)
    d.text((W / 2, 200), 'FALTAM 3 HORAS', font=F('Black', 116), fill=VE, anchor='mm'); d.text((W / 2, 310), 'pra essa PCX ter dono', font=F('Medium', 56), fill=VE, anchor='mm')
    d.rounded_rectangle((150, 400, W - 150, 640), 48, fill=VE)
    d.text((W / 2, 500), '03:00:00', font=F('Black', 170), fill=OURO, anchor='mm')
    for i in range(10): d.rounded_rectangle((250 + i * 60, 600, 290 + i * 60, 618), 6, fill=OURO if i < 3 else VE2)
    moto(b, 1040, W / 2, 1370, (OURO2, OURO3))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'Honda PCX 160 · hoje, às 20h'); lance(d, 1640); logo(b)
    salva(b, 'PCX-4-17h-3-horas')

def semaforo(b, x0, y0, acesa, corpo=VE, apagada=VE2):
    d = ImageDraw.Draw(b); w, h = 600, 210
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), h / 2, fill=corpo)
    for i, cor in enumerate([(226, 64, 52), AMBAR, NEON]):
        cx = x0 + 110 + i * 190; cy = y0 + h / 2; on = i == acesa
        if on:
            g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx - 130, cy - 130, cx + 130, cy + 130), fill=cor + (150,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(b)
        d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=cor if on else apagada)
    return ImageDraw.Draw(b)

# 5 · 19h · ATENÇÃO, 1 HORA (semáforo amarelo — no ouro, a luz acesa É a cor da marca)
if quer('19h'):
    b = base(OURO); agua(b, ['1H'], OURO2, 1000, 640); d = ImageDraw.Draw(b)
    d.text((W / 2, 200), 'ATENÇÃO:', font=F('Medium', 80), fill=VE, anchor='mm'); d.text((W / 2, 330), 'FALTA 1 HORA', font=F('Black', 140), fill=VE, anchor='mm')
    d = semaforo(b, 240, 430, 1)
    moto(b, 1040, W / 2, 1370, (OURO2, OURO3))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'quem já deu lance segue na disputa'); lance(d, 1640); logo(b)
    salva(b, 'PCX-5-19h-1-hora')

# 6 · 19h50 · ACELERA! 10 MINUTOS (inverte: verde-escuro + ouro = alarme da marca)
if quer('19h50'):
    b = base(VM); agua(b, ['10'], VE2, 1000, 760); d = ImageDraw.Draw(b)
    d.text((W / 2, 200), 'ACELERA!', font=F('Black', 150), fill=OURO, anchor='mm'); d.text((W / 2, 330), 'FALTAM 10 MINUTOS', font=F('Black', 82), fill=BR, anchor='mm')
    d = semaforo(b, 240, 430, 2, corpo=VE, apagada=(20, 90, 55))
    moto(b, 1040, W / 2, 1370, ((22, 104, 61), (17, 88, 51)))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'quem já deu lance pode cobrir', MENTA); lance(d, 1640, BR, MENTA); logo(b)
    salva(b, 'PCX-6-19h50-10-minutos')

# 7 · 20h · É AGORA! (inverte + faixa quadriculada de largada em ouro e verde)
if quer('20h'):
    b = base(VM); d = ImageDraw.Draw(b); q = 60
    for yy in range(2):   # bandeira de largada atravessando, atrás da moto
        for xx in range(0, W, q):
            d.rectangle((xx, 1140 + yy * q, xx + q, 1140 + yy * q + q), fill=OURO if (xx // q + yy) % 2 == 0 else (22, 104, 61))
    d.text((W / 2, 220), 'É AGORA!', font=F('Black', 200), fill=OURO, anchor='mm'); d.text((W / 2, 370), 'o martelo vai bater às 20h', font=F('Medium', 58), fill=BR, anchor='mm')
    selo(b, W - 200, 560, 130, ['QUEM', 'DÁ MAIS?'], OURO, VE)
    moto(b, 1040, W / 2, 1370, ((22, 104, 61), (17, 88, 51)))
    d = ImageDraw.Draw(b); rotulo(d, 1470, 'Honda PCX 160 · leilão ao vivo', MENTA); lance(d, 1640, BR, MENTA); logo(b)
    salva(b, 'PCX-7-20h-e-agora')
