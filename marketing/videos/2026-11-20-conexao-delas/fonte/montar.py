# Conexão Delas · Mulheres que transformam (20/11): manhã aconchegante, vários takes + fotos com Ken Burns, fusões suaves,
# tom quente, trilha suave e cartões de abertura/fecho. SEM rosto de criança (cortes evitam o menino/menina; o bebê da foto do grupo é borrado).
# Uso: montar.py <pasta w/> <saida.mp4>
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IN, SAIDA = sys.argv[1:3]; TMP = os.path.join(os.path.dirname(SAIDA), 'tmp-conexao'); os.makedirs(TMP, exist_ok=True)
MK = '/home/user/Leil-onozaplivoo/marketing'; W, H, FPS = 1080, 1920, 30
SER = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'; SERI = '/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
ROSA, CREME, VINHO = (236, 170, 170), (255, 247, 238), (120, 40, 60)
def run(*a): subprocess.run(a, check=True)
QUENTE = 'eq=saturation=1.08:brightness=0.02,colorbalance=rs=.05:gs=.01:bs=-.05:rm=.04:bm=-.04,vignette=PI/7'
# (tipo, fonte, início, duração, legenda)
CENAS = [('v', 'v3b98.mp4', 9.0, 3.2, None),            # cavalete Conexão Delas (abertura)
         ('v', 'v3b98.mp4', 1.0, 3.0, None),
         ('f', 'f6060.jpg', 0, 2.8, None),
         ('v', 'v6059.mp4', 0.8, 3.4, None),
         ('f', 'f6081.jpg', 0, 2.8, 'cada história importa'),
         ('f', 'f6107.jpg', 0, 2.6, None),
         ('v', 'v6064.mp4', 0.2, 3.0, None),
         ('f', 'f6111.jpg', 0, 2.6, 'troca, escuta e acolhimento'),
         ('v', 'v6093.mp4', 9.0, 3.2, None),
         ('v', 'v6093.mp4', 19.0, 4.0, 'juntas somos mais'),
         ('f', 'f6062.jpg', 0, 3.2, None),
         ('f', 'f6101b.jpg', 0, 5.6, None)]
X = 0.7  # duração da fusão
# foto do grupo: borra o rosto do bebê (canto inferior esquerdo)
g = Image.open(f'{IN}/f6101.jpg'); box = (40, 2380, 440, 2860); g.paste(g.crop(box).filter(ImageFilter.GaussianBlur(45)), box); g.save(f'{IN}/f6101b.jpg', quality=93)
def texto_png(nome, linhas, fundo=0):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    if fundo:
        y0, y1 = linhas[0][1] - 170, linhas[-1][1] + 120
        sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).rectangle((0, y0, W, y1), fill=(40, 12, 22, fundo)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(70))); d = ImageDraw.Draw(im)
    for t, y, f, cor in linhas:
        d.text((W / 2 + 3, y + 4), t, font=f, fill=(0, 0, 0, 120), anchor='mm'); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm')
    im.save(f'{TMP}/{nome}.png')
segs = []
for i, (tp, src, a, dur, leg) in enumerate(CENAS):
    out = f'{TMP}/s{i:02d}.mp4'
    if tp == 'v':
        vf = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},{QUENTE},format=yuv420p'
        run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(a), '-t', str(dur), '-i', f'{IN}/{src}', '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out)
    else:
        n = int(dur * FPS); z = 'min(zoom+0.0009,1.12)' if i % 2 else 'if(eq(on,0),1.12,max(zoom-0.0009,1.0))'
        vf = f"scale=-2:3840,crop=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},{QUENTE},format=yuv420p"
        run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-loop', '1', '-i', f'{IN}/{src}', '-vf', vf, '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out)
    if leg:
        texto_png(f'l{i}', [(leg, 1540, ImageFont.truetype(SERI, 84), CREME)])
        o2 = out.replace('.mp4', 'L.mp4'); run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', out, '-loop', '1', '-i', f'{TMP}/l{i}.png', '-filter_complex', f"[1]format=rgba,fade=in:st=0.3:d=0.5:alpha=1,fade=out:st={dur - .8}:d=0.5:alpha=1[t];[0][t]overlay=shortest=1", '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', o2); out = o2
    segs.append((out, dur))
# encadeia com fusões suaves (alternando fade / suave pra esquerda / zoom)
TR = ['fade', 'smoothleft', 'fade', 'circleopen', 'fade', 'smoothup', 'fade', 'dissolve', 'fade', 'smoothleft', 'fade', 'fadewhite']
cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y']
for p, _ in segs: cmd += ['-i', p]
fc = ''; prev = '[0:v]'; off = 0
for i in range(1, len(segs)):
    off += segs[i - 1][1] - X; fc += f'{prev}[{i}:v]xfade=transition={TR[(i - 1) % len(TR)]}:duration={X}:offset={off:.3f}[x{i}];'; prev = f'[x{i}]'
total = off + segs[-1][1]
# títulos: abertura e fecho
texto_png('abre', [('CONEXÃO', 760, ImageFont.truetype(SER, 150), CREME), ('DELAS', 900, ImageFont.truetype(SER, 190), ROSA), ('mulheres que transformam', 1030, ImageFont.truetype(SERI, 66), CREME)], fundo=150)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((240, 100))
texto_png('fecha', [('CONEXÃO DELAS', 820, ImageFont.truetype(SER, 120), CREME), ('mulheres que transformam', 930, ImageFont.truetype(SERI, 68), ROSA), ('obrigada a cada uma de vocês', 1040, ImageFont.truetype(SERI, 50), CREME)], fundo=0)
fe = Image.new('RGBA', (W, H), (40, 12, 22, 175)); fe.alpha_composite(Image.open(f'{TMP}/fecha.png')); fe.alpha_composite(lg, (int(W / 2 - lg.width / 2), 1180)); fe.save(f'{TMP}/fecha.png')
n = len(segs); cmd += ['-loop', '1', '-framerate', str(FPS), '-t', f'{total:.2f}', '-i', f'{TMP}/abre.png', '-loop', '1', '-framerate', str(FPS), '-t', f'{total:.2f}', '-i', f'{TMP}/fecha.png']
fc += f"[{n}:v]format=rgba,fade=in:st=0.2:d=0.8:alpha=1,fade=out:st=2.6:d=0.7:alpha=1[ab];{prev}[ab]overlay=eof_action=pass:enable='lt(t,3.4)'[y1];"
fc += f"[{n + 1}:v]format=rgba,fade=in:st={total - 3.4:.2f}:d=1.0:alpha=1[fc];[y1]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.0:t=fill[y2];[y2][fc]overlay=eof_action=pass:enable='gte(t,{total - 3.4:.2f})',fade=out:st={total - 0.8:.2f}:d=0.8[v]"
cmd += ['-filter_complex', fc, '-map', '[v]', '-t', f'{total:.2f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', f'{TMP}/video.mp4']
run(*cmd)
TRILHA = sys.argv[3] if len(sys.argv) > 3 else f'{MK}/marca/trilhas-base/trilha-deep-house-elegante.mp3'
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', TRILHA, '-filter_complex', f'[1:a]atrim=0:{total:.2f},loudnorm=I=-17:TP=-2,afade=t=in:d=1.5,afade=t=out:st={total - 2.5:.2f}:d=2.5[a]',
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA)
print('ok', round(total, 1))
