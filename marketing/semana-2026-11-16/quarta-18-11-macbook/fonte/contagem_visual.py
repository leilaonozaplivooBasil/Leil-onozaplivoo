# Contagem do MacBook (qua 18/11) — cada arte com UMA imagem que prende o olho, quase sem texto (pedido da Natália: "as pessoas
# são visuais, estão com preguiça de ler"). 10h folha de calendário QUA 18 · 14h ampulheta · 17h despertador tocando ·
# 18h30 bateria acabando · 19h50 placar digital 00:10:00 · 20h martelo batendo. Uso: contagem_visual.py <lance>
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/visual'; MK = '/home/user/Leil-onozaplivoo/marketing'
os.makedirs(OUT, exist_ok=True); LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
BR, OURO, OCLARO, OESC, ESC, VERM, AMA, PRETO = (250, 248, 242), (226, 186, 104), (248, 226, 170), (150, 112, 52), (4, 20, 12), (222, 30, 38), (255, 210, 0), (14, 14, 14)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def fundo(c1, c0, cy=900):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - cy) * .85) / 1150, 0, 1) ** 1.2
    a = np.array(c1)[None, None] * (1 - d[..., None]) + np.array(c0)[None, None] * d[..., None]
    a += np.random.default_rng(3).normal(0, 1.6, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
def glow(b, box, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse(box, fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
def mac(b, larg, cx, base, sombra=True):
    mm = MAC.resize((larg, int(MAC.height * larg / MAC.width)), Image.LANCZOS)
    if sombra:
        s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - larg * .47, base - 16, cx + larg * .47, base + 20), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    b.alpha_composite(mm, (int(cx - larg / 2), int(base - mm.height)))
def logo(b, y=80, larg=170):
    lg = LOGO.copy(); lg.thumbnail((larg, larg)); b.alpha_composite(lg, ((W - lg.width) // 2, y))
def palavra(d, y, t, tam, cor, sombra=(0, 0, 0, 160), peso='Black'):
    while d.textlength(t, font=F(peso, tam)) > W * .92: tam -= 4
    f = F(peso, tam); d.text((W / 2 + 4, y + 8), t, font=f, fill=sombra, anchor='mm'); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def lance(d, y, cor=OCLARO, sub=None):
    d.text((W / 2, y), f'lance atual  R$ {real(LANCE)}', font=F('Black', 58), fill=cor, anchor='mm')
    if sub: d.text((W / 2, y + 64), sub, font=F('Bold', 36), fill=(255, 255, 255, 220), anchor='mm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=94); print('ok', n)

# 10h · folha de calendário arrancada: QUA 18 + "HOJE" carimbado
b = fundo((26, 92, 58), ESC, 800); logo(b); d = ImageDraw.Draw(b)
cx, top, cw, ch = W / 2, 260, 700, 820
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).rounded_rectangle((cx - cw / 2 + 20, top + 30, cx + cw / 2 + 20, top + ch + 30), 40, fill=(0, 0, 0, 160)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(30)))
cal = Image.new('RGBA', (cw, ch)); c = ImageDraw.Draw(cal); c.rounded_rectangle((0, 0, cw, ch), 40, fill=BR); c.rounded_rectangle((0, 0, cw, 210), 40, fill=VERM); c.rectangle((0, 150, cw, 210), fill=VERM)
c.text((cw / 2, 108), 'QUARTA', font=F('Black', 96), fill=BR, anchor='mm')
c.text((cw / 2, 470), '18', font=F('Black', 420), fill=PRETO, anchor='mm'); c.text((cw / 2, 720), 'NOVEMBRO', font=F('Bold', 54), fill=(120, 120, 120), anchor='mm')
for x in (150, cw - 150): c.ellipse((x - 26, -26, x + 26, 26), fill=(60, 60, 60))
cal = cal.rotate(-4, resample=Image.BICUBIC, expand=True); b.alpha_composite(cal, (int(cx - cal.width / 2), top - 20))
carimbo = Image.new('RGBA', (620, 230)); k = ImageDraw.Draw(carimbo); k.rounded_rectangle((8, 8, 612, 222), 30, outline=VERM + (235,), width=14); k.text((310, 118), 'É HOJE!', font=F('Black', 150), fill=VERM + (235,), anchor='mm')
carimbo = carimbo.rotate(14, resample=Image.BICUBIC, expand=True); b.alpha_composite(carimbo, (int(cx - carimbo.width / 2 + 80), 790))
mac(b, 560, W / 2, 1500); d = ImageDraw.Draw(b); palavra(d, 1590, 'ÀS 20H', 130, AMA); lance(d, 1720, sub='⚠ 1º lance até as 19h'.replace('⚠ ', ''))
salva(b, 'V1-10h-calendario-e-hoje')

# 14h · ampulheta com areia dourada caindo
b = fundo((20, 70, 46), ESC, 760); logo(b); d = ImageDraw.Draw(b)
cx, y0, y1, hw = W / 2, 250, 1080, 300; mid = (y0 + y1) / 2
glow(b, (cx - 420, y0, cx + 420, y1), OURO, 70, 140); d = ImageDraw.Draw(b)
vid = [(cx - hw, y0 + 40), (cx + hw, y0 + 40), (cx + 40, mid), (cx + hw, y1 - 40), (cx - hw, y1 - 40), (cx - 40, mid)]
d.polygon(vid, fill=(220, 240, 230, 40)); d.line(vid + [vid[0]], fill=(230, 245, 238), width=8)
top_sand = [(cx - hw * .55, mid - 190), (cx + hw * .55, mid - 190), (cx + 40, mid - 10), (cx - 40, mid - 10)]; d.polygon(top_sand, fill=OURO)
d.polygon([(cx - hw * .92, y1 - 44), (cx + hw * .92, y1 - 44), (cx + 80, y1 - 250), (cx - 80, y1 - 250)], fill=OURO)
d.line((cx, mid - 10, cx, y1 - 250), fill=OCLARO, width=10)
for yy in (y0, y1 - 40): d.rounded_rectangle((cx - hw - 60, yy - 10, cx + hw + 60, yy + 50), 18, fill=(120, 84, 40)); d.rounded_rectangle((cx - hw - 60, yy - 10, cx + hw + 60, yy + 10), 18, fill=OURO)
palavra(d, 1205, '6 HORAS', 190, BR); mac(b, 420, W / 2, 1645); d = ImageDraw.Draw(b); lance(d, 1720, sub='pro martelo bater no MacBook')
salva(b, 'V2-14h-ampulheta-6-horas')

# 17h · despertador tocando (tremendo), ponteiro nas 7 = 19h
b = fundo((150, 22, 28), (40, 4, 8), 760); logo(b); d = ImageDraw.Draw(b)
cx, cy, r = W / 2, 760, 330
glow(b, (cx - 480, cy - 480, cx + 480, cy + 480), AMA, 80, 120); d = ImageDraw.Draw(b)
for sgn in (-1, 1):
    bx, by = cx + sgn * 230, cy - 300; d.ellipse((bx - 110, by - 110, bx + 110, by + 110), fill=AMA, outline=PRETO, width=10)
    for k_ in range(3): d.arc((bx - 170 - k_ * 40, by - 170 - k_ * 40, bx + 170 + k_ * 40, by + 170 + k_ * 40), 200 if sgn < 0 else 290, 250 if sgn < 0 else 340, fill=BR, width=10)
d.line((cx - 200, cy + 290, cx - 260, cy + 380), fill=PRETO, width=26); d.line((cx + 200, cy + 290, cx + 260, cy + 380), fill=PRETO, width=26)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BR, outline=PRETO, width=26)
for k_ in range(12):
    an = k_ / 12 * 2 * math.pi; r1, r2 = r * .78, r * (.90 if k_ % 3 else .66); d.line((cx + r1 * math.sin(an), cy - r1 * math.cos(an), cx + r2 * math.sin(an), cy - r2 * math.cos(an)), fill=PRETO, width=12)
an = 7 / 12 * 2 * math.pi; d.line((cx, cy, cx + r * .5 * math.sin(an), cy - r * .5 * math.cos(an)), fill=VERM, width=26); d.line((cx, cy, cx, cy - r * .74), fill=PRETO, width=16); d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=VERM)
palavra(d, 1250, 'ACORDA!', 190, AMA); palavra(d, 1420, '1º LANCE ATÉ 19H', 96, BR)
lance(d, 1700, BR, 'faltam 2 horas · depois fica de fora')
salva(b, 'V3-17h-despertador-acorda')

# 18h30 · bateria acabando (vermelha, 1 barrinha)
b = fundo((40, 40, 40), (6, 6, 6), 760); logo(b); d = ImageDraw.Draw(b)
bx0, by0, bx1, by1 = 170, 380, 850, 900
glow(b, (bx0 - 60, by0 - 60, bx1 + 120, by1 + 60), VERM, 90, 110); d = ImageDraw.Draw(b)
d.rounded_rectangle((bx0, by0, bx1, by1), 60, outline=BR, width=30); d.rounded_rectangle((bx1 + 20, by0 + 170, bx1 + 90, by1 - 170), 20, fill=BR)
d.rounded_rectangle((bx0 + 50, by0 + 50, bx0 + 210, by1 - 50), 30, fill=VERM)
d.text(((bx0 + bx1) / 2 + 80, (by0 + by1) / 2), '30', font=F('Black', 300), fill=VERM, anchor='mm')
palavra(d, 1080, 'MINUTOS', 160, BR); palavra(d, 1250, 'PRO SEU 1º LANCE', 92, VERM)
mac(b, 480, W / 2, 1600); d = ImageDraw.Draw(b); lance(d, 1700, BR, 'às 19h a entrada fecha')
salva(b, 'V4-18h30-bateria-30-min')

# 19h50 · placar digital 00:10:00
b = fundo((10, 10, 10), (0, 0, 0), 700); logo(b); d = ImageDraw.Draw(b)
d.rounded_rectangle((60, 380, W - 60, 760), 40, fill=(20, 0, 0), outline=(90, 10, 10), width=6)
dig = '00:10:00'; f = F('Black', 220)
g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).text((W / 2, 570), dig, font=f, fill=VERM + (255,), anchor='mm'); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(24))); b.alpha_composite(g)
d = ImageDraw.Draw(b)
for yy in range(380, 760, 8): d.line((60, yy, W - 60, yy), fill=(0, 0, 0, 70), width=2)   # linhas de LED
palavra(d, 880, 'RETA FINAL', 140, BR); glow(b, (W / 2 - 400, 1050, W / 2 + 400, 1500), OURO, 60, 120)
mac(b, 640, W / 2, 1480); d = ImageDraw.Draw(b); lance(d, 1620, OCLARO, 'o martelo bate às 20h')
salva(b, 'V5-19h50-placar-10-min')

# 20h · martelo batendo com estouro
b = fundo((30, 100, 62), ESC, 900); logo(b); d = ImageDraw.Draw(b)
cx, cy = W / 2, 980
random.seed(4)
for k_ in range(22):
    an = k_ / 22 * 2 * math.pi; r1, r2 = 300, 560 + random.randint(-60, 80); d.polygon([(cx + r1 * math.cos(an - .05), cy + r1 * math.sin(an - .05)), (cx + r2 * math.cos(an), cy + r2 * math.sin(an)), (cx + r1 * math.cos(an + .05), cy + r1 * math.sin(an + .05))], fill=AMA)
glow(b, (cx - 360, cy - 360, cx + 360, cy + 360), OCLARO, 200, 60)
mac(b, 600, cx, cy + 190, sombra=False)
gv = Image.new('RGBA', (900, 900)); g_ = ImageDraw.Draw(gv)
g_.rounded_rectangle((420, 300, 470, 860), 22, fill=(120, 70, 30)); g_.rounded_rectangle((220, 170, 670, 370), 50, fill=(150, 90, 40)); g_.rounded_rectangle((220, 170, 670, 220), 40, fill=(190, 130, 70))
for xx in (260, 630): g_.rectangle((xx - 18, 170, xx + 18, 370), fill=OURO)
gv = gv.rotate(38, resample=Image.BICUBIC, expand=True); b.alpha_composite(gv, (int(cx - gv.width / 2 + 210), int(cy - gv.height / 2 - 250)))
d = ImageDraw.Draw(b); palavra(d, 380, 'É AGORA!', 200, BR); palavra(d, 1520, 'QUEM DÁ MAIS?', 120, AMA)
lance(d, 1700, BR, 'últimos segundos do leilão')
salva(b, 'V6-20h-martelo-e-agora')
