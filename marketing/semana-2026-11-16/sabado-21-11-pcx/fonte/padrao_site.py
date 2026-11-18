# PCX sáb 21/11 · 3 banners do site no MESMO PADRÃO dos que estão no ar (indicação +5% e R$ 10 de bônus):
# personagem à esquerda, à direita logo grande + título condensado (Anton) branco e dourado 3D + botão verde neon + risco dourado.
# Texto fica de x=1080 pra direita (o "Toque para ouvir" do site fica no meio). Sai FINAL + camadas pra virar vídeo.
# Uso: padrao_site.py <lance> [1,2,3]
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/padrao-site-3-versoes'; MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '497'; SO = sys.argv[2].split(',') if len(sys.argv) > 2 else '123'
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
FD = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1920, 1080; CX, X0, X1 = 1460, 1080, 1840
BR, NEON, VNOITE, OURO = (255, 255, 255), (63, 208, 126), (6, 40, 24), (245, 196, 81)
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def novo(): return Image.new('RGBA', (W, H))
def caber(t, f_, tam, larg):
    while f_(tam).getlength(t) > larg: tam -= 2
    return f_(tam)
def mascara(xy, t, f):
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor='mm'); return m
def foto(arq):
    im = Image.open(arq).convert('RGB'); k = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS); x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)).convert('RGBA')
def escurecer():
    xs = np.arange(W) / W; g = np.tile(np.clip((xs - .42) / .25, 0, 1) ** 1.3 * 200, (H, 1))
    s = Image.new('RGBA', (W, H), (4, 26, 15, 0)); s.putalpha(Image.fromarray(g.astype('uint8'))); return s
def ouro3d(xy, t, f, prof=14):
    m = mascara(xy, t, f); bb = m.getbbox(); c = novo()
    gl = Image.new('RGBA', (W, H), (255, 200, 90, 0)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * .45))); c.alpha_composite(gl)
    for i in range(prof, 0, -1):   # extrusão: camadas cada vez mais escuras para baixo-direita
        k = i / prof; cor = tuple(int(a * (1 - k) + b * k) for a, b in zip((150, 100, 30), (60, 36, 8))) + (255,)
        lay = Image.new('RGBA', (W, H), cor); c.alpha_composite(Image.composite(lay, novo(), ImageChops.offset(m, int(i * .5), i)))
    face = novo(); fd = ImageDraw.Draw(face); h = max(1, bb[3] - bb[1])
    pal = [(0, (255, 244, 200)), (.35, (246, 205, 110)), (.55, (196, 140, 50)), (.62, (232, 182, 86)), (1, (150, 98, 32))]
    for y in range(bb[1], bb[3] + 1):
        r = (y - bb[1]) / h
        for (a, ca), (b, cb) in zip(pal, pal[1:]):
            if a <= r <= b: k = (r - a) / (b - a); fd.line((0, y, W, y), fill=tuple(int(p + (q - p) * k) for p, q in zip(ca, cb)) + (255,)); break
    c.alpha_composite(Image.composite(face, novo(), m))
    luz = ImageChops.subtract(m, ImageChops.offset(m, 0, 3)).filter(ImageFilter.GaussianBlur(1))   # brilho na borda de cima
    hl = Image.new('RGBA', (W, H), (255, 252, 230, 0)); hl.putalpha(luz.point(lambda v: int(v * .9))); c.alpha_composite(hl); return c
def branco3d(xy, t, f, prof=8):
    m = mascara(xy, t, f); c = novo()
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(ImageChops.offset(m, 6, 12).filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .55))); c.alpha_composite(sh)
    for i in range(prof, 0, -1):
        lay = Image.new('RGBA', (W, H), (150, 170, 160, 255)); c.alpha_composite(Image.composite(lay, novo(), ImageChops.offset(m, int(i * .4), i)))
    c.alpha_composite(Image.composite(Image.new('RGBA', (W, H), (250, 252, 248, 255)), novo(), m)); return c
def logo(y=200, larg=500):
    c = novo(); lg = LOGO.copy(); lg.thumbnail((larg, larg)); g = Image.new('RGBA', lg.size, (0, 0, 0, 0)); g.putalpha(lg.split()[3].point(lambda v: int(v * .5)))
    c.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)), (CX - lg.width // 2 + 6, y - lg.height // 2 + 12)); c.alpha_composite(lg, (CX - lg.width // 2, y - lg.height // 2)); return c
def frase(y, partes, tam=74):
    """partes = [(texto, cor), ...] numa linha só, centrada, em Anton"""
    f = AN(tam); tot = sum(f.getlength(t) for t, _ in partes)
    while tot > X1 - X0: tam -= 2; f = AN(tam); tot = sum(f.getlength(t) for t, _ in partes)
    c = novo(); d = ImageDraw.Draw(c); x = CX - tot / 2
    for t, cor in partes: d.text((x + 3, y + 5), t, font=f, fill=(0, 0, 0, 150), anchor='lm'); d.text((x, y), t, font=f, fill=cor, anchor='lm'); x += f.getlength(t)
    return c
def botao(y, t):
    f = caber(t, AN, 64, X1 - X0 - 140); w = f.getlength(t) + 130; hh = 112; c = novo()
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).rounded_rectangle((CX - w / 2, y - hh / 2, CX + w / 2, y + hh / 2), hh / 2, fill=NEON + (210,)); c.alpha_composite(g.filter(ImageFilter.GaussianBlur(26)))
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).rounded_rectangle((CX - w / 2, y - hh / 2, CX + w / 2, y + hh / 2), hh / 2, fill=255)
    gr = novo(); gd = ImageDraw.Draw(gr)
    for yy in range(int(y - hh / 2), int(y + hh / 2) + 1):
        k = (yy - (y - hh / 2)) / hh; gd.line((0, yy, W, yy), fill=tuple(int(a + (b - a) * k) for a, b in zip((110, 238, 160), (28, 160, 84))) + (255,))
    c.alpha_composite(Image.composite(gr, novo(), m)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((CX - w / 2, y - hh / 2, CX + w / 2, y + hh / 2), hh / 2, outline=(170, 255, 205), width=3); d.text((CX, y + 2), t, font=f, fill=VNOITE, anchor='mm'); return c
def risco(y):
    c = novo(); d = ImageDraw.Draw(c); pts = [(X0 + 120 + i * 6, y + 40 - 70 * (1 - ((i * 6) / 560 - .5) ** 2 * 4) ** .5 * .5) for i in range(94)]
    for k, wdt in ((0, 14), (1, 8)): d.line(pts, fill=((200, 150, 60) if k == 0 else (255, 225, 150)) + (255,), width=wdt, joint='curve')
    return c.filter(ImageFilter.GaussianBlur(.8))
def rodape(t='retirada em mãos com a equipe Leilão no Zap'):
    c = novo(); ImageDraw.Draw(c).text((CX, 1048), t, font=FD('Medium', 24), fill=(200, 220, 208), anchor='mm'); return c
def salvar(nome, camadas):
    os.makedirs(f'{OUT}/{nome}-camadas', exist_ok=True); b = camadas[0][1].copy()
    for i, (n, im) in enumerate(camadas):
        if i: b.alpha_composite(im)
        (im.convert('RGB').save(f'{OUT}/{nome}-camadas/{i:02d}-{n}.jpg', quality=93) if i == 0 else im.save(f'{OUT}/{nome}-camadas/{i:02d}-{n}.png'))
    b.convert('RGB').save(f'{OUT}/{nome}-FINAL-1920x1080.jpg', quality=93); print('ok', nome)

if '1' in SO and os.path.exists(f'{AQ}/site-1.jpg'):
    salvar('1-sua-pcx-te-espera', [('foto', foto(f'{AQ}/site-1.jpg')), ('escurece', escurecer()), ('logo', logo()),
        ('titulo-1', branco3d((CX, 440), 'SUA PCX', caber('SUA PCX', AN, 190, 700))), ('titulo-2', ouro3d((CX, 615), 'TE ESPERA.', caber('TE ESPERA.', AN, 200, 760))),
        ('frase', frase(760, [('Lance inicial de só ', BR), (f'R$ {real(LANCE)}!', OURO)])), ('botao', botao(905, 'SÁBADO 21/11 · DÊ SEU LANCE')), ('risco', risco(970)), ('rodape', rodape())])
if '2' in SO and os.path.exists(f'{AQ}/site-2.jpg'):
    salvar('2-sabado-e-dia-de-pcx', [('foto', foto(f'{AQ}/site-2.jpg')), ('escurece', escurecer()), ('logo', logo()),
        ('titulo-1', branco3d((CX, 440), 'SÁBADO É DIA', caber('SÁBADO É DIA', AN, 170, 760))), ('titulo-2', ouro3d((CX, 625), 'DE PCX.', caber('DE PCX.', AN, 230, 760))),
        ('frase', frase(775, [('Honda PCX 160 · lance inicial ', BR), (f'R$ {real(LANCE)}', OURO)])), ('botao', botao(900, 'PARTICIPE DO LEILÃO')), ('risco', risco(970)), ('rodape', rodape())])
if '3' in SO and os.path.exists(f'{AQ}/site-3.jpg'):
    salvar('3-comeca-em-497', [('foto', foto(f'{AQ}/site-3.jpg')), ('escurece', escurecer()), ('logo', logo(170, 420)),
        ('titulo-1', branco3d((CX, 365), 'A PCX COMEÇA EM', caber('A PCX COMEÇA EM', AN, 130, 760))), ('titulo-2', ouro3d((CX, 600), f'R$ {real(LANCE)}', caber(f'R$ {real(LANCE)}', AN, 290, 760), prof=18)),
        ('frase', frase(778, [('E a chave pode ser ', BR), ('sua!', OURO)])), ('botao', botao(895, 'SÁBADO 21/11 · DÊ SEU LANCE')), ('risco', risco(965)), ('rodape', rodape())])
