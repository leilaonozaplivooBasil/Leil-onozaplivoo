# Carrossel "Como funciona o leilão" — explicado como para uma criança de 6 anos.
# Dados reais do PS5 Slim Digital (leilão f11f54a6f4a87eb64112ac0f, conferido em 10/11 17h20): começou R$ 197, lances 197 → 247 → 400,
# 3 pessoas disputando, fecha sáb 14/11 às 20h. Nunca nome de quem deu lance. Instagram: sem link e sem %.
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]; F0 = os.path.dirname(os.path.abspath(__file__)); MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1350
NOITE, VERDE, NEON, OURO, BR, CINZA, FOGO = (10,26,20), (27,122,72), (61,220,132), (245,196,81), (255,255,255), (170,190,180), (243,91,18)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
PROB = []

def fundo():
    im = Image.new('RGB', (W, H), NOITE); d = ImageDraw.Draw(im)
    for r in range(900, 0, -6):                       # brilho verde suave no centro
        a = int(38 * (1 - r/900)); d.ellipse((W/2-r, H*0.42-r, W/2+r, H*0.42+r), fill=(10+a//3, 26+a, 20+a//2))
    return im.convert('RGBA')

def recorte(path, lim=238):
    im = Image.open(path).convert('RGB'); px = im.load(); w, h = im.size
    m = Image.new('L', (w, h), 255); pm = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > lim and g > lim and b > lim: pm[x, y] = 0
    m = m.filter(ImageFilter.GaussianBlur(1.2)); im = im.convert('RGBA'); im.putalpha(m); return im.crop(m.getbbox())

def texto(d, xy, t, f, cor, maxw=W-140, anchor='la'):
    while d.textlength(t, font=f) > maxw: f = ImageFont.truetype(f.path, f.size - 2)
    d.text(xy, t, font=f, fill=cor, anchor=anchor); return f

def pilula(d, cx, cy, t, f, fundo_, cor, r=38):
    w = d.textlength(t, font=f)
    if w + 2*r > W - 60: PROB.append(f'pílula não cabe: {t}')
    d.rounded_rectangle((cx-w/2-r, cy-r, cx+w/2+r, cy+r), r, fill=fundo_); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')

def rodape(im, n, total, seta=True):
    d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((230, 84)); im.alpha_composite(lg, (60, H-120))
    for i in range(total):
        x = W/2 - (total-1)*14 + i*28; d.ellipse((x-6, H-84, x+6, H-72), fill=NEON if i == n-1 else (60,90,75))
    if seta: d.text((W-70, H-78), 'arrasta  →', font=F('Bold', 34), fill=CINZA, anchor='rm')

def paragrafo(d, x, y, linhas, f, gap=12, maxw=W-140):
    for t, cor in linhas:
        ff = texto(d, (x, y), t, f, cor, maxw); y += ff.size + gap
    return y

ps5 = recorte(f'{F0}/ps5-1.jpg'); caixa = recorte(f'{F0}/ps5-0.jpg')
leil = Image.open(f'{MK}/marca/leiloeiro-aponta-moeda-recorte.png').convert('RGBA')
T = 8; S = []

# 1 — capa
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (W/2, 150), 'R$ 197', F('Black', 190), OURO, anchor='mt')
texto(d, (W/2, 360), 'NÃO é o preço final', F('Black', 86), BR, anchor='mt')
pilula(d, W/2, 520, 'entenda o leilão em 1 minuto', F('Bold', 46), VERDE, BR)
p = ps5.copy(); p.thumbnail((520, 560)); im.alpha_composite(p, ((W-p.width)//2, 610))
rodape(im, 1, T); S.append(im)

# 2 — o que é um leilão
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 130), 'O que é um leilão?', F('Black', 92), OURO)
y = paragrafo(d, 70, 300, [('É uma disputa.', BR), ('Várias pessoas querem', BR), ('a mesma coisa.', BR)], F('Bold', 64), 18)
pilula(d, W/2, y+90, 'quem oferece MAIS, leva', F('Black', 58), NEON, NOITE, 46)
l = leil.copy(); l.thumbnail((430, 470)); im.alpha_composite(l, (W-l.width-40, H-l.height-150))
rodape(im, 2, T); S.append(im)

# 3 — R$ 197 é só o começo
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 130), 'R$ 197 é só o', F('Black', 92), BR); texto(d, (70, 240), 'COMEÇO', F('Black', 130), OURO)
y = paragrafo(d, 70, 430, [('É o primeiro lance.', BR), ('Igual à largada', CINZA), ('de uma corrida:', CINZA), ('ninguém ganha na largada!', BR)], F('Bold', 60), 16)
d.rounded_rectangle((70, y+50, W-70, y+250), 36, fill=(18,52,38), outline=NEON, width=4)
texto(d, (W/2, y+100), 'LANCE INICIAL', F('Bold', 40), CINZA, anchor='mt'); texto(d, (W/2, y+150), 'R$ 197', F('Black', 86), NEON, anchor='mt')
rodape(im, 3, T); S.append(im)

# 4 — o PS5 de verdade
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 110), 'Olha o PlayStation 5', F('Black', 76), BR); texto(d, (70, 200), 'de verdade, no site:', F('Black', 76), OURO)
c = caixa.copy(); c.thumbnail((300, 260)); im.alpha_composite(c, (W-c.width-70, 330))
lances = [('1º lance', 'R$ 197', CINZA), ('2º lance', 'R$ 247', BR), ('3º lance  ·  AGORA', 'R$ 400', NEON)]
y = 640
for i, (rot, val, cor) in enumerate(lances):
    d.rounded_rectangle((70, y, W-70, y+130), 30, fill=(18,52,38) if i < 2 else (22,80,52), outline=cor if i == 2 else None, width=4)
    d.text((110, y+65), rot, font=F('Bold', 44), fill=CINZA if i < 2 else BR, anchor='lm'); d.text((W-110, y+65), val, font=F('Black', 64), fill=cor, anchor='rm')
    if i < 2: d.polygon([(W/2-18, y+142), (W/2+18, y+142), (W/2, y+162)], fill=NEON)
    y += 170
texto(d, (70, 430), 'subiu de', F('Bold', 46), CINZA); texto(d, (70, 485), 'R$ 197 → R$ 400', F('Black', 60), OURO, maxw=600)
texto(d, (70, 560), '3 pessoas disputando', F('Bold', 44), BR, maxw=600)
rodape(im, 4, T); S.append(im)

# 5 — e agora? (simulação)
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 120), 'E agora?', F('Black', 110), OURO)
paragrafo(d, 70, 290, [('Cada pessoa nova que entra', BR), ('dá um lance MAIOR.', BR)], F('Bold', 58), 14)
pilula(d, W/2, 490, 'EXEMPLO  ·  simulação', F('Bold', 38), FOGO, BR, 32)
sim = [('Ana dá', 'R$ 450'), ('Beto dá', 'R$ 500'), ('Ana volta e dá', 'R$ 550')]
y = 570
for t, v in sim:
    d.rounded_rectangle((70, y, W-70, y+120), 28, fill=(18,52,38)); d.text((110, y+60), t, font=F('Bold', 46), fill=BR, anchor='lm'); d.text((W-110, y+60), v, font=F('Black', 58), fill=NEON, anchor='rm'); y += 140
texto(d, (W/2, y+30), 'o preço vai subindo, subindo…', F('Bold', 46), CINZA, anchor='mt')
texto(d, (W/2, y+95), '(nomes de mentira, só pra explicar)', F('Medium', 32), CINZA, anchor='mt')
rodape(im, 5, T); S.append(im)

# 6 — quando o tempo acaba
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 130), 'Quando o tempo acaba…', F('Black', 78), BR)
texto(d, (W/2, 290), 'TOC!', F('Black', 200), OURO, anchor='mt')
paragrafo(d, 70, 540, [('O martelo bate.', BR), ('Quem deu o lance', BR), ('MAIS ALTO, leva.', NEON)], F('Black', 70), 18)
d.rounded_rectangle((70, 900, W-70, 1110), 32, fill=(18,52,38))
texto(d, (W/2, 935), 'o PS5 fecha', F('Bold', 44), CINZA, anchor='mt'); texto(d, (W/2, 995), 'SÁBADO (14/11) ÀS 20H', F('Black', 62), OURO, anchor='mt')
rodape(im, 6, T); S.append(im)

# 7 — como dar seu lance
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 120), 'Como dar seu lance', F('Black', 86), OURO)
passos = [('1', 'Faça seu cadastro', 'no site do Leilão no Zap'), ('2', 'Entre na sala', 'do produto que você quer'), ('3', 'Toque em DAR LANCE', 'e escolha o seu valor')]
y = 300
for n, a, b in passos:
    d.ellipse((70, y, 190, y+120), fill=NEON); d.text((130, y+60), n, font=F('Black', 70), fill=NOITE, anchor='mm')
    texto(d, (230, y+8), a, F('Black', 58), BR, maxw=W-300); texto(d, (230, y+78), b, F('Medium', 42), CINZA, maxw=W-300); y += 220
pilula(d, W/2, y+60, 'dá pra acompanhar tudo ao vivo', F('Bold', 46), VERDE, BR)
rodape(im, 7, T); S.append(im)

# 8 — resumão + CTA
im = fundo(); d = ImageDraw.Draw(im)
texto(d, (70, 110), 'Resumindo:', F('Black', 96), OURO)
itens = ['Leilão = quem dá mais, leva', 'R$ 197 é só o 1º lance', 'O preço sobe a cada lance', 'O martelo bate na hora marcada']
y = 290
for t in itens:
    d.ellipse((70, y+14, 110, y+54), fill=NEON); texto(d, (135, y), t, F('Bold', 58), BR, maxw=W-200); y += 115
paragrafo(d, 70, y+20, [('Às vezes sai bem abaixo do preço', CINZA), ('da loja. Às vezes não: depende de', CINZA), ('quantas pessoas disputam.', CINZA)], F('Medium', 42), 10)
d.rounded_rectangle((70, 1000, W-70, 1180), 40, fill=NEON)
texto(d, (W/2, 1045), 'Ficou dúvida? Comenta', F('Bold', 46), NOITE, anchor='mt'); texto(d, (W/2, 1100), 'LEILÃO', F('Black', 66), NOITE, anchor='mt')
rodape(im, 8, T, seta=False); S.append(im)

os.makedirs(OUT, exist_ok=True)
for i, s in enumerate(S, 1): s.convert('RGB').save(f'{OUT}/SLIDE-{i:02d}.jpg', quality=93)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', len(S))
