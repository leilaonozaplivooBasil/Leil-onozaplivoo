# Contagem regressiva ANIMADA do MacBook (story/status, 10 s): relógio de LED descendo segundo a segundo, tic-tac, lance atual.
# Uso: contagem_video.py <lance> <segundos_restantes> <pessoas> <saida.mp4>
import sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
LANCE, REST, PES, SAIDA = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
MK = '/home/user/Leil-onozaplivoo/marketing'; W, H, FPS, DUR = 1080, 1920, 30, 10
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
AN = lambda t: ImageFont.truetype(f'{MK}/marca/fontes/anton-latin-400-normal.woff', t)
BR, AMA, VERM, OURO, NOITE = (255, 255, 255), (255, 214, 10), (235, 35, 40), (245, 196, 81), (8, 16, 12)
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 760) * .85) / 1150, 0, 1) ** 1.2
a = np.array((70, 8, 12))[None, None] * (1 - dd[..., None]) + np.array((8, 2, 3))[None, None] * dd[..., None]
BASE = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((210, 210))
mac = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA'); mac = mac.crop(mac.getbbox()); mac = mac.resize((520, int(mac.height * 520 / mac.width)), Image.LANCZOS)
fT = AN(250)
enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', SAIDA + '.v.mp4'], stdin=subprocess.PIPE)
for n in range(DUR * FPS):
    t = n / FPS; r = max(0, REST - int(t)); fr_s = t % 1; pulso = 1 + .06 * max(0, 1 - fr_s / .25)
    b = BASE.copy(); d = ImageDraw.Draw(b); x0 = (W - lg.width) // 2
    d.rounded_rectangle((x0 - 22, 66, x0 + lg.width + 22, 94 + lg.height), 26, fill=(10, 20, 16, 235)); b.alpha_composite(lg, (x0, 80))
    d.rounded_rectangle((W / 2 - 300, 300, W / 2 + 300, 390), 45, fill=VERM); d.text((W / 2, 346), 'CONTAGEM REGRESSIVA', font=F('Black', 46), fill=BR, anchor='mm')
    # painel LED
    d.rounded_rectangle((50, 450, W - 50, 860), 44, fill=(20, 0, 0), outline=(120, 20, 20), width=6)
    txt = f'{r // 3600:02d}:{r % 3600 // 60:02d}:{r % 60:02d}'
    g = Image.new('RGBA', (W, H)); f = AN(int(250 * pulso)); ImageDraw.Draw(g).text((W / 2, 655), txt, font=f, fill=VERM + (255,), anchor='mm')
    b.alpha_composite(g.filter(ImageFilter.GaussianBlur(22))); b.alpha_composite(g); d = ImageDraw.Draw(b)
    for yy in range(450, 860, 8): d.line((50, yy, W - 50, yy), fill=(0, 0, 0, 60), width=2)
    d.text((W / 2, 920), 'PRO MARTELO BATER · HOJE 20H', font=F('Black', 50), fill=BR, anchor='mm')
    # tic-tac
    lado = 'TIC' if int(t) % 2 == 0 else 'TAC'; k = max(0, 1 - fr_s / .5)
    if k: d.text((W / 2 + (-260 if lado == 'TIC' else 260), 1010), lado, font=AN(90), fill=AMA + (int(255 * k),), anchor='mm')
    # lance
    d.rounded_rectangle((150, 1090, W - 150, 1300), 34, fill=(0, 0, 0, 210), outline=AMA, width=4)
    d.text((W / 2, 1140), 'LANCE ATUAL', font=F('Bold', 36), fill=AMA, anchor='mm'); d.text((W / 2, 1228), f'R$ {real(LANCE)}', font=F('Black', 116), fill=BR, anchor='mm')
    d.text((W / 2, 1360), f'{PES} pessoas na disputa · quem deu lance pode cobrir', font=F('SemiBold', 38), fill=(255, 225, 225), anchor='mm')
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - 240, 1800, W / 2 + 240, 1840), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(16)))
    b.alpha_composite(mac, (int(W / 2 - 260), 1815 - mac.height))
    enc.stdin.write(b.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
# áudio: tic-tac a cada segundo (clique agudo/grave alternado)
sr = 48000; au = np.zeros(sr * DUR)
for s_ in range(DUR):
    f0 = 1800 if s_ % 2 == 0 else 1200; tt = np.arange(int(sr * .05)) / sr
    au[s_ * sr: s_ * sr + len(tt)] += np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * 70) * .6
pcm = (np.clip(au, -1, 1) * 32767).astype('<i2').tobytes()
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', SAIDA + '.v.mp4', '-f', 's16le', '-ar', str(sr), '-ac', '1', '-i', '-', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', SAIDA], input=pcm, check=True)
print('ok')
