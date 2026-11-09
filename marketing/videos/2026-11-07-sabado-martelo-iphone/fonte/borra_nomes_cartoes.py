# Borra o NOME de quem deu lance nos cartões brancos da tela (regra: nunca mostrar nome de cliente).
# Acha cada cartão branco no quadro e borra a faixa de cima (onde fica o nome); o valor do lance continua legível.
import cv2, numpy as np, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]; vf = sys.argv[3] if len(sys.argv) > 3 else 'null'
p = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-vf',f'{vf},scale=1080:1920,fps=30','-f','rawvideo','-pix_fmt','bgr24','-'], stdout=subprocess.PIPE)
o = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
W, H = 1080, 1920; n = 0; achados = 0
while True:
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = ((hsv[...,2] > 150) & (hsv[...,1] < 70)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    for i in range(1, k):
        x, y, w, h, a = st[i]
        if w < 90 or h < 45 or w > 800 or h > 520 or a < 0.45*w*h or w < 0.75*h: continue   # cartão (às vezes grudado no ícone da mão)
        y1 = y + int(min(h*0.36, w*0.30)); xa, xb = max(0, x-6), min(W, x+w+6); ya = max(0, y-6)
        roi = f[ya:y1, xa:xb]
        if roi.size: f[ya:y1, xa:xb] = cv2.GaussianBlur(roi, (0, 0), 9); achados += 1
    o.stdin.write(f.tobytes()); n += 1
o.stdin.close(); o.wait(); print('quadros', n, 'cartões borrados', achados)
