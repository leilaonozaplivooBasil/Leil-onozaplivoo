# Foco "dinâmico" para vídeo andando com o celular: a PESSOA (recorte por IA, quadro a quadro) e a TV (o que é colorido e
# brilhante na cena) ficam nítidos; parede, prateleiras e o resto ficam desfocados, mais escuros e sem cor.
# A máscara é suavizada no tempo para não tremer. A borda da pessoa é apertada (sem halo branco da parede) e ganha um
# brilho verde da marca, bem suave. Uso: foco_dinamico.py <entrada.mov> <saida.mov>
import sys, subprocess, numpy as np, cv2
from rembg import remove, new_session
from PIL import Image
src, out = sys.argv[1:3]; W, H = 1080, 1920; w, h = 288, 512
tm = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=rgb24"
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'{tm},scale={W}:{H},fps=30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-i', src, '-map', '0:v', '-map', '1:a:0',
                        '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-shortest', out], stdin=subprocess.PIPE)
ses = new_session('u2net_human_seg'); ema = None; pe_ema = None; n = 0
VERDE = np.array([46, 160, 96], np.float32)
while True:
    buf = dec.stdout.read(W*H*3)
    if len(buf) < W*H*3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    sm = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA)
    pes = np.asarray(remove(Image.fromarray(sm), session=ses, only_mask=True)).astype(np.float32)/255
    hsv = cv2.cvtColor(sm, cv2.COLOR_RGB2HSV); tv = ((hsv[..., 1] > 90) & (hsv[..., 2] > 60)).astype(np.uint8)
    tv = cv2.morphologyEx(tv, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))
    k_, lab, st, _ = cv2.connectedComponentsWithStats(tv); keep = np.zeros_like(tv)
    for i in range(1, k_):
        if st[i, cv2.CC_STAT_AREA] > 0.03*w*h: keep[lab == i] = 1
    tv = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))).astype(np.float32)
    pes = cv2.erode(pes, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))  # aperta a borda: some o halo da parede
    m = np.maximum(pes, tv); m = cv2.GaussianBlur(m, (0, 0), 2.5)
    ema = m if ema is None else 0.55*ema + 0.45*m
    pe = pes if pe_ema is None else 0.55*pe_ema + 0.45*pes; pe_ema = pe
    M = cv2.resize(ema, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    fundo = cv2.GaussianBlur(f, (0, 0), 9).astype(np.float32); cinza = fundo.mean(2, keepdims=True)
    fundo = (0.35*fundo + 0.65*cinza)*0.66
    o = M*f.astype(np.float32) + (1-M)*fundo
    P = cv2.resize(pe, (W, H), interpolation=cv2.INTER_LINEAR)
    aro = np.clip(cv2.GaussianBlur(P, (0, 0), 22) - P, 0, 1)[..., None]*0.55  # brilho verde só do lado de fora da pessoa
    o = (o*(1-aro) + VERDE*aro).clip(0, 255).astype(np.uint8)
    enc.stdin.write(o.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait(); print('ok', n)
