"""Gera a foto da Leila com a tela do celular mostrando o iPhone 17 Pro Max.
Uso: python3 tela_celular.py "Começa em 1 dia" saida.png"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
AQUI = os.path.dirname(os.path.abspath(__file__))
F = '/usr/share/fonts/opentype/inter/'
status, saida = sys.argv[1], sys.argv[2]
src = Image.open(os.path.join(AQUI, 'leila-oficial.webp')).convert('RGB')
K = 4
X0, Y0, X1, Y1 = 40, 340, 300, 780
reg = src.crop((X0, Y0, X1, Y1)).resize(((X1-X0)*K, (Y1-Y0)*K), Image.LANCZOS)
d = ImageDraw.Draw(reg)
R = lambda x0, y0, x1, y1: [(x0-X0)*K, (y0-Y0)*K, (x1-X0)*K, (y1-Y0)*K]
P = lambda x, y: ((x-X0)*K, (y-Y0)*K)
f = lambda n, s: ImageFont.truetype(F+n, int(s*K))
def restretch(x0, x1, y0, y1, yclean):
    row = reg.crop((int((x0-X0)*K), int((yclean-Y0)*K), int((x1-X0)*K), int((yclean-Y0)*K)+1))
    reg.paste(row.resize((row.width, int((y1-y0)*K))), (int((x0-X0)*K), int((y0-Y0)*K)))
restretch(100, 240, 370, 393, 369.5)
d.text(P(170, 381.5), "Entre e Dê o Lance", font=f('Inter-SemiBold.otf', 10.5), fill='white', anchor='mm')
d.rounded_rectangle(R(61, 409, 272.5, 604), radius=6*K, fill=(246, 247, 249))
ip = Image.open(os.path.join(AQUI, 'iphone.png')); h = int(178*K)
ip = ip.resize((int(ip.width*h/ip.height), h), Image.LANCZOS)
reg.paste(ip, (int(((61+272.5)/2-X0)*K-ip.width/2), int((415-Y0)*K)), ip)
d.rectangle(R(62, 606, 273, 629), fill=(3, 31, 52))
d.text(P(67, 617.5), "iPhone 17 Pro Max", font=f('Inter-SemiBold.otf', 11.5), fill='white', anchor='lm')
d.rectangle(R(62, 630, 276, 672), fill=(2, 28, 49))
d.ellipse(R(68, 646.5, 75, 653.5), fill=(255, 196, 70))
d.text(P(81, 650), status, font=f('Inter-Bold.otf', 12), fill=(255, 196, 70), anchor='lm')
restretch(128, 235, 727, 753, 726.5)
d.text(P(184, 740), "Comparar Preço", font=f('Inter-SemiBold.otf', 10), fill='white', anchor='mm')
reg = reg.resize((X1-X0, Y1-Y0), Image.LANCZOS)
out = src.copy(); out.paste(reg, (X0, Y0))
out.crop((0, 0, 900, out.height)).save(saida)
