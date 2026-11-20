# "ATENÇÃO: o leilão mais esperado do ano" — Honda PCX 160 (sáb 21/11, 20h), foto oficial da plataforma. Story 1080x1920 e feed 1080x1350.
# Uso: maior_leilao.py <lance>
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/maior-leilao'; MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
BR, OURO, OCL, OESC, NOITE, AMA, NEON = (255, 255, 255), (245, 196, 81), (252, 232, 175), (160, 110, 38), (5, 20, 12), (255, 214, 10), (63, 208, 126)
MOTO = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); MOTO = MOTO.crop(MOTO.getbbox())
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def ouro(b, xy, t, f):
    W, H = b.size; m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor='mm'); bb = m.getbbox()
    g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        k = min(1, abs((y - bb[1]) / max(1, bb[3] - bb[1]) - .35) * 1.6); gd.line((0, y, W, y), fill=tuple(int(p + (q - p) * k) for p, q in zip(OCL, OESC)) + (255,))
    gl = Image.new('RGBA', (W, H), OURO + (0,)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * .4))); b.alpha_composite(gl)
    sh = Image.new('RGBA', (W, H)); sh.putalpha(m.point(lambda v: int(v * .55)).transform((W, H), Image.AFFINE, (1, 0, -6, 0, 1, -9))); b.alpha_composite(sh)
    b.alpha_composite(Image.composite(g, Image.new('RGBA', (W, H)), m))
def arte(W, H, nome):
    k = H / 1920; Y = lambda v: int(v * k)
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - H * .55) * .85) / 1150, 0, 1) ** 1.2
    a = np.array((20, 92, 56))[None, None] * (1 - dd[..., None]) + np.array(NOITE)[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.5, a.shape)
    b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
    cy = Y(1000); d = ImageDraw.Draw(b)
    for i in range(24):   # holofote dourado em raios
        an = i / 24 * 2 * math.pi; r1, r2 = 260, 1100
        d.polygon([(W / 2 + r1 * math.cos(an - .04), cy + r1 * math.sin(an - .04)), (W / 2 + r2 * math.cos(an), cy + r2 * math.sin(an)), (W / 2 + r1 * math.cos(an + .04), cy + r1 * math.sin(an + .04))], fill=OURO + (34,))
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((W / 2 - 520, cy - 380, W / 2 + 520, cy + 380), fill=OURO + (90,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    lg = LOGO.copy(); lg.thumbnail((200, 200)); x0 = (W - lg.width) // 2; d = ImageDraw.Draw(b)
    d.rounded_rectangle((x0 - 22, Y(70) - 14, x0 + lg.width + 22, Y(70) + lg.height + 14), 26, fill=(5, 20, 12, 230)); b.alpha_composite(lg, (x0, Y(70)))
    # ATENÇÃO
    f = F('Black', 44); t = '⚠ ATENÇÃO'.replace('⚠ ', ''); w = d.textlength(t, font=f)
    d.rounded_rectangle((W / 2 - w / 2 - 70, (Y(250) if H > 1500 else 190), W / 2 + w / 2 + 70, (Y(250) if H > 1500 else 190) + 82), 41, fill=AMA) if True else None; d.polygon([(W / 2 - w / 2 - 50, (Y(250) if H > 1500 else 190) + 60), (W / 2 - w / 2 - 30, (Y(250) if H > 1500 else 190) + 22), (W / 2 - w / 2 - 10, (Y(250) if H > 1500 else 190) + 60)], fill=NOITE)
    d.text((W / 2 + 12, (Y(250) if H > 1500 else 190) + 42), t, font=f, fill=NOITE, anchor='mm')
    fz = 1 if H > 1500 else .8
    for txt, yy, tam in (('O LEILÃO MAIS', 420 if H > 1500 else 448, int(118 * fz)), ('ESPERADO', 545 if H > 1500 else 590, int(150 * fz))): 
        d.text((W / 2 + 4, Y(yy) + 7), txt, font=AN(tam), fill=(0, 0, 0, 160), anchor='mm'); d.text((W / 2, Y(yy)), txt, font=AN(tam), fill=BR, anchor='mm')
    ouro(b, (W / 2, Y(690) if H > 1500 else Y(765)), 'DO ANO', AN(int(170 * fz)))
    # moto (foto da plataforma) com reflexo no chão
    mw = 900 if H > 1500 else 640; m = MOTO.resize((mw, int(MOTO.height * mw / MOTO.width)), Image.LANCZOS); base = Y(1360) if H > 1500 else Y(1440)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 420, base - 22, W / 2 + 420, base + 30), fill=(0, 0, 0, 190)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(22)))
    r = m.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, mw, int(m.height * .3))); al = np.array(r.split()[3]).astype(float) * np.linspace(.28, 0, r.height)[:, None]; r.putalpha(Image.fromarray(al.astype('uint8')))
    b.alpha_composite(r, (int(W / 2 - mw / 2), base)); b.alpha_composite(m, (int(W / 2 - mw / 2), base - m.height)); d = ImageDraw.Draw(b)
    d.text((W / 2, base + Y(70)), 'HONDA PCX 160', font=F('Black', 64), fill=BR, anchor='mm')
    d.text((W / 2, base + Y(70) + 52), 'branca perolizada · retirada em mãos', font=F('SemiBold', 34), fill=(200, 230, 212), anchor='mm')
    # data + lance
    yb = base + Y(70) + (120 if H > 1500 else 100)
    d.rounded_rectangle((70, yb, W / 2 - 15, yb + 170), 30, fill=(0, 0, 0, 200), outline=OURO, width=3)
    d.text((W / 4 + 20, yb + 48), 'SÁBADO · 21/11', font=F('Black', 40), fill=OURO, anchor='mm'); d.text((W / 4 + 20, yb + 118), 'ÀS 20H', font=AN(84), fill=BR, anchor='mm')
    d.rounded_rectangle((W / 2 + 15, yb, W - 70, yb + 170), 30, fill=(0, 0, 0, 200), outline=OURO, width=3)
    d.text((W * .75 - 20, yb + 48), 'LANCE INICIAL', font=F('Black', 40), fill=OURO, anchor='mm'); d.text((W * .75 - 20, yb + 118), f'R$ {real(LANCE)}', font=AN(84), fill=BR, anchor='mm')
    if H > 1500:
        f = F('Black', 48); t = 'leilaonozap.net'; w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - 50, H - 150, W / 2 + w / 2 + 50, H - 62), 44, fill=NEON); d.text((W / 2, H - 106), t, font=f, fill=NOITE, anchor='mm')
    b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print('ok', nome)
arte(1080, 1920, 'PCX-maior-leilao-do-ano-STORY-1080x1920')
arte(1080, 1350, 'PCX-maior-leilao-do-ano-FEED-1080x1350')
