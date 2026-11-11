# Arte "FALTA 1 HORA!" (19h) do iPhone 18 Pro Max — relógio 01:00:00, Bordô em destaque com Glacial e Silver atrás, lance atual.
# Uso: arte_1hora.py <saida.jpg> <lance> <n_lances> <stories|vendedores>  (stories: sem link; vendedores: com leilaonozap.net)
import sys, os, importlib.util
from PIL import Image, ImageDraw, ImageFilter
F0 = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('A', f'{F0}/artes_hoje_lib.py'); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
out, LANCE, NL, VER = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W, H = A.W, A.H
sc = Image.open(f'{F0}/fundo-texto.jpg').convert('RGB'); e = H/sc.height; sc = sc.resize((round(sc.width*e), H), Image.LANCZOS); x = (sc.width-W)//2
b = sc.crop((x, 0, x+W, H)).convert('RGBA')
A.logo(b)
A.pil(b, W/2, 268, 'iPHONE 18 PRO MAX · MARTELO ÀS 20H', A.F('Black', 38))
A.T(b, (W/2, 405), 'FALTA SÓ', A.F('Black', 118), A.BR)
A.OURO_T(b, (W/2, 575), '1 HORA!', A.F('Black', 230))
# relógio digital 01 : 00 : 00
d = ImageDraw.Draw(b); fd = A.F('Black', 120); fl = A.F('Bold', 28); y0, hh, ww, gap = 730, 170, 220, 70
xs = [W/2 - ww*1.5 - gap, W/2 - ww/2, W/2 + ww/2 + gap]
for (xx, num, lab) in zip(xs, ('01', '00', '00'), ('HORA', 'MIN', 'SEG')):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).rounded_rectangle((xx, y0+12, xx+ww, y0+hh+12), 30, fill=(0,0,0,160)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(12)))
    d.rounded_rectangle((xx, y0, xx+ww, y0+hh), 30, fill=(6,16,11,235), outline=A.OURO, width=5)
    d.line((xx+12, y0+hh/2, xx+ww-12, y0+hh/2), fill=(0,0,0,255), width=3)
    d.text((xx+ww/2, y0+hh/2+4), num, font=fd, fill=A.OURO if lab == 'HORA' else A.BR, anchor='mm')
    d.text((xx+ww/2, y0+hh+34), lab, font=fl, fill=A.CINZA, anchor='mm')
for xx in (xs[0]+ww+gap/2, xs[1]+ww+gap/2):
    for dy in (-28, 28): d.ellipse((xx-11, y0+hh/2+dy-11, xx+11, y0+hh/2+dy+11), fill=A.OURO)
# os 3 iPhones: Bordô na frente, Glacial e Silver atrás
base = 1480
A.luz(b, W/2, base-260, 300, 120)
for nome, cx, alt in (('glacial', W*0.27, 380), ('silver', W*0.73, 380)):
    f = A.fone(nome, alt); f.putalpha(f.split()[3].point(lambda v: int(v*0.92))); A.poe(b, f, cx, base-40)
A.poe(b, A.fone('bordo', 520), W/2, base)
A.pil(b, W/2, 1560, f'JÁ TEM DISPUTA · {NL} LANCES', A.F('Black', 40), fundo=A.FOGO if hasattr(A, 'FOGO') else (243,91,18), cor=A.BR, borda=None, padx=36)
A.pil(b, W/2, 1665, f'LANCE AGORA  {A.real(LANCE)}', A.F('Black', 50), fundo=A.FLOR, cor=A.BR, borda=A.OURO, h=100)
A.T(b, (W/2, 1752), 'Quem der o maior lance até o martelo, leva.', A.F('Bold', 40), A.CINZA)
rod = 'DÁ SEU LANCE · leilaonozap.net' if VER == 'vendedores' else 'CHAMA NO DIRECT: IPHONE'
A.pil(b, W/2, 1840, rod, A.F('Black', 44), fundo=A.OURO, cor=A.NOITE, borda=None, h=100)
b.convert('RGB').save(out, quality=94); print('ok', A.PROB)
