# Post de FEED do resultado da PCX (21/11): "saiu barata" — loja (uns R$ 20 mil) × arremate (R$ 10.667), lado a lado.
# Sem nome de quem arrematou, sem link, sem %. Cor: verde da arte da placa. Uso: resultado_feed.py <valor> <lances>
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/resultado'; MK = '/home/user/Leil-onozaplivoo/marketing'
VAL = sys.argv[1] if len(sys.argv) > 1 else '10667'; LCS = sys.argv[2] if len(sys.argv) > 2 else '116'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
STORY = len(sys.argv) > 3 and sys.argv[3] == 'story'
W, H = 1080, 1350; VE, MENTA, BR, NEON = (10, 61, 38), (214, 236, 221), (255, 255, 255), (63, 208, 126)
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 600) * .85) / 1000, 0, 1) ** 1.2
a = np.array((30, 108, 66))[None, None] * (1 - dd[..., None]) + np.array((12, 62, 38))[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
b = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); r = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(r)
for i in range(26): yy = 120 + i * 52; d.line((0, yy, W, yy + 40), fill=(255, 255, 255, 12), width=2)
b.alpha_composite(r)
FUNDO = b
if STORY: b = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(b)
d.text((W / 2, 105), 'OLHA POR QUANTO', font=F('Black', 92), fill=BR, anchor='mm')
d.text((W / 2, 205), 'SAIU ESSA MOTO', font=F('Black', 92), fill=MENTA, anchor='mm')
m = Image.open(f'{AQ}/fotos/pcx-plataforma-lado.webp').convert('RGBA'); m = m.crop(m.getbbox()); m = m.resize((860, int(m.height * 860 / m.width)), Image.LANCZOS)
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 380, 790, W / 2 + 380, 826), fill=(0, 0, 0, 120)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
b.alpha_composite(m, ((W - 860) // 2, 812 - m.height)); d = ImageDraw.Draw(b)
# loja × leilão
d.rounded_rectangle((70, 860, 470, 1100), 36, fill=(6, 40, 24))
d.text((270, 915), 'NA LOJA', font=F('Bold', 36), fill=MENTA, anchor='mm'); d.text((270, 990), 'uns R$', font=F('Medium', 40), fill=MENTA, anchor='mm'); d.text((270, 1050), '20 mil', font=F('Black', 70), fill=MENTA, anchor='mm')
d.line((140, 1050, 400, 1050), fill=MENTA, width=6)
d.rounded_rectangle((500, 860, W - 70, 1100), 36, fill=BR)
d.text((755, 915), 'NO LEILÃO', font=F('Bold', 36), fill=(27, 122, 72), anchor='mm')
d.text((755, 1000), f'R$ {real(VAL)}', font=F('Black', 88), fill=VE, anchor='mm')
d.text((755, 1068), 'arremate final', font=F('Medium', 30), fill=(27, 122, 72), anchor='mm')
d.text((W / 2, 1160), f'Honda PCX 160 · {LCS} lances · ao vivo', font=F('Bold', 38), fill=BR, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((200, 200)); b.alpha_composite(lg, ((W - lg.width) // 2, 1210))
if not STORY:
    FUNDO.alpha_composite(b); FUNDO.convert('RGB').save(f'{OUT}/FEED-resultado-pcx-{VAL}.jpg', quality=94); print('ok feed')
else:   # story 1080x1920: mesmo conteúdo no meio, com chamada em cima e pedido único embaixo
    HS = 1920; yy, xx = np.mgrid[0:HS, 0:W]; d2 = np.clip(np.hypot(xx - W / 2, (yy - 900) * .85) / 1150, 0, 1) ** 1.2
    a2 = np.array((30, 108, 66))[None, None] * (1 - d2[..., None]) + np.array((12, 62, 38))[None, None] * d2[..., None]; a2 += np.random.default_rng(3).normal(0, 1.6, a2.shape)
    st = Image.fromarray(np.clip(a2, 0, 255).astype('uint8')).convert('RGBA'); rr = Image.new('RGBA', (W, HS)); dr = ImageDraw.Draw(rr)
    for i in range(36): y0 = 150 + i * 52; dr.line((0, y0, W, y0 + 40), fill=(255, 255, 255, 12), width=2)
    st.alpha_composite(rr); st.alpha_composite(b, (0, 250)); ds = ImageDraw.Draw(st)
    f = F('Black', 40); t = 'RESULTADO DO LEILÃO DE SÁBADO'; w = ds.textlength(t, font=f)
    ds.rounded_rectangle((W / 2 - w / 2 - 36, 150, W / 2 + w / 2 + 36, 222), 36, fill=NEON); ds.text((W / 2, 186), t, font=f, fill=VE, anchor='mm')
    ds.rounded_rectangle((110, 1640, W - 110, 1790), 40, fill=MENTA)
    ds.text((W / 2, 1690), 'Quer ser o próximo?', font=F('Black', 50), fill=VE, anchor='mm'); ds.text((W / 2, 1748), 'responde LEILÃO que eu te mando o link', font=F('Medium', 36), fill=VE, anchor='mm')
    st.convert('RGB').save(f'{OUT}/STORY-arremate-loja-x-leilao-{VAL}.jpg', quality=94); print('ok story')
