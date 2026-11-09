# Banner do site 1920x1080 a partir da cena gerada no Gamma (Leila + 3 iPhones, Bordô no centro). Texto por cima, nítido.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CENA, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); MENTA=(226,242,232)
W, H = 1920, 1080; PROB = []
b = Image.open(CENA).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
b.convert('RGB').save(f'{OUT}/BANNER-SITE-iphone18-SEM-TEXTO-para-video-1920x1080.jpg', quality=95)
def T(xy, t, f, cor, anchor='mm'):
    d = ImageDraw.Draw(b); bb = d.textbbox(xy, t, font=f, anchor=anchor)
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).text((xy[0], xy[1]+6), t, font=f, fill=(0,0,0,170), anchor=anchor); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(b).text(xy, t, font=f, fill=cor, anchor=anchor); return bb
def pil(cx, cy, t, f, fundo, cor, padx=34, borda=None):
    d = ImageDraw.Draw(b); w = d.textlength(t, font=f) + 2*padx; h = f.size + 28
    d.rounded_rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), h/2, fill=fundo, outline=borda, width=2 if borda else 0); d.text((cx, cy), t, font=f, fill=cor, anchor='mm'); return (cx-w/2, cy-h/2, cx+w/2, cy+h/2)
CX = 1245
caixas = [pil(CX, 72, 'QUARTA 11/11 · MARTELO 20H', F('Black', 40), FOGO, BR)]
caixas.append(T((CX, 168), 'iPHONE 18 PRO MAX', F('Black', 96), BR))
caixas.append(T((CX, 270), 'ESCOLHA SUA COR', F('Black', 104), OURO))
# nomes das cores embaixo de cada aparelho (posições medidas na cena)
for x, nome, cor in ((977, 'GLACIAL', (214,226,234)), (1239, 'BORDÔ', (122,30,52)), (1507, 'SILVER', (196,198,202))):
    d = ImageDraw.Draw(b); f = F('Black', 32); w = d.textlength(nome, font=f) + 84; h = 58; y = 968
    d.rounded_rectangle((x-w/2, y-h/2, x+w/2, y+h/2), h/2, fill=(6,30,18,235), outline=(255,255,255,110), width=2)
    d.ellipse((x-w/2+16, y-14, x-w/2+44, y+14), fill=cor, outline=BR, width=3); d.text((x-w/2+56, y), nome, font=f, fill=BR, anchor='lm'); caixas.append((x-w/2, y-h/2, x+w/2, y+h/2))
caixas.append(T((CX, 1040), '256GB · lacrado · quem arrematar escolhe a cor', F('Bold', 32), MENTA))
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg = lg.resize((200, int(lg.height*200/lg.width)), Image.LANCZOS)
d = ImageDraw.Draw(b); lx, ly = W-250, H-lg.height-50; d.rounded_rectangle((lx-16, ly-12, lx+200+16, ly+lg.height+12), 24, fill=(6,30,18,190)); b.alpha_composite(lg, (lx, ly)); caixas.append((lx-16, ly-12, lx+216, ly+lg.height+12))
# trava: nada fora da tela, nada encostando, texto longe da Leila (ela vai até x≈690)
for i, c in enumerate(caixas):
    if c[0] < 700 or c[2] > W-20 or c[1] < 10 or c[3] > H-8: PROB.append(f'peça {i} fora da área {c}')
    for j, e in enumerate(caixas[:i]):
        if not (c[2] + 12 < e[0] or e[2] + 12 < c[0] or c[3] + 8 < e[1] or e[3] + 8 < c[1]): PROB.append(f'peças {j} e {i} encostam')
b.convert('RGB').save(f'{OUT}/BANNER-SITE-iphone18-escolha-sua-cor-1920x1080.jpg', quality=94)
b.convert('RGB').resize((390, 219), Image.LANCZOS).save(f'{OUT}/fonte/previa-celular-390px.jpg')
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok')
