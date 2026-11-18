# Ribeiro no galpão (18/11): filtro, torradeira e cafeteira Três Corações. Pedido da Natália: quando o RIBEIRO fala, a câmera
# aproxima nele (e no produto na mão); quando ela fala ou os dois conversam, plano aberto com os dois. Cortes nas pausas
# (sem cortar fala), legenda com palavras-chave em destaque, etiqueta do produto, trilha baixinha e cartão final com a assinatura.
# Quem fala = tom de voz (Natália > 180 Hz). Rosto do Ribeiro = detector YuNet (o rosto mais à direita/alto).
# Uso: montar.py <proxy1080.mp4> <rostos.json> <falas.txt> <f0.npy> <rms.npy> <saida.mp4>
import sys, json, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PX, ROS, FAL, F0, RMS, SAIDA = sys.argv[1:7]
MK = '/home/user/Leil-onozaplivoo/marketing'; W, H, FPS = 1080, 1920, 24
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE, OURO, AMA, NOITE, BR = (27, 122, 72), (245, 196, 81), (255, 214, 10), (10, 20, 16), (255, 255, 255)
# ---- falas, quem fala
f0 = np.load(F0); rms = np.load(RMS); HOP = 320 / 16000
falas = []
for l in open(FAL):
    a, b, t = l.split(' ', 2); a, b = float(a), float(b); i0, i1 = int(a / HOP), int(b / HOP)
    f = f0[i0:i1]; r = rms[i0:i1]; v = f[r > np.percentile(rms, 60)]; v = v[(v > 75) & (v < 380)]
    hz = float(np.median(v)) if len(v) else 150
    falas.append((a, b, t.strip(), 'N' if hz > 180 else 'R'))
# ---- trechos mantidos: cada fala com folga, juntando o que está perto (respiração curta fica, silêncio longo sai)
tre = []
for a, b, t, q in falas:
    a, b = a - .15, b + .22
    if tre and a - tre[-1][1] < .45: tre[-1][1] = b
    else: tre.append([a, b])
# ---- rosto do Ribeiro ao longo do tempo
ros = json.load(open(ROS)); tr = []
for t, fs in ros:
    c = [f for f in fs if f[0] + f[2] / 2 > 480 and f[4] > .7]
    if c: f = max(c, key=lambda f: f[0] + f[2] / 2); tr.append((t, f[0] + f[2] / 2, f[1] + f[3] / 2))
T = np.array([x[0] for x in tr]); X = np.array([x[1] for x in tr]); Y = np.array([x[2] for x in tr])
def rosto(t):
    k = np.abs(T - t) < 1.2
    if k.any(): return float(np.median(X[k])), float(np.median(Y[k]))
    return float(np.interp(t, T, X)), float(np.interp(t, T, Y))
def quem(t):
    for a, b, tx, q in falas:
        if a - .3 <= t <= b + .3: return q
    return 'N'
# alvo de zoom por instante do original: Ribeiro sozinho falando -> 1.5 nele; resto -> 1.0 (os dois)
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
# ---- etiquetas de produto (tempo do original)
PROD = [(84.2, 109.6, 'FILTRO DE ÁGUA', 'novo, zerado'), (118.1, 134.8, 'TORRADEIRA', 'nova, zerada'), (153.0, 182.0, 'CAFETEIRA TRÊS CORAÇÕES', 'nova, zerada')]
CHAVE = {'site': 1, 'site,': 1, 'galpão': 1, 'galpão,': 1, 'galpão.': 1, 'zerado': 1, 'zerada': 1, 'zerada,': 1, 'zerada.': 1, 'zerado.': 1, 'nova': 1, 'nova,': 1, 'novo,': 1, 'abaixo': 1, 'preço': 1, 'mercado.': 1, 'link': 1, 'imbatível.': 1, 'perdeu.': 1, 'levou,': 1, 'leilão,': 1, 'três': 1, 'corações.': 1, 'cafeteira.': 1, 'torradeira.': 1, 'filtro': 1, 'unidades.': 1, 'rápido.': 1, 'usado.': 1, 'segunda-feira.': 1, 'escritório.': 1}
def pedacos(a, b, t):
    ws = t.split(); n = max(1, math.ceil(len(ws) / 3)); k = math.ceil(len(ws) / n); d = (b - a) / n
    return [(a + i * d, a + (i + 1) * d, ws[i * k:(i + 1) * k]) for i in range(n)]
LEG = [p for a, b, t, q in falas for p in pedacos(a, b, t)]
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((230, 90))
def legenda(fr, to):
    for a, b, ws in LEG:
        if a <= to < b:
            d = ImageDraw.Draw(fr); tam = 76; txt = [(w.upper(), CHAVE.get(w.lower().strip('!?"'), 0)) for w in ws]
            while sum(d.textlength(w + ' ', font=F('Black', tam)) for w, _ in txt) > 960: tam -= 4
            f = F('Black', tam); tot = sum(d.textlength(w + ' ', font=f) for w, _ in txt); x = W / 2 - tot / 2; y = 1560
            pop = 1 + .12 * max(0, 1 - (to - a) / .12)
            for w, k in txt:
                ww = d.textlength(w, font=f)
                if k: d.rounded_rectangle((x - 10, y - 50, x + ww + 10, y + 46), 14, fill=AMA)
                d.text((x, y), w, font=f, fill=NOITE if k else BR, anchor='lm', stroke_width=0 if k else 7, stroke_fill=(0, 0, 0))
                x += d.textlength(w + ' ', font=f)
            return
def etiqueta(fr, to, tl):
    for a, b, t1, t2 in PROD:
        if a <= to < b:
            k = ease((to - a) / .35) * ease((b - to) / .35); d = ImageDraw.Draw(fr); f1, f2 = F('Black', 50), F('Bold', 36)
            w = max(d.textlength(t1, font=f1), d.textlength(t2, font=f2)) + 70; x0 = -w + (w + 40) * k
            d.rounded_rectangle((x0, 260, x0 + w, 400), 26, fill=VERDE); d.rounded_rectangle((x0, 260, x0 + 16, 400), 8, fill=AMA)
            d.text((x0 + 40, 305), t1, font=f1, fill=BR, anchor='lm'); d.text((x0 + 40, 360), t2, font=f2, fill=AMA, anchor='lm')
def topo(fr):
    p = Image.new('RGBA', (W, H)); ImageDraw.Draw(p).rounded_rectangle((W / 2 - LOGO.width / 2 - 20, 110, W / 2 + LOGO.width / 2 + 20, 130 + LOGO.height), 26, fill=(10, 20, 16, 160))
    fr.alpha_composite(p); fr.alpha_composite(LOGO, (int(W / 2 - LOGO.width / 2), 120))
def gancho(fr, tl):
    if tl > 2.6: return
    d = ImageDraw.Draw(fr); k = ease(tl / .3)
    for txt, y, cor, tam in (('TOUR NO GALPÃO', 1180, BR, 120), ('tudo que tá no site tá aqui', 1310, AMA, 62)):
        f = F('Black', int(tam * (.8 + .2 * k))); d.text((W / 2, y), txt, font=f, fill=cor, anchor='mm', stroke_width=9, stroke_fill=(0, 0, 0))
# ---- render
enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', SAIDA + '.video.mp4'], stdin=subprocess.PIPE)
tl = 0.0; zoom = 1.0; cx_s = None; cortes = []; cy_s = None
for ti, (a, b) in enumerate(tre):
    cortes.append(tl)
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{a:.3f}', '-i', PX, '-t', f'{b - a:.3f}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        to = a + n / FPS; im = Image.frombytes('RGB', (W, H), buf)
        alvo = 1.38 if quem(to) == 'R' else 1.0
        zoom += (alvo - zoom) * (.18 if n else 1.0)          # no corte já entra no enquadramento certo; dentro do trecho, desliza
        rx, ry = rosto(to)
        kz = (zoom - 1) / .38; cx_t = (rx - 60) * kz + W / 2 * (1 - kz); cy_t = (ry + 330) * kz + H / 2 * (1 - kz)
        cx_s = cx_t if (cx_s is None or n == 0) else cx_s + (cx_t - cx_s) * .12; cy_s = cy_t if (cy_s is None or n == 0) else cy_s + (cy_t - cy_s) * .12
        soco = 1 + .045 * max(0, 1 - n / 5) if ti else 1            # leve "soco" de zoom em cada corte
        z = zoom * soco; cw, ch = W / z, H / z
        x0 = min(max(0, cx_s - cw / 2), W - cw); y0 = min(max(0, cy_s - ch / 2), H - ch)
        fr = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS)
        if z > 1.2: fr = fr.filter(ImageFilter.UnsharpMask(2, 60, 2))
        fr = fr.convert('RGBA'); topo(fr); etiqueta(fr, to, tl); legenda(fr, to); gancho(fr, tl)
        enc.stdin.write(fr.convert('RGB').tobytes()); n += 1; tl += 1 / FPS
    p.wait()
# cartão final 3,8 s
FIM = 3.8
for n in range(int(FIM * FPS)):
    t = n / FPS; fr = Image.new('RGBA', (W, H), NOITE + (255,))
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((-200, 380, W + 200, 1500), fill=VERDE + (140,)); fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((520, 220)); fr.alpha_composite(lg, (int(W / 2 - lg.width / 2), 420))
    d = ImageDraw.Draw(fr); k = ease(t / .35); k2 = ease((t - .5) / .35); k3 = ease((t - 1.1) / .35)
    if k: d.text((W / 2, 860), 'ACHOU, LEVOU.', font=F('Black', int(118 * (.85 + .15 * k))), fill=BR, anchor='mm')
    if k2: d.text((W / 2, 1000), 'PISCOU, PERDEU.', font=F('Black', int(118 * (.85 + .15 * k2))), fill=OURO, anchor='mm')
    if k3:
        f = F('Black', 56); tx = 'Escreve LINK aqui embaixo'; w = d.textlength(tx, font=f)
        d.rounded_rectangle((W / 2 - w / 2 - 40, 1180, W / 2 + w / 2 + 40, 1290), 55, fill=AMA); d.text((W / 2, 1236), tx, font=f, fill=NOITE, anchor='mm')
        d.text((W / 2, 1360), 'que a gente te envia o link 💚'.replace(' 💚', ''), font=F('SemiBold', 44), fill=BR, anchor='mm')
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
# ---- áudio: as mesmas falas + trilha baixa + assinatura no cartão final
fc = ''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - .04:.3f}:d=0.04[a{i}];' for i, (a, b) in enumerate(tre))
fc += ''.join(f'[a{i}]' for i in range(len(tre))) + f'concat=n={len(tre)}:v=0:a=1,loudnorm=I=-16:TP=-1.5,apad=pad_dur={FIM}[fala];'
fc += f'[1:a]aloop=-1:size=2e9,atrim=0:{tl + FIM:.3f},volume=0.075,afade=t=out:st={tl + FIM - 1.2:.3f}:d=1.2[tri];'
fc += f'[2:a]adelay={int(tl * 1000)}|{int(tl * 1000)},volume=1.1[ass];[fala][tri][ass]amix=inputs=3:normalize=0:duration=first[mix]'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', PX, '-i', f'{MK}/marca/trilhas-base/trilha-house-brasileiro.mp3',
                '-i', f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3', '-i', SAIDA + '.video.mp4',
                '-filter_complex', fc, '-map', '3:v', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA], check=True)
print('ok', round(tl + FIM, 1), 's ·', len(tre), 'trechos · cortes em', [round(c, 1) for c in cortes])
