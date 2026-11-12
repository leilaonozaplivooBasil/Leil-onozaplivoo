# Vídeo completo: parte 1 (funk + ATENÇÃO / VEM QUE VEM) -> transição (zoom + flash) -> vinheta da logo com a assinatura
# sonora oficial (POC POC POC + "Leilão no Zap!") -> parte 2 (IMG_3293, foco dinâmico, pausas cortadas, legenda na marca,
# batida de funk baixinha por baixo da voz). Uso: juntar.py <pasta-trabalho> <saida.mp4>
import sys, subprocess, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; F0 = f'{MK}/videos/2026-11-12-funk-tv-roleta'
W, H, FPS = 1080, 1920, 30
OURO, VERDE, NOITE, BR = (245, 196, 81), (27, 122, 72), (8, 30, 20), (255, 255, 255)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
ASS = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
# ---------- vinheta da logo (2,0 s): fundo verde-noite com brilho, 3 marteladas sacodem a tela, logo entra no "Leilão no Zap!"
VD = 2.0; os.makedirs(f'{S}/vin', exist_ok=True)
logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((760, 300))
POCS, VOZ = (0.19, 0.56, 0.81), 1.02
import random; random.seed(4)
PT = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 3), random.uniform(0, 6.28)) for _ in range(90)]
for k in range(round(VD*FPS)):
    t = k/FPS; b = Image.new('RGBA', (W, H), NOITE + (255,))
    g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((W/2-620, H/2-620, W/2+620, H/2+620), fill=VERDE + (230,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(220)))
    bat = max([max(0, 1 - (t - p)/0.12) for p in POCS if t >= p] + [0])
    if bat:  # clarão dourado a cada martelada
        cl = Image.new('RGBA', (W, H)); ImageDraw.Draw(cl).ellipse((W/2-420, H/2-420, W/2+420, H/2+420), fill=OURO + (int(120*bat),)); b.alpha_composite(cl.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(b)
    for x, y, r, ph in PT:
        yy = (y - t*120) % H; a = int(120 + 100*math.sin(ph + t*6)); d.ellipse((x-r, yy-r, x+r, yy+r), fill=OURO + (max(0, a),))
    if t >= VOZ:
        s_ = pop((t - VOZ)/0.35); lg = logo.resize((max(1, int(logo.width*s_)), max(1, int(logo.height*s_))), Image.LANCZOS)
        gl = Image.new('RGBA', lg.size, OURO + (0,)); gl.putalpha(lg.split()[3].filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v*0.5)))
        b.alpha_composite(gl, ((W-lg.width)//2, (H-lg.height)//2)); b.alpha_composite(lg, ((W-lg.width)//2, (H-lg.height)//2))
        if t >= VOZ + 0.3:
            a = min(1, (t - VOZ - 0.3)/0.25); f = F('Bold', 46); tx = 'aqui você ganha ou ganha!'
            d.text((W/2, H/2 + 230), tx, font=f, fill=OURO + (int(255*a),), anchor='mm')
    sx = int(18*bat*math.sin(t*90)); sy = int(12*bat*math.cos(t*80))
    fr = Image.new('RGB', (W, H), NOITE); fr.paste(b.convert('RGB'), (sx, sy)); fr.save(f'{S}/vin/v{k:03d}.jpg', quality=93)
run(['-framerate', str(FPS), '-i', f'{S}/vin/v%03d.jpg', '-i', ASS, '-filter_complex', f'[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=0:{VD}[a]',
     '-map', '0:v', '-map', '[a]', '-t', str(VD), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'pcm_s16le', f'{S}/vinheta.mov'])
# ---------- parte 2: cortes de pausa + legenda + logo pequena + batida baixinha
SEGS = [(0.55, 5.50), (6.10, 17.75), (18.80, 32.00)]
def saida(t):
    acc = 0
    for a, b in SEGS:
        if a - 0.001 <= t <= b + 0.001: return acc + t - a
        acc += b - a
    raise ValueError(t)
D2 = round(sum(b - a for a, b in SEGS), 3)
LA = [(0.74, 2.10, 'não pule', 'ESSE VÍDEO!'), (2.28, 3.58, 'vem aqui que eu vou', 'te contar'), (3.58, 5.50, 'uma fofoca', 'BOMBA!'),
      (6.22, 7.95, 'Leilão no Zap', 'PS5'), (8.24, 9.42, 'lacrado', 'NA CAIXA'), (9.42, 11.30, '1 ano de garantia', 'e nota fiscal'),
      (11.66, 13.35, 'vem aqui, bate o olho', 'NO LANCE'), (13.46, 14.95, 'bate o olho', 'NO LANCE'), (15.02, 16.55, 'bate o olho', 'NO LANCE'),
      (16.55, 17.75, None, 'R$ 460'), (18.85, 21.15, 'com apenas', 'R$ 460'), (21.15, 22.68, 'você dá', 'o seu lance'),
      (22.68, 24.40, 'e tem a chance', 'de arrematar'), (24.40, 26.28, 'esse produto no', 'Leilão no Zap'), (26.30, 27.72, None, 'vem aqui!'),
      (27.72, 28.95, 'faça o seu', 'CADASTRO'), (28.95, 30.98, 'e não fique', 'fora dessa!'), (30.98, 32.00, None, 'JOGA PRA LUA!')]
os.makedirs(f'{S}/leg', exist_ok=True); PROB = []
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(t)
    x0 = (W - w)/2 - raio; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio, y + raio), raio, fill=cor); d.text((W/2, y + 2), t, font=f, fill=txt, anchor='mm')
ent = ['-i', f'{S}/p2foco.mov']; fc = ''; cat = ''
for i, (a, b) in enumerate(SEGS):
    fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,eq=contrast=1.05:saturation=1.1,vignette=angle=0.5[v{i}];"
           f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03[a{i}];"); cat += f'[v{i}][a{i}]'
fc += cat + f'concat=n={len(SEGS)}:v=1:a=1[v][a0];[a0]highpass=f=80,deesser=i=0.5,acompressor=threshold=-22dB:ratio=3:attack=10:release=180:makeup=2[a]'
run(ent + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/p2base.mov'])
run(['-i', f'{S}/p2base.mov', '-vn', '-af', 'loudnorm=I=-16:TP=-2:LRA=8', '-ar', '48000', f'{S}/p2voz.wav'])
subprocess.run(['python3', f'{F0}/fonte/batida_funk.py', f'{S}/bat2.wav', str(D2 + 0.5), '129.3', '0.0'], check=True)
run(['-i', f'{S}/p2voz.wav', '-i', f'{S}/bat2.wav', '-filter_complex',
     f"[1:a]atrim=0:{D2},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.20,afade=t=out:st={D2-1.0}:d=1.0[b];"
     "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[b][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300[bd];"
     "[v][bd]amix=inputs=2:duration=first:normalize=0", '-ar', '48000', f'{S}/p2audio.wav'])
# legendas + logo pequena
lg = logo.copy(); lg.thumbnail((240, 90)); topo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(topo)
dt.rounded_rectangle((40, 230, 80 + lg.width, 256 + lg.height), 28, fill=NOITE + (160,)); topo.alpha_composite(lg, (60, 243)); topo.save(f'{S}/leg/topo.png')
ent = ['-i', f'{S}/p2base.mov', '-loop', '1', '-t', str(D2), '-i', f'{S}/leg/topo.png']; vf = '[0:v][1:v]overlay=0:0[b0]'; k = 2
for j, (a, b, t1, t2) in enumerate(LA):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 1450
    if t1: pilula(d, y, t1, F('Black', 54), VERDE + (245,), BR, 44); y += 104
    pilula(d, y, t2.upper(), F('Black', 68), OURO, (10, 60, 32), 50)
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v*0.45); s_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s_.putalpha(sh)
    Image.alpha_composite(s_, im).save(f'{S}/leg/l{j}.png')
    a_, b_ = saida(a), saida(min(b, [x for x in (5.5, 17.75, 32.0) if x >= a][0]))
    ent += ['-loop', '1', '-t', str(D2), '-i', f'{S}/leg/l{j}.png']; vf += f";[b{j}][{k}:v]overlay=0:0:enable='between(t,{round(a_,3)},{round(b_-0.04,3)})'[b{j+1}]"; k += 1
vf += f';[b{len(LA)}]null[vout]'
run(ent + ['-i', f'{S}/p2audio.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{k}:a', '-t', str(D2), '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'pcm_s16le', f'{S}/parte2.mov'])
# ---------- junta: parte1 -[zoom]-> vinheta -[flash branco]-> parte2
p1 = f'{F0}/REELS-funk-tv-roleta.mp4'; d1 = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p1], capture_output=True, text=True).stdout)
T1, T2 = 0.25, 0.20
fc = (f"[0:v]fps={FPS},settb=1/{FPS},format=yuv420p[a];[1:v]fps={FPS},settb=1/{FPS},format=yuv420p[b];[2:v]fps={FPS},settb=1/{FPS},format=yuv420p[c];"
      f"[a][b]xfade=transition=zoomin:duration={T1}:offset={round(d1-T1,3)}[ab];[ab][c]xfade=transition=fadewhite:duration={T2}:offset={round(d1-T1+VD-T2,3)}[v];"
      f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[x];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[y];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[z];"
      f"[x][y]acrossfade=d={T1}[xy];[xy][z]acrossfade=d={T2}[a0]")
run(['-i', p1, '-i', f'{S}/vinheta.mov', '-i', f'{S}/parte2.mov', '-filter_complex', fc, '-map', '[v]', '-map', '[a0]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/tudo.mov'])
run(['-i', f'{S}/tudo.mov', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT])
if PROB: print('NAO CABE', PROB); sys.exit(1)
print('ok', round(d1 + VD + D2 - T1 - T2, 2))
