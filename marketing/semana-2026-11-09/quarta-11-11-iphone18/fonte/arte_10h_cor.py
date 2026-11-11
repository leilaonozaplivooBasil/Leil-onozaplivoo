# Arte 1 (10h) do dia do iPhone 18 — "QUAL VAI SER A SUA COR?": as 3 cores lado a lado, cada uma no seu pedestal dourado (vitrine).
# Reaproveita os ajudantes de artes_hoje.py (mesmas cores e letras aprovadas). Uso: arte_10h_cor.py <saida.jpg> [lance]
import sys, os, importlib.util
from PIL import Image, ImageDraw, ImageFilter
F0 = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('A', f'{F0}/artes_hoje_lib.py'); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
out = sys.argv[1]; LANCE = float(sys.argv[2]) if len(sys.argv) > 2 else 197.0
W, H = A.W, A.H
sc = Image.open(f'{F0}/fundo-texto.jpg').convert('RGB'); e = H/sc.height; sc = sc.resize((round(sc.width*e), H), Image.LANCZOS); x = (sc.width-W)//2
b = sc.crop((x, 0, x+W, H)).convert('RGBA')
A.logo(b)
A.pil(b, W/2, 268, 'HOJE · 20H · LEILÃO AO VIVO', A.F('Black', 40))
A.T(b, (W/2, 410), 'QUAL VAI SER', A.F('Black', 130), A.BR)
A.OURO_T(b, (W/2, 560), 'A SUA COR?', A.F('Black', 170))
A.T(b, (W/2, 690), 'Quem arrematar o iPhone 18 Pro Max escolhe.', A.F('Bold', 44), A.CINZA)
# três pedestais dourados com o nome de cada cor
cores = [('glacial', 'GLACIAL', W*0.185), ('bordo', 'BORDÔ', W*0.5), ('silver', 'SILVER', W*0.815)]
chao = 1300
for nome, rot, cx in cores:
    destaque = nome == 'bordo'; alt = 450 if destaque else 330; base = chao - (30 if destaque else 0)
    f = A.fone(nome, alt); rx = f.width/2 + (24 if destaque else 14)
    A.luz(b, cx, base-alt*0.45, 190 if destaque else 140, 105 if destaque else 80)
    pd = Image.new('RGBA', b.size); d = ImageDraw.Draw(pd)
    d.ellipse((cx-rx, base+40, cx+rx, base+100), fill=(8,26,18,255)); d.rectangle((cx-rx, base, cx+rx, base+70), fill=(12,38,26,255))
    for k in range(70): d.line((cx-rx, base+k, cx+rx, base+k), fill=(int(22-k*0.12), int(66-k*0.4), int(44-k*0.25), 255))
    d.ellipse((cx-rx, base+40, cx+rx, base+100), fill=(10,30,20,255))
    d.ellipse((cx-rx, base-30, cx+rx, base+30), fill=(30,86,56,255), outline=A.OURO+(255,), width=6)
    gl = Image.new('RGBA', b.size); ImageDraw.Draw(gl).ellipse((cx-rx, base-30, cx+rx, base+30), outline=(255,220,140,200), width=12); b.alpha_composite(gl.filter(ImageFilter.GaussianBlur(8)))
    b.alpha_composite(pd)
    A.poe(b, f, cx, base+6)
    A.pil(b, cx, 1470, rot, A.F('Black', 40 if destaque else 34), fundo=A.OURO if destaque else A.FLOR, cor=A.NOITE if destaque else A.OURO, borda=None if destaque else A.OURO, padx=34)
A.T(b, (W/2, 1600), 'iPhone 18 Pro Max · 256GB · lacrado, novo e com garantia', A.F('Bold', 38), A.BR)
rot = 'LANCE INICIAL' if LANCE <= 197.0001 else 'LANCE AGORA'
A.pil(b, W/2, 1700, f'{rot}  {A.real(LANCE)}', A.F('Black', 44), fundo=A.FLOR, cor=A.BR, borda=A.OURO, h=92)
A.pil(b, W/2, 1815, 'ESCOLHE A SUA · leilaonozap.net', A.F('Black', 42), fundo=A.OURO, cor=A.NOITE, borda=None, h=104)
b.convert('RGB').save(out, quality=94); print('ok', A.PROB)
