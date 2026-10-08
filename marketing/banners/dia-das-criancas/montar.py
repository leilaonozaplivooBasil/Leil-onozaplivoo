"""Junta a arte do Gamma (sem texto) com a camada de texto.
Uso: python3 montar.py arte-menino.jpg banner-menino-1920x1080"""
import sys
from PIL import Image, ImageOps
arte, saida = sys.argv[1], sys.argv[2]
base = ImageOps.fit(Image.open(arte).convert('RGB'), (1920, 1080), Image.LANCZOS)
texto = Image.open('texto-camada.png').convert('RGBA')
base = base.convert('RGBA'); base.alpha_composite(texto)
base.convert('RGB').save(saida + '.png')
base.convert('RGB').save(saida + '.jpg', quality=92, optimize=True)
print('ok', saida)
