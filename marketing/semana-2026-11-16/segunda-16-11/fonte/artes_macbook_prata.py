# MacBook Neo PRATEADO (qua 18/11, 20h) — fotos reais do próprio anúncio (aberto visto de cima + tampa fechada),
# sombra natural (sem reflexo), fundo verde da marca, texto exatamente como a descrição do site. Uso: artes_macbook_prata.py <lance>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
BRANCO, CREME, OURO, OURO2, VERDEC = (247, 247, 244), (205, 222, 210), (226, 186, 104), (246, 214, 140), (150, 190, 165)
FOTO = f'{AQ}/fotos/1793811070147_2_macbook-neo-de-13-polegadas-chip-a18-pro-cpu-6-nucleos-gpu-5.jpg'
TAMPA = f'{AQ}/fotos/1793811071242_4_macbook-neo-de-13-polegadas-chip-a18-pro-cpu-6-nucleos-gpu-5.jpg'
W = H = 0

def recorta(caminho, larg, ang=0):
    # fundo = só o branco que encosta na borda da foto (as teclas brancas, por dentro, ficam)
    from scipy import ndimage
    im = Image.open(caminho).convert('RGB'); a = np.asarray(im).astype(float); mn = a.min(axis=2)
    lab, _ = ndimage.label(mn > 246); borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fundo = np.isin(lab, list(borda)); obj = ndimage.binary_fill_holes(~fundo)
    suave = np.clip((252 - mn) / 7, 0, 1)                                 # borda macia só na beirada
    alfa = np.where(ndimage.binary_erosion(obj, iterations=2), 1.0, np.where(obj, suave, 0))
    al = Image.fromarray((alfa * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6))
    p = im.convert('RGBA'); p.putalpha(al); p = p.crop(al.getbbox()); p = p.resize((larg, int(p.height * larg / p.width)), Image.LANCZOS)
    return p.rotate(ang, resample=Image.BICUBIC, expand=True) if ang else p

def sombra(b, p, x, y, dx=0, dy=34, blur=38, a=0.55):
    s = Image.new('RGBA', (W, H)); m = p.split()[3].point(lambda v: int(v * a))
    s.paste((0, 12, 6, 255), (int(x + dx), int(y + dy)), m); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
    s2 = Image.new('RGBA', (W, H)); s2.paste((0, 10, 5, 255), (int(x), int(y + 8)), p.split()[3].point(lambda v: int(v * .35))); b.alpha_composite(s2.filter(ImageFilter.GaussianBlur(8)))

def fundo(cy):
    y, x = np.mgrid[0:H, 0:W]; d = np.clip(np.hypot(x - W / 2, (y - cy) * .9) / (W * 1.0), 0, 1) ** 1.3
    a = np.array((28, 92, 60))[None, None] * (1 - d[..., None]) + np.array((5, 26, 16))[None, None] * d[..., None]
    a += np.random.default_rng(4).normal(0, 1.8, a.shape); return Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')

def centro(d, y, t, f, cor): d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def espac(t): return ' '.join(t)

def arte(w, h, nome, y):
    global W, H; W, H = w, h
    b = fundo(y['grupo']); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((170, 70))
    b.alpha_composite(lg, ((W - lg.width) // 2, y['logo'])); d = ImageDraw.Draw(b)
    centro(d, y['kicker'], espac('LEILÃO DE QUARTA · 20H'), F('SemiBold', 30), OURO)
    centro(d, y['nome'], 'MacBook Neo', F('SemiBold', y['tam']), BRANCO)
    centro(d, y['sub'], 'de 13 polegadas · Prateado', F('Medium', y['tam'] * 30 // 100), CREME)
    # as duas fotos do anúncio: a tampa fechada atrás, o aberto na frente
    t = recorta(TAMPA, y['lt'], 7); k = recorta(FOTO, y['lk'], -5)
    tx, ty = W / 2 - t.width * .62, y['grupo'] - t.height * .95; kx, ky = W / 2 - k.width * .36, y['grupo'] - k.height * .25
    sombra(b, t, tx, ty); b.alpha_composite(t, (int(tx), int(ty))); sombra(b, k, kx, ky, dy=40, a=.6); b.alpha_composite(k, (int(kx), int(ky)))
    d = ImageDraw.Draw(b)
    for i, l in enumerate(['Chip A18 Pro  ·  CPU de 6 núcleos', 'GPU de 5 núcleos  ·  256GB']):
        centro(d, y['spec'] + i * y['ent'], l, F('Medium', y['tspec']), VERDEC)
    centro(d, y['rotulo'], espac('LANCE ATUAL'), F('SemiBold', 30), OURO)
    fR, fN = F('Medium', y['tlance'] * 34 // 100), F('Bold', y['tlance']); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
    d.text((x0, y['lance']), 'R$', font=fR, fill=OURO2, anchor='ls'); d.text((x0 + wr, y['lance']), LANCE, font=fN, fill=OURO2, anchor='ls')
    tx_ = 'quarta-feira, 18/11, às 20h'; ft = F('SemiBold', 38); wt = d.textlength(tx_, font=ft)
    d.rounded_rectangle((W / 2 - wt / 2 - 44, y['data'] - 44, W / 2 + wt / 2 + 44, y['data'] + 44), 44, fill=(4, 22, 13))
    d.rounded_rectangle((W / 2 - wt / 2 - 44, y['data'] - 44, W / 2 + wt / 2 + 44, y['data'] + 44), 44, outline=OURO, width=2)
    centro(d, y['data'], tx_, ft, BRANCO)
    b.convert('RGB').save(f'{OUT}/{nome}', quality=95); print('ok', nome)

arte(1080, 1920, 'arte-macbook-story.jpg', dict(logo=100, kicker=270, nome=375, tam=150, sub=480, grupo=980, lt=600, lk=650, desl=0,
     spec=1430, ent=52, tspec=34, rotulo=1545, lance=1715, tlance=180, data=1825))
arte(1080, 1350, 'arte-macbook-feed.jpg', dict(logo=35, kicker=140, nome=222, tam=108, sub=300, grupo=700, lt=420, lk=445, desl=0,
     spec=995, ent=38, tspec=28, rotulo=1075, lance=1182, tlance=104, data=1262))
