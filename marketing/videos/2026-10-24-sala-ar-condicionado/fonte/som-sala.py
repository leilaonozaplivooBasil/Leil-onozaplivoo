import numpy as np, wave, json, sys
pasta=sys.argv[1]
SR=44100; FPS=30; DUR=30.0; N=int(SR*DUR); a=np.zeros(N); rng=np.random.default_rng(3)
marcas=json.load(open(f'{pasta}/marcas.json'))
def put(sig,t,g=1.0):
    i=int(t*SR)
    if i>=N: return
    e=min(N,i+len(sig)); a[i:e]+=sig[:e-i]*g
tt=lambda d: np.arange(int(d*SR))/SR
def kick(): s=tt(0.3); return np.sin(2*np.pi*(50+80*np.exp(-s*20))*s)*np.exp(-s*10)
def hat(): n=rng.standard_normal(int(0.05*SR)); return np.diff(n,prepend=0)*np.exp(-tt(0.05)*70)
def batida(de,ate,bpm,g):
    t=de; b=60/bpm
    while t<ate: put(kick(),t,0.5*g); put(hat(),t+b/2,0.10*g); t+=b
batida(2.5,8,110,0.8); batida(8,18,128,1.0); batida(18,25.7,150,1.1)
for de,ate,f,g in [(0,8,55,0.10),(8,18,61.7,0.12),(18,25.7,73.4,0.14)]:
    s=tt(ate-de); env=np.minimum(1,s*2)*np.minimum(1,(ate-de-s)*4)
    put((np.sin(2*np.pi*f*s)+0.5*np.sin(2*np.pi*2*f*s)+0.25*np.sin(2*np.pi*3*f*s))*env,de,g)
t=18.0
while t<25.7: put(np.sin(2*np.pi*2400*tt(0.03))*np.exp(-tt(0.03)*120), t, 0.25); t+=0.5
def ding(f=1568): s=tt(0.5); return (np.sin(2*np.pi*f*s)+0.4*np.sin(2*np.pi*2*f*s))*np.exp(-s*7)
def riser(): s=tt(0.45); f=600+1400*s/0.45; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*s/0.45)
for m in marcas:
    t=m['q']/FPS
    if m['tipo']=='lance': put(ding(1568 if t<8 else 1760),t,0.35)
    else: put(riser(),t,0.22)
def whoosh(d=0.5):
    n=rng.standard_normal(int(d*SR)); s=tt(d); n=np.convolve(n,np.ones(30)/30,'same'); return n*np.sin(np.pi*s/d)**2
for t in [2.45,7.95,17.95]: put(whoosh(),t,1.2)
s=tt(0.6); martelo=(rng.standard_normal(len(s))*np.exp(-s*40)*0.6+np.sin(2*np.pi*90*s)*np.exp(-s*12))
put(martelo,25.7,1.0); put(martelo,25.95,0.7)
s=tt(3.0); acorde=sum(np.sin(2*np.pi*f*s) for f in [523.25,659.25,783.99,1046.5])*np.exp(-s*1.2)*np.minimum(1,s*20)
put(acorde,27.0,0.25)
fade=np.ones(N); fade[-int(1.2*SR):]=np.linspace(1,0,int(1.2*SR)); a*=fade
a=a/np.max(np.abs(a))*0.88
pcm=(np.stack([a,a],1)*32767).astype('<i2')
with wave.open(f'{pasta}/som.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
