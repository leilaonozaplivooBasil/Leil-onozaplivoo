# Vídeo da Natália "ESPERA, ESPERA…" — iPhone 18 Pro Max, quarta 11/11 às 20h.
# Pausas cortadas, o tropeço ("você pode ser o…") sai do meio e volta no final como ERROS DE GRAVAÇÃO (preto e branco).
# 10/11: tirado o barulho de boca (25,2→25,8) antes do "você pode ser o próximo".
# Transições estilo CapCut: zoom-punch + flash nas viradas de assunto, zoom alternado nos cortes, glitch na entrada do blooper.
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
SRC, BANNER = f'{S}/in/espera.mov', f'{S}/banner.mp4'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR, FOGO = (27,122,72), (245,196,81), (10,20,16), (255,255,255), (243,91,18)
PROB = []
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
# (início, fim, zoom, punch) no tempo do vídeo original. punch = virada de assunto (zoom rápido + flash + whoosh)
SEGS = [(0.30, 6.92, 1.00, True), (7.12, 8.96, 1.08, False), (9.26, 11.34, 1.00, True), (11.54, 12.68, 1.00, False),
        (12.94, 13.94, 1.00, True), (14.10, 16.78, 1.10, True), (17.00, 18.82, 1.00, False), (18.96, 20.84, 1.08, False),
        (21.00, 22.60, 1.00, True), (26.56, 35.38, 1.08, False), (35.84, 39.06, 1.00, True),
        (39.58, 44.58, 1.00, True)]
BLOOP = (22.80, 28.00)      # o tropeço inteiro, pro final
def saida(t):
    acc = 0.0
    for a, b, *_ in SEGS:
        if a - 0.001 <= t <= b + 0.001: return round(acc + min(max(t, a), b) - a, 3)
        acc += b - a
    raise ValueError(t)
DA = round(sum(b - a for a, b, *_ in SEGS), 3); DB = round(BLOOP[1] - BLOOP[0], 3); dur = round(DA + DB, 3)
BROLL = (saida(9.26), saida(12.68))   # "um iPhone 18 Pro Max vai pro leilão": vídeo do iPhone do site em tela cheia
# 1) voz tratada num wav separado (loudnorm sozinho, fora do grafo de mix)
run(['-i', SRC, '-vn', '-ac', '1', '-ar', '48000', '-af', 'highpass=f=80,afftdn=nf=-25,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=10:release=200:makeup=2', f'{S}/voz_tratada.wav'])
run(['-i', f'{S}/voz_tratada.wav', '-af', 'loudnorm=I=-16:TP=-2:LRA=9', '-ar', '48000', f'{S}/voz_ok.wav'])
# 2) base: cortes + zoom alternado + punch/flash; blooper em P&B com glitch na entrada
fc, cat = '', ''
for i, (a, b, z, p) in enumerate(SEGS):
    zz = f"{z}*(1+0.14*max(0\\,1-t/0.28))" if p else f"{z}"
    fl = ",eq=brightness='0.55*max(0\\,1-t/0.12)':eval=frame" if p and i > 0 else ''
    fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=w='trunc(1080*{zz}/2)*2':h='trunc(1920*{zz}/2)*2':eval=frame,crop=1080:1920:(iw-1080)/2:(ih-1920)/2{fl},setsar=1,fps=30[v{i}];"
           f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03[a{i}];")
    cat += f"[v{i}][a{i}]"
n = len(SEGS); a, b = BLOOP
fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1080:1920,hue=s=0,eq=contrast=1.15,noise=alls=14:allf=t,vignette=PI/4,"
       f"rgbashift=rh=-14:bh=14:enable='lt(t,0.3)',eq=brightness='0.6*max(0\\,1-t/0.15)':eval=frame,setsar=1,fps=30[v{n}];"
       f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.3,3)}:d=0.3[a{n}];")
cat += f"[v{n}][a{n}]"
fc += cat + f"concat=n={n+1}:v=1:a=1[v][a]"
run(['-i', SRC, '-i', f'{S}/voz_ok.wav', '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/base.mov'])
run(['-i', f'{S}/base.mov', '-vn', '-ac', '1', '-ar', '48000', f'{S}/voz_final.wav'])
# 3) whoosh nas viradas (ruído filtrado, baixinho) + música da playlist (pegada orla) com ducking na voz
viradas = [saida(a) for a, b, z, p in SEGS if p and a > 0.3] + [DA]
run(['-f', 'lavfi', '-t', '0.35', '-i', 'anoisesrc=color=pink:amplitude=0.6:r=48000', '-af', 'bandpass=f=1800:width_type=o:w=2,afade=t=in:d=0.12,afade=t=out:st=0.12:d=0.23,volume=0.5', f'{S}/whoosh.wav'])
m = f'{MK}/marca/trilhas-base/pegada-orla/02-nu-disco-por-do-sol.mp3'
wl = ''.join(f'[w{k}]' for k in range(len(viradas)))
run(['-stream_loop', '-1', '-i', m, '-i', f'{S}/voz_final.wav', '-i', f'{S}/whoosh.wav', '-filter_complex',
     f"[0:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.24,afade=t=in:d=0.6,afade=t=out:st={dur-1.5}:d=1.5[m];"
     f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit={len(viradas)}" + ''.join(f'[s{k}]' for k in range(len(viradas))) + ';' +
     ''.join(f"[s{k}]adelay={int(max(0, t-0.18)*1000)}:all=1,apad=whole_dur={dur}[w{k}];" for k, t in enumerate(viradas)) +
     f"{wl}amix=inputs={len(viradas)}:normalize=0,asetpts=N/SR/TB,atrim=0:{dur}[wh];"
     "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];"
     f"[v][md][wh]amix=inputs=3:duration=first:normalize=0,volume=1.3", '-ar', '48000', f'{S}/audio.wav'])
# 4) camadas: selo, B-roll do iPhone, legendas, título do blooper
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(f'"{t}" não cabe')
    x0 = (W - w) / 2 - raio + 8; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio - 16, y + raio), raio, fill=cor); d.text((W/2, y), t, font=f, fill=txt, anchor='mm')
def legenda(txt, dest, nome, y=1430, cor_dest=OURO):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    if txt: pilula(d, y, txt, F('Black', 56), VERDE + (245,), BR, 46); y += 106
    if dest: pilula(d, y, dest.upper(), F('Black', 66), cor_dest + (255,), (10,60,32) if cor_dest == OURO else BR, 50)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def selo():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
    d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
    f = F('Black', 34); t = 'IPHONE 18 · QUARTA 20H'; w = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=FOGO + (240,)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
LA = [(0.30, 2.40, 'espera, espera…', 'para tudo!'), (2.40, 4.05, None, 'não é possível'), (4.05, 6.92, 'você não vai acreditar', 'no que vai acontecer'),
      (7.12, 8.96, 'nessa', 'quarta-feira'), (9.26, 11.34, 'um', 'iPhone 18 Pro Max'), (11.54, 12.68, 'vai pro', 'leilão'),
      (12.94, 14.80, 'e o lance…', 'vocês não vão crer'), (14.80, 16.78, None, 'R$ 197,00'), (17.00, 18.82, 'é isso mesmo', 'que você ouviu'),
      (18.96, 20.84, 'na', 'quarta-feira'), (21.00, 22.60, 'olha só:', 'iPhone 18'), (26.56, 28.10, 'você pode ser', 'o próximo'),
      (28.10, 30.60, 'a arrematar', 'essa máquina'), (30.60, 33.05, 'já imaginou sair na quarta', 'com o iPhone 18'), (33.05, 35.38, None, 'arrematado?'),
      (35.84, 37.30, 'mas', 'atenção'), (37.30, 39.06, 'o relógio', 'está correndo'), (39.58, 42.10, 'escreva IPHONE', 'aqui embaixo'),
      (42.10, 44.58, 'que eu te envio', 'o link agora')]
LEG = [(saida(a), saida(b), t, d) for a, b, t, d in LA]
selo()
ent = ['-i', f'{S}/base.mov', '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png', '-stream_loop', '-1', '-i', BANNER]
b0, b1 = BROLL
vf = (f"[2:v]setpts=PTS-STARTPTS+{b0}/TB,split[bA][bB];"
      f"[bA]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.12,format=yuva420p,fade=t=in:st={b0}:d=0.2:alpha=1,fade=t=out:st={round(b1-0.2,3)}:d=0.2:alpha=1[fundo];"
      f"[bB]scale=1080:-2,format=yuva420p,fade=t=in:st={b0}:d=0.2:alpha=1,fade=t=out:st={round(b1-0.2,3)}:d=0.2:alpha=1[frente];"
      f"[0:v][fundo]overlay=0:0:enable='between(t,{b0},{b1})':eof_action=pass[s0];[s0][frente]overlay=0:(H-h)/2-80:enable='between(t,{b0},{b1})':eof_action=pass[s1];"
      f"[s1][1:v]overlay=0:0:enable='lt(t,{DA})'[b0]")
k = 3
for j, (a, b, t, d) in enumerate(LEG):
    legenda(t, d, f'l{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{j}.png']
    vf += f";[b{j}][{k}:v]overlay=0:0:enable='between(t,{round(a,3)},{round(b-0.04,3)})'[b{j+1}]"; k += 1
# título do blooper (entra e fica até o fim)
im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
pilula(d, 330, 'ERROS DE GRAVAÇÃO', F('Black', 76), OURO + (255,), (10,60,32), 58); pilula(d, 440, 'acontece nas melhores famílias kkkk', F('Bold', 44), VERDE + (240,), BR, 40)
a_ = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s_ = Image.new('RGBA', (W, H), (0,0,0,0)); s_.putalpha(a_); Image.alpha_composite(s_, im).save(f'{S}/bloop.png')
ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/bloop.png']; nl = len(LEG)
vf += f";[b{nl}][{k}:v]overlay=0:0:enable='gte(t,{round(DA+0.25,3)})'[bf]"; k += 1
vf += f";[bf]fade=t=out:st={round(dur-0.4,3)}:d=0.4[vout]"
run(ent + ['-i', f'{S}/audio.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{k}:a', '-t', f'{dur}',
           '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-maxrate', '9M', '-bufsize', '18M', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
           f'{OUT}/REELS-STORY-natalia-iphone18-espera-com-blooper.mp4'])
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', dur, 'principal', DA, 'blooper', DB, 'broll', BROLL)
