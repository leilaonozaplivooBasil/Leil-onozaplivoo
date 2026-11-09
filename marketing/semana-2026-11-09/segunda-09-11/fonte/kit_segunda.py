# Kit dos vendedores — segunda 09/11 (plano do Emanuel: kit até 9h; 10h lista com leilão do dia + 10 oportunidades;
# 20h peça do high ticket de sábado). Lances e datas vêm do sistema; conferir de novo às 9h antes de disparar.
import sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IN, OUT = sys.argv[1], sys.argv[2]; D = json.load(open(sys.argv[3]))
MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920
VERDE=(27,122,72); NEON=(63,208,126); FOGO=(243,91,18); OURO=(245,196,81); NOITE=(10,20,16); FLOR=(12,66,40); MENTA=(226,242,232); BR=(255,255,255); LIMA=(190,245,90)
PROB = []
real = lambda v: 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def fundo():
    import numpy as np
    y, x = np.mgrid[0:H, 0:W]; r = np.clip(((x-W/2)**2 + (y-H*0.42)**2)**.5 / (H*0.62), 0, 1)[..., None]
    return Image.fromarray((np.array([22,92,58])*(1-r) + np.array([5,22,14])*r).astype('uint8')).convert('RGBA')
def logo(b, y=110, larg=230):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg = lg.resize((larg, int(lg.height*larg/lg.width)), Image.LANCZOS)
    b.alpha_composite(lg, ((W-larg)//2, y))
def txt(b, xy, t, f, cor, anchor='mm', lim=W-60):
    d = ImageDraw.Draw(b); bb = d.textbbox(xy, t, font=f, anchor=anchor)
    if bb[0] < 60-1 or bb[2] > lim+1: PROB.append(f'"{t}" sai da margem {bb}')
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+6), t, font=f, fill=(0,0,0,140), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor); return bb
def pil(b, cx, cy, t, f, fundo_, cor, padx=38):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2*padx; h = f.size + 32
    if w > W-120: PROB.append(f'pílula "{t}" larga demais')
    d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), h/2, fill=fundo_); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def vitrine(b, foto, box):
    x0, y0, x1, y1 = box; s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((x0, y0+18, x1, y1+18), 44, fill=(0,0,0,150)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(26)))
    ImageDraw.Draw(b).rounded_rectangle(box, 44, fill=BR)
    p = Image.open(f'{IN}/{foto}').convert('RGB'); pw, ph = x1-x0-80, y1-y0-80; e = min(pw/p.width, ph/p.height); p = p.resize((int(p.width*e), int(p.height*e)), Image.LANCZOS)
    b.paste(p, (x0 + (x1-x0-p.width)//2, y0 + (y1-y0-p.height)//2))
def card_lance(b, y, valor, rot='LANCE AGORA'):
    x0, x1 = 160, 920; s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((x0, y, x1, y+210), 34, fill=(6,30,18,225), outline=(255,255,255,120), width=3); b.alpha_composite(s)
    d = ImageDraw.Draw(b); d.text((W/2, y+52), rot, font=F('Black', 38), fill=LIMA, anchor='mm'); d.text((W/2, y+140), real(valor), font=F('Black', 104), fill=BR, anchor='mm')
def sv(b, nome): b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print(nome)

# 1 · 10h — LEILÃO DE HOJE (o único leilão diário que fecha na segunda)
L = D['led']; b = fundo(); logo(b)
pil(b, W/2, 300, 'LEILÃO DE HOJE · 20H', F('Black', 44), FOGO, BR)
vitrine(b, 'led.webp', (110, 380, 970, 960))
txt(b, (W/2, 1040), 'Kit 8 Barras de LED', F('Black', 72), BR)
txt(b, (W/2, 1112), 'compatível com TV LG 40LF5700', F('Bold', 42), MENTA)
card_lance(b, 1180, L['lance'])
txt(b, (W/2, 1450), f"começou em {real(L['inicio'])} · quem der mais leva", F('Bold', 38), (200,230,210))
txt(b, (W/2, 1560), 'toca no link e dá seu lance', F('Black', 52), OURO)
sv(b, 'SEG-01-10h-leilao-de-hoje-kit-led')

# 2 · 10h — 10 OPORTUNIDADES (lista de transmissão)
b = fundo(); logo(b)
txt(b, (W/2, 330), '10 OPORTUNIDADES', F('Black', 96), BR); txt(b, (W/2, 420), 'pra você dar lance esta semana', F('Bold', 44), OURO)
y = 500; d = ImageDraw.Draw(b)
for i, o in enumerate(D['ops']):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((60, y, W-60, y+112), 26, fill=(6,30,18,200)); b.alpha_composite(s); d = ImageDraw.Draw(b)
    d.ellipse((84, y+28, 140, y+84), fill=NEON); d.text((112, y+56), str(i+1), font=F('Black', 32), fill=FLOR, anchor='mm')
    f = F('Bold', 38); nome = o['nome']
    while d.textlength(nome, font=f) > 560 and f.size > 28: f = F('Bold', f.size-2)
    if d.textlength(nome, font=f) > 560: PROB.append(f'nome "{nome}" não cabe')
    d.text((168, y+40), nome, font=f, fill=BR, anchor='lm'); d.text((168, y+84), o['fim'], font=F('Medium', 30), fill=(170,215,190), anchor='lm')
    d.text((W-90, y+40), 'lance', font=F('Medium', 28), fill=(170,215,190), anchor='rm'); d.text((W-90, y+80), real(o['lance']), font=F('Black', 40), fill=OURO, anchor='rm')
    y += 124
txt(b, (W/2, y+40), 'links na mensagem 👇'.replace(' 👇',''), F('Black', 46), LIMA)
sv(b, 'SEG-02-10h-10-oportunidades')

# 3 · 20h — HIGH TICKET DE SÁBADO (segunda a quinta, 20h)
P = D['ps5']; b = fundo(); logo(b)
pil(b, W/2, 300, 'SÁBADO 14/11 · MARTELO 20H', F('Black', 42), FOGO, BR)
vitrine(b, 'ps5.jpg', (110, 380, 970, 1000))
txt(b, (W/2, 1085), 'PlayStation 5 Slim', F('Black', 80), BR)
txt(b, (W/2, 1160), 'Edição Digital', F('Bold', 46), MENTA)
card_lance(b, 1230, P['lance'])
txt(b, (W/2, 1510), 'já tem gente de olho. e você?', F('Black', 50), OURO)
sv(b, 'SEG-03-20h-sabado-ps5')
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
