from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np
W,H=1080,1920
y,x=np.mgrid[0:H,0:W].astype(float)
a=np.array([13,59,36]);b=np.array([27,122,72]);d=np.array([10,20,16])
t=np.clip((x/W*0.35+ (1-y/H)*0.65),0,1)[...,None]
img=d*(1-t)**1.6+ (a*(1-t)+b*t)*(1-(1-t)**1.6)
g=np.exp(-(((x-W*0.8)/700)**2+((y-H*0.12)/600)**2))[...,None]
img=img+np.array([60,140,90])*0.35*g
img=img+np.random.default_rng(1).normal(0,2.2,(H,W,1))
im=Image.fromarray(np.clip(img,0,255).astype('uint8'))
dr=ImageDraw.Draw(im)
lg=Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA')
lg.thumbnail((360,140)); im.paste(lg,((W-lg.width)//2,130),lg)
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf',44)
txt='O PRÓXIMO LEILÃO É VOCÊ QUEM ESCOLHE'
w=dr.textlength(txt,font=f); dr.rounded_rectangle(((W-w)/2-28,1700,(W+w)/2+28,1786),43,fill=(245,196,81))
dr.text(((W-w)/2,1716),txt,font=f,fill=(10,20,16))
im.save('FUNDO-enquete-verde.png')
# prévia: vídeo + enquete onde vão ficar
p=im.copy().convert('RGBA'); pd=ImageDraw.Draw(p)
fr=Image.open('quadro.png').convert('RGB').resize((640,1138))
m=Image.new('L',fr.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0)+fr.size,36,fill=255)
p.paste(fr,(80,330),m)
pd.rounded_rectangle((500,1180,1010,1640),40,fill=(255,255,255,235))
pd.rounded_rectangle((500,1180,1010,1300),40,fill=(18,18,18,255));pd.rectangle((500,1260,1010,1300),fill=(18,18,18,255))
f2=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',30)
pd.text((530,1205),'QUAL DESSES VOCÊ QUERIA\nVER NO PRÓXIMO LEILÃO?',font=f2,fill='white')
for i,o in enumerate(['iPhone','PS5','MacBook']):
  yy=1325+i*100; pd.rounded_rectangle((530,yy,980,yy+80),30,fill=(235,238,240)); pd.text((560,yy+22),o,font=f2,fill=(20,20,20))
p.convert('RGB').save('PREVIA-enquete.jpg',quality=90)
