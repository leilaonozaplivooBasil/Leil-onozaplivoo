# Campanha do iPhone 17 Pro Max — sábado 07/11, martelo 20h. Uma arte = uma ideia (pedido da Natália: no nível do
# notebook, mas nada igual). iPhone sempre a FOTO REAL recortada. Lance do sistema: python3 campanha_iphone.py <lance>
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps
from kit import logo, leiloeiro, sombra
AQ = os.path.dirname(os.path.abspath(__file__)); IMG = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = os.path.join(AQ, '..', '..', 'semana-2026-11-05', 'sabado-07-11', 'campanha')
LANCE = float(sys.argv[1]) if len(sys.argv) > 1 else 463.80
LANCES = [float(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 else [197, 253.80, 353.80, 363.80, LANCE]
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE = (27, 122, 72); NEON = (63, 208, 126); FOGO = (243, 91, 18); OURO = (245, 196, 81); NOITE = (10, 20, 16)
FLOR = (12, 66, 40); MENTA = (226, 242, 232); AREIA = (246, 239, 226); BR = (255, 255, 255); LIMA = (190, 245, 90)
def real(v): return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
LJ = 'R$ 9.464,78'
random.seed(7)

def tela(w, h, c): return Image.new('RGBA', (w, h), c + (255,))
def radial(w, h, c0, c1, cx=.5, cy=.42, raio=.75):
    import numpy as np
    y, x = np.mgrid[0:h, 0:w]; d = np.sqrt(((x - w * cx) / w) ** 2 + ((y - h * cy) / h) ** 2); t = np.clip(d / raio, 0, 1)[..., None]
    return Image.fromarray((np.array(c0) * (1 - t) + np.array(c1) * t).astype('uint8')).convert('RGBA')
def raios(b, cx, cy, n, cor, alfa, larg=7):
    m = Image.new('L', b.size, 0); d = ImageDraw.Draw(m)
    for k in range(n):
        a0 = math.radians(k * 360 / n); a1 = a0 + math.radians(larg)
        d.polygon([(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)), (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))], fill=alfa)
    c = Image.new('RGBA', b.size, cor + (0,)); c.putalpha(m.filter(ImageFilter.GaussianBlur(6))); b.alpha_composite(c)
def brilhos(b, n, cor, area=None):
    w, h = b.size; x0, y0, x1, y1 = area or (0, 0, w, h); s = Image.new('RGBA', b.size); d = ImageDraw.Draw(s)
    for _ in range(n):
        x, y, r = random.randint(x0, x1), random.randint(y0, y1), random.choice([2, 3, 4, 6])
        d.ellipse((x - r, y - r, x + r, y + r), fill=cor + (random.randint(90, 220),))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(1))); b.alpha_composite(s)
def luz(b, cx, cy, r, cor, alfa=150):
    g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor + (alfa,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * .45)))
def iph(alt, ang=0):
    p = Image.open(f'{IMG}/c-iphone.png').convert('RGBA'); p = p.crop(p.getbbox()); p = p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
    return p.rotate(ang, expand=True, resample=Image.BICUBIC) if ang else p
def poe(b, p, cx, base, brilho=None, forca=150, reflexo=False):
    x, y = int(cx - p.width / 2), int(base - p.height)
    if brilho:
        g = Image.new('RGBA', b.size, brilho + (0,)); m = Image.new('L', b.size, 0); m.paste(p.split()[-1].point(lambda v: 140 if v > 20 else 0), (x, y))
        g.putalpha(m.filter(ImageFilter.GaussianBlur(50))); b.alpha_composite(g)
    if reflexo:
        r = ImageOps.flip(p).crop((0, 0, p.width, int(p.height * .35))); a = r.split()[-1]
        grad = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255 - v) * .35)); r.putalpha(Image.composite(grad, Image.new('L', r.size, 0), a))
        b.alpha_composite(r, (x, base + 4))
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((cx - p.width * .44, base - 14, cx + p.width * .44, base + 14), fill=(0, 0, 0, forca)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(12)))
    b.alpha_composite(p, (x, y))
def T(b, xy, t, f, cor, anchor='mm', somb=150, contorno=0, ccor=(0, 0, 0)):
    if somb:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1] + 8), t, font=f, fill=(0, 0, 0, somb), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor, stroke_width=contorno, stroke_fill=ccor)
def vazado(b, xy, t, f, cor, w=4, anchor='mm', alfa=255):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text(xy, t, font=f, fill=(0, 0, 0, 0), anchor=anchor, stroke_width=w, stroke_fill=cor + (alfa,)); b.alpha_composite(s)
def pil(b, cx, cy, t, f, fundo, cor, padx=40, h=None, borda=None):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2 * padx; h = h or f.size + 34
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, fill=fundo, outline=borda, width=3 if borda else 0); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def vidro(b, cx_, claro=False, r=34, borda=(255, 255, 255, 150)):
    cx_ = tuple(int(round(v)) for v in cx_)
    v = b.crop(cx_).filter(ImageFilter.GaussianBlur(20)); v = Image.alpha_composite(v, Image.new('RGBA', v.size, (255, 255, 255, 110) if claro else (4, 26, 14, 165)))
    m = Image.new('L', v.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, v.width - 1, v.height - 1), r, fill=255); b.paste(v, cx_[:2], m)
    ImageDraw.Draw(b).rounded_rectangle(cx_, r, outline=borda, width=2)
def riscar(b, xy, t, f, cor, anchor='mm', lin=FOGO):
    d = ImageDraw.Draw(b); d.text(xy, t, font=f, fill=cor, anchor=anchor); bb = d.textbbox(xy, t, font=f, anchor=anchor)
    y = (bb[1] + bb[3]) / 2 + 3; d.line((bb[0] - 6, y, bb[2] + 6, y), fill=lin, width=max(5, f.size // 12))
def martelo(d, x, y, s, cor):
    d.rounded_rectangle((x, y + s * .15, x + s * .55, y + s * .45), 6, fill=cor); d.line((x + s * .27, y + s * .45, x + s * .9, y + s * 1.05), fill=cor, width=int(s * .12))
def lance_card(b, cx, y, w=720, claro=False, rot='LANCE AGORA'):
    vidro(b, (cx - w // 2, y, cx + w // 2, y + 220), claro=claro); d = ImageDraw.Draw(b)
    martelo(d, cx - w // 2 + 50, y + 34, 50, LIMA if not claro else VERDE)
    d.text((cx - w // 2 + 120, y + 58), rot, font=F('Black', 38), fill=LIMA if not claro else VERDE, anchor='lm')
    d.text((cx, y + 150), real(LANCE), font=F('Black', 112), fill=BR if not claro else FLOR, anchor='mm')
def logo_(b, y=110, larg=220, placa=False):
    if placa:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((b.width / 2 - 145, y - 14, b.width / 2 + 145, y + 100), 34, fill=(10, 44, 26, 230)); b.alpha_composite(s)
    logo(b, y=y, largura=larg)
PROBLEMAS = []
def cabe(d, xy, t, fonte_nome, tam, limite_x, cor, anchor='lm', minimo=24):
    f = F(fonte_nome, tam)
    while d.textbbox(xy, t, font=f, anchor=anchor)[2] > limite_x - 4 and tam > minimo:
        tam -= 2; f = F(fonte_nome, tam)
    if d.textbbox(xy, t, font=f, anchor=anchor)[2] > limite_x - 4: PROBLEMAS.append(f'texto "{t}" não cabe na caixa')
    d.text(xy, t, font=f, fill=cor, anchor=anchor)
def sv(b, nome):
    os.makedirs(OUT, exist_ok=True); b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print(nome)
W, H = 1080, 1920

# 1 · 08h — BOM DIA, FUTURO DONO: verde com raios, "20H" gigante vazado atrás, iPhone com reflexo
def s1():
    b = radial(W, H, (24, 150, 76), (3, 40, 20)); raios(b, W / 2, 1000, 22, (150, 255, 160), 40); vazado(b, (W / 2, 1000), '20H', F('Black', 640), LIMA, 5, alfa=90)
    logo_(b); T(b, (W / 2, 330), 'BOM DIA,', F('Black', 120), BR); T(b, (W / 2, 460), 'FUTURO DONO.', F('Black', 120), LIMA)
    T(b, (W / 2, 570), 'hoje às 20h esse iPhone encontra dono', F('Medium', 46), MENTA, somb=0)
    luz(b, W / 2, 1050, 330, (120, 255, 150), 120); brilhos(b, 40, (220, 255, 200), (100, 650, 980, 1300)); poe(b, iph(640), W / 2, 1330, (120, 255, 150), reflexo=True)
    lance_card(b, W / 2, 1450); sv(b, 'S01-08h-bom-dia-futuro-dono')

# 2 · 10h — ELE TÁ EM R$ 463: ouro, preço gigante ATRÁS do iPhone (sobreposição)
def s2():
    b = tela(W, H, OURO); d = ImageDraw.Draw(b); n = f'{int(LANCE):,}'.replace(',', '.')
    logo_(b, placa=True); T(b, (W / 2, 330), 'ELE TÁ EM', F('Black', 96), FLOR, somb=0)
    d.text((W / 2, 600), n, font=F('Black', 400), fill=FLOR, anchor='mm'); d.text((110, 470), 'R$', font=F('Black', 96), fill=FLOR, anchor='lm')
    poe(b, iph(700, -10), W / 2 + 80, 1540, forca=110)
    vidro(b, (90, 1540, 990, 1740), claro=True); d = ImageDraw.Draw(b)
    d.text((W / 2, 1595), f'{real(LANCE)}. isso mesmo: por enquanto.', font=F('Bold', 46), fill=FLOR, anchor='mm')
    riscar(b, (W / 2, 1675), f'na loja {LJ}', F('Black', 52), (90, 90, 80)); sv(b, 'S02-10h-ele-ta-em')

# 3 · 12h — A ESCADA DOS LANCES: lances REAIS virando degraus, iPhone no topo
def s3():
    b = radial(W, H, (16, 40, 30), NOITE, cy=.6); logo_(b)
    T(b, (W / 2, 320), 'A ESCADA', F('Black', 120), BR); T(b, (W / 2, 445), 'DOS LANCES', F('Black', 120), NEON)
    T(b, (W / 2, 545), 'cada degrau é um lance de verdade', F('Medium', 44), MENTA, somb=0)
    vals = LANCES; n = len(vals); base = 1640; x0 = 90; gap = 14; lw = (W - 2 * x0 - gap * (n - 1)) / n
    d = ImageDraw.Draw(b)
    for k, v in enumerate(vals):
        h = 120 + (v - vals[0]) / (max(vals) - vals[0]) * 560; x = x0 + k * (lw + gap)
        cor = NEON if k == n - 1 else (36, 110, 74)
        d.rounded_rectangle((x, base - h, x + lw, base), 14, fill=cor)
        rot = f'{v:,.0f}'.replace(',', '.') if v != int(v) or True else str(int(v))
        d.text((x + lw / 2, base - h - 30), rot, font=F('Black', 30 if n > 6 else 34), fill=BR if k < n - 1 else LIMA, anchor='mm')
    xt = x0 + (n - 1) * (lw + gap) + lw / 2; luz(b, xt - 60, base - 760, 200, NEON, 110); poe(b, iph(330, 8), xt - 70, base - 740, NEON, forca=0)
    d = ImageDraw.Draw(b); d.text((x0, base + 40), f'R$ 197 → {real(LANCE)} em {len(LANCES)} lances', font=F('Bold', 40), fill=MENTA)
    pil(b, W / 2, 1790, 'E O MARTELO SÓ BATE ÀS 20H', F('Black', 40), NEON, NOITE, h=96); sv(b, 'S03-12h-escada-dos-lances')

# 4 · 14h — QUANTO VOCÊ PAGARIA?: areia, etiqueta de preço pendurada no iPhone
def s4():
    b = tela(W, H, AREIA); logo_(b, placa=True)
    T(b, (W / 2, 330), 'QUANTO VOCÊ', F('Black', 108), FLOR, somb=0); T(b, (W / 2, 450), 'PAGARIA?', F('Black', 150), VERDE, somb=0)
    poe(b, iph(820, -6), 470, 1500, forca=90)
    e = Image.new('RGBA', (430, 230)); d = ImageDraw.Draw(e); d.rounded_rectangle((0, 0, 429, 229), 30, fill=OURO); d.ellipse((30, 95, 70, 135), fill=AREIA)
    d.text((245, 80), 'R$', font=F('Black', 54), fill=FLOR, anchor='mm'); d.text((245, 160), '???', font=F('Black', 110), fill=FLOR, anchor='mm')
    e = e.rotate(-14, expand=True, resample=Image.BICUBIC); s = Image.new('RGBA', e.size); s.putalpha(e.split()[-1].point(lambda v: 90 if v else 0))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)), (530, 880)); b.alpha_composite(e, (520, 860))
    d = ImageDraw.Draw(b); d.line((520, 760, 585, 960), fill=(120, 100, 60), width=5)
    riscar(b, (W / 2, 1600), f'na loja {LJ}', F('Black', 56), (110, 110, 100))
    T(b, (W / 2, 1690), 'aqui, o preço quem escreve é você', F('Bold', 46), FLOR, somb=0); sv(b, 'S04-14h-quanto-voce-pagaria')

# 5 · 15h — FALTAM 5 HORAS: diagonal verde/floresta, "5" vazado gigante, iPhone rompendo a moldura
def s5():
    b = tela(W, H, FLOR); d = ImageDraw.Draw(b); d.polygon([(0, 0), (W, 0), (W, 760), (0, 1260)], fill=VERDE)
    vazado(b, (760, 1050), '5', F('Black', 1200), LIMA, 7, alfa=120); logo_(b)
    T(b, (90, 330), 'FALTAM', F('Black', 120), BR, 'lm'); T(b, (90, 460), '5 HORAS', F('Black', 120), LIMA, 'lm')
    T(b, (90, 570), 'pro martelo bater', F('Medium', 48), MENTA, 'lm', somb=0)
    poe(b, iph(860, 14), 620, 1560, (150, 255, 140), forca=170)
    lance_card(b, W / 2, 1580, w=760); sv(b, 'S05-15h-faltam-5-horas')

# 6 · 17h — 3 HORAS PRA ELE TER DONO: pódio neon com moedas e martelo
def s6():
    p = Image.open(f'{IMG}/s-verde1.png').convert('RGB'); e = max(W / p.width, H / p.height); p = p.resize((round(p.width * e), round(p.height * e)), Image.LANCZOS)
    x = (p.width - W) // 2; b = p.crop((x, 0, x + W, H)).convert('RGBA'); logo_(b)
    T(b, (W / 2, 330), '3 HORAS', F('Black', 170), LIMA); T(b, (W / 2, 470), 'PRA ELE TER DONO', F('Black', 80), BR)
    poe(b, iph(720), W / 2 + 10, 1515, (120, 255, 140), forca=170)
    lance_card(b, W / 2, 1580, w=760); sv(b, 'S06-17h-3-horas-pra-ter-dono')

# 7 · 18h — O ÚLTIMO SAIU POR R$ 4.640 (a única com a foto real do arremate), em duotone verde
def s7():
    f = Image.open(f'{AQ}/iphone-ultimo-arremate.jpg').convert('L'); e = max(W / f.width, H / f.height); f = f.resize((round(f.width * e), round(f.height * e)), Image.LANCZOS)
    x = (f.width - W) // 2; f = f.crop((x, 0, x + W, H))
    cor = Image.open(f'{AQ}/iphone-ultimo-arremate.jpg').convert('RGB'); cor = cor.resize((round(cor.width * e), round(cor.height * e)), Image.LANCZOS).crop((x, 0, x + W, H))
    cor = ImageEnhance.Color(cor).enhance(0.75); cor = ImageEnhance.Brightness(cor).enhance(1.08)
    b = Image.blend(cor, Image.new('RGB', (W, H), (27, 122, 72)), 0.18).convert('RGBA'); g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
    for y in range(H): gd.line((0, y, W, y), fill=(4, 30, 16, int(245 * max(0, (y - 820) / 1100) ** .7)))
    b.alpha_composite(g); logo_(b)
    pil(b, W / 2, 330, 'FALTAM 2 HORAS', F('Black', 44), FOGO, BR)
    T(b, (W / 2, 1180), 'O ÚLTIMO SAIU POR', F('Black', 64), MENTA); T(b, (W / 2, 1330), 'R$ 4.640', F('Black', 210), OURO)
    riscar(b, (W / 2, 1470), 'na loja ele custava R$ 8.404', F('Black', 46), BR)
    T(b, (W / 2, 1600), 'hoje é a vez de quem?', F('Black', 72), LIMA); sv(b, 'S07-18h-o-ultimo-saiu-por')

# 8 · 19h — FALTA 1 HORA: Leiloeiro de relógio na mão + iPhone, raios dourados
def s8():
    b = radial(W, H, (30, 140, 80), (6, 50, 28), cy=.55); raios(b, W / 2, 1150, 18, (255, 220, 120), 45, 6); logo_(b)
    T(b, (W / 2, 330), 'FALTA', F('Black', 130), BR); T(b, (W / 2, 470), '1 HORA', F('Black', 170), OURO)
    p = leiloeiro('a-relogio', 880); sombra(p, b, (-80, 1560 - p.height))
    luz(b, 770, 1150, 260, OURO, 120); poe(b, iph(600, -8), 790, 1450, (255, 230, 140), forca=160)
    pil(b, W / 2, 1640, 'o martelo bate às 20h em ponto', F('Bold', 44), FLOR, BR); sv(b, 'S08-19h-falta-1-hora')

# 9 · 19h30 — ÚLTIMA CHAMADA: noite, fogo, rastro de velocidade atrás do iPhone
def s9():
    b = tela(W, H, NOITE); luz(b, W / 2, 1150, 480, FOGO, 150); logo_(b)
    T(b, (W / 2, 340), 'ÚLTIMA', F('Black', 180), BR); T(b, (W / 2, 520), 'CHAMADA', F('Black', 180), FOGO)
    T(b, (W / 2, 650), 'fecha às 20h. quem der o maior lance, leva.', F('Medium', 42), (255, 220, 200), somb=0)
    p = iph(700, 12)
    for k, a in ((5, 40), (3, 70), (1, 110)):
        r = p.copy(); r.putalpha(r.split()[-1].point(lambda v: a if v else 0)); b.alpha_composite(r.filter(ImageFilter.GaussianBlur(6)), (int(W / 2 - p.width / 2 - k * 40), int(1530 - p.height)))
    poe(b, p, W / 2, 1530, (255, 140, 60), forca=180)
    lance_card(b, W / 2, 1580, w=760, rot='PRA LEVAR, SUPERE'); sv(b, 'S09-19h30-ultima-chamada')

# 10 · 19h50 — 10 MINUTOS: cronômetro com o iPhone dentro do relógio
def s10():
    b = radial(W, H, (14, 44, 30), (2, 10, 6), cy=.45); logo_(b); d = ImageDraw.Draw(b)
    d.ellipse((90, 260, 990, 1160), outline=(30, 70, 50), width=30); d.arc((90, 260, 990, 1160), -90, -30, fill=NEON, width=30)
    for k in range(60):
        a = math.radians(k * 6 - 90); r1, r2 = 410, (380 if k % 5 == 0 else 395)
        d.line((540 + r1 * math.cos(a), 710 + r1 * math.sin(a), 540 + r2 * math.cos(a), 710 + r2 * math.sin(a)), fill=(60, 110, 80), width=3)
    luz(b, 540, 760, 240, NEON, 90); poe(b, iph(560), 540, 1020, NEON, forca=120)
    T(b, (W / 2, 1290), '10:00', F('Black', 250), BR); T(b, (W / 2, 1440), 'MINUTOS PRO MARTELO', F('Black', 60), NEON)
    pil(b, W / 2, 1600, 'é agora ou só no próximo', F('Bold', 46), (20, 60, 40), BR); sv(b, 'S10-19h50-faltam-10-minutos')

# 11 · contagem — espaço para a figurinha de CONTAGEM REGRESSIVA do Instagram
def s11():
    b = radial(W, H, (24, 150, 76), (4, 44, 22), cy=.62); brilhos(b, 70, (220, 255, 200)); logo_(b)
    T(b, (W / 2, 320), 'O MARTELO BATE', F('Black', 86), BR); T(b, (W / 2, 450), 'HOJE ÀS 20H', F('Black', 130), LIMA)
    d = ImageDraw.Draw(b)
    for x in range(160, 920, 34): d.line((x, 560, x + 18, 560), fill=LIMA, width=4); d.line((x, 820, x + 18, 820), fill=LIMA, width=4)
    for y in range(560, 820, 34): d.line((160, y, 160, y + 18), fill=LIMA, width=4); d.line((920, y, 920, y + 18), fill=LIMA, width=4)
    d.text((W / 2, 690), 'cole aqui a contagem regressiva', font=F('Bold', 38), fill=MENTA, anchor='mm')
    luz(b, W / 2, 1220, 300, (120, 255, 150), 110); poe(b, iph(600), W / 2, 1500, (120, 255, 150), reflexo=True)
    pil(b, W / 2, 1640, 'ativa o lembrete e não perde o martelo', F('Bold', 42), FLOR, BR); sv(b, 'S11-contagem-figurinha')

# ---- FEED 1080x1350
def f1():
    p = Image.open(f'{IMG}/s-luxo.png').convert('RGBA').resize((1080, 1350), Image.LANCZOS); b = p; logo_(b, y=50, larg=190)
    T(b, (540, 230), 'HOJE ÀS 20H', F('Black', 118), OURO); T(b, (540, 340), 'ELE ENCONTRA DONO', F('Black', 74), BR)
    poe(b, iph(560), 545, 1030, (255, 225, 150), forca=170)
    vidro(b, (90, 1080, 990, 1290)); d = ImageDraw.Draw(b)
    d.text((140, 1130), 'iPhone 17 Pro Max · 256GB', font=F('Bold', 38), fill=MENTA, anchor='lm'); d.text((140, 1215), 'lance agora', font=F('Medium', 40), fill=MENTA, anchor='lm')
    d.text((950, 1215), real(LANCE), font=F('Black', 92), fill=OURO, anchor='rm'); sv(b, 'F01-12h-card1-hoje-ele-encontra-dono')
def f2():
    b = radial(1080, 1350, (24, 150, 76), (4, 44, 22), cy=.3); logo_(b, y=50, larg=190)
    T(b, (540, 240), 'COMO LEVAR', F('Black', 96), BR); T(b, (540, 345), 'ESSE IPHONE', F('Black', 96), LIMA)
    d = ImageDraw.Draw(b)
    for k, (a, c) in enumerate([('Comenta IPHONE', 'aqui embaixo'), ('Recebe o link', 'no seu direct'), ('Dá o seu lance', 'até as 20h')]):
        y = 500 + k * 230; vidro(b, (70, y, 600, y + 190)); d = ImageDraw.Draw(b)
        d.ellipse((110, y + 45, 210, y + 145), fill=LIMA); d.text((160, y + 95), str(k + 1), font=F('Black', 60), fill=FLOR, anchor='mm')
        cabe(d, (240, y + 70), a, 'Black', 46, 600 - 24, BR); cabe(d, (240, y + 128), c, 'Medium', 38, 600 - 24, MENTA)
    luz(b, 870, 900, 220, (120, 255, 150), 110); poe(b, iph(560, 8), 870, 1250, (120, 255, 150)); sv(b, 'F02-12h-card2-como-levar')
def f3():
    b = tela(1080, 1350, AREIA); logo_(b, y=50, larg=190, placa=True)
    T(b, (540, 250), 'NA LOJA', F('Black', 70), FLOR, somb=0); riscar(b, (540, 360), LJ, F('Black', 120), (120, 120, 110))
    T(b, (540, 480), 'AQUI, AGORA', F('Black', 70), VERDE, somb=0); T(b, (540, 610), real(LANCE), F('Black', 170), VERDE, somb=0)
    poe(b, iph(560, -6), 540, 1270, forca=100); pil(b, 540, 1290, 'martelo hoje às 20h', F('Black', 40), FLOR, BR, h=86); sv(b, 'F03-loja-x-lance')

for fn in (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, f1, f2, f3): fn()
if PROBLEMAS: print('PROBLEMAS:', PROBLEMAS); sys.exit(1)
