# "O único enigma que importa" (17/11, para o leilão de qua 18/11 20h): gancho no hype da capa da revista do momento,
# SEM usar a capa, nome ou logo da revista (pôster-enigma próprio, gerado no Gamma). Leila = atendente virtual (Gamma, banner
# oficial como referência). MacBook = fotos OFICIAIS da Apple do modelo prateado. Sem voz (sem créditos de TTS): texto + trilha.
# Uso: montar.py <pasta_imagens> <saida.mp4> <lance>
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
L, SAIDA, LANCE = sys.argv[1], sys.argv[2], sys.argv[3]
MK = '/home/user/Leil-onozaplivoo/marketing'; AP = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/apple'
FR = os.path.join(os.path.dirname(SAIDA), 'quadros'); os.makedirs(FR, exist_ok=True)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H, FPS = 1080, 1920, 30
BR, OURO, VERDE, ESC, LAR = (255, 255, 255), (245, 196, 81), (27, 122, 72), (5, 28, 17), (240, 96, 40)
ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))

def cobre(im, w=W, h=H):
    k = max(w / im.width, h / im.height); im = im.resize((math.ceil(im.width * k), math.ceil(im.height * k)), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
def zoom(im, z, cx=.5, cy=.5):
    w, h = im.size; nw, nh = w / z, h / z; x0 = (w - nw) * cx; y0 = (h - nh) * cy
    return im.crop((x0, y0, x0 + nw, y0 + nh)).resize((W, H), Image.BILINEAR)
def texto(d, y, t, tam, cor, sombra=True):
    while d.textlength(t, font=F('Black', tam)) > 980: tam -= 4
    f = F('Black', tam)
    if sombra: d.text((W / 2, y + 6), t, font=f, fill=(0, 0, 0, 170), anchor='mm')
    d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
def pilula(d, y, t, f, fundo, cor, a=255):
    w = d.textlength(t, font=f); h = f.size + 30
    d.rounded_rectangle((W / 2 - w / 2 - 32, y - h / 2, W / 2 + w / 2 + 32, y + h / 2), h / 2, fill=fundo + (a,)); d.text((W / 2, y), t, font=f, fill=cor + (a,), anchor='mm')
def degrade(b, y0, y1, a0, a1):
    g = np.zeros((y1 - y0, W, 4), np.uint8); g[..., :3] = ESC; g[..., 3] = np.linspace(a0, a1, y1 - y0)[:, None]; b.alpha_composite(Image.fromarray(g), (0, y0))
def tag_virtual(b):
    d = ImageDraw.Draw(b); f = F('SemiBold', 28); t = 'Leila · atendente virtual'; w = d.textlength(t, font=f)
    d.rounded_rectangle((40, 60, 40 + w + 40, 112), 26, fill=(0, 0, 0, 120)); d.text((60, 86), t, font=f, fill=(255, 255, 255, 230), anchor='lm')

enigma = cobre(Image.open(f'{L}/poster.jpg').convert('RGB')).convert('RGBA')
PRETO, VERM = (17, 17, 17), (214, 40, 40)
charme = cobre(Image.open(f'{L}/charme.jpg').convert('RGB')); piscada = cobre(Image.open(f'{L}/piscada.jpg').convert('RGB'))
mac = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')
tampa = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-tampa.png').convert('RGBA')
# moldura brilhante do pôster (medida na imagem 1080x1920)
a = np.asarray(enigma.convert('RGB')).astype(int); m = (a[..., 0] > 170) & (a[..., 1] < 110) & (a[..., 2] < 110)
sub = m[700:1150, 200:880]; ys, xs = np.where(sub); MX0, MX1, MY0, MY1 = xs.min() + 200, xs.max() + 200, ys.min() + 700, ys.max() + 700
CX, CY = (MX0 + MX1) / 2 / W, (MY0 + MY1) / 2 / H

def fundo_verde():
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 900) * .8) / 1100, 0, 1)
    arr = np.array((24, 84, 54))[None, None] * (1 - dd[..., None]) + np.array(ESC)[None, None] * dd[..., None]
    return Image.fromarray(arr.astype('uint8')).convert('RGBA')
VERDE_BG = fundo_verde()

CENAS = []  # (duração, função(t_local, dur) -> RGBA)
def c1(t, D):   # o pôster-enigma, câmera aproximando
    b = zoom(enigma, 1 + .08 * ease(t / D), CX, CY).convert('RGBA'); d = ImageDraw.Draw(b)
    pilula(d, 190, 'A CAPA QUE TODO MUNDO TÁ DECIFRANDO', F('Black', 34), VERM, BR)
    texto(d, 320, 'TODO MUNDO', 120, PRETO, False); texto(d, 440, 'TENTANDO DECIFRAR…', 96, VERM, False); return b
def c2(t, D):   # mergulha na moldura e o MacBook aparece dentro dela
    z = 1.08 + .5 * ease(t / (D * .8)); b = zoom(enigma, z, CX, CY).convert('RGBA')
    k = min(1, max(0, (t - .3) / .5)); mm = MAC_C2.copy()
    mm.putalpha(mm.split()[3].point(lambda v: int(v * k))); b.alpha_composite(mm, ((W - mm.width) // 2, int(H * CY - mm.height / 2 + 30 * (1 - k)) + int((H / 2 - H * CY) * ease(t / (D * .8)))))
    d = ImageDraw.Draw(b); texto(d, 300, 'MAS O ÚNICO ENIGMA', 100, PRETO, False); texto(d, 420, 'QUE IMPORTA É…', 100, VERM, False); return b
MAC_C2 = mac.resize((int(W * .62), int(mac.height * W * .62 / mac.width)), Image.LANCZOS)
def c3(t, D):   # Leila com charme
    b = zoom(charme, 1.04 + .07 * ease(t / D), .5, .32).convert('RGBA'); degrade(b, 1280, H, 0, 245); tag_virtual(b); d = ImageDraw.Draw(b)
    texto(d, 1500, 'POR QUANTO SAI', 108, BR); texto(d, 1625, 'ESSE MACBOOK', 108, OURO); texto(d, 1740, 'AMANHÃ?', 108, BR); return b
def c4(t, D):   # o produto: fotos oficiais, novo e lacrado
    b = VERDE_BG.copy(); k = ease(t / D)
    mw = int(W * (.86 + .05 * k)); mm = mac.resize((mw, int(mac.height * mw / mac.width)), Image.BILINEAR)
    sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).ellipse((W / 2 - mw * .48, 1060, W / 2 + mw * .48, 1110), fill=(0, 0, 0, 170)); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    b.alpha_composite(mm, ((W - mw) // 2, 1090 - mm.height)); d = ImageDraw.Draw(b)
    texto(d, 250, 'MacBook Neo 13"', 104, BR); d.text((W / 2, 345), 'Prateado · Chip A18 Pro · 256GB', font=F('Medium', 40), fill=(214, 230, 218), anchor='mm')
    for i, txt in enumerate(['✓ novo e lacrado na caixa', '✓ com nota fiscal', '✓ com garantia']):
        a_ = int(255 * min(1, max(0, (t - .4 - i * .55) / .35))); pilula(d, 1250 + i * 125, txt.replace('✓ ', ''), F('Black', 46), VERDE, BR, a_)
        if a_: d.text((W / 2 - d.textlength(txt.replace('✓ ', ''), font=F('Black', 46)) / 2 - 2, 1250 + i * 125), '', fill=BR)
    return b
def c5(t, D):   # Leila piscando + lance
    b = zoom(piscada, 1.03 + .06 * ease(t / D), .5, .3).convert('RGBA'); degrade(b, 1150, H, 0, 250); tag_virtual(b); d = ImageDraw.Draw(b)
    d.text((W / 2, 1300), 'LANCE ATUAL', font=F('SemiBold', 40), fill=OURO, anchor='mm')
    fR, fN = F('Medium', 70), F('Black', 210); wr = d.textlength('R$ ', font=fR); wn = d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
    d.text((x0, 1530), 'R$', font=fR, fill=OURO, anchor='ls'); d.text((x0 + wr, 1530), LANCE, font=fN, fill=OURO, anchor='ls')
    pilula(d, 1640, 'quarta-feira, 18/11, às 20h', F('Black', 46), VERDE, BR); d.text((W / 2, 1760), 'dá o seu lance 👇'.replace(' 👇', ''), font=F('Black', 56), fill=BR, anchor='mm'); return b
def c6(t, D):   # assinatura
    b = VERDE_BG.copy(); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((640, 300))
    k = .9 + .1 * ease(t / D); lg = lg.resize((int(lg.width * k), int(lg.height * k)), Image.LANCZOS); b.alpha_composite(lg, ((W - lg.width) // 2, 760 - lg.height // 2))
    d = ImageDraw.Draw(b); d.text((W / 2, 1040), 'comenta LEILÃO que a gente', font=F('Black', 56), fill=BR, anchor='mm'); d.text((W / 2, 1115), 'te manda o link no direct', font=F('Black', 56), fill=OURO, anchor='mm'); return b
CENAS = [(2.8, c1), (2.8, c2), (3.0, c3), (3.6, c4), (3.4, c5), (2.2, c6)]
TRANS = 0.25; ULT = {}
total = sum(d for d, _ in CENAS); n = int(total * FPS); inicio = np.cumsum([0] + [d for d, _ in CENAS])
for i in range(n):
    t = i / FPS; k = max(j for j in range(len(CENAS)) if inicio[j] <= t + 1e-9); D, fn = CENAS[k]; tl = t - inicio[k]
    fr = fn(tl, D)
    if k > 0 and tl < TRANS:
        if k not in ULT: ULT[k] = CENAS[k - 1][1](CENAS[k - 1][0], CENAS[k - 1][0]).convert('RGB')
        fr = Image.blend(ULT[k], fr.convert('RGB'), tl / TRANS)
    fr.convert('RGB').save(f'{FR}/f{i:04d}.jpg', quality=90)
TR = f'{MK}/marca/trilhas-base/trilha-deep-house-elegante.mp3'; ASS = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
st = inicio[-2]
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{FR}/f%04d.jpg', '-i', TR, '-i', ASS, '-filter_complex',
    f"[1:a]atrim=0:{total},afade=t=in:d=0.4,afade=t=out:st={st - .4:.2f}:d=0.6,loudnorm=I=-17:TP=-2[m];[2:a]adelay={int(st * 1000)}|{int(st * 1000)},loudnorm=I=-16:TP=-1.5[s];[m][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]",
    '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.2f}', '-movflags', '+faststart', SAIDA], check=True)
print('ok', SAIDA, round(total, 1))
