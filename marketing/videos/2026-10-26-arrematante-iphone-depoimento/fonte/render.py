# Edição do Reels do arrematante: zoom nas ênfases, transições sutis, legenda no fundinho verde com animação, logo PNG.
import subprocess, numpy as np, cv2, math, re
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
DUR=90.47
FONTE='/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
VERDE=(63,208,126); NOITE=(0,24,13)

LEG=[
(0.00,1.74,"Eu estou aqui com o Mu•••,"),(1.78,3.60,"o [arrematante] do iPhone"),(3.72,5.85,"do nosso leilão do sábado."),
(5.94,8.40,"Então, está aqui: esse é o iPhone."),(9.40,11.45,"Então, pra gente fazer algumas perguntinhas:"),
(11.50,13.10,"como que foi no começo?"),(13.14,15.30,"Ficou desconfiado? Teve medo do leilão?"),(16.20,16.95,"Conta pra nós."),
(17.04,19.80,"No início, eu fiquei um pouco [desconfiado],"),(19.82,21.74,"porque é uma quantia alta"),(21.76,23.22,"pra gente colocar na carteira."),
(23.24,26.40,"Aí eu fiquei meio desconfiado,"),(26.42,27.95,"mas depois, quando eu vi todo mundo"),(28.00,29.15,"dando lance, dando lance,"),
(29.18,30.20,"eu fiquei indo pra trás."),(30.24,31.85,"Falei: não, vou ter que ir [com tudo]."),(31.94,34.10,"E qual foi a sensação durante o leilão,"),
(34.14,36.70,"que você sentiu ali, dando lance?"),(36.80,38.44,"Vou te confessar:"),(38.46,39.98,"eu nunca fiquei tão [nervoso],"),
(40.00,41.85,"porque eu estava suando em todo momento,"),(41.90,43.60,"[suando, suando, suando.]"),(43.74,45.24,"Aí tinha um camarada lá dando mais lance,"),
(45.26,47.90,"eu falei: vou pegar ele agora, no lance."),(48.44,49.70,"Aí deixei por último."),(49.72,50.66,"Quando deixei por último,"),
(50.68,52.10,"eu fui e dei o [último lance]."),(52.16,54.10,"Aí falei: agora é meu, agora é meu,"),(54.12,56.55,"cruzando os dedos, cruzando os dedos,"),
(56.62,57.40,"daqui a pouco:"),(57.42,58.10,"dou-lhe uma,"),(58.10,58.60,"dou-lhe duas,"),(58.60,59.35,"dou-lhe três..."),
(59.40,61.40,"[ARREMATADO! ARREMATADO!]"),(61.98,64.10,"Só não vou abrir, pessoal, porque é presente."),(64.36,66.98,"De repente, quando eu chegar em casa,"),
(67.00,69.36,"faço um videozinho, gravo e mando pra vocês."),(69.42,72.30,"Já tô indicando o [Leilão No Zap] pros meus amigos,"),
(72.32,75.45,"porque isso daqui foi [surreal, surreal]."),(75.50,77.02,"O preço que eu paguei no [Leilão No Zap]"),(77.04,78.50,"foi [surreal] mesmo, bem bacana."),
(78.58,79.78,"E aí, tá tudo certinho, né?"),(79.80,81.70,"Tudo certinho, tudo [lacrado]."),(81.84,83.95,"Tudo [lacrado], gente, tudo certinho."),
(84.98,86.40,"E foi o [17 Pro Max]!"),(86.70,87.90,"Show de bola. É isso."),(88.60,89.70,"Obrigada!"),
]
# zoom nas ênfases: (instante, força). ARREMATADO ganha tremida.
import json
ZOOM=[(z[0],z[1],z[2],z[3]) for z in json.load(open('zooms.json'))]  # (instante, força, x, y do rosto de quem fala)
TRANS=[9.40,31.94,61.98,78.58]   # mudança de assunto: pulso + clarão leve
TREME=(59.4,0.7)

fb=ImageFont.truetype(FONTE,58)
def pilula(texto):
    # quebra em até 2 linhas de ~860 px; [..] = ênfase (texto verde dentro de um bloco escuro)
    texto=re.sub(r'\]([,.!?:]+)',r'\1]',texto)   # a pontuação depois da ênfase entra no bloco
    partes=re.split(r'(\[[^\]]+\])',texto); tokens=[]
    d=ImageDraw.Draw(Image.new('RGB',(10,10)))
    for p in partes:
        if not p: continue
        if p.startswith('['):
            frase=p.strip('[]')
            if d.textlength(frase,font=fb)+18<=860: tokens.append((frase,True))   # a ênfase fica num bloco só
            else: tokens+=[(w,True) for w in frase.split(' ') if w]
        else:
            tokens+=[(w,False) for w in p.split(' ') if w]
    esp=d.textlength(' ',font=fb); linhas=[[]]; larg=0
    for w,e in tokens:
        lw=d.textlength(w,font=fb)+(18 if e else 0)
        if linhas[-1] and larg+esp+lw>860: linhas.append([]); larg=0
        linhas[-1].append((w,e,lw)); larg+=(esp if larg else 0)+lw
    lh=76; padx,pady=34,18
    wl=[sum(t[2] for t in l)+esp*(len(l)-1) for l in linhas]
    bw=int(max(wl)+2*padx); bh=int(lh*len(linhas)+2*pady)
    im=Image.new('RGBA',(bw+20,bh+20),(0,0,0,0)); dr=ImageDraw.Draw(im)
    dr.rounded_rectangle((10+3,10+6,10+bw+3,10+bh+6),radius=34,fill=(0,0,0,70))   # sombra
    dr.rounded_rectangle((10,10,10+bw,10+bh),radius=34,fill=VERDE+(245,))
    y=10+pady
    for l,wli in zip(linhas,wl):
        x=10+(bw-wli)/2
        for w,e,lw in l:
            if e:
                dr.rounded_rectangle((x,y+4,x+lw,y+lh-4),radius=14,fill=NOITE+(255,))
                dr.text((x+9,y+lh/2),w,font=fb,fill=(255,224,138,255),anchor='lm')
            else:
                dr.text((x,y+lh/2),w,font=fb,fill=NOITE+(255,),anchor='lm')
            x+=lw+esp
        y+=lh
    return np.array(im)
PIL_LEG=[(a,b,pilula(t)) for a,b,t in LEG]
topo1=np.array(Image.open('topo1.png').convert('RGBA')); topo2=np.array(Image.open('topo2.png').convert('RGBA'))

def ease(x): return 1-(1-x)**3
def zoom_em(t):
    z=0.0; c=(540,880)
    for t0,a,x,y in ZOOM:
        dt=t-t0
        if -0.05<dt<1.9:
            if dt<0.22: k=ease(max(0,dt)/0.22)
            elif dt<1.3: k=1
            else: k=1-ease((dt-1.3)/0.6)
            if a*k>z: z=a*k; c=(x,y)
    for t0 in TRANS:
        dt=t-t0
        if 0<=dt<0.32 and 0.07*math.sin(math.pi*dt/0.32)>z: z=0.07*math.sin(math.pi*dt/0.32); c=(540,880)
    return 1+z, c
def flash(t):
    for t0 in TRANS:
        dt=t-t0
        if 0<=dt<0.28: return 0.22*(1-dt/0.28)
    if 0<=t-59.4<0.18: return 0.45*(1-(t-59.4)/0.18)
    return 0.0
def compor(fr,ov,x,y,alpha=1.0):
    h,w=ov.shape[:2]; x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    o=ov[y0-y:y1-y,x0-x:x1-x].astype(np.float32); a=o[...,3:4]/255.0*alpha
    reg=fr[y0:y1,x0:x1].astype(np.float32); fr[y0:y1,x0:x1]=(reg*(1-a)+o[...,:3]*a).astype(np.uint8)

dec=subprocess.Popen(['ffmpeg','-v','error','-i','../video.mp4','-an','-vf','scale=1080:1920,fps=30','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','video-sem-som.mp4'],stdin=subprocess.PIPE)
i=0; tam=W*H*3
while True:
    buf=dec.stdout.read(tam)
    if len(buf)<tam: break
    t=i/FPS; fr=np.frombuffer(buf,np.uint8).reshape(H,W,3)
    z,(cx,cy)=zoom_em(t); sx=sy=0.0
    if TREME[0]<=t<TREME[0]+TREME[1]:
        k=1-(t-TREME[0])/TREME[1]; sx=9*k*math.sin(t*95); sy=7*k*math.cos(t*80)
    if z!=1 or sx or sy:
        # zoom no rosto de quem fala, puxando o rosto para o meio da tela sem mostrar borda
        tx=min(max(540-cx,-(z-1)*(W-cx)),(z-1)*cx); ty=min(max(900-cy,-(z-1)*(H-cy)),(z-1)*cy)
        M=np.array([[z,0,cx-z*cx+tx+sx],[0,z,cy-z*cy+ty+sy]],np.float32)
        fr=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    else: fr=fr.copy()
    fl=flash(t)
    if fl: fr=(fr.astype(np.float32)*(1-fl)+255*fl).astype(np.uint8)
    compor(fr, topo1 if t<8.4 else topo2, 0, 0)
    for a,b,img in PIL_LEG:
        if a<=t<b:
            dt=t-a; s=1.0
            if dt<0.16: s=0.82+0.18*ease(dt/0.16)+0.04*math.sin(math.pi*dt/0.16)
            al=min(1.0,dt/0.08, (b-t)/0.08 if b-t<0.08 else 1.0)
            im=img if s==1.0 else cv2.resize(img,(int(img.shape[1]*s),int(img.shape[0]*s)),interpolation=cv2.INTER_LINEAR)
            compor(fr,im,(W-im.shape[1])//2,1440-im.shape[0]//2,al)
            break
    enc.stdin.write(fr.tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('quadros',i)
