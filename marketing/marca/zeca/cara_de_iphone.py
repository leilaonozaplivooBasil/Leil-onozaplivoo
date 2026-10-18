# Tira o "acabamento de IA" de uma foto e imita o processamento da câmera frontal do iPhone:
# perde o microdetalhe perfeito, achata o contraste (Smart HDR), puxa a cor para lâmpada comum,
# aplica a nitidez exagerada do celular, granulado nas sombras e compressão JPEG.
import sys, io, numpy as np
from PIL import Image, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
quente = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
im = Image.open(src).convert('RGB')
w, h = im.size
alvo_w = 1179                                # largura de foto da câmera frontal (12 MP reduzida pelo app)
im = im.resize((alvo_w, round(h * alvo_w / w)), Image.LANCZOS)
p = im.resize((int(im.width * .62), int(im.height * .62)), Image.BILINEAR).resize(im.size, Image.BICUBIC)
a = np.asarray(p).astype(np.float32) / 255
lum = a.mean(2, keepdims=True)
a = 0.06 + a * 0.90                           # sombras levantadas, realces contidos (HDR achatado)
a = lum + (a - lum) * 0.90                    # um pouco menos de saturação
a *= np.array([1.0 + .03 * quente, 1.0 + .015 * quente, 1.0 - .045 * quente])  # lâmpada amarelo-esverdeada
rng = np.random.default_rng(7)
ruido = rng.normal(0, 1, a.shape[:2])[..., None] * (0.022 * (1.15 - lum))      # granulado mais forte no escuro
croma = rng.normal(0, 0.006, a.shape)
a = np.clip(a + ruido + croma, 0, 1)
im = Image.fromarray((a * 255).astype(np.uint8))
im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=85, threshold=2))   # nitidez de celular
b = io.BytesIO(); im.save(b, 'JPEG', quality=80, subsampling=2); b.seek(0)
Image.open(b).save(dst, 'JPEG', quality=88, subsampling=2)
print('ok', im.size)
