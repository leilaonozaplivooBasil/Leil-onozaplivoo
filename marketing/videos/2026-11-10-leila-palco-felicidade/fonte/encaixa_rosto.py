# Encaixa a cabeça refeita (rosto da Leila certa) de volta na imagem do palco, com borda suave.
# Uso: encaixa_rosto.py <base.png> <cabeca.png> <saida.png> <escala> <x0> <y0> <cx> <cy> <rx> <ry> <pena>
import sys
from PIL import Image, ImageDraw, ImageFilter
b, h, out = sys.argv[1:4]; s, x0, y0, cx, cy, rx, ry, pena = map(float, sys.argv[4:12])
base = Image.open(b).convert('RGB'); cab = Image.open(h).convert('RGB')
m = Image.new('L', cab.size, 0); ImageDraw.Draw(m).ellipse((cx-rx, cy-ry, cx+rx, cy+ry), fill=255)
m = m.filter(ImageFilter.GaussianBlur(pena))
n = (round(cab.width*s), round(cab.height*s))
base.paste(cab.resize(n, Image.LANCZOS), (round(x0), round(y0)), m.resize(n, Image.LANCZOS))
base.save(out)
