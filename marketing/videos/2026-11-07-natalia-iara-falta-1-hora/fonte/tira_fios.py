# Tira o bolo de fio preto do chão (pedido da Natália). Segue o bolo quadro a quadro e preenche com o piso em volta.
# Só mexe em pixel escuro dentro da caixa do fio, no chão — rosto e corpo ficam intactos.
import cv2, numpy as np, subprocess, sys
src, dst, sx, sy, sw, sh, t0 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7]), float(sys.argv[7])
W, H = 1080, 1920; FPS = 30
p = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','bgr24','-'], stdout=subprocess.PIPE)
o = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
fr = []
while True:
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    fr.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
k0 = int(round(t0*FPS)); N = len(fr)
def escuro(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return ((g < 62) & (hsv[...,1] < 140)).astype(np.uint8)
def acha(img, box):
    x, y, w, h = box; m = escuro(img); pad = 70
    X0, Y0, X1, Y1 = max(0,x-pad), max(1250,y-pad), min(W,x+w+pad), min(H,y+h+pad)
    if X1-X0 < 20 or Y1-Y0 < 20: return None, None
    sub = m[Y0:Y1, X0:X1]; n, l, st, _ = cv2.connectedComponentsWithStats(sub)
    keep = np.zeros_like(sub)
    for i in range(1, n):
        cx, cy, cw, ch, a = st[i]
        gx, gy = cx+X0, cy+Y0
        if a < 25: continue
        if gx+cw < x-25 or gx > x+w+25 or gy+ch < y-25 or gy > y+h+25: continue   # tem que encostar na caixa anterior
        if cw > 1.6*max(w,120) or ch > 1.6*max(h,120): continue                    # nada gigante (perna, cadeira)
        keep[l == i] = 1
    if keep.sum() < 400: return None, None
    ys, xs = np.nonzero(keep); nb = (xs.min()+X0, ys.min()+Y0, xs.max()-xs.min()+1, ys.max()-ys.min()+1)
    if nb[2] > 1.3*sw or nb[3] > 1.3*sh: return None, None          # cresceu demais = pegou outra coisa: para
    dens = keep.sum() / (nb[2]*nb[3])
    if not 0.12 < dens < 0.75: return None, None                     # bolo de fio tem densidade média
    full = np.zeros((H, W), np.uint8); full[Y0:Y1, X0:X1] = keep
    return nb, full
caixas = [None]*N; mascaras = [None]*N
for direcao in (1, -1):                              # segue pra frente e pra trás a partir do quadro marcado
    box = (sx, sy, sw, sh); k = k0
    while 0 <= k < N:
        nb, m = acha(fr[k], box)
        if nb is None: break
        if caixas[k] is None: caixas[k], mascaras[k] = nb, m
        box = nb; k += direcao
achados = sum(c is not None for c in caixas)
tmpl = None
for k in range(N):
    if caixas[k] is not None:
        x, y, w, h = caixas[k]; tmpl = cv2.cvtColor(fr[k], cv2.COLOR_BGR2GRAY)[y:y+h, x:x+w].copy(); break
# reencontra o fio quando ele some e volta (template no chão)
k = 0
while k < N:
    if caixas[k] is None and tmpl is not None:
        g = cv2.cvtColor(fr[k], cv2.COLOR_BGR2GRAY); reg = g[1250:, :]
        if reg.shape[0] > tmpl.shape[0] and reg.shape[1] > tmpl.shape[1]:
            r = cv2.matchTemplate(reg, tmpl, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(r)
            if mx > 0.72:
                box = (loc[0], loc[1]+1250, tmpl.shape[1], tmpl.shape[0]); kk = k
                while kk < N and caixas[kk] is None:
                    nb, m = acha(fr[kk], box)
                    if nb is None: break
                    caixas[kk], mascaras[kk] = nb, m; box = nb; kk += 1
    k += 1
print('quadros com fio:', sum(c is not None for c in caixas), 'de', N, '(seguidos do marco:', achados, ')')
for k in range(N):
    img = fr[k]
    if mascaras[k] is not None:
        m = cv2.dilate(mascaras[k], cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
        x, y, w, h = caixas[k]; X0, Y0, X1, Y1 = max(0,x-40), max(0,y-40), min(W,x+w+40), min(H,y+h+40)
        roi = img[Y0:Y1, X0:X1]; mr = m[Y0:Y1, X0:X1]
        pin = cv2.inpaint(roi, mr, 9, cv2.INPAINT_TELEA)
        a = cv2.GaussianBlur(mr.astype(np.float32), (9, 9), 0)[..., None]
        img[Y0:Y1, X0:X1] = (pin*a + roi*(1-a)).astype(np.uint8)
    o.stdin.write(img.tobytes())
o.stdin.close(); o.wait()
np.save(dst + '.caixas.npy', np.array([c if c is not None else (-1,-1,-1,-1) for c in caixas]))
