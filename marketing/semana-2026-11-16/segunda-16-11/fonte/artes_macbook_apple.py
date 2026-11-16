# MacBook Neo (qua 18/11, 20h) no jeito das propagandas da Apple (referências da Natália, 16/11): fundo preto,
# produto herói com a luz da tela "acendendo" a cena, reflexo no chão, pouco texto em branco/cinza. Foto principal do leilão.
# Uso: artes_macbook_apple.py <lance>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
BRANCO, CINZA, CINZA2 = (245, 245, 247), (161, 161, 166), (110, 110, 115)
GRAD = [(64, 120, 255), (150, 90, 255), (235, 90, 200), (255, 150, 110)]   # as cores da tela do produto
W = H = 0

def produto(larg):
    im = Image.open(f'{AQ}/fotos/1793811068141_1_macbook-neo-de-13-polegadas-chip-a18-pro-cpu-6-nucleos-gpu-5.webp').convert('RGB')
    im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 120, 2))
    a = np.asarray(im).astype(float); al = Image.fromarray((np.clip((246 - a.min(axis=2)) / 14, 0, 1) * 255).astype('uint8'))
    al = al.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
    p = im.convert('RGBA'); p.putalpha(al); p = p.crop(al.getbbox()); return p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)

def gradiente_txt(b, xy, t, f, anchor='mm'):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor=anchor); x0, y0, x1, y1 = m.getbbox()
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for x in range(x0, x1 + 1):
        k = (x - x0) / max(1, x1 - x0) * (len(GRAD) - 1); i = min(int(k), len(GRAD) - 2); t2 = k - i
        gd.line((x, 0, x, H), fill=tuple(int(c0 + (c1 - c0) * t2) for c0, c1 in zip(GRAD[i], GRAD[i + 1])) + (255,))
    b.alpha_composite(Image.composite(g, Image.new('RGBA', (W, H), (0, 0, 0, 0)), m))

def luz(b, cx, cy, rx, ry, cor, a, blur):
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=cor + (a,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))

def arte(w, h, nome, y):
    global W, H; W, H = w, h
    b = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(b)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((150, 60)); b.alpha_composite(lg, ((W - lg.width) // 2, y['logo']))
    d = ImageDraw.Draw(b)
    d.text((W / 2, y['kicker']), 'Leilão de quarta-feira', font=F('Medium', 34), fill=CINZA, anchor='mm')
    d.text((W / 2, y['nome']), 'MacBook Neo', font=F('SemiBold', y['tam']), fill=BRANCO, anchor='mm')
    gradiente_txt(b, (W / 2, y['frase']), 'O próximo pode ser seu.', F('SemiBold', y['tam'] * 46 // 100))
    p = produto(y['larg']); px, base = (W - p.width) // 2, y['base']
    # a tela acende a cena: brilho colorido atrás e no chão
    luz(b, W / 2 - p.width * .22, base - p.height * .55, p.width * .38, p.height * .42, GRAD[0], 120, 140)
    luz(b, W / 2 + p.width * .2, base - p.height * .5, p.width * .38, p.height * .42, GRAD[2], 110, 140)
    luz(b, W / 2, base + 20, p.width * .55, 70, GRAD[1], 120, 60)
    r = p.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, p.width, int(p.height * .22)))
    gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255 - v) * .22)); r.putalpha(ImageChops.multiply(r.split()[3], gm))
    b.alpha_composite(r, (px, base + 4)); b.alpha_composite(p, (px, base - p.height))
    d = ImageDraw.Draw(b)
    d.text((W / 2, y['spec']), '13 polegadas  ·  chip A18 Pro  ·  256GB', font=F('Regular', 32), fill=CINZA, anchor='mm')
    d.text((W / 2, y['rotulo']), 'Lance atual', font=F('Medium', 40), fill=CINZA, anchor='mm')
    fR, fN = F('Medium', y['tam_lance'] * 36 // 100), F('SemiBold', y['tam_lance']); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
    d.text((x0, y['lance']), 'R$', font=fR, fill=BRANCO, anchor='ls'); d.text((x0 + wr, y['lance']), LANCE, font=fN, fill=BRANCO, anchor='ls')
    t = 'quarta, 18/11, às 20h'; ft = F('Medium', 38); wt = d.textlength(t, font=ft)
    d.rounded_rectangle((W / 2 - wt / 2 - 40, y['data'] - 42, W / 2 + wt / 2 + 40, y['data'] + 42), 42, outline=CINZA2, width=2)
    d.text((W / 2, y['data']), t, font=ft, fill=BRANCO, anchor='mm')
    b.convert('RGB').save(f'{OUT}/{nome}', quality=95); print('ok', nome)

arte(1080, 1920, 'arte-macbook-story.jpg', dict(logo=120, kicker=300, nome=410, tam=150, frase=530, larg=900, base=1230,
     spec=1370, rotulo=1470, lance=1640, tam_lance=190, data=1760))
arte(1080, 1350, 'arte-macbook-feed.jpg', dict(logo=45, kicker=150, nome=238, tam=112, frase=328, larg=690, base=860,
     spec=955, rotulo=1030, lance=1165, tam_lance=128, data=1262))
