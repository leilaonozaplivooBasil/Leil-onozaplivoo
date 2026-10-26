# Trilha ORIGINAL que acompanha a história do vídeo (feita aqui, sem direito de terceiros), 96 bpm:
#  0–17s calma | 17–36s ganha corpo | 36–57,4s suspense (menor, coração) | 57,4–59,3 relógio + subida, silêncio
#  59,4s IMPACTO e comemoração | 75–90,5s final leve com fade.
import numpy as np, wave
SR=44100; DUR=90.6; N=int(SR*DUR); mix=np.zeros(N); BEAT=60/96
def f(m): return 440*2**((m-69)/12)
def env(n,a,r):
    e=np.ones(n); A=max(1,int(a*SR)); R=max(1,min(int(r*SR),n)); e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
def add(t0,dur,sig):
    i=int(t0*SR); n=min(len(sig),N-i)
    if n>0 and i>=0: mix[i:i+n]+=sig[:n]
def pad(m,dur,v,bright=0.5):
    n=int(dur*SR); t=np.arange(n)/SR; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+bright*np.sin(2*np.pi*fr*2.003*t)+0.3*np.sin(2*np.pi*fr*0.997*t); return v*s*env(n,0.35,0.7)
def ep(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; fr=f(m)
    return v*(np.sin(2*np.pi*fr*t)+0.3*np.sin(2*np.pi*fr*3*t)*np.exp(-t*6))*np.exp(-t*2.6)*env(n,0.005,0.08)
def baixo(m,dur,v):
    n=int(dur*SR); t=np.arange(n)/SR; return v*np.sin(2*np.pi*f(m)*t)*np.exp(-t*1.4)*env(n,0.01,0.08)
def bumbo(v):
    n=int(0.3*SR); t=np.arange(n)/SR; return v*np.sin(2*np.pi*(50+80*np.exp(-t*28))*t)*np.exp(-t*10)
def chocalho(v):
    n=int(0.05*SR); return v*np.random.randn(n)*np.exp(-np.arange(n)/SR*90)
def palma(v):
    n=int(0.12*SR); t=np.arange(n)/SR; return v*np.random.randn(n)*np.exp(-t*30)
MAIOR=[([60,64,67],36),([55,59,62],43),([57,60,64],45),([53,57,60],41)]
MENOR=[([57,60,64],45),([53,57,60],41),([50,53,57],38),([52,56,59],40)]
def secao(t0,t1,acordes,arp=True,bat=0,vpad=0.05,bright=0.5,velarp=0.06):
    c=0; t=t0; comp=4*BEAT
    while t<t1:
        a,b=acordes[c%4]; d=min(comp,t1-t)
        for m in a: add(t,d*1.05,pad(m,d*1.05,vpad,bright))
        if bat>=1: add(t,d,baixo(b,d,0.17))
        if arp:
            for k in range(8):
                if t+k*BEAT/2<t1: add(t+k*BEAT/2,BEAT,ep([a[0]+12,a[1]+12,a[2]+12,a[1]+12][k%4],BEAT,velarp))
        if bat>=1:
            for x in (0,2):
                if t+x*BEAT<t1: add(t+x*BEAT,0.3,bumbo(0.2))
        if bat>=2:
            for x in range(8):
                if t+x*BEAT/2+BEAT/4<t1: add(t+x*BEAT/2+BEAT/4,0.05,chocalho(0.03))
            for x in (1,3):
                if t+x*BEAT<t1: add(t+x*BEAT,0.12,palma(0.06))
        c+=1; t+=comp
secao(0,17,MAIOR,arp=True,bat=0,vpad=0.045)
secao(17,36,MAIOR,arp=True,bat=1,vpad=0.05)
# suspense: menor, sem arpejo alegre, batida de coração
secao(36,57.4,MENOR,arp=False,bat=0,vpad=0.055,bright=0.2)
t=36.0
while t<57.4:
    add(t,0.3,bumbo(0.16)); add(t+0.22,0.3,bumbo(0.11)); t+=0.95
# relógio acelerando + subida de ruído até o silêncio
t=57.42; passo=0.5
while t<59.2:
    n=int(0.03*SR); tk=np.arange(n)/SR; add(t,0.03,0.12*np.sin(2*np.pi*2400*tk)*np.exp(-tk*160)); t+=passo; passo=max(0.12,passo*0.8)
n=int(1.9*SR); tr=np.arange(n)/SR; add(57.4,1.9,0.06*np.random.randn(n)*(tr/1.9)**2)
mix[int(59.25*SR):int(59.4*SR)]*=0.0
# IMPACTO + comemoração
n=int(1.2*SR); ti=np.arange(n)/SR; add(59.4,1.2,0.35*np.sin(2*np.pi*(40+60*np.exp(-ti*8))*ti)*np.exp(-ti*3))
secao(59.4,75,MAIOR,arp=True,bat=2,vpad=0.05,bright=0.7,velarp=0.07)
secao(75,90.6,MAIOR,arp=True,bat=1,vpad=0.045)
d=int(0.28*SR); eco=np.zeros_like(mix); eco[d:]=mix[:-d]*0.22; mix+=eco
mix[:int(1.2*SR)]*=np.linspace(0,1,int(1.2*SR)); fd=int(2.5*SR); mix[-fd:]*=np.linspace(1,0,fd)
mix/=np.max(np.abs(mix))*1.1
st=np.stack([mix,np.roll(mix,160)],1)
with wave.open('trilha2.wav','w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
