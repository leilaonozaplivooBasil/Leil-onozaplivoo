import numpy as np
from PIL import Image, ImageFilter, ImageDraw
D='/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/joao-fundo'
R='/home/user/Leil-onozaplivoo/marketing/fotos/2026-11-04-joao-fundo-loja'
orig=Image.open('/root/.claude/uploads/0ed67ded-c847-5a23-a4f2-d97436f79693/020bf712-image.jpg').convert('RGB')
W,H=orig.size; rng=np.random.default_rng(11)
mask=Image.open(f'{D}/recorte.png').split()[3].resize(orig.size).filter(ImageFilter.GaussianBlur(1.0))
m=np.asarray(mask,np.float32)/255.
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def campo(esc):
    n=rng.normal(0,1,(H//esc+2,W//esc+2)).astype(np.float32)
    return np.asarray(Image.fromarray(((n-n.min())/(n.ptp() if hasattr(n,'ptp') else (n.max()-n.min()))*255).astype(np.uint8)).resize((W,H),Image.BICUBIC),np.float32)/255.-0.5
# geometria (câmera de baixo pra cima, como a selfie original): teto branco no alto, quina da parede à direita
y_teto = 300 + (xx/W)*(-150)          # linha parede/teto inclinada, igual ao ângulo do teto da foto original
x_quina = 960 + (yy/H)*70             # quina vertical, levemente inclinada pela perspectiva
teto = yy < y_teto
lado = (xx > x_quina) & ~teto
# textura "casca de laranja" de tinta acrílica: relevo fino iluminado de cima
alt = campo(3)*0.6 + campo(7)*0.4
alt = np.asarray(Image.fromarray(((alt+0.5)*255).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.8)),np.float32)/255.
gy,gx = np.gradient(alt)
relevo = 1 + (-gy*0.9 + gx*0.35)*1.5
manchas = 1 + campo(140)*0.06 + campo(45)*0.03     # parede pintada à mão: rolo deixa leve variação
menta = np.array([176,214,194],np.float32); branco = np.array([238,236,230],np.float32)
luz = 1.07 - 0.20*np.sqrt(((xx-W*0.35)/W)**2 + ((yy-H*0.05)/H)**2)   # lâmpada do teto, perto e acima
img = np.where(teto[...,None], branco[None,None,:]*(0.96+0.04*relevo[...,None]), menta[None,None,:]*(luz*manchas*relevo)[...,None])
img = np.where(lado[...,None], img*0.86, img)                       # parede do lado recebe menos luz
# sombra de contato na quina e na linha do teto (oclusão)
dq = np.abs(xx-x_quina); img *= (1-0.10*np.exp(-dq/25))[...,None]
dt = np.clip(yy-y_teto,0,None); img = np.where(~teto[...,None], img*(1-0.12*np.exp(-dt/35))[...,None], img)
# moldura de gesso (sanca) fininha entre parede e teto
moldura = (yy>=y_teto) & (yy<y_teto+14); img = np.where(moldura[...,None], branco[None,None,:]*0.97, img)
img = np.where(((yy>=y_teto+14)&(yy<y_teto+17))[...,None], img*0.80, img)
# tomada/interruptor na parede (meio escondido atrás do ombro, como numa sala de verdade)
pil = Image.fromarray(np.clip(img,0,255).astype(np.uint8)); d=ImageDraw.Draw(pil)
x0,y0=70,780; d.rounded_rectangle((x0+4,y0+5,x0+124,y0+185),10,fill=(120,150,135)); d.rounded_rectangle((x0,y0,x0+120,y0+180),10,fill=(236,234,228)); d.rounded_rectangle((x0+40,y0+55,x0+80,y0+125),6,fill=(222,220,214))
img=np.asarray(pil,np.float32)
# sombra do João na parede e profundidade de campo de celular
sh=Image.fromarray((m*255).astype(np.uint8)).transform((W,H),Image.AFFINE,(1,0,60,0,1,-35)).filter(ImageFilter.GaussianBlur(55))
img *= (1-0.20*np.asarray(sh,np.float32)/255.)[...,None]
img=np.asarray(Image.fromarray(np.clip(img,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2)),np.float32)
foto=np.asarray(orig,np.float32)
borda=np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)),np.float32)/255.
wrap=np.clip((1-borda)*m*1.6,0,0.35)[...,None]; foto=foto*(1-wrap)+img*wrap
out=foto*m[...,None]+img*(1-m[...,None]); out+=rng.normal(0,3.2,out.shape).astype(np.float32)
res=Image.fromarray(np.clip(out,0,255).astype(np.uint8)); res.save(f'{R}/JOAO-parede-verde-menta-v2.jpg',quality=93)
h=900; a=orig.resize((int(W*h/H),h)); b=res.resize(a.size); c=Image.new('RGB',(a.width*2+10,h),'white'); c.paste(a,(0,0)); c.paste(b,(a.width+10,0)); c.save(f'{D}/comparar5.jpg',quality=85)
res.crop((0,0,W,700)).resize((W//2,350)).save(f'{D}/detalhe.jpg')
