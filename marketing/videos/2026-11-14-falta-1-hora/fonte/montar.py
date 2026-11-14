# FALTA 1 HORA (vídeo da ampulheta) — Natália x Emanuel 'brigando' pelo PS5, para soltar às 19h (sáb 14/11, martelo 20h). Som estourado consertado (adeclip + compressor +
# limitador), imagem clareada, pausas cortadas, legenda em pílulas, relógio de contagem regressiva no topo, final
# "enquanto a gente editava… já tá em R$ X" com a assinatura sonora. Uso: montar.py <pasta> <saida.mp4> <lance_agora> <segundos_ate_20h>
import sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT, AGORA, FALTA = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H, FPS = 1080, 1920, 30; VERDE, OURO, NOITE, BR, FOGO = (27,122,72), (245,196,81), (8,30,20), (255,255,255), (243,91,18)
PROB = []
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
SEGS = [(2.70, 10.00), (10.90, 29.95), (31.05, 38.40), (38.90, 40.10)]
def saida(t):
    acc = 0.0
    for a, b in SEGS:
        if a - 0.001 <= t <= b + 0.001: return round(acc + t - a, 3)
        acc += b - a
    raise ValueError(t)
D1 = round(sum(b - a for a, b in SEGS), 3)
fc = ''; cat = ''
for i, (a, b) in enumerate(SEGS):
    z = 1.0 if i % 2 == 0 else 1.06
    fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2',crop=1080:1920,setsar=1[v{i}];"
           f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03[a{i}];"); cat += f'[v{i}][a{i}]'
fc += cat + f'concat=n={len(SEGS)}:v=1:a=1[v][a]'
run(['-i', f'{S}/v1080.mov', '-i', f'{S}/voz_ok.wav', '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/base.mov'])
# cartão final (2,6 s): "enquanto a gente editava… já tá em R$ X"
CF = 2.6; fim = Image.new('RGBA', (W, H), NOITE + (255,)); d = ImageDraw.Draw(fim)
g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((W/2-560, H/2-640, W/2+560, H/2+640), fill=VERDE + (190,)); fim.alpha_composite(g.filter(ImageFilter.GaussianBlur(220)))
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((360, 130)); fim.alpha_composite(lg, ((W-lg.width)//2, 300))
for txt, y, f, cor in (('QUEM VAI', 640, F('Black', 120), BR), ('LEVAR?', 780, F('Black', 150), OURO), ('lance agora', 930, F('Bold', 54), BR), (f'R$ {AGORA}', 1060, F('Black', 170), OURO)):
    d.text((W/2+5, y+8), txt, font=f, fill=(0,0,0), anchor='mm'); d.text((W/2, y), txt, font=f, fill=cor, anchor='mm')
def pil(d, cx, cy, t, f, fundo, cor, r):
    w = d.textlength(t, font=f); d.rounded_rectangle((cx-w/2-r, cy-r, cx+w/2+r, cy+r), r, fill=fundo); d.text((cx, cy+2), t, font=f, fill=cor, anchor='mm')
pil(d, W/2, 1260, 'FALTA 1 HORA · MARTELO ÀS 20H', F('Black', 46), FOGO, BR, 46)
pil(d, W/2, 1410, 'DÁ SEU LANCE', F('Black', 64), OURO, NOITE, 58)
fim.convert('RGB').save(f'{S}/fim.png')
run(['-loop', '1', '-t', str(CF), '-i', f'{S}/fim.png', '-i', f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3', '-filter_complex',
     f"[0:v]scale={W}:{H},fps={FPS},format=yuv420p,zoompan=z='1+0.03*on/{int(CF*FPS)}':d=1:s={W}x{H}:fps={FPS}[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=300:all=1,apad,atrim=0:{CF}[a]",
     '-map', '[v]', '-map', '[a]', '-t', str(CF), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/fim.mov'])
# música por baixo (pegada orla, brazilian bass) com ducking na voz
run(['-i', f'{S}/base.mov', '-vn', '-ac', '2', '-ar', '48000', f'{S}/voz_base.wav'])
run(['-stream_loop', '-1', '-i', f'{MK}/marca/trilhas-base/pegada-orla/05-brazilian-bass.mp3', '-i', f'{S}/voz_base.wav', '-filter_complex',
     f"[0:a]atrim=0:{D1},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.20,afade=t=in:d=0.5,afade=t=out:st={D1-1.0}:d=1.0[m];"
     "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[md];[v][md]amix=inputs=2:duration=first:normalize=0",
     '-ar', '48000', f'{S}/audio1.wav'])
# legendas
LA = [(3.20, 7.00, None, 'TIC, TAC, TIC, TAC...'), (7.02, 9.95, 'gente, falta', '1 HORA PRO PS5!'), (10.98, 12.58, 'e aí, Natália,', 'VAI ARREMATAR?'),
      (12.62, 14.74, 'eu tô louca!', 'TÁ ME ESPERANDO'), (14.76, 16.90, 'é o presente', 'DE NATAL DELA'), (16.94, 17.90, 'tu não vai', 'LEVAR NÃO!'),
      (17.92, 18.92, None, 'EU VOU LEVAR SIM!'), (18.94, 19.50, None, 'NÃO, EU VOU!'), (19.52, 22.90, None, 'EMANUEL, EMANUEL!'),
      (22.96, 25.18, None, 'OLHA ISSO, GENTE!'), (25.22, 26.90, 'nós tamos brigando…', 'CADÊ O SEU LANCE?'), (27.34, 29.95, 'dá teu lance', 'QUE EU VOU TE FALAR'),
      (31.18, 34.10, 'esse PS5', 'LACRADINHO NA CAIXA'), (34.16, 35.95, '1 ano de garantia', 'E NOTA FISCAL'), (36.62, 38.40, 'se você não der seu lance', 'VAI FICAR…'),
      (38.95, 40.10, None, 'CHORANDO!')]
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(t)
    x0 = (W - w)/2 - raio; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio, y + raio), raio, fill=cor); d.text((W/2, y + 2), t, font=f, fill=txt, anchor='mm')
ent = ['-i', f'{S}/base.mov']; vf = '[0:v]null[b0]'; k = 1
for j, (a, b, t1, t2) in enumerate(LA):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); y = 1450
    if t1: pilula(d, y, t1, F('Black', 54), VERDE + (245,), BR, 44); y += 104
    pilula(d, y, t2, F('Black', 68), OURO, (10,60,32), 50)
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v*0.45); s_ = Image.new('RGBA', (W, H), (0,0,0,0)); s_.putalpha(sh)
    Image.alpha_composite(s_, im).save(f'{S}/l{j}.png')
    ent += ['-loop', '1', '-t', str(D1), '-i', f'{S}/l{j}.png']; vf += f";[b{j}][{k}:v]overlay=0:0:enable='between(t,{saida(a)},{round(saida(min(b, 40.10))-0.04,3)})'[b{j+1}]"; k += 1
# topo: logo + relógio de contagem regressiva até as 20h (conta segundo a segundo durante o vídeo)
topo = Image.new('RGBA', (W, H), (0,0,0,0)); dt = ImageDraw.Draw(topo); lgp = lg.copy(); lgp.thumbnail((230, 86))
dt.rounded_rectangle((40, 232, 80 + lgp.width, 258 + lgp.height), 28, fill=NOITE + (160,)); topo.alpha_composite(lgp, (60, 245))
dt.rounded_rectangle((W-470, 232, W-40, 336), 52, fill=FOGO + (240,)); dt.text((W-412, 284), 'FALTAM', font=F('Black', 30), fill=BR, anchor='lm')
topo.save(f'{S}/topo.png')
fnt = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
hh = f"%{{eif\\:trunc(({FALTA}-t)/3600)\\:d\\:2}}"; mm = f"%{{eif\\:mod(trunc(({FALTA}-t)/60)\\,60)\\:d\\:2}}"; ss = f"%{{eif\\:mod(trunc({FALTA}-t)\\,60)\\:d\\:2}}"
ent += ['-loop', '1', '-t', str(D1), '-i', f'{S}/topo.png']
vf += (f";[b{len(LA)}][{k}:v]overlay=0:0,drawtext=fontfile={fnt}:text='{hh}\\:{mm}\\:{ss}':fontsize=50:fontcolor=white:x=w-262:y=284-th/2[vout]"); k += 1
run(ent + ['-i', f'{S}/audio1.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{k}:a', '-t', str(D1), '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'pcm_s16le', f'{S}/corpo.mov'])
# junta corpo + cartão final (deslize rápido) e normaliza volume
run(['-i', f'{S}/corpo.mov', '-i', f'{S}/fim.mov', '-filter_complex',
     f"[0:v]fps={FPS},settb=1/{FPS}[a];[1:v]fps={FPS},settb=1/{FPS}[b];[a][b]xfade=transition=slideup:duration=0.35:offset={round(D1-0.35,3)}[v];[0:a][1:a]acrossfade=d=0.35[a0]",
     '-map', '[v]', '-map', '[a0]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/tudo.mov'])
run(['-i', f'{S}/tudo.mov', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT])
if PROB: print('NAO CABE', PROB); sys.exit(1)
print('ok', round(D1 + CF - 0.35, 2))
