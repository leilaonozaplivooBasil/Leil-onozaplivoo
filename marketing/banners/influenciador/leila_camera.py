"""Cola a tela da câmera (tela-camera.png, 920x2000) no celular da foto oficial da Leila.
Uso: python3 leila_camera.py tela-camera.png leila-camera.png"""
import sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
AQUI = os.path.dirname(os.path.abspath(__file__))
tela_p, saida = sys.argv[1], sys.argv[2]
src = Image.open(os.path.join(AQUI, 'leila-oficial.webp')).convert('RGB')
tela = Image.open(tela_p).convert('RGB')
W, H = tela.size
# cantos da área de tela na foto (TL, TR, BR, BL), medidos na imagem 1216x1294
quad = np.float32([[57, 299], [284, 299], [278, 803], [46, 803]])
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), quad)
warp = cv2.warpPerspective(np.array(tela), M, src.size, flags=cv2.INTER_AREA)
# máscara com cantos arredondados (no espaço da tela) e recorte do notch
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
d.rounded_rectangle([0, 0, W - 1, H - 1], radius=int(W * .1), fill=255)
mask = cv2.warpPerspective(np.array(m), M, src.size, flags=cv2.INTER_LINEAR)
mask = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(.6))
out = src.copy(); out.paste(Image.fromarray(warp), (0, 0), mask)
# notch preto por cima
d2 = ImageDraw.Draw(out)
d2.rounded_rectangle([118, 290, 214, 322], radius=12, fill=(8, 8, 10))
out.save(saida)
