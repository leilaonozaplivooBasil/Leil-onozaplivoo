# Artes do dia do leilão do iPhone 18 Pro Max (qua 11/11, 20h) — estilo da arte "É HOJE ÀS 20H" (cores aprovadas).
# Uso: artes_hoje.py <saida> [lance_atual]  — sem lance (ou igual ao inicial) aparece "LANCE INICIAL R$ 197".
# Formato story 9:16 (vendedores/WhatsApp/Stories). Link só vai para WhatsApp; no Instagram usar a versão sem link.
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]; LANCE = float(sys.argv[2]) if len(sys.argv) > 2 else 197.0
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
def base_fundo():
    sc = Image.open(f'{F0}/fundo-podio.jpg').convert('RGB'); e = H/sc.height; sc = sc.resize((round(sc.width*e), H), Image.LANCZOS)
    x = (sc.width-W)//2; return sc.crop((x, 0, x+W, H)).convert('RGBA')
PODIO = int(0.765*H) + 6
def arte(nome, l1, l2, pilula, l1_ouro=False):
    b = base_fundo()
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((240, 90)); x = (W-lg.width)//2
    pl = Image.new('RGBA', b.size); ImageDraw.Draw(pl).rounded_rectangle((x-26, 96, x+lg.width+26, 124+lg.height), 28, fill=(6,16,11,190)); b.alpha_composite(pl); b.alpha_composite(lg, (x, 110))
    if l1_ouro: OURO_T(b, (W/2, 330), l1, F('Black', 190))
    else: T(b, (W/2, 330), l1, F('Black', 200), BR)
    OURO_T(b, (W/2, 530), l2, F('Black', 200))
    pil(b, W/2, 720, pilula, F('Black', 46))
    # 3 cores: Glacial e Silver atrás, Bordô na frente, no pódio
    luz(b, W/2, PODIO-330, 300)
    g = fone('glacial', 470); s = fone('silver', 470); bo = fone('bordo', 600)
    poe(b, g, W/2-250, PODIO-40, False); poe(b, s, W/2+250, PODIO-40, False); poe(b, bo, W/2, PODIO)
    gr = Image.new('RGBA', b.size); gd = ImageDraw.Draw(gr)
    for yy in range(1500, H): gd.line((0, yy, W, yy), fill=(3,12,8, int(215*min(1, (yy-1500)/130))))
    b.alpha_composite(gr)
    T(b, (W/2, 1575), 'iPhone 18 Pro Max · 256GB · lacrado', F('Bold', 48), BR)
    T(b, (W/2, 1635), 'quem arrematar escolhe a cor: Bordô, Glacial ou Silver', F('Medium', 34), CINZA, somb=0)
    rot = 'LANCE INICIAL' if LANCE <= 197.0001 else 'LANCE AGORA'
    pil(b, W/2, 1725, f'{rot}  {real(LANCE)}', F('Black', 44), fundo=FLOR, cor=BR, borda=OURO, h=92)
    pil(b, W/2, 1832, 'DÊ SEU LANCE · leilaonozap.net', F('Black', 42), fundo=OURO, cor=NOITE, borda=None, h=104)
    b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=94); print(nome)
os.makedirs(OUT, exist_ok=True)
arte('1-10H-e-hoje-as-20h', 'É HOJE', 'ÀS 20H', 'OPORTUNIDADE ÚNICA')
arte('2-14H-faltam-6-horas', 'FALTAM', '6 HORAS', 'O MARTELO BATE ÀS 20H')
arte('3-18H-faltam-2-horas', 'FALTAM', '2 HORAS', 'QUEM DER MAIS, LEVA')
arte('4-19H-falta-1-hora', 'FALTA', '1 HORA', 'ÚLTIMA CHAMADA')
arte('5-19H50-faltam-10-minutos', 'FALTAM', '10 MIN', 'ENTRA NA SALA AGORA')
arte('6-20H-e-agora-ao-vivo', 'É AGORA!', 'AO VIVO', 'A DISPUTA COMEÇOU')
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
