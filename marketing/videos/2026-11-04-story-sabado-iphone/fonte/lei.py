# Leiloeiro entra andando pela direita e fala; legendas da fala dele no padrão da marca. Gera uma camada com transparência.
import math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S='/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/story-enquete'; MK='/home/user/Leil-onozaplivoo/marketing'
F=lambda p,t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'%p,t)
W,H,FPS=1080,1920,30; VERDE=(27,122,72); OURO=(245,196,81)
T0=6.0; TV=6.5; TOTAL=13.4
LEI=Image.open(f'{MK}/marca/leiloeiro-aponta-moeda-recorte.png').convert('RGBA'); bb=LEI.split()[3].getbbox(); LEI=LEI.crop(bb); LEI.thumbnail((720,820))
sh=Image.new('RGBA',(LEI.width+120,90),(0,0,0,0)); ImageDraw.Draw(sh).ellipse((20,20,LEI.width+100,70),fill=(0,0,0,110)); SH=sh.filter(ImageFilter.GaussianBlur(14))
FALAS=[(0.03,0.85,'É isso aí!',None),(0.89,2.23,'Sábado às','20h'),(2.25,4.05,'tem iPhone','17 Pro Max'),(4.09,5.3,'Quem dá','mais?')]
def leg(d,txt,dest,y=1330,cx=380):
    f=F('Black',58); fd=F('Black',68); w=d.textlength(txt,font=f); x0=cx-w/2-34
    d.rounded_rectangle((x0,y-46,x0+w+68,y+46),46,fill=VERDE+(245,)); d.text((cx,y),txt,font=f,fill=(255,255,255),anchor='mm')
    if dest:
        t=dest.upper(); w=d.textlength(t,font=fd); x0=cx-w/2-38; y+=104; d.rounded_rectangle((x0,y-50,x0+w+76,y+50),50,fill=OURO+(255,)); d.text((cx,y),t,font=fd,fill=(10,60,32),anchor='mm')
ease=lambda x: 1-(1-max(0,min(1,x)))**3
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','qtrle',f'{S}/camada-lei.mov'],stdin=subprocess.PIPE)
for n in range(int(TOTAL*FPS)):
    t=n/FPS; im=Image.new('RGBA',(W,H),(0,0,0,0))
    if t>=T0:
        k=ease((t-T0)/0.9); x=int(W+40-(W+40-(W-LEI.width+60))*k)   # anda da borda direita até o canto
        andando=(t-T0)<0.9
        bob=abs(math.sin((t-T0)*11))*22 if andando else abs(math.sin((t-T0)*3.2))*6
        if TV+4.09<=t<=TV+4.6: bob+=math.sin((t-TV-4.09)/0.51*math.pi)*28   # pulinho no "quem dá mais?"
        ang=math.sin((t-T0)*11)*3.5 if andando else math.sin((t-T0)*2.4)*1.2
        L=LEI.rotate(ang,resample=Image.BICUBIC,expand=True)
        y=int(H-L.height-30-bob)
        im.alpha_composite(SH,(x-60+ (L.width-LEI.width)//2, H-110))
        im.alpha_composite(L,(x,y))
        d=ImageDraw.Draw(im)
        for a,b,txt,dest in FALAS:
            if TV+a<=t<TV+b+0.15: leg(d,txt,dest)
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print('ok camada')
