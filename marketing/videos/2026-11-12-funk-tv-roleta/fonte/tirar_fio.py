# Tira o fio que desce da TV pela parede (lado direito) e a tomada no pé dele — em TODOS os quadros, sem piscar.
# Como: marca o fio no 1º quadro (do pé da TV até a tomada), segue o tremido da câmera com rastreio de pontos da parede
# (fluxo óptico, mediana dos deslocamentos) e apaga sempre a mesma faixa, deslocada junto com a câmera (inpaint).
# Uso: tirar_fio.py <entrada.mov> <saida.mov>
import sys, subprocess, numpy as np, cv2
src, out = sys.argv[1:3]; W, H = 1080, 1920
tm = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=rgb24"
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'{tm},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
n = len(raw)//(W*H*3); FR = np.frombuffer(raw, np.uint8).reshape(n, H, W, 3)
# fio no 1º quadro: do pé da TV (topo) até a tomada (fim), medido na imagem
TOPO, FIM = (891, 975), (876, 1405)
def acha_fio(g):  # refina o fio no quadro 0 pelo ponto mais escuro de cada linha perto da estimativa
    pts = []
    for y in range(TOPO[1]+10, FIM[1]-40, 10):
        x0 = int(TOPO[0] + (FIM[0]-TOPO[0])*(y-TOPO[1])/(FIM[1]-TOPO[1])); row = g[y, x0-25:x0+26]
        pts.append((x0-25+int(np.argmin(row)), y))
    p = np.array(pts, float); a, b = np.polyfit(p[:, 1], p[:, 0], 1); return a, b
g0 = cv2.cvtColor(FR[0], cv2.COLOR_RGB2GRAY); A_, B_ = acha_fio(g0)
# rastreio do tremido: pontos da parede/TV no lado direito, longe da pessoa
roi = np.zeros_like(g0); roi[600:1700, 640:1080] = 255; roi[g0 < 100] = 0
p0 = cv2.goodFeaturesToTrack(g0, 300, 0.01, 12, mask=roi)
desl = [(0.0, 0.0)]; prev = g0; pp = p0; acum = np.zeros(2)
for k in range(1, n):
    g = cv2.cvtColor(FR[k], cv2.COLOR_RGB2GRAY)
    p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, pp, None, winSize=(31, 31), maxLevel=4)
    pb, st2, _ = cv2.calcOpticalFlowPyrLK(g, prev, p1, None, winSize=(31, 31), maxLevel=4)
    ok = (st[:, 0] == 1) & (st2[:, 0] == 1) & (np.linalg.norm((pb - pp).reshape(-1, 2), axis=1) < 1.0)
    d = np.median((p1 - pp).reshape(-1, 2)[ok], 0) if ok.sum() > 8 else np.zeros(2)
    acum += d; desl.append(tuple(acum))
    pp = p1[ok].reshape(-1, 1, 2) if ok.sum() > 40 else cv2.goodFeaturesToTrack(g, 300, 0.01, 12, mask=roi)
    if ok.sum() <= 40:  # re-semeia: o acumulado continua valendo
        pass
    prev = g
desl = np.array(desl)
# suaviza o caminho (tira tremor do próprio rastreio)
k_ = np.ones(5)/5; sm = np.stack([np.convolve(np.pad(desl[:, i], 2, mode='edge'), k_, 'valid') for i in range(2)], 1)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for k in range(n):
    dx, dy = sm[k]; f = FR[k].copy(); m = np.zeros((H, W), np.uint8)
    y0, y1 = TOPO[1] - 6, FIM[1] + 34
    pts = [(A_*y + B_ + dx, y + dy) for y in (y0, y1)]
    cv2.line(m, tuple(map(int, pts[0])), tuple(map(int, pts[1])), 255, 30)
    tx, ty = A_*FIM[1] + B_ + dx, FIM[1] + dy; cv2.rectangle(m, (int(tx-32), int(ty-34)), (int(tx+30), int(ty+40)), 255, -1)  # tomada
    f = cv2.inpaint(f, m, 9, cv2.INPAINT_TELEA)
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait(); print('ok', n, 'quadros; tremido máx', np.abs(sm).max(0).round(1))
