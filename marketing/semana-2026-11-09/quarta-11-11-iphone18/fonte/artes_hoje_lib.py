# Artes do dia do leilão do iPhone 18 Pro Max (qua 11/11, 20h) — estilo da arte "É HOJE ÀS 20H" (cores aprovadas).
# Uso: artes_hoje.py <saida> [lance_atual]  — sem lance (ou igual ao inicial) aparece "LANCE INICIAL R$ 197".
# Formato story 9:16 (vendedores/WhatsApp/Stories). Link só vai para WhatsApp; no Instagram usar a versão sem link.
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F0 = os.path.dirname(os.path.abspath(__file__)); MK = '/home/user/Leil-onozaplivoo/marketing'
W, H = 1080, 1920; NOITE, FLOR, OURO, BR, CINZA = (6,16,11), (16,60,36), (245,196,81), (255,255,255), (220,226,218)
OA, OB = (255,232,155), (214,152,44)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
PROB = []
def real(v): return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def cabe(d, t, f, maxw):
    while d.textlength(t, font=f) > maxw:
        if f.size < 28: PROB.append(t); break
        f = ImageFont.truetype(f.path, f.size - 2)
    return f
def T(b, xy, t, f, cor, maxw=W-100, somb=170, anchor='mm'):
    d = ImageDraw.Draw(b); f = cabe(d, t, f, maxw)
    if somb:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+9), t, font=f, fill=(0,0,0,somb), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(13)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor)
def OURO_T(b, xy, t, f, maxw=W-100):
    d = ImageDraw.Draw(b); f = cabe(d, t, f, maxw)
    m = Image.new('L', b.size); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor='mm'); bb = m.getbbox()
    g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3]+1):
        k = (y-bb[1])/max(1, bb[3]-bb[1]); gd.line((0, y, W, y), fill=tuple(int(a+(z-a)*k) for a, z in zip(OA, OB))+(255,))
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+10), t, font=f, fill=(0,0,0,180), anchor='mm'); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(Image.composite(g, Image.new('RGBA', b.size, (0,0,0,0)), m))
def pil(b, cx, cy, t, f, fundo=FLOR, cor=OURO, borda=OURO, padx=46, h=None):
    d = ImageDraw.Draw(b); f = cabe(d, t, f, W-170); w = d.textlength(t, font=f); h = h or f.size + 46
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((cx-w/2-padx, cy-h/2+8, cx+w/2+padx, cy+h/2+8), h/2, fill=(0,0,0,150)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle((cx-w/2-padx, cy-h/2, cx+w/2+padx, cy+h/2), h/2, fill=fundo, outline=borda, width=4 if borda else 0); d.text((cx, cy+2), t, font=f, fill=cor, anchor='mm')
def luz(b, cx, cy, r, alfa=110):
    g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((cx-r, cy-r, cx+r, cy+r), fill=(255,215,140,alfa)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r*0.55)))
def fone(nome, alt):
    im = Image.open(f'{F0}/fotos/c-{nome}.png').convert('RGBA'); im = im.crop(im.getbbox()); e = alt/im.height
    return im.resize((round(im.width*e), alt), Image.LANCZOS)
def poe(b, p, cx, base, sombra=True):
    if sombra:
        s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((cx-p.width*0.45, base-20, cx+p.width*0.45, base+18), fill=(0,0,0,170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(p, (int(cx-p.width/2), int(base-p.height)))

def logo(b, y=110):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((240, 90)); x = (W-lg.width)//2
    pl = Image.new('RGBA', b.size); ImageDraw.Draw(pl).rounded_rectangle((x-26, y-14, x+lg.width+26, y+14+lg.height), 28, fill=(6,16,11,190)); b.alpha_composite(pl); b.alpha_composite(lg, (x, y))
