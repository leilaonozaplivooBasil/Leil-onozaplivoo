from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/iphone2'; R='/home/user/Leil-onozaplivoo/marketing/videos/2026-11-07-iphone-17-pro-max'
F=lambda p,t: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf'%p,t)
W,H=1080,1920; OURO=(245,196,81); VERDE=(27,122,72)
im=Image.open(f'{S}/base-capa.png').convert('RGBA')
g=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(g)
for y in range(950,H): d.line((0,y,W,y),fill=(0,0,0,int(200*min(1,(y-950)/550))))
im=Image.alpha_composite(im,g); d=ImageDraw.Draw(im)
def cont(xy,t,f,cor,w=6):
    for dx in range(-w,w+1,3):
        for dy in range(-w,w+1,3): d.text((xy[0]+dx,xy[1]+dy),t,font=f,fill=(0,0,0,200),anchor='mm')
    d.text(xy,t,font=f,fill=cor,anchor='mm')
f=F('ExtraBold',44); t='SÉRIE · EP. 01'; w=d.textlength(t,font=f)
d.rounded_rectangle((W/2-w/2-34,1115,W/2+w/2+34,1195),40,fill=VERDE+(255,)); d.text((W/2,1155),t,font=f,fill=(255,255,255),anchor='mm')
cont((W/2,1285),'JÁ ENCONTROU',F('Black',118),(255,255,255,255))
cont((W/2,1420),'O DONO',F('Black',150),OURO+(255,))
d.text((W/2,1540),'iPhone 17 Pro Max',font=F('Bold',50),fill=(255,255,255),anchor='mm')
lg=Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((260,95))
pill=Image.new('RGBA',(W,H),(0,0,0,0)); dp=ImageDraw.Draw(pill); dp.rounded_rectangle((W/2-lg.width/2-22,300-14,W/2+lg.width/2+22,300+lg.height+14),28,fill=(10,20,16,170)); im=Image.alpha_composite(im,pill); im.alpha_composite(lg,(int(W/2-lg.width/2),300))
im.convert('RGB').save(f'{R}/CAPA-ja-encontrou-o-dono-ep01.jpg',quality=94)
im.convert('RGB').crop((0,285,1080,1635)).resize((360,450)).save(f'{S}/capa-grade.jpg',quality=90)
