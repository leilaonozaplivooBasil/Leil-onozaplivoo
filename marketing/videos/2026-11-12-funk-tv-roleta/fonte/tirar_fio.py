# Tira o fio fino que desce da TV pela parede (lado direito): acha, quadro a quadro, a linha escura e fina numa faixa
# da parede e preenche com a parede em volta (inpaint). Objetos largos (braço, corpo) não são tocados. Uso: tirar_fio.py <entrada.mov> <saida.mov>
import sys, subprocess, numpy as np, cv2
src, out = sys.argv[1:3]; W, H = 1080, 1920
tm = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=rgb24"
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'{tm},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
X0, X1, Y0, Y1 = 820, 1000, 850, 1470; n = 0; tot = 0
while True:
    buf = dec.stdout.read(W*H*3)
    if len(buf) < W*H*3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    g = cv2.cvtColor(f[Y0:Y1, X0:X1], cv2.COLOR_RGB2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (1, 9), 0)  # alisa na vertical (o fio é vertical)
    m = np.zeros(g.shape, np.uint8); med = np.median(g, 1); xmin = g.argmin(1); vmin = g.min(1)
    xs_prev = None
    for y in range(g.shape[0]):
        if med[y] < 140: continue  # linha que não é parede (braço, corpo, TV)
        prof = med[y] - vmin[y]; x = int(xmin[y])
        if xs_prev is not None and abs(x - xs_prev) > 25: continue
        if prof > 28:
            larg = 24 if vmin[y] < 95 else 0  # tomada/presilha
            m[y, max(0, x-14-larg):x+10+larg] = 255; xs_prev = x
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 9)))
    full = np.zeros((H, W), np.uint8); full[Y0:Y1, X0:X1] = m; tot += int((m > 0).sum())
    if m.any(): f = cv2.inpaint(f, full, 6, cv2.INPAINT_TELEA)
    enc.stdin.write(f.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait(); print('ok', n, 'quadros, px corrigidos', tot)
