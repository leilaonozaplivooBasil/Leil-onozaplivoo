# Stories "vitrine de ARREMATADOS" no formato dos stories do Mercado Livre (cards brancos limpos, faixa da marca em cima,
# etiqueta no canto e selo redondo com o valor), no verde da arte da placa (Natália, 22/11). Valores reais do sistema.
# Sem nome de quem arrematou, sem link, sem %. Uso: vitrine_arrematados.py
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
FOT = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/arrem'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920; VE, MENTA, BR, NEON = (10, 61, 38), (214, 236, 221), (255, 255, 255), (63, 208, 126)
def real(v): return f'{v:,.0f}'.replace(',', '.')
# (foto, valor, dia, lances, nome curto)
P = {
 'pcx': (f'{MK}/semana-2026-11-16/sabado-21-11-pcx/fonte/fotos/pcx-plataforma-lado.webp', 10667, '21/11', 116, 'Honda PCX 160'),
 'iphone18': (f'{FOT}/iphone18.src', 7750, '11/11', 62, 'iPhone 18 Pro Max'),
 'iphone17': (f'{FOT}/iphone17.src', 6370, '07/11', 143, 'iPhone 17 Pro Max'),
 'macbook': (f'{FOT}/macbook.src', 5597, '18/11', 47, 'MacBook Neo 13"'),
 'ps5': (f'{FOT}/ps5.src', 3570, '14/11', 59, 'PlayStation 5 Slim'),
 'tv': (f'{FOT}/tv.src', 3247, '10/10', 12, 'Smart TV LG 65"'),
}
def fundo():
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 900) * .85) / 1150, 0, 1) ** 1.2
    a = np.array((30, 108, 66))[None, None] * (1 - dd[..., None]) + np.array((12, 62, 38))[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
    b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); r = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(r)
    for i in range(36): yy = 150 + i * 52; d.line((0, yy, W, yy + 40), fill=(255, 255, 255, 12), width=2)
    b.alpha_composite(r); return b
def foto(path):
    im = Image.open(path).convert('RGBA')
    if im.getpixel((2, 2))[3] == 0: im = im.crop(im.getbbox())
    else:   # fundo branco: corta a sobra branca
        g = np.array(im.convert('L')); m = g < 245; ys, xs = np.where(m)
        if len(xs): im = im.crop((max(0, xs.min() - 6), max(0, ys.min() - 6), min(im.width, xs.max() + 6), min(im.height, ys.max() + 6)))
    return im
def estrela(d, cx, cy, r, pontas=22, fill=VE):
    pts = []
    for i in range(pontas * 2):
        a = math.pi * i / pontas; rr = r if i % 2 == 0 else r * .88; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
def card(k, w, h):
    path, val, dia, lan, nome = P[k]; esc = w / 960; pq = esc < .7; et = max(esc, .64)   # et = escala dos textos pequenos (mínimo legível no celular)
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(34 * esc), fill=255)
    base = Image.new('RGBA', (w, h), BR + (255,)); d = ImageDraw.Draw(base)
    bh = int(96 * esc); d.rectangle((0, 0, w, bh), fill=VE)
    d.text((int(30 * esc), bh / 2), 'leilão no zap', font=F('Black', int(40 * esc)), fill=BR, anchor='lm')
    d.text((w - int(30 * esc), bh / 2), 'ARREMATADO', font=F('Black', int(50 * esc)), fill=NEON, anchor='rm')
    # foto do produto
    im = foto(path); aw, ah = w - int(90 * esc), h - bh - int(140 * esc); k_ = min(aw / im.width, ah / im.height); im = im.resize((int(im.width * k_), int(im.height * k_)), Image.LANCZOS)
    base.alpha_composite(im, ((w - im.width) // 2, bh + int(40 * esc) + (ah - im.height) // 2)); d = ImageDraw.Draw(base)
    # pílula estilo "cupom novo todo dia": dia e lances
    f = F('Black', int(30 * et)); t = f'{dia} · {lan} lances'; tw = d.textlength(t, font=f); px = w - int(30 * esc) - tw - int(56 * esc); py = bh + int(26 * esc)
    d.rounded_rectangle((px, py, px + tw + int(56 * esc), py + int(64 * esc)), int(14 * esc), fill=(20, 30, 24), outline=NEON, width=max(2, int(4 * esc)))
    d.text((px + (tw + int(56 * esc)) / 2, py + int(32 * esc)), t, font=f, fill=BR, anchor='mm')
    # etiqueta "AO VIVO" (no lugar do "frete grátis")
    ty = h - int(120 * esc); tl = int(190 * esc)
    d.polygon([(0, ty), (tl, ty), (tl + int(36 * esc), ty + int(42 * esc)), (tl, ty + int(84 * esc)), (0, ty + int(84 * esc))], fill=NEON)
    d.text((int(22 * esc), ty + int(42 * esc)), 'AO VIVO', font=F('Black', int(36 * et)), fill=VE, anchor='lm')
    # selo redondo com o valor (no lugar do "até 10% off")
    r = int(150 * (esc if not pq else .6)); cx, cy = w - r - int(18 * esc), h - r - int(18 * esc); estrela(d, cx, cy, r)
    d.text((cx, cy - int(62 * (esc if not pq else .6))), 'SAIU POR', font=F('Bold', int(30 * et)), fill=MENTA, anchor='mm')
    fv = F('Black', int(62 * (esc if not pq else .66))); s = f'R$ {real(val)}'
    while d.textlength(s, font=fv) > r * 1.7: fv = F('Black', fv.size - 2)
    d.text((cx, cy + int(6 * esc)), s, font=fv, fill=BR, anchor='mm')
    if not pq: d.text((cx, cy + int(66 * esc)), nome if d.textlength(nome, font=F('Medium', int(24 * esc))) < r * 1.6 else nome.split()[0], font=F('Medium', int(24 * esc)), fill=MENTA, anchor='mm')
    c.paste(base, (0, 0), m); return c
def sombra(b, x, y, c):
    s = Image.new('RGBA', (W, H)); s.paste((0, 0, 0, 90), (x + 8, y + 14, x + c.width + 8, y + c.height + 14), c.split()[3]); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14))); b.alpha_composite(c, (x, y))
def topo(d, t):
    d.text((W / 2, 120), t, font=F('Black', 64), fill=BR, anchor='mm')
def rodape(d, b):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((180, 180)); b.alpha_composite(lg, (60, H - 40 - lg.height))
    f = F('Black', 36); t = 'responde LEILÃO que eu te mando o link'; tw = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - tw - 60, H - 112, W - 60, H - 40), 36, fill=MENTA); d.text((W - 60 - (tw + 60) / 2, H - 76), t, font=f, fill=VE, anchor='mm')
def destaque(nome, grande, peq):
    b = fundo(); d = ImageDraw.Draw(b); topo(d, 'JÁ FORAM ARREMATADOS')
    sombra(b, 60, 200, card(grande, 960, 900))
    sombra(b, 60, 1140, card(peq[0], 465, 600)); sombra(b, 555, 1140, card(peq[1], 465, 600))
    d = ImageDraw.Draw(b); rodape(d, b); b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print('ok', nome)
def grade(nome, ks):
    b = fundo(); d = ImageDraw.Draw(b); topo(d, 'JÁ FORAM ARREMATADOS')
    for i, k in enumerate(ks): sombra(b, 60 + (i % 2) * 495, 200 + (i // 2) * 525, card(k, 465, 495))
    d = ImageDraw.Draw(b); rodape(d, b); b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print('ok', nome)
destaque('STORY-1-arrematados-pcx', 'pcx', ['iphone18', 'macbook'])
destaque('STORY-2-arrematados-iphone17', 'iphone17', ['ps5', 'tv'])
grade('STORY-3-arrematados-vitrine', ['pcx', 'iphone18', 'iphone17', 'macbook', 'ps5', 'tv'])
