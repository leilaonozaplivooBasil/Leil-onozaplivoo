# Batida de funk (tamborzão) sintetizada do zero — sem direito autoral. Uso: batida_funk.py <saida.wav> <segundos> [bpm]
import sys, numpy as np, wave
out, dur = sys.argv[1], float(sys.argv[2]); bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 130
SR = 48000; n = int(dur*SR); mix = np.zeros(n)
st = 60/bpm/4  # semicolcheia
def kick(a=1.0):
    t = np.arange(int(0.32*SR))/SR; f = 45 + 110*np.exp(-t*28); ph = 2*np.pi*np.cumsum(f)/SR
    return a*np.sin(ph)*np.exp(-t*9) + a*0.35*np.random.default_rng(1).normal(0, 1, len(t))*np.exp(-t*220)
def clap(a=0.6):
    t = np.arange(int(0.18*SR))/SR; r = np.random.default_rng(2).normal(0, 1, len(t))
    env = sum(np.exp(-np.clip(t-d, 0, None)*60)*(t >= d) for d in (0, 0.008, 0.016)); r = np.convolve(r, [1, -0.6], 'same')
    return a*r*env*0.5
def hat(a=0.18):
    t = np.arange(int(0.05*SR))/SR; r = np.random.default_rng(3).normal(0, 1, len(t)); r = np.diff(np.concatenate([[0], r]))
    return a*r*np.exp(-t*90)
def tom(a=0.5, f0=180):
    t = np.arange(int(0.16*SR))/SR; f = f0*(1+0.6*np.exp(-t*30)); return a*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*18)
def poe(s, t):
    i = int(t*SR)
    if i < n: m = min(len(s), n-i); mix[i:i+m] += s[:m]
# padrão de 1 compasso (16 semicolcheias): tum..tum..tum.tum..tum. (tamborzão) + palma no 2 e no 4
K = [0, 3, 6, 10, 13]; C = [4, 12]; T = [7, 15]
compasso = 16*st; c = 0
while c*compasso < dur:
    b0 = c*compasso
    for s in K: poe(kick(1.0 if s in (0, 10) else 0.8), b0 + s*st)
    for s in C: poe(clap(), b0 + s*st)
    for s in T: poe(tom(0.45, 200 if s == 7 else 160), b0 + s*st)
    for s in range(0, 16, 2): poe(hat(0.16 if s % 4 else 0.22), b0 + s*st)
    c += 1
mix = np.tanh(mix*1.4)/np.tanh(1.4); mix /= max(1e-9, np.abs(mix).max()); mix *= 0.9
pcm = (np.stack([mix, mix], 1)*32767).astype('<i2')
with wave.open(out, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', bpm)
