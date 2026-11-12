# Vídeo completo: parte 1 (funk + ATENÇÃO / VEM QUE VEM) -> transição de 0,5 s arrastando para o lado, com a logo do
# Leilão no Zap entrando em movimento junto e a assinatura sonora oficial (POC POC POC + "Leilão no Zap!") -> parte 2
# (IMG_3293 com desfoque leve e FIXO nas bordas — não oscila —, legenda na marca, batida baixinha, 'bate o olho no lance'
# com 👀 + som + zoom, e no 'joga pra lua!' a tela fecha de cima para baixo) -> martelada no fim.
# Uso: juntar.py <pasta-trabalho> <saida.mp4>
import sys, subprocess, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; F0 = f'{MK}/videos/2026-11-12-funk-tv-roleta'
W, H, FPS = 1080, 1920, 30
OURO, VERDE, NOITE, BR = (245, 196, 81), (27, 122, 72), (8, 30, 20), (255, 255, 255)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
ASS = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((760, 300))
# ---------- parte 2: base com desfoque fixo nas bordas (máscara estática, não oscila)
mk = Image.new('L', (W, H), 0); ImageDraw.Draw(mk).ellipse((40, 120, W-40, H-60), fill=255); mk.filter(ImageFilter.GaussianBlur(170)).save(f'{S}/masc2.png')
tm = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
if not os.path.exists(f'{S}/p2simples.mov'):
    run(['-i', f'{S}/p2.mov', '-loop', '1', '-i', f'{S}/masc2.png', '-filter_complex',
         f"[0:v]{tm},scale={W}:{H},fps={FPS},split[a][b];[b]gblur=sigma=7,eq=brightness=-0.10:saturation=0.6[f];[1:v]format=gray,scale={W}:{H}[m];[a][m]alphamerge[fr];[f][fr]overlay=0:0:shortest=1[v]",
         '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', '-shortest', f'{S}/p2simples.mov'])
# ---------- parte 2: cortes de pausa + legenda + logo pequena + batida baixinha
SEGS = [(0.05, 5.50), (6.10, 32.95)]  # sem corte na pausa do 'R$ 460'; vai até o fechamento da tela
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
      (16.55, 18.80, None, 'R$ 460'), (18.85, 21.15, 'com apenas', 'R$ 460'), (21.15, 22.68, 'você dá', 'o seu lance'),
      (22.68, 24.40, 'e tem a chance', 'de arrematar'), (24.40, 26.28, 'esse produto no', 'Leilão no Zap'), (26.30, 27.72, None, 'vem aqui!'),
      (27.72, 28.95, 'faça o seu', 'CADASTRO'), (28.95, 30.98, 'e não fique', 'fora dessa!'), (30.98, 32.10, None, 'JOGA PRA LUA!')]
os.makedirs(f'{S}/leg', exist_ok=True); PROB = []
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(t)
    x0 = (W - w)/2 - raio; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio, y + raio), raio, fill=cor); d.text((W/2, y + 2), t, font=f, fill=txt, anchor='mm')
ent = ['-i', f'{S}/p2simples.mov']; fc = ''; cat = ''
for i, (a, b) in enumerate(SEGS):
    fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,eq=contrast=1.05:saturation=1.1,vignette=angle=0.5[v{i}];"
           f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03[a{i}];"); cat += f'[v{i}][a{i}]'
fc += cat + f'concat=n={len(SEGS)}:v=1:a=1[v][a0];[a0]highpass=f=80,deesser=i=0.5,acompressor=threshold=-22dB:ratio=3:attack=10:release=180:makeup=2[a]'
run(ent + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/p2base.mov'])
run(['-i', f'{S}/p2base.mov', '-vn', '-af', 'loudnorm=I=-16:TP=-2:LRA=8', '-ar', '48000', f'{S}/p2voz.wav'])
subprocess.run(['python3', f'{F0}/fonte/batida_funk.py', f'{S}/bat2.wav', str(D2 + 0.5), '129.3', '0.0'], check=True)
OLHO = [saida(x) for x in (12.68, 14.28, 15.90)]; PLIM = f'{MK}/videos/leila-chegou-iphone/sfx/plim.mp3'
run(['-i', f'{S}/p2voz.wav', '-i', f'{S}/bat2.wav', '-i', PLIM, '-i', PLIM, '-i', PLIM, '-filter_complex',
     f"[1:a]atrim=0:{D2},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.20,afade=t=out:st={D2-1.0}:d=1.0[b];"
     "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[b][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300[bd];"
     "[v][bd]amix=inputs=2:duration=first:normalize=0[m0];" + ''.join(f"[{2+i_}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.7,adelay={int((a-0.03)*1000)}:all=1[s{i_}];" for i_, a in enumerate(OLHO))
     + "[m0]" + ''.join(f"[s{i_}]" for i_ in range(3)) + "amix=inputs=4:duration=first:normalize=0", '-ar', '48000', f'{S}/p2audio.wav'])
# legendas + logo pequena
lg = logo.copy(); lg.thumbnail((240, 90)); topo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(topo)
dt.rounded_rectangle((40, 230, 80 + lg.width, 256 + lg.height), 28, fill=NOITE + (160,)); topo.alpha_composite(lg, (60, 243)); topo.save(f'{S}/leg/topo.png')
OLHO = [saida(x) for x in (12.68, 14.28, 15.90)]  # cada "...no LANCE" do "bate o olho no lance"
FECHA0, FECHA1 = saida(31.95), saida(32.85)       # logo depois do "joga pra lua!": a tela fecha de cima para baixo
zexp = '+'.join(f"0.16*between(t,{a:.2f},{a+0.7:.2f})*sin(PI*(t-{a:.2f})/0.7)" for a in OLHO)
from PIL import ImageFont as _IF
em = _IF.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109); ei = Image.new('RGBA', (160, 140), (0, 0, 0, 0))
ImageDraw.Draw(ei).text((10, 5), '\U0001F440', font=em, embedded_color=True); ei = ei.crop(ei.getbbox()).resize((260, int(300*ei.height/ei.width)), Image.LANCZOS)
os.makedirs(f'{S}/olho', exist_ok=True); NO = 24
for k_ in range(NO):  # 0,8 s: entra com mola, balança e some
    t_ = k_/FPS; fr_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sc_ = pop(t_/0.25)*(1 - max(0, (t_-0.6)/0.2))
    if sc_ > 0.02:
        im_ = ei.resize((max(1, int(ei.width*sc_)), max(1, int(ei.height*sc_))), Image.LANCZOS).rotate(8*math.sin(t_*14), resample=Image.BICUBIC, expand=True)
        fr_.alpha_composite(im_, (int(W*0.76 - im_.width/2), int(560 - im_.height/2)))
    fr_.save(f'{S}/olho/o{k_:02d}.png')
cort = Image.new('RGBA', (W, H), NOITE + (255,)); dc = ImageDraw.Draw(cort); dc.rectangle((0, H-10, W, H), fill=OURO)
lgc = logo.copy(); lgc.thumbnail((520, 200)); cort.alpha_composite(lgc, ((W-lgc.width)//2, (H-lgc.height)//2)); cort.save(f'{S}/cortina.png')
ent = ['-i', f'{S}/p2base.mov']; vf = (f"[0:v]scale=w='trunc({W}*(1+{zexp})/2)*2':h='trunc({H}*(1+{zexp})/2)*2':eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})/2,setsar=1[b0]"); k = 1
for j, (a, b, t1, t2) in enumerate(LA):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 1450
    if t1: pilula(d, y, t1, F('Black', 54), VERDE + (245,), BR, 44); y += 104
    pilula(d, y, t2.upper(), F('Black', 68), OURO, (10, 60, 32), 50)
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v*0.45); s_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s_.putalpha(sh)
    Image.alpha_composite(s_, im).save(f'{S}/leg/l{j}.png')
    a_, b_ = saida(a), saida(min(b, [x for x in (5.5, 32.95) if x >= a][0]))
    ent += ['-loop', '1', '-t', str(D2), '-i', f'{S}/leg/l{j}.png']; vf += f";[b{j}][{k}:v]overlay=0:0:enable='between(t,{round(a_,3)},{round(b_-0.04,3)})'[b{j+1}]"; k += 1
nb = len(LA)
for i_, a in enumerate(OLHO):
    ent += ['-framerate', str(FPS), '-i', f'{S}/olho/o%02d.png']; vf += f";[{k}:v]setpts=PTS+{a-0.05:.3f}/TB[ol{i_}];[b{nb}][ol{i_}]overlay=0:0:eof_action=pass[b{nb+1}]"; nb += 1; k += 1
DC = FECHA1 - FECHA0
ent += ['-loop', '1', '-i', f'{S}/cortina.png']
vf += f";[{k}:v]format=rgba[ct];[b{nb}][ct]overlay=x=0:y='-H+H*(1-cos(PI*min(1,max(0,(t-{FECHA0:.3f})/{DC:.3f}))))/2':enable='gte(t,{FECHA0:.3f})'[vout]"; k += 1
run(ent + ['-i', f'{S}/p2audio.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{k}:a', '-t', str(D2), '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'pcm_s16le', f'{S}/parte2.mov'])
# ---------- junta: parte1 -[arrasta p/ a esquerda, 0,5 s]-> parte2, logo voando junto e indo para o canto, assinatura, martelo
p1 = f'{F0}/REELS-funk-tv-roleta.mp4'; d1 = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p1], capture_output=True, text=True).stdout)
TR = 0.5; OF = round(d1 - TR, 3); MEIO = OF + TR/2; TOT = round(d1 + D2 - TR, 3)
T_ASS = MEIO - 1.02  # a voz "Leilão no Zap!" da assinatura cai no meio do arrasto
L0, L1 = OF - 0.05, OF + 1.35  # janela da animação da logo
os.makedirs(f'{S}/lg', exist_ok=True)
canto = logo.copy(); canto.thumbnail((240, 90)); CX, CY = 60 + canto.width/2, 243 + canto.height/2
def eo(x): x = max(0, min(1, x)); return 1 - (1 - x)**3
def eio(x): x = max(0, min(1, x)); return 3*x*x - 2*x*x*x
for k in range(round((L1 - L0)*FPS) + 1):
    t = L0 + k/FPS; fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if t < MEIO + 0.55:  # entra da direita junto com o arrasto, passa um pouco do centro e volta (mola)
        x = (t - L0)/(MEIO + 0.2 - L0); px = W*1.15 + (W/2 - W*1.15)*eo(x) + (-30*math.sin(min(1, max(0, (t-MEIO-0.2)/0.35))*math.pi))
        py, s_, rot = H*0.5, 0.8 + 0.2*eo(x), -10*(1 - eo(x))
    else:  # encolhe e vai para o canto, onde fica até o fim
        x = eio((t - MEIO - 0.55)/0.55); px, py = W/2 + (CX - W/2)*x, H*0.5 + (CY - H*0.5)*x
        s_, rot = 1 + (canto.width/logo.width - 1)*x, 0
    lg = logo.resize((max(1, int(logo.width*s_)), max(1, int(logo.height*s_))), Image.LANCZOS)
    if rot: lg = lg.rotate(rot, resample=Image.BICUBIC, expand=True)
    if t < MEIO + 0.55:  # rastro de movimento enquanto voa
        for j_, a_ in ((3, 0.18), (2, 0.28), (1, 0.4)):
            gh = lg.copy(); gh.putalpha(gh.split()[3].point(lambda v: int(v*a_))); fr.alpha_composite(gh, (int(px - lg.width/2 + j_*38*(1 - eo(x))), int(py - lg.height/2)))
    gl = Image.new('RGBA', lg.size, (46, 160, 96, 0)); gl.putalpha(lg.split()[3].filter(ImageFilter.GaussianBlur(24)).point(lambda v: int(v*0.45)))
    fr.alpha_composite(gl, (int(px - lg.width/2), int(py - lg.height/2))); fr.alpha_composite(lg, (int(px - lg.width/2), int(py - lg.height/2)))
    fr.save(f'{S}/lg/g{k:03d}.png')
topo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dt = ImageDraw.Draw(topo)
dt.rounded_rectangle((40, 230, 80 + canto.width, 256 + canto.height), 28, fill=NOITE + (150,)); topo.alpha_composite(canto, (60, 243)); topo.save(f'{S}/topo.png')
HIT = round(OF + FECHA1 - 0.02, 2)  # martelada quando a tela acaba de fechar
MART = f'{MK}/videos/leila-chegou-iphone/sfx/martelo.mp3'
fc = (f"[0:v]fps={FPS},settb=1/{FPS},format=yuv420p[a];[1:v]fps={FPS},settb=1/{FPS},format=yuv420p[b];"
      f"[a][b]xfade=transition=slideleft:duration={TR}:offset={OF}[ab];"
      f"[2:v]setpts=PTS+{L0}/TB[lg];[ab][lg]overlay=0:0:eof_action=pass[ab2];"
      f"[3:v]format=rgba[tp];[ab2][tp]overlay=0:0:enable='between(t,{round(L1-0.02,3)},{round(OF+FECHA0+0.12,3)})'[ab3];"
      f"[ab3]eq=brightness=0.35:enable='between(t,{HIT},{HIT+0.08})',crop=iw-28:ih-28:'14+12*sin(t*90)*between(t,{HIT},{HIT+0.25})':'14+8*cos(t*80)*between(t,{HIT},{HIT+0.25})',scale={W}:{H},setsar=1,tpad=stop_mode=clone:stop_duration=0.7[v];"
      f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume='if(gte(t,{round(T_ASS,2)}),0.45,1)':eval=frame[x];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[z];"
      f"[x][z]acrossfade=d={TR},apad=pad_dur=0.7[xz];"
      f"[4:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(T_ASS*1000)}:all=1,volume=1.15[as];"
      f"[5:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(HIT*1000)}:all=1,volume=4.0[mt];"
      f"[xz][as][mt]amix=inputs=3:duration=first:normalize=0,asetpts=N/SR/TB[a0]")
run(['-i', p1, '-i', f'{S}/parte2.mov', '-framerate', str(FPS), '-i', f'{S}/lg/g%03d.png', '-loop', '1', '-i', f'{S}/topo.png', '-i', ASS, '-i', MART,
     '-filter_complex', fc, '-map', '[v]', '-map', '[a0]', '-t', str(round(TOT + 0.7, 2)), '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/tudo.mov'])
run(['-i', f'{S}/tudo.mov', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT])
if PROB: print('NAO CABE', PROB); sys.exit(1)
print('ok', TOT, 'assinatura em', round(T_ASS, 2), 'martelo em', HIT)
