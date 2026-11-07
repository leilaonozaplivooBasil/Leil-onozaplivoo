# "É HOJE ÀS 20H · OPORTUNIDADE ÚNICA" — peça de desejo do iPhone (07/11). Story 9:16 e feed 4:5.
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.argv = [sys.argv[0], '800']
import campanha_iphone as C
from kit import logo
S = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/hoje20h'
OUT = C.OUT
def grad_txt(b, xy, t, f, c0, c1):
    m = Image.new('L', b.size); ImageDraw.Draw(m).text(xy, t, font=f, fill=255, anchor='mm'); bb = m.getbbox()
    g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
    for y in range(bb[1], bb[3] + 1):
        k = (y - bb[1]) / max(1, bb[3] - bb[1]); gd.line((0, y, b.width, y), fill=tuple(int(a + (z - a) * k) for a, z in zip(c0, c1)) + (255,))
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1] + 10), t, font=f, fill=(0, 0, 0, 170), anchor='mm'); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(Image.composite(g, Image.new('RGBA', b.size, (0, 0, 0, 0)), m)); return bb
def peca(w, h, nome):
    sc = Image.open(f'{S}/c1.png').convert('RGBA'); e = max(w / sc.width, h / sc.height); sc = sc.resize((round(sc.width * e), round(sc.height * e)), Image.LANCZOS)
    x = (sc.width - w) // 2; top = 0 if h >= 1900 else int(0.758 * sc.height) - 1160; b = sc.crop((x, top, x + w, top + h))
    base = int(0.758 * sc.height) - top
    logo(b, y=70 if h < 1900 else 110, largura=200 if h < 1900 else 230)
    yT = 290 if h >= 1900 else 210
    C.T(b, (w / 2, yT), 'É HOJE', C.F('Black', 210 if h >= 1900 else 170), C.BR)
    grad_txt(b, (w / 2, yT + (200 if h >= 1900 else 165)), 'ÀS 20H', C.F('Black', 210 if h >= 1900 else 170), (255, 230, 150), (220, 160, 50))
    py = yT + (370 if h >= 1900 else 305); f = C.F('Black', 46 if h >= 1900 else 40); d = ImageDraw.Draw(b); tw = d.textlength('OPORTUNIDADE ÚNICA', font=f)
    C.pil(b, w / 2, py, 'OPORTUNIDADE ÚNICA', f, (16, 60, 36), C.OURO, padx=44, borda=C.OURO)
    alt = 640 if h >= 1900 else 560
    pil_baixo = py + f.size / 2 + 17
    if base - alt < pil_baixo + 30: raise SystemExit(f'ERRO {nome}: o iPhone ficaria em cima do texto ({base - alt:.0f} < {pil_baixo + 30:.0f})')
    C.luz(b, w / 2, base - alt * 0.5, int(alt * 0.45), (255, 215, 140), 110)
    C.poe(b, C.iph(alt), w / 2, base + 6, (255, 220, 150), forca=180, reflexo=True)
    if h >= 1900:
        g = Image.new('RGBA', b.size); gd = ImageDraw.Draw(g)
        for yy in range(1500, h): gd.line((0, yy, w, yy), fill=(3, 12, 8, int(200 * min(1, (yy - 1500) / 140))))
        b.alpha_composite(g)
        C.T(b, (w / 2, 1600), 'iPhone 17 Pro Max · 256GB', C.F('Bold', 46), C.BR)
        C.T(b, (w / 2, 1660), 'na loja R$ 9.464,78', C.F('Medium', 38), (220, 225, 215), somb=0)
        C.pil(b, w / 2, 1760, 'DÊ SEU LANCE · leilaonozap.net', C.F('Black', 40), C.OURO, C.NOITE, h=104)
    else:
        C.pil(b, w / 2, h - 70, 'iPhone 17 Pro Max · comenta IPHONE', C.F('Black', 34), C.OURO, C.NOITE, h=84)
    b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=95); print(nome)
peca(1080, 1920, 'HOJE-20H-oportunidade-unica-story')
peca(1080, 1350, 'HOJE-20H-oportunidade-unica-feed')
