# Vídeo do Emanuel (selfie IMG_7435 + indicação IMG_7436) — leilão do iPhone 18 Pro Max, qua 11/11 às 20h.
# Uso: montar.py <pasta-fontes> <saida> <vendedores|instagram>. Instagram: sem o trecho da indicação (tem %) e sem o fim com '+5%' na TV.
# Pausas cortadas sem cortar fala, zoom alternado + punch/flash nas viradas, legenda em pílulas, música da playlist (pegada orla).
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT, VER = sys.argv[1], sys.argv[2], sys.argv[3]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR, FOGO = (27,122,72), (245,196,81), (10,20,16), (255,255,255), (243,91,18)
PROB = []
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
# (arquivo, início, fim, zoom, punch)
A_ = [('A', 0.00, 1.62, 1.00, False), ('A', 2.22, 4.52, 1.06, True), ('A', 4.85, 7.05, 1.00, True), ('A', 7.35, 12.50, 1.06, True),
      ('A', 13.15, 22.45, 1.00, True), ('A', 22.45, 32.75, 1.07, True)]
if VER == 'vendedores':
    SEGS = A_ + [('A', 32.80, 38.10, 1.00, True), ('B', 0.00, 5.05, 1.00, True), ('B', 5.30, 7.10, 1.06, True), ('B', 7.40, 12.65, 1.00, True),
                 ('B', 12.95, 15.70, 1.06, True), ('B', 16.00, 19.67, 1.00, True)]
else:
    SEGS = A_ + [('B', 16.00, 19.67, 1.00, True)]
def saida(arq, t):
    acc = 0.0
    for a_, a, b, *_ in SEGS:
        if a_ == arq and a - 0.001 <= t <= b + 0.001: return round(acc + t - a, 3)
        acc += b - a
    raise ValueError((arq, t))
dur = round(sum(b - a for _, a, b, *_ in SEGS), 3)
# voz tratada (wav separado, loudnorm sozinho)
for x in ('A', 'B'):
    eqv = 'highpass=f=85,equalizer=f=300:t=o:w=1.2:g=-2,equalizer=f=4200:t=o:w=1:g=-2,highshelf=f=8000:g=-3,'
    run(['-i', f'{S}/{x}1080.mov', '-vn', '-ac', '1', '-ar', '48000', '-af', eqv + 'afftdn=nf=-25,deesser=i=0.8:m=0.6:f=0.5,acompressor=threshold=-26dB:ratio=4:attack=8:release=180:knee=6:makeup=3,alimiter=limit=0.7:attack=3:release=60:level=false', f'{S}/{x}-voz.wav'])
    run(['-i', f'{S}/{x}-voz.wav', '-af', 'loudnorm=I=-17:TP=-3:LRA=6', '-ar', '48000', f'{S}/{x}-voz_ok.wav'])
ent = ['-i', f'{S}/A1080.mov', '-i', f'{S}/B1080.mov', '-i', f'{S}/A-voz_ok.wav', '-i', f'{S}/B-voz_ok.wav']; fc = ''; cat = ''
for i, (x, a, b, z, p) in enumerate(SEGS):
    vi, ai = (0, 2) if x == 'A' else (1, 3)
    zz = f"{z}*(1+0.12*max(0\\,1-t/0.28))" if p else f"{z}"
    fl = ",eq=brightness='0.45*max(0\\,1-t/0.12)':eval=frame" if (p and x == 'B' and SEGS[i-1][0] == 'A') else ''
    fc += (f"[{vi}:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=w='trunc(1080*{zz}/2)*2':h='trunc(1920*{zz}/2)*2':eval=frame,crop=1080:1920:(iw-1080)/2:(ih-1920)/2{fl},setsar=1,fps=30[v{i}];"
           f"[{ai}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={round(b-a-0.03,3)}:d=0.03[a{i}];")
    cat += f"[v{i}][a{i}]"
fc += cat + f"concat=n={len(SEGS)}:v=1:a=1[v][a]"
run(ent + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', f'{S}/base.mov'])
run(['-i', f'{S}/base.mov', '-vn', '-ac', '1', '-ar', '48000', f'{S}/voz_final.wav'])
m = f'{MK}/marca/trilhas-base/pegada-orla/04-funky-soul-house.mp3'
run(['-stream_loop', '-1', '-i', m, '-i', f'{S}/voz_final.wav', '-filter_complex',
     f"[0:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.22,afade=t=in:d=0.6,afade=t=out:st={dur-1.5}:d=1.5[m];"
     "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];"
     "[v][md]amix=inputs=2:duration=first:normalize=0", '-ar', '48000', f'{S}/audio_mix.wav'])
run(['-i', f'{S}/audio_mix.wav', '-af', 'loudnorm=I=-15:TP=-1.5:LRA=6', '-ar', '48000', f'{S}/audio.wav'])
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(f'"{t}" não cabe')
    x0 = (W - w) / 2 - raio + 8; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio - 16, y + raio), raio, fill=cor); d.text((W/2, y), t, font=f, fill=txt, anchor='mm')
def legenda(txt, dest, nome, y=1450):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    if txt: pilula(d, y, txt, F('Black', 54), VERDE + (245,), BR, 44); y += 102
    if dest: pilula(d, y, dest.upper(), F('Black', 64), OURO + (255,), (10,60,32), 48)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def selo():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
    d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
    f = F('Black', 34); t = 'IPHONE 18 · HOJE 20H'; w = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=FOGO + (240,)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
LA = [('A', 0.00, 1.62, 'ei, ei,', 'foca aqui!'), ('A', 2.22, 4.52, 'deixa eu falar', 'com você'),
      ('A', 4.85, 7.05, 'seja muito bem-vindo ao', 'Leilão no Zap'), ('A', 7.35, 12.50, 'a maior plataforma de', 'leilão do Brasil'),
      ('A', 13.15, 18.60, 'hoje tem leilão de um', 'iPhone 18 Pro Max'), ('A', 18.60, 22.45, None, 'lacradinho na caixa'),
      ('A', 22.45, 24.40, '1 ano de garantia', 'e nota fiscal'), ('A', 24.40, 27.85, 'faz seu cadastro', 'e dá o seu lance'),
      ('A', 27.85, 30.55, 'porque se você', 'piscar…'), ('A', 30.55, 32.75, 'vai perder essa', 'grande oportunidade!')]
if VER == 'vendedores':
    LA += [('A', 32.80, 34.25, 'vem pro', 'Leilão no Zap!'), ('A', 34.25, 36.70, 'me chama no privado', 'pra tirar dúvidas'),
           ('A', 36.70, 38.10, None, 'vão pra cima, pessoal!'), ('B', 0.00, 3.50, 'e você, que procura', 'uma renda extra?'),
           ('B', 3.50, 5.05, 'aqui no', 'Leilão no Zap'), ('B', 5.30, 7.10, 'você indica', 'e você ganha!'),
           ('B', 7.40, 10.30, 'indica 10 amigos', 'e ganha'), ('B', 10.30, 12.65, None, '10% de comissão'),
           ('B', 12.95, 15.70, 'em cima de cada depósito', 'feito na plataforma')]
LA += [('B', 16.00, 17.80, 'vem pro', 'Leilão no Zap!'), ('B', 17.80, 19.67, 'o leilão já tá', 'rolando!')]
LEG = [(saida(x, a), saida(x, b), t, d) for x, a, b, t, d in LA]
selo()
ent = ['-i', f'{S}/base.mov', '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png']; vf = '[0:v]eq=brightness=0.03:saturation=1.08,vignette=angle=0.4:eval=init,format=yuv420p[vg];[vg][1:v]overlay=0:0[b0]'; k = 2  # vinheta leve nos cantos, só no vídeo (selo e legendas por cima)
for j, (a, b, t, d) in enumerate(LEG):
    legenda(t, d, f'l{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{j}.png']
    vf += f";[b{j}][{k}:v]overlay=0:0:enable='between(t,{round(a,3)},{round(b-0.04,3)})'[b{j+1}]"; k += 1
vf += f";[b{len(LEG)}]fade=t=out:st={round(dur-0.35,3)}:d=0.35[vout]"
run(ent + ['-i', f'{S}/audio.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{k}:a', '-t', f'{dur}',
           '-c:v', 'libx264', '-crf', '22', '-preset', 'medium', '-maxrate', '9M', '-bufsize', '18M', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
           f'{OUT}/REELS-emanuel-iphone18-hoje-' + VER.upper() + '.mp4'])
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', dur)
