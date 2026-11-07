# Capa final: quadro 32,5 s escolhido pela Natália, sem texto, cor mais quente.
# O grid do perfil (corte 3:4 do meio) mostra exatamente o enquadramento do print dela.
import sys, numpy as np
from PIL import Image, ImageEnhance, ImageFilter
D, O = sys.argv[1], sys.argv[2]
src = Image.open(f'{D}/capa/o.jpg').convert('RGB')          # 2160x3840, original 4K
def quente(im):
    a = np.asarray(im).astype(float)/255
    a[...,0] = a[...,0]*1.09+0.02; a[...,1] = a[...,1]*1.03+0.008; a[...,2] = a[...,2]*0.87
    a = np.clip(a,0,1)**0.95
    w = Image.fromarray((a*255).astype('uint8'))
    return ImageEnhance.Contrast(ImageEnhance.Color(w).enhance(1.12)).enhance(1.04)
W, H = 2160, 3840
x0, y0, cw = 18, 1230, 2116                                  # enquadramento do print (largura toda das pessoas)
k = W/cw                                                     # escala p/ largura 2160
ch = cw*1440/1170                                            # altura do print no quadro
gy0 = 480 + (2880 - ch*k)/2                                  # topo do print dentro da área 3:4 (y 480..3360)
top = y0 - gy0/k                                             # de onde começa no quadro original
big = src.resize((round(src.width*k), round(src.height*k)), Image.LANCZOS)
out = Image.new('RGB', (W, H))
py = round(top*k); part = big.crop((round(x0*k), py, round(x0*k)+W, min(big.height, py+H)))
out.paste(part, (0, 0))
falta = H - part.height
if falta > 0:                                                # embaixo o quadro acaba: estende com desfoque escuro
    tira = part.crop((0, part.height-falta, W, part.height)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(40))
    tira = Image.blend(tira, Image.new('RGB', tira.size, (20,14,10)), 0.35)
    out.paste(tira, (0, part.height))
print('falta embaixo', falta, 'px de', H)
out = quente(out)
out.save(f'{O}/CAPA-FINAL-reel-emanuel-natalia.jpg', quality=95)
out.crop((0,480,W,3360)).resize((585,780)).save(f'{D}/capa/grid_final.jpg')
out.resize((540,960)).save(f'{D}/capa/final_9x16.jpg')
