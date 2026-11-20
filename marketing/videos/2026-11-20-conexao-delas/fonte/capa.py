# Capa do Conexão Delas (20/11): a foto do grupo inteiro (todas as mulheres) + título elegante. Rosto do bebê borrado.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FOTO, OUT = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; W, H = 1080, 1920
SER = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'; SERI = '/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf'
CREME, ROSA, VINHO = (255, 247, 238), (240, 175, 178), (58, 18, 32)
g = Image.open(FOTO).convert('RGB')
g = g.crop((430, 1150, 3024, 3950))   # recorte só nas mulheres: o bebê (canto esquerdo) fica de fora
fundo = g.resize((W, int(g.height * W / g.width))).crop((0, 0, W, H)) if False else g.resize((W * 2, int(g.height * W * 2 / g.width)))
bg = g.resize((W, H)).filter(ImageFilter.GaussianBlur(40)).convert('RGBA'); bg.alpha_composite(Image.new('RGBA', (W, H), VINHO + (170,)))
foto = g.resize((W, int(g.height * W / g.width)), Image.LANCZOS).convert('RGBA')
y0 = H - foto.height
m = Image.new('L', foto.size, 255); md = ImageDraw.Draw(m)
for i in range(160): md.line((0, i, W, i), fill=int(255 * i / 160))   # funde o topo da foto com o fundo
foto.putalpha(m); bg.alpha_composite(foto, (0, y0))
d = ImageDraw.Draw(bg)
def t(xy, s, f, cor):
    d.text((xy[0] + 3, xy[1] + 5), s, font=f, fill=(0, 0, 0, 130), anchor='mm'); d.text(xy, s, font=f, fill=cor, anchor='mm')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((180, 80)); bg.alpha_composite(lg, ((W - lg.width) // 2, 70))
t((W / 2, 250), 'CONEXÃO', ImageFont.truetype(SER, 150), CREME); t((W / 2, 400), 'DELAS', ImageFont.truetype(SER, 200), ROSA)
d.line((W / 2 - 170, 515, W / 2 + 170, 515), fill=ROSA, width=3); t((W / 2, 570), 'mulheres que transformam', ImageFont.truetype(SERI, 66), CREME)
bg.convert('RGB').save(OUT, quality=94); print('ok', y0)
