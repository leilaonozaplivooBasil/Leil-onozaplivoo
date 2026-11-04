from PIL import Image,ImageDraw,ImageFont
W,H=1080,1920
im=Image.open('FUNDO-enquete-verde.png').convert('RGBA')
# tira a faixa dourada de baixo do fundo base: refaz o fundo sem ela
import numpy as np
base=np.array(im); base[1680:1800]=base[1560:1680]; im=Image.fromarray(base)
d=ImageDraw.Draw(im)
B='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; F=lambda s:ImageFont.truetype(B,s)
def ctext(y,t,f,fill):
  w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
ctext(330,'RESULTADO DA ENQUETE',F(40),(245,196,81))
ctext(395,'Vocês escolheram',F(84),(255,255,255))
# cartão
x0,x1=90,990; d.rounded_rectangle((x0,540,x1,1170),48,fill=(255,255,255))
q=F(38); d.text((x0+50,585),'Qual desses você queria ver',font=q,fill=(10,20,16)); d.text((x0+50,632),'no próximo leilão?',font=q,fill=(10,20,16))
opts=[('iPhone',100),('PS5',0),('MacBook',0)]
for i,(o,p) in enumerate(opts):
  y=730+i*140; d.rounded_rectangle((x0+40,y,x1-40,y+110),55,fill=(232,239,234))
  if p: d.rounded_rectangle((x0+40,y,x1-40,y+110),55,fill=(27,122,72))
  c=(255,255,255) if p else (60,70,64)
  d.text((x0+85,y+28),o,font=F(50),fill=c)
  t=f'{p}%'; w=d.textlength(t,font=F(54)); d.text((x1-85-w,y+25),t,font=F(54),fill=c)
# chamada
ctext(1235,'Pedido feito,',F(64),(255,255,255))
ctext(1310,'pedido atendido:',F(64),(255,255,255))
t='SÁBADO TEM iPHONE 17 PRO MAX'; f=F(50); w=d.textlength(t,font=f)
d.rounded_rectangle(((W-w)/2-34,1410,(W+w)/2+34,1510),50,fill=(245,196,81)); d.text(((W-w)/2,1428),t,font=f,fill=(10,20,16))
ctext(1560,'às 20h  ·  veja no próximo story  →',F(40),(220,235,226))
im.convert('RGB').save('STORY-resultado-enquete.png')
