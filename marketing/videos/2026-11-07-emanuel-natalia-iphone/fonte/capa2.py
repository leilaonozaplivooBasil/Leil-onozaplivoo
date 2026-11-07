# Capa v2: foto escolhida pela Natália (32,9 s), pessoas livres, texto em cima
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D, O = sys.argv[1], sys.argv[2]; MK='/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W,H=1080,1920; OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); NOITE=(10,20,16)
PROB=[]
im=Image.open(f'{D}/capa/full.jpg').convert('RGBA')
g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for y in range(0,900):  # fundo escuro até 760, some até 900
    a=int(240*max(0,min(1,(900-y)/140))) if y>760 else 240
    gd.line([(0,y),(W,y)],fill=(8,30,20,a))
im=Image.alpha_composite(im,g); d=ImageDraw.Draw(im)
lg=Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((250,94))
im.alpha_composite(lg,(56,268)); d=ImageDraw.Draw(im)
ip=Image.open(f'{MK}/semana-2026-10-28/fonte/iphone17pm-recorte.png').convert('RGBA'); ip.thumbnail((260,400))
sx,sy=W-ip.width-50,276
glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse((sx-50,sy+40,sx+ip.width+50,sy+ip.height+30),fill=OURO+(110,))
im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(55))); im.alpha_composite(ip,(sx,sy)); d=ImageDraw.Draw(im)
LIM=sx-14
def txt(xy,t,f,cor):
    b=d.textbbox(xy,t,font=f,anchor='ls')
    if b[2]>LIM or b[1]<240: PROB.append(f'"{t}" fora {b}')
    d.text(xy,t,font=f,fill=cor,anchor='ls'); return b
f=F('Black',34); t='LEILÃO AO VIVO'; w=d.textlength(t,font=f)
d.rounded_rectangle((60,392,60+w+70,450),29,fill=FOGO); d.ellipse((80,411,100,431),fill=BR); d.text((112,421),t,font=f,fill=BR,anchor='lm')
txt((54,566),'HOJE',F('Black',128),BR)
b=txt((54,690),'ÀS 20H',F('Black',128),OURO)
b2=txt((60,748),'iPhone 17 Pro Max · lacrado',F('Bold',40),BR)
im.convert('RGB').save(f'{O}/CAPA-emanuel-natalia-iphone-20h.jpg',quality=95)
im.convert('RGB').crop((0,240,1080,1680)).resize((540,720)).save(f'{O}/PREVIA-capa-no-grid.jpg')
print('texto termina em y', b2[3], 'iPhone até', sy+ip.height)
if PROB: print(PROB); sys.exit(1)
print('ok')
