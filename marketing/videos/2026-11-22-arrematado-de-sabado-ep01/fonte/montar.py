# Série "ARREMATADO DE SÁBADO" (todo domingo) · EP. 01: Honda PCX 160 (21/11). Vídeo de 15 s para o feed:
# os 116 lances REAIS (auction_messages) passando acelerados → contagem 10…1 → PUM (martelo) → ARREMATADO R$ 10.667.
# Sem nome de ninguém. Cor: verde da arte da placa. Uso: montar.py
import os, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
T = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/arremate'; os.makedirs(T, exist_ok=True)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H, FPS, DUR = 1080, 1920, 30, 15.0
VE, MENTA, BR, NEON, OURO = (10, 61, 38), (214, 236, 221), (255, 255, 255), (63, 208, 126), (245, 196, 81)
L = [(l.split()[0], int(l.split()[1])) for l in open(f'{AQ}/lances.txt') if l.strip()]
N = len(L); FINAL = L[-1][1]
def real(v): return f'{v:,.0f}'.replace(',', '.')
# tempos
T_INI, T_CD, T_PUM, T_FIM = 1.4, 7.6, 11.1, DUR      # lances de 1.4 a 11.1 s; contagem 10…1 de 7.6 a 11.1; PUM em 11.1
# fundo: verde da placa
y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - W / 2, (y - 900) * .85) / 1150, 0, 1) ** 1.2
a = np.array((30, 108, 66))[None, None] * (1 - dd[..., None]) + np.array((12, 62, 38))[None, None] * dd[..., None]; a += np.random.default_rng(3).normal(0, 1.6, a.shape)
BASE = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); r = Image.new('RGBA', (W, H)); dr = ImageDraw.Draw(r)
for i in range(36): yy = 150 + i * 52; dr.line((0, yy, W, yy + 40), fill=(255, 255, 255, 12), width=2)
BASE.alpha_composite(r)
MOTO = Image.open(f'{MK}/semana-2026-11-16/sabado-21-11-pcx/fonte/fotos/pcx-plataforma-lado.webp').convert('RGBA'); MOTO = MOTO.crop(MOTO.getbbox())
MT = Image.open(f'{MK}/marca/leiloeiro-martelo-sem-fundo.png').convert('RGBA').crop((0, 140, 270, 470))
al = np.array(MT.split()[3]).astype(float); fade = np.clip((MT.height - np.arange(MT.height)) / (MT.height * .35), 0, 1)[:, None]; MT.putalpha(Image.fromarray((al * fade).astype('uint8')))
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((220, 220))
def moto(b, larg, cy):
    m = MOTO.resize((larg, int(MOTO.height * larg / MOTO.width)), Image.LANCZOS)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - larg * .42, cy + m.height / 2 - 14, W / 2 + larg * .42, cy + m.height / 2 + 18), fill=(0, 0, 0, 120)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(m, (int(W / 2 - larg / 2), int(cy - m.height / 2)))
def pil(d, cx, cy, t, f, fu, co, px=34):
    w = d.textlength(t, font=f); d.rounded_rectangle((cx - w / 2 - px, cy - f.size * .85, cx + w / 2 + px, cy + f.size * .85), f.size, fill=fu); d.text((cx, cy), t, font=f, fill=co, anchor='mm')
# fundo fixo da fase dos lances (moto pequena no topo + título da série)
FASE = BASE.copy(); d = ImageDraw.Draw(FASE)
pil(d, W / 2, 140, 'ARREMATADO DE SÁBADO · EP. 01', F('Black', 40), NEON, VE)
d.text((W / 2, 255), 'Quanto saiu a PCX?', font=F('Black', 86), fill=BR, anchor='mm')
moto(FASE, 620, 520)
FASE.alpha_composite(LOGO, ((W - LOGO.width) // 2, 1790))
def idx_em(t):   # quantos lances já apareceram (acelera: começo devagar, fim rápido)
    if t < T_INI: return 0
    p = min(1, (t - T_INI) / (T_PUM - T_INI)); return max(1, min(N, int(round(N * p ** 1.55))))
fr = []; bips = []; ult = 0
enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', f'{T}/v.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    t = n / FPS
    if t < T_PUM:
        b = FASE.copy(); d = ImageDraw.Draw(b); k = idx_em(t)
        if k > ult: bips.append(t); ult = k
        hora, val = L[k - 1] if k else ('--:--:--', L[0][1])
        # painel do lance
        d.rounded_rectangle((90, 760, W - 90, 1060), 44, fill=(6, 40, 24), outline=NEON, width=4)
        d.text((W / 2, 810), 'LANCE ATUAL', font=F('Bold', 36), fill=NEON, anchor='mm')
        novo = k and (t - bips[-1]) < .18
        fv = F('Black', 150 if not novo else 162); d.text((W / 2, 940), f'R$ {real(val)}', font=fv, fill=BR, anchor='mm')
        d.text((W / 2, 1025), f'{k} lances · {hora}', font=F('Medium', 34), fill=MENTA, anchor='mm')
        # últimos lances (só valores, sem nomes)
        for j in range(5):
            i = k - 1 - j
            if i < 0: break
            yy = 1130 + j * 92; op = int(255 * (1 - j * .17))
            d.rounded_rectangle((150, yy - 36, W - 150, yy + 36), 30, fill=(6, 40, 24) if j else NEON)
            cor = VE if j == 0 else MENTA
            d.text((190, yy), 'novo lance' if j == 0 else 'lance', font=F('Bold', 32), fill=cor, anchor='lm'); d.text((W - 190, yy), f'R$ {real(L[i][1])}', font=F('Black', 40), fill=cor, anchor='rm')
        # contagem 10…1
        if t >= T_CD:
            c = 10 - int((t - T_CD) / ((T_PUM - T_CD) / 10)); c = max(1, c); fase = ((t - T_CD) % ((T_PUM - T_CD) / 10)) / ((T_PUM - T_CD) / 10)
            sc = 1.35 - .35 * min(1, fase * 3)
            g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g); gd.ellipse((W / 2 - 170 * sc, 520 - 170 * sc, W / 2 + 170 * sc, 520 + 170 * sc), fill=(6, 40, 24, 235), outline=NEON, width=8)
            gd.text((W / 2, 520), str(c), font=F('Black', int(210 * sc)), fill=BR, anchor='mm'); b.alpha_composite(g)
    else:
        tp = t - T_PUM; b = BASE.copy(); d = ImageDraw.Draw(b)
        if tp < .12: b.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, 230)))   # flash do PUM
        tr = min(1, tp / .25); sh = int((1 - tr) * 26 * math.sin(tp * 90))               # tremida
        d.text((W / 2 + sh, 230), 'PUM!', font=F('Black', 120), fill=NEON, anchor='mm')
        d.text((W / 2 + sh, 370), 'ARREMATADO!', font=F('Black', 118), fill=BR, anchor='mm')
        ang = 35 * (1 - min(1, tp / .18)); mt = MT.rotate(ang, resample=Image.BICUBIC, expand=True, center=(MT.width * .8, MT.height * .3)); mt.thumbnail((200, 220))
        b.alpha_composite(mt, (W - 215, 40))
        moto(b, 900, 780)
        d = ImageDraw.Draw(b); d.text((W / 2, 1090), 'A Honda PCX 160 saiu por', font=F('Medium', 50), fill=MENTA, anchor='mm')
        k = min(1, tp / .5); v = int(FINAL * (0.9 + .1 * k)) if k < 1 else FINAL
        fr_, fn = F('Black', 80), F('Black', 210); s1 = real(v); wr, wn = d.textlength('R$', font=fr_), d.textlength(s1, font=fn); x0 = (W - wr - 16 - wn) / 2
        d.text((x0, 1150), 'R$', font=fr_, fill=NEON, anchor='lt'); d.text((x0 + wr + 16, 1240), s1, font=fn, fill=BR, anchor='lm')
        if tp > .6:
            d.rounded_rectangle((110, 1400, W - 110, 1540), 40, fill=(6, 40, 24))
            d.text((W / 2, 1445), 'na loja, uns R$ 20 mil', font=F('Bold', 44), fill=MENTA, anchor='mm'); d.line((300, 1447, 780, 1447), fill=MENTA, width=5)
            d.text((W / 2, 1505), f'{N} lances · ao vivo · 20h37', font=F('Medium', 34), fill=MENTA, anchor='mm')
        if tp > 1.2:
            d.rounded_rectangle((110, 1590, W - 110, 1720), 40, fill=MENTA)
            d.text((W / 2, 1632), 'Todo domingo: o arremate de sábado', font=F('Black', 40), fill=VE, anchor='mm'); d.text((W / 2, 1685), 'segue pra não perder o próximo', font=F('Medium', 34), fill=VE, anchor='mm')
        b.alpha_composite(LOGO, ((W - LOGO.width) // 2, 1790))
    enc.stdin.write(b.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
# som: música + "bip" a cada lance novo (mais forte na contagem) + PUM grave do martelo
SR = 48000; au = np.zeros(int(DUR * SR))
for tb in bips:
    i = int(tb * SR); m = int(.045 * SR); f0 = 1500 if tb >= T_CD else 1100; amp = .22 if tb >= T_CD else .10
    au[i:i + m] += amp * np.sin(2 * np.pi * f0 * np.arange(m) / SR)[: len(au[i:i + m])] * np.exp(-np.arange(m) / (m / 3))[: len(au[i:i + m])]
for c in range(10):   # tique de cada número da contagem
    i = int((T_CD + c * (T_PUM - T_CD) / 10) * SR); m = int(.09 * SR); au[i:i + m] += .35 * np.sin(2 * np.pi * 880 * np.arange(m) / SR) * np.exp(-np.arange(m) / (m / 4))
i = int(T_PUM * SR); m = int(.6 * SR); tt = np.arange(m) / SR
au[i:i + m] += .9 * np.sin(2 * np.pi * (70 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 7) + .25 * np.random.default_rng(1).normal(0, 1, m) * np.exp(-tt * 40)
au = np.clip(au, -1, 1); open(f'{T}/sfx.raw', 'wb').write((au * 32767).astype('<i2').tobytes())
MUS = f'{MK}/marca/trilhas-base/pegada-orla/05-brazilian-bass.mp3'
subprocess.run(f'ffmpeg -nostdin -v error -y -f s16le -ar {SR} -ac 1 -i {T}/sfx.raw -i {MUS} -filter_complex "[1:a]atrim=0:{DUR},asetpts=N/SR/TB,volume=0.55,afade=t=in:d=0.3,afade=t=out:st={DUR - 1.2}:d=1.2[m];[0:a]aformat=channel_layouts=stereo[s];[m][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95" -ar 48000 -ac 2 {T}/a.wav', shell=True, check=True)
final = f'{OUT}/ARREMATADO-DE-SABADO-EP01-PCX.mp4'
subprocess.run(f'ffmpeg -nostdin -v error -y -i {T}/v.mp4 -i {T}/a.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "{final}"', shell=True, check=True)
print('ok', final, 'bips', len(bips))
