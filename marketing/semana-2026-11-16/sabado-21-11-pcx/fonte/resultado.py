# Story de resultado da PCX (sáb 21/11): martelo batido às 20h37 por R$ 10.667, 116 lances. Sem nome de quem arrematou.
# Cor: o verde da arte da placa (pedido da Natália). Uso: resultado.py <valor> <lances>
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/resultado'; MK = '/home/user/Leil-onozaplivoo/marketing'
VAL, LCS = (sys.argv[1:3] + ['10667', '116'])[:2] if len(sys.argv) > 2 else ('10667', '116')
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920; VE, MENTA, BR, NEON = (10, 61, 38), (214, 236, 221), (255, 255, 255), (63, 208, 126)
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 950) * .85) / 1150, 0, 1) ** 1.2
a = np.array((30, 108, 66))[None, None] * (1 - dd[..., None]) + np.array((12, 62, 38))[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); r = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(r)
for i in range(34): yy = 200 + i * 52; d.line((0, yy, W, yy + 40), fill=(255, 255, 255, 12), width=2)
b.alpha_composite(r); d = ImageDraw.Draw(b)
def pil(cy, t, f, fu, co, px=40):
    w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - px, cy - f.size * .9, W / 2 + w / 2 + px, cy + f.size * .9), f.size, fill=fu); d.text((W / 2, cy), t, font=f, fill=co, anchor='mm')
pil(150, 'RESULTADO DE HOJE', F('Black', 42), NEON, VE)
d.text((W / 2, 290), 'MARTELO', font=F('Black', 150), fill=BR, anchor='mm'); d.text((W / 2, 440), 'BATIDO! 🔨'.replace(' 🔨', ''), font=F('Black', 150), fill=MENTA, anchor='mm')
# martelo (o mesmo do leiloeiro, recortado)
mt = Image.open(f'{MK}/marca/leiloeiro-martelo-sem-fundo.png').convert('RGBA').crop((0, 140, 270, 470)); mt.thumbnail((190, 230))
al = np.array(mt.split()[3]).astype(float); fade = np.clip((mt.height - np.arange(mt.height)) / (mt.height * .35), 0, 1)[:, None]; mt.putalpha(Image.fromarray((al * fade).astype('uint8')))   # some a mão aos poucos, sem corte reto
b.alpha_composite(mt, (W - 215, 320)); d = ImageDraw.Draw(b)
m = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); m = m.crop(m.getbbox()); m = m.resize((960, int(m.height * 960 / m.width)), Image.LANCZOS)
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 420, 1135, W / 2 + 420, 1175), fill=(0, 0, 0, 120)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
b.alpha_composite(m, ((W - 960) // 2, 1160 - m.height)); d = ImageDraw.Draw(b)
d.text((W / 2, 1230), 'A Honda PCX 160 saiu por', font=F('Medium', 50), fill=MENTA, anchor='mm')
fr, fn = F('Black', 80), F('Black', 210); n = real(VAL); wr, wn = d.textlength('R$', font=fr), d.textlength(n, font=fn); x0 = (W - wr - 16 - wn) / 2
d.text((x0, 1310), 'R$', font=fr, fill=NEON, anchor='lt'); d.text((x0 + wr + 16, 1400), n, font=fn, fill=BR, anchor='lm')
d.text((W / 2, 1545), f'{LCS} lances · arrematado ao vivo às 20h37', font=F('Bold', 40), fill=BR, anchor='mm')
d.rounded_rectangle((110, 1620, W - 110, 1760), 40, fill=MENTA)
d.text((W / 2, 1665), 'Amanhã tem mais leilão às 20h', font=F('Black', 46), fill=VE, anchor='mm'); d.text((W / 2, 1720), 'fica de olho nos stories 👀'.replace(' 👀', ''), font=F('Medium', 36), fill=VE, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((210, 210)); b.alpha_composite(lg, ((W - lg.width) // 2, 1800))
b.convert('RGB').save(f'{OUT}/STORY-resultado-pcx-{VAL}.jpg', quality=94); print('ok')
