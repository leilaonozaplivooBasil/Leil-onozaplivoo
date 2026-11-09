# Vídeo Natália — leilão do iPhone 18 Pro Max (quarta 11/11, 20h). Começa no copy_50722 (fala), termina no "ATENÇÃO QUARTA-FEIRA".
# Durante as características e as cores entra o vídeo do banner do site (o mesmo que está no topo do leilaonozap.net).
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1], sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
BANNER = sys.argv[3]
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR = (27,122,72), (245,196,81), (10,20,16), (255,255,255)
PROB = []
SEGS = [(0.0, 19.4), (24.2, 33.95), (36.3, 54.1)]              # pausas longas cortadas (19,4→24,2 e 33,95→36,3)
def saida(t):                                                  # tempo do copy_50722 → tempo do vídeo final
    acc = 0.0
    for a, b in SEGS:
        if a <= t <= b: return round(acc + t - a, 3)
        acc += b - a
    raise ValueError(t)
DA = round(sum(b - a for a, b in SEGS), 3); DB = 4.5
CARD = (saida(4.9), saida(19.4))                               # vídeo do site: do "um iPhone 18 Pro Max" ao "frete grátis"
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(f'"{t}" não cabe')
    x0 = (W - w) / 2 - raio + 8; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio - 16, y + raio), raio, fill=cor); d.text((W/2, y), t, font=f, fill=txt, anchor='mm')
def legenda(txt, dest, nome, y):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    if txt: pilula(d, y, txt, F('Black', 56), VERDE + (245,), BR, 46); y += 106
    if dest: pilula(d, y, dest.upper(), F('Black', 66), OURO + (255,), (10,60,32), 50)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def selo():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
    d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
    f = F('Black', 34); t = 'IPHONE 18 · QUARTA 20H'; w = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=(243,91,18,240)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
def mascara():
    m = Image.new('L', (1000, 562), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 999, 561), 34, fill=255); m.save(f'{S}/mascara.png')
    s = Image.new('RGBA', (W, H), (0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle((40, 900, 1040, 1462), 34, fill=(0,0,0,150)); s.filter(ImageFilter.GaussianBlur(22)).save(f'{S}/sombra.png')
# (início, fim, texto, destaque) no tempo do copy_50722 — "hoje" da fala fica fora da legenda (o leilão é quarta)
LA = [(0.0, 2.1, 'olha a oportunidade', None), (2.1, 4.9, 'que você vai ter de', 'arrematar'),
      (4.9, 7.4, 'um', 'iPhone 18 Pro Max'), (7.4, 9.3, None, '256GB'), (9.3, 12.0, 'lacrado, novo e', 'com garantia'),
      (12.0, 15.1, 'quem arrematar', 'escolhe a cor'), (15.1, 17.7, 'Bordô, Glacial', 'ou Silver'), (17.7, 19.4, 'e ainda tem', 'frete grátis'),
      (24.2, 27.7, 'o lance começa em', 'R$ 197'), (27.7, 30.7, 'já imaginou arrematar', 'um iPhone desse'),
      (30.7, 33.95, 'por um valor abaixo', 'do preço de mercado?'),
      (36.3, 38.8, 'mas atenção:', 'só participa'), (38.8, 42.6, 'quem estiver cadastrado', 'e com lance confirmado'),
      (42.6, 44.6, 'então', 'não fica de fora!'), (44.6, 46.8, 'escreve IPHONE', 'aqui embaixo'),
      (46.8, 48.2, 'que eu te envio o link', None), (48.2, 50.4, 'faz o cadastro e', 'dá o seu lance'),
      (50.4, 54.1, 'o martelo bate', 'quarta às 20h')]
LB = [(0.0, 1.6, 'quarta é', 'o dia'), (1.6, DB, None, 'Leilão no Zap!')]
LEG = [(saida(a), saida(b), t, d) for a, b, t, d in LA] + [(DA + a, DA + b, t, d) for a, b, t, d in LB]
dur = round(DA + DB, 3)
# 1) base: os 3 pedaços da fala + o final, mesma voz tratada (wav separado, sem loudnorm junto com mix)
partes = ''.join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[2:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={round(b-a-0.04,3)}:d=0.04[a{i}];" for i, (a, b) in enumerate(SEGS))
fc = partes + f"[1:v]trim=0:{DB},setpts=PTS-STARTPTS[v3];[3:a]atrim=0:{DB},asetpts=PTS-STARTPTS[a3];" + "[v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[v][a]"
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{S}/in/A.mov','-i',f'{S}/in/B.mov','-i',f'{S}/A-voz_ok.wav','-i',f'{S}/B-voz_ok.wav','-filter_complex',fc,'-map','[v]','-map','[a]','-r','30','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','pcm_s16le',f'{S}/base.mov'], check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{S}/base.mov','-vn','-ac','1','-ar','48000',f'{S}/voz_final.wav'], check=True)
# 2) música baixinha embaixo da fala
m = f'{MK}/marca/trilhas-base/pegada-orla/02-nu-disco-por-do-sol.mp3'
subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','-1','-i',m,'-i',f'{S}/voz_final.wav','-filter_complex',
    f"[0:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.24,afade=t=in:d=0.8,afade=t=out:st={dur-2}:d=2[m];"
    "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];"
    "[v][md]amix=inputs=2:duration=first:normalize=0,volume=1.41",'-ar','48000',f'{S}/audio.wav'], check=True)
# 3) camadas: selo, cartão com o vídeo do site, legendas
selo(); mascara()
a0, a1 = CARD
ent = ['-i', f'{S}/base.mov', '-loop','1','-t',f'{dur}','-i',f'{S}/selo.png', '-stream_loop','-1','-i',BANNER, '-loop','1','-i',f'{S}/mascara.png', '-loop','1','-t',f'{dur}','-i',f'{S}/sombra.png']
# cena cheia (B-roll): o vídeo do site ocupa a tela, com o próprio vídeo desfocado atrás; a voz segue por baixo.
# (versão com cartão no meio foi descartada: cobria o rosto da Natália)
vf = (f"[2:v]setpts=PTS-STARTPTS+{a0}/TB,split[bA][bB];"
      f"[bA]scale=-2:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.12,format=yuva420p,fade=t=in:st={a0}:d=0.3:alpha=1,fade=t=out:st={round(a1-0.3,3)}:d=0.3:alpha=1[fundo];"
      f"[bB]scale=1080:-2,format=yuva420p,fade=t=in:st={a0}:d=0.3:alpha=1,fade=t=out:st={round(a1-0.3,3)}:d=0.3:alpha=1[frente];"
      f"[0:v][fundo]overlay=0:0:enable='between(t,{a0},{a1})':eof_action=pass[s0];[s0][frente]overlay=0:(H-h)/2-80:enable='between(t,{a0},{a1})':eof_action=pass[s1];"
      f"[s1][1:v]overlay=0:0[b0]")
for j, (a, b, t, d) in enumerate(LEG):
    y = 1430
    legenda(t, d, f'l{j}', y); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{j}.png']
    vf += f";[b{j}][{5+j}:v]overlay=0:0:enable='between(t,{round(a,3)},{round(b-0.04,3)})'[b{j+1}]"
n = len(LEG)
subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-i', f'{S}/audio.wav', '-filter_complex', vf, '-map', f'[b{n}]', '-map', f'{5+n}:a', '-t', f'{dur}',
    '-c:v','libx264','-crf','19','-preset','medium','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart', f'{OUT}/REELS-STORY-natalia-iphone18-quarta.mp4'], check=True)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', dur, 'cartão', CARD)
