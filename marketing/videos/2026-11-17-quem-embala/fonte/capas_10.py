# 10 capas para o "Quem embala o seu pedido?" SEM o rosto do Angel (idade não confirmada): pacote, mãos, impressora, tela.
# Quadros do vídeo original (720x1280), recortados abaixo do rosto. Uso: capas_10.py <pasta_mp4_720> <saida>
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
MK = '/home/user/Leil-onozaplivoo/marketing'; F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
LAR, AMA, VER, BR, ESC = (240, 96, 40), (245, 196, 81), (27, 122, 72), (255, 255, 255), (5, 28, 17)
# (arquivo, tempo, recorte (x0,y0,x1,y1) no 720x1280 ou None=tela cheia, pílula, linha1, linha2, sub)
CAPAS = [('IMG_5764', 0.1, None, 'BASTIDOR DO GALPÃO', 'QUEM EMBALA', 'O SEU PEDIDO?', 'do clique até a sua casa'),
         ('IMG_5762', 3.0, (0, 560, 720, 1280), 'BASTIDOR', 'DO CLIQUE', 'ATÉ A SUA CASA', 'olha o caminho do seu pedido'),
         ('IMG_5297', 2.0, (0, 480, 720, 1200), 'FOFOCA DO GALPÃO', 'O SEU PEDIDO', 'PASSA POR AQUI', 'a etiqueta sai na hora'),
         ('IMG_5291', 1.5, (0, 0, 720, 470), 'NA TELA DO SISTEMA', '931 PEDIDOS', 'E CONTANDO', 'e cada um embalado à mão'),
         ('IMG_5757', 6.0, (0, 560, 720, 1280), 'CAPRICHO', 'EMBALADO', 'COM CUIDADO', 'plástico bolha, caixa e papel'),
         ('IMG_5759', 4.0, (0, 480, 720, 1200), 'VOCÊ NUNCA VIU ISSO', 'O CAMINHO', 'DO SEU PEDIDO', 'do galpão até a sua porta'),
         ('IMG_5758', 30.0, (0, 560, 720, 1280), 'BASTIDOR', 'COMO CHEGA', 'NA SUA CASA?', 'a gente te mostra'),
         ('IMG_5760', 5.0, (0, 560, 720, 1280), 'SOM LIGADO', 'ASMR DE', 'EMBALAGEM', 'papel pardo e fita'),
         ('IMG_5763', 5.3, (0, 480, 720, 1200), 'FOFOCA DO GALPÃO', 'ESSE PACOTE', 'PODE SER SEU', 'quem embala é da equipe'),
         ('IMG_5756', 4.0, (0, 300, 720, 1020), 'BASTIDOR', 'DE ONDE SAI', 'O SEU PRODUTO?', 'o galpão da Leilão no Zap')]

def quadro(n, t):
    p = f'{OUT}/.q_{n}_{t}.png'
    if not os.path.exists(p): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-i', f'{IN}/{n}.mp4', '-frames:v', '1', p], check=True)
    im = Image.open(p).convert('RGB'); return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.06)).enhance(1.08)
def pil(d, cy, t, f, fundo, cor):
    w = d.textlength(t, font=f); h = f.size + 32
    d.rounded_rectangle((540 - w / 2 - 34, cy - h / 2, 540 + w / 2 + 34, cy + h / 2), h / 2, fill=fundo); d.text((540, cy), t, font=f, fill=cor, anchor='mm')
def titulo(d, y, t, cor, tam=120):
    while d.textlength(t, font=F('Black', tam)) > 980: tam -= 4
    f = F('Black', tam); d.text((540, y + 7), t, font=f, fill=(0, 0, 0, 160), anchor='mm'); d.text((540, y), t, font=f, fill=cor, anchor='mm'); return f.size
def fundo():
    y, x = np.mgrid[0:1920, 0:1080]; dd = np.clip(np.hypot(x - 540, (y - 1100) * .8) / 1100, 0, 1)
    a = np.array((24, 84, 54))[None, None] * (1 - dd[..., None]) + np.array(ESC)[None, None] * dd[..., None]
    return Image.fromarray(a.astype('uint8')).convert('RGBA')

grade = []
for i, (n, t, rc, p, l1, l2, sub) in enumerate(CAPAS, start=1):
    im = quadro(n, t)
    if rc is None:   # tela cheia (só o pacote)
        b = im.resize((1080, 1920), Image.LANCZOS).convert('RGBA'); g = np.zeros((1920, 1080, 4), np.uint8); g[..., :3] = ESC
        g[:620, :, 3] = (np.linspace(1, 0, 620) ** 1.2 * 225)[:, None].astype(np.uint8); g[1250:, :, 3] = (np.linspace(0, 1, 670) * 235)[:, None].astype(np.uint8)
        b.alpha_composite(Image.fromarray(g)); d = ImageDraw.Draw(b); pil(d, 206, p, F('Black', 40), LAR, BR)
        titulo(d, 1470, l1, BR); titulo(d, 1595, l2, AMA); pil(d, 1737, sub, F('Bold', 42), VER, BR)
    else:            # foto num cartão, sem rosto
        b = fundo(); d = ImageDraw.Draw(b); pil(d, 190, p, F('Black', 40), LAR, BR)
        s1 = titulo(d, 340, l1, BR); titulo(d, 340 + s1 * 1.02, l2, AMA)
        foto = im.crop(rc); k = 980 / foto.width; foto = foto.resize((980, int(foto.height * k)), Image.LANCZOS)
        foto = foto.filter(ImageFilter.UnsharpMask(2, 60, 2)); hy = min(foto.height, 1700 - 600); foto = foto.crop((0, 0, 980, hy))
        y0 = 600 + (1110 - hy) // 2; m = Image.new('L', foto.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 980, hy), 40, fill=255)
        sh = Image.new('RGBA', (1080, 1920)); ImageDraw.Draw(sh).rounded_rectangle((50, y0 + 24, 1030, y0 + hy + 24), 40, fill=(0, 0, 0, 150)); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
        b.paste(foto, (50, y0), m); d = ImageDraw.Draw(b); d.rounded_rectangle((50, y0, 1030, y0 + hy), 40, outline=AMA, width=4)
        pil(d, 1790, sub, F('Bold', 42), VER, BR)
        lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((150, 62)); b.alpha_composite(lg, ((1080 - lg.width) // 2, 40))
    d = ImageDraw.Draw(b); d.text((1040, 1890), f'{i:02d}', font=F('Bold', 32), fill=(255, 255, 255, 150), anchor='rs')
    b.convert('RGB').save(f'{OUT}/capa-{i:02d}.jpg', quality=92); grade.append(b.convert('RGB').resize((216, 384)))
s = Image.new('RGB', (216 * 5, 384 * 2))
for i, im in enumerate(grade): s.paste(im, ((i % 5) * 216, (i // 5) * 384))
s.save(f'{OUT}/TODAS-as-10-capas.jpg', quality=90)
for f in os.listdir(OUT):
    if f.startswith('.q_'): os.remove(os.path.join(OUT, f))
print('ok')
