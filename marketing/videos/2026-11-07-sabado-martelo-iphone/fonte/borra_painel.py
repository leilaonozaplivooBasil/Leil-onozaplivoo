# Borra o painel "ARREMATADO!" abaixo do título (lá aparecem o nome do vencedor e o histórico com nomes).
# Fica só o martelo e a palavra ARREMATADO!; o valor entra por cima, escrito por nós. Cartões de lance também são borrados.
import cv2, numpy as np, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]
p = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','bgr24','-'], stdout=subprocess.PIPE)
o = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
W, H = 1080, 1920; n = 0; pain = 0
while True:
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy(); hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    # painel: verde-água claro e saturado, grande
    m = ((hsv[...,0] >= 75) & (hsv[...,0] <= 100) & (hsv[...,1] > 90) & (hsv[...,2] > 140)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31)))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if k > 1:
        i = 1 + int(np.argmax(st[1:, 4])); x, y, w, h, a = st[i]
        if w > 200 and h > 350:   # do martelo pra baixo: título, vencedor e histórico somem (o ARREMATADO entra escrito por nós)
            ya = y + int(h * 0.19); roi = f[ya:min(H, y+h+20), max(0, x-20):min(W, x+w+20)]
            f[ya:min(H, y+h+20), max(0, x-20):min(W, x+w+20)] = cv2.GaussianBlur(roi, (0, 0), 22); pain += 1
    # cartões brancos de lance (tela de longe)
    mc = ((hsv[...,2] > 150) & (hsv[...,1] < 70)).astype(np.uint8)
    mc = cv2.morphologyEx(mc, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))
    k, lab, st, _ = cv2.connectedComponentsWithStats(mc)
    for i in range(1, k):
        x, y, w, h, a = st[i]
        if 25 < w < 500 and 12 < h < 400 and a > 0.45*w*h and w > 0.75*h:
            roi = f[max(0,y-4):y+int(min(h*0.45, w*0.35)), max(0,x-4):x+w+4]
            if roi.size: f[max(0,y-4):y+int(min(h*0.45, w*0.35)), max(0,x-4):x+w+4] = cv2.GaussianBlur(roi, (0,0), 7)
    o.stdin.write(f.tobytes()); n += 1
o.stdin.close(); o.wait(); print('quadros', n, 'com painel', pain)
