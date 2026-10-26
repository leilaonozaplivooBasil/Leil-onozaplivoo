# Trilha original (feita aqui, sem direito autoral de terceiros): pop leve e otimista, 96 bpm, C–G–Am–F.
import numpy as np, wave
SR=44100; BPM=96; BEAT=60/BPM; DUR=94
t_total=int(SR*DUR); mix=np.zeros(t_total)
def nota(f): return 440*2**((f-69)/12)
def env(n, a=0.01, r=0.3):
    e=np.ones(n); A=int(a*SR); R=min(int(r*SR), n)
    e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
def tocar(ini, dur, midi, vol, timbre):
    i=int(ini*SR); n=int(dur*SR)
    if i>=t_total: return
    n=min(n,t_total-i); t=np.arange(n)/SR; f=nota(midi)
    if timbre=='pad': s=(np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*2.003*t)+0.25*np.sin(2*np.pi*f*0.998*t)); s*=env(n,0.4,0.8)
    elif timbre=='ep': s=(np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*f*3*t)*np.exp(-t*6))*np.exp(-t*2.5)*env(n,0.005,0.1)
    elif timbre=='baixo': s=np.sin(2*np.pi*f*t)*np.exp(-t*1.5)*env(n,0.01,0.1)
    mix[i:i+n]+=vol*s
acordes=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]]  # C G Am F
baixos=[36,43,45,41]
compasso=4*BEAT; c=0; tt=0.0
while tt<DUR:
    a=acordes[c%4]
    for m in a: tocar(tt, compasso*1.05, m, 0.05, 'pad')
    tocar(tt, compasso, baixos[c%4], 0.18, 'baixo'); tocar(tt+2*BEAT, 2*BEAT, baixos[c%4], 0.12, 'baixo')
    arp=[a[0]+12,a[1]+12,a[2]+12,a[1]+12]
    for k in range(8):
        if tt>6: tocar(tt+k*BEAT/2, BEAT, arp[k%4], 0.06, 'ep')
    # batida leve: bumbo no 1 e 3, chocalho nos contratempos
    if tt>12:
        for b in (0,2):
            i=int((tt+b*BEAT)*SR); n=int(0.25*SR)
            if i+n<t_total: tk=np.arange(n)/SR; mix[i:i+n]+=0.22*np.sin(2*np.pi*(55+70*np.exp(-tk*30))*tk)*np.exp(-tk*12)
        for b in range(8):
            i=int((tt+b*BEAT/2+BEAT/4)*SR); n=int(0.05*SR)
            if i+n<t_total: mix[i:i+n]+=0.025*np.random.randn(n)*np.exp(-np.arange(n)/SR*90)
    c+=1; tt+=compasso
# eco suave
d=int(0.28*SR); eco=np.zeros_like(mix); eco[d:]=mix[:-d]*0.25; mix+=eco
fade=int(3*SR); mix[-fade:]*=np.linspace(1,0,fade); mix[:int(1.5*SR)]*=np.linspace(0,1,int(1.5*SR))
mix/=np.max(np.abs(mix))*1.1
st=np.stack([mix, np.roll(mix,180)],1)
with wave.open('trilha.wav','w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
