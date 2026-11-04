from PIL import Image, ImageDraw, ImageFont, ImageOps
S='/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/encontrou2'; D='/home/user/Leil-onozaplivoo/marketing/videos/2026-11-03-encontrou-dono'
F=lambda p,t: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf'%p,t)
W,H=1080,1920; OURO=(245,196,81); VERDE=(27,122,72)
im=Image.open(f'{S}/cap-1.2.png').convert('RGBA')
g=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(g)
for y in range(880,H): d.line((0,y,W,y),fill=(0,0,0,int(215*min(1,(y-880)/520))))
im=Image.alpha_composite(im,g); d=ImageDraw.Draw(im)
def cont(xy,t,f,cor,w=6):
    for dx in range(-w,w+1,3):
        for dy in range(-w,w+1,3): d.text((xy[0]+dx,xy[1]+dy),t,font=f,fill=(0,0,0,200),anchor='mm')
    d.text(xy,t,font=f,fill=cor,anchor='mm')
# 4 entregas reais em miniatura, como "figurinhas" da série
th=[]
for n in range(1,5):
    t=Image.open(f'{S}/th{n}.png').convert('RGB'); t=ImageOps.fit(t,(190,190),centering=(0.5,0.45))
    m=Image.new('L',(190,190),0); ImageDraw.Draw(m).rounded_rectangle((0,0,189,189),36,fill=255)
    c=Image.new('RGBA',(202,202),(255,255,255,255)); mm=Image.new('L',(202,202),0); ImageDraw.Draw(mm).rounded_rectangle((0,0,201,201),40,fill=255); c.putalpha(mm)
    c.paste(t,(6,6),m); th.append(c)
x0=(W-(4*202+3*22))//2
for i,c in enumerate(th): im.alpha_composite(c,(x0+i*224,1010))
d=ImageDraw.Draw(im)
f=F('ExtraBold',42); t='SÉRIE · EP. 01'; w=d.textlength(t,font=f)
d.rounded_rectangle((W/2-w/2-32,1250,W/2+w/2+32,1326),38,fill=VERDE+(255,)); d.text((W/2,1288),t,font=f,fill=(255,255,255),anchor='mm')
cont((W/2,1410),'JÁ ENCONTROU',F('Black',116),(255,255,255,255))
cont((W/2,1540),'O DONO',F('Black',146),OURO+(255,))
lg=Image.open('/home/user/Leil-onozaplivoo/marketing/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((260,95))
pill=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(pill).rounded_rectangle((W/2-lg.width/2-22,300-14,W/2+lg.width/2+22,300+lg.height+14),28,fill=(10,20,16,170)); im=Image.alpha_composite(im,pill); im.alpha_composite(lg,(int(W/2-lg.width/2),300))
im.convert('RGB').save(f'{D}/CAPA-ja-encontrou-o-dono-ep01.jpg',quality=94)
im.convert('RGB').crop((0,285,1080,1635)).resize((360,450)).save(f'{S}/capa-grade.jpg',quality=90)
