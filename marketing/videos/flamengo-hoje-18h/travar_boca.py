# Trava a boca do leiloeiro: cola em cada quadro a região bigode+boca do quadro 0
# (boca fechada), acompanhando o deslocamento da cabeça e a luz do quadro.
import subprocess, sys, numpy as np, cv2
src, dst = sys.argv[1], sys.argv[2]
W, H = 1072, 1928
probe = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip()
rd = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',probe,'-i','-','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p',dst],stdin=subprocess.PIPE)
def ler():
    b = rd.stdout.read(W*H*3)
    return None if len(b) < W*H*3 else np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
f0 = ler()
CX, CY, RX, RY = 555, 908, 128, 60           # elipse bigode + boca
X0, X1, Y0, Y1 = CX-RX-40, CX+RX+40, CY-RY-40, CY+RY+40
patch = f0[Y0:Y1, X0:X1].astype(np.float32)
mask = np.zeros((Y1-Y0, X1-X0), np.float32)
cv2.ellipse(mask, (CX-X0, CY-Y0), (RX, RY), 0, 0, 360, 1, -1)
mask = cv2.GaussianBlur(mask, (0,0), 14)[..., None]
anel = np.zeros_like(mask[...,0]); cv2.ellipse(anel,(CX-X0,CY-Y0),(RX+30,RY+30),0,0,360,1,-1); anel = (anel>0.5)&(mask[...,0]<0.02)
TX0, TX1, TY0, TY1 = 420, 700, 770, 862         # óculos e nariz (referência de posição)
tmpl = cv2.cvtColor(f0[TY0:TY1, TX0:TX1], cv2.COLOR_BGR2GRAY)
ref_anel = patch[anel].mean(0)
S = 40; n = 0; desl = []
f = f0
while f is not None:
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    area = g[TY0-S:TY1+S, TX0-S:TX1+S]
    r = cv2.matchTemplate(area, tmpl, cv2.TM_CCOEFF_NORMED)
    _, conf, _, (mx, my) = cv2.minMaxLoc(r)
    dx, dy = mx - S, my - S
    desl.append((dx, dy, round(conf,2)))
    y0, x0 = Y0+dy, X0+dx
    alvo = f[y0:y0+patch.shape[0], x0:x0+patch.shape[1]].astype(np.float32)
    ganho = np.clip(alvo[anel].mean(0) / np.maximum(ref_anel,1), 0.6, 1.6)
    p = np.clip(patch * ganho, 0, 255)
    f[y0:y0+patch.shape[0], x0:x0+patch.shape[1]] = (p*mask + alvo*(1-mask)).astype(np.uint8)
    wr.stdin.write(f.tobytes()); n += 1
    f = ler()
wr.stdin.close(); wr.wait()
print('quadros', n, 'desloc. max', max(abs(d[0]) for d in desl), max(abs(d[1]) for d in desl), 'confiança min', min(d[2] for d in desl))
