import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D, O = sys.argv[1], sys.argv[2]; MK='/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W,H=1080,1920; OURO=(245,196,81); FOGO=(243,91,18); BR=(255,255,255); NOITE=(10,20,16); VERDE=(27,122,72)
PROB=[]
bg=Image.open(f'{D}/capa/b31.5.jpg').convert('RGB').resize((W,H))
im=bg.convert('RGBA')
# degradê escuro embaixo (floresta → noite)
g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for y in range(1000,H):
    a=min(235,int((y-1000)/420*235)); gd.line([(0,y),(W,y)],fill=(8,30,20,a))
im=Image.alpha_composite(im,g); d=ImageDraw.Draw(im)
# logo (dentro da área segura 3:4: y 240–1680)
lg=Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280,104))
d.rounded_rectangle((40,262,80+lg.width,290+lg.height),30,fill=NOITE+(160,)); im.alpha_composite(lg,(60,276))
# iPhone real à direita
ip=Image.open(f'{MK}/semana-2026-10-28/fonte/iphone17pm-recorte.png').convert('RGBA'); ip.thumbnail((330,520))
sh=Image.new('RGBA',(W,H),(0,0,0,0)); sx,sy=W-ip.width-30,1660-ip.height
glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse((sx-40,sy+80,sx+ip.width+40,sy+ip.height+40),fill=OURO+(90,))
im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(60)))
im.alpha_composite(ip,(sx,sy)); d=ImageDraw.Draw(im)
LIM=sx-10
def txt(xy,t,f,cor,anchor='ls'):
    b=d.textbbox(xy,t,font=f,anchor=anchor)
    if b[2]>LIM or b[3]>1680 or b[1]<240: PROB.append(f'"{t}" fora {b}')
    d.text(xy,t,font=f,fill=cor,anchor=anchor)
# chip
f=F('Black',38); t='LEILÃO AO VIVO'; w=d.textlength(t,font=f)
d.rounded_rectangle((60,1150,60+w+60,1216),33,fill=FOGO); d.ellipse((84,1172,106,1194),fill=BR); d.text((118+ (w+60-58)/2-6,1183),t,font=f,fill=BR,anchor='mm')
txt((56,1350),'HOJE',F('Black',150),BR)
txt((56,1500),'ÀS 20H',F('Black',150),OURO)
txt((62,1572),'iPhone 17 Pro Max · lacrado',F('Bold',44),BR)
txt((62,1640),'o martelo bate hoje à noite',F('Bold',38),(200,230,210))
im.convert('RGB').save(f'{O}/CAPA-emanuel-natalia-iphone-20h.jpg',quality=95)
# prévia de como fica no grid (corte 3:4)
im.convert('RGB').crop((0,240,1080,1680)).resize((540,720)).save(f'{D}/capa/grid.jpg')
if PROB: print(PROB); sys.exit(1)
print('ok')
