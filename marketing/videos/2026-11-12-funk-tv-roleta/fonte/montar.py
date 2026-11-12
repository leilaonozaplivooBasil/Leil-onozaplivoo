# Vídeo curto (IMG_3291): foco na pessoa dançando e na TV com a roleta; parede, antena e fios escurecidos/sem cor nas bordas.
# Áudio: o som enviado (Deck_Boutique_Gourmet) + batida de funk sintetizada no tempo da voz (129 bpm, 1º tempo em 0,19 s).
# Fio da parede apagado antes (tirar_fio.py -> <pasta>/limpo.mov). Tela: 'ATENÇÃO!!' e 'GIRA A ROLETA!' pulsando na batida.
# Uso: montar.py <pasta-trabalho> <saida.mp4>
import sys, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
S, OUT = sys.argv[1:3]; F0 = '/home/user/Leil-onozaplivoo/marketing/videos/2026-11-12-funk-tv-roleta/fonte'
W, H = 1080, 1920; VEL = 0.88; DUR = round(3.345/VEL, 2)
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
# máscara de foco: TV inteira + a pessoa (elipse), bordas bem suaves
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
d.rounded_rectangle((-20, 175, W+20, 935), 30, fill=255)
d.ellipse((190, 960, 890, 2060), fill=255)
m.filter(ImageFilter.GaussianBlur(70)).save(f'{S}/mascara.png')
BPM, T1 = 129.3, 0.19; BAT = 60/BPM
subprocess.run(['python3', f'{F0}/tirar_fio.py', f'{F0}/v.mov', f'{S}/limpo.mov'], check=True)
subprocess.run(['python3', f'{F0}/batida_funk.py', f'{S}/batida.wav', str(DUR + 0.3), str(BPM), str(T1)], check=True)
# letreiros quadro a quadro: ATENÇÃO!! (0,19 s) e GIRA A ROLETA! (2,05 s), pulando em cada batida
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO, PRETO, VERM, BR = (245, 196, 81), (12, 12, 10), (230, 40, 40), (255, 255, 255)
import os; os.makedirs(f'{S}/ov', exist_ok=True)
def placa(txt, cor_fundo, cor_txt, tam, icone):
    f = F('Black', tam); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = d0.textlength(txt, font=f); h = tam + 60; ic = h if icone else 0
    im = Image.new('RGBA', (int(w + 90 + ic), h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 20, im.width-1, 20+h), 28, fill=cor_fundo)
    if icone:
        cx, cy, r = 30 + ic/2 - 6, 20 + h/2 + 4, h*0.36
        d.polygon([(cx, cy-r), (cx+r*1.1, cy+r*0.8), (cx-r*1.1, cy+r*0.8)], fill=VERM); d.text((cx, cy+r*0.18), '!', font=F('Black', int(r*1.1)), fill=BR, anchor='mm')
    d.text((45 + ic + w/2 - 10, 20 + h/2 + 3), txt, font=f, fill=cor_txt, anchor='mm')
    return im
P1 = placa('ATENÇÃO!!', OURO, PRETO, 120, True); P2 = placa('GIRA A ROLETA!', (27, 122, 72), BR, 96, False)
def fita(y):  # fita zebrada preta e dourada
    im = Image.new('RGBA', (W + 200, 54), PRETO + (255,)); d = ImageDraw.Draw(im)
    for x in range(-60, W + 260, 70): d.polygon([(x, 0), (x+35, 0), (x-19, 54), (x-54, 54)], fill=OURO)
    return im.rotate(-4, resample=Image.BICUBIC, expand=True)
FITA = fita(0)
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
for k in range(round(DUR*30)):
    t = k/30; fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fase = ((t - T1) % BAT)/BAT if t >= T1 else 1; pulso = 1 + 0.07*max(0, 1 - fase*4)
    if T1 <= t < 1.95:
        a = pop((t - T1)/0.3); sx = int(14*math.sin(t*70)*max(0, 1 - (t-T1)/0.4))
        ff = FITA.copy(); fr.alpha_composite(ff, (-100 + int((t-T1)*-260) % 70 - 70, 1555))
        s_ = a*pulso; im = P1.resize((max(1, int(P1.width*s_)), max(1, int(P1.height*s_)))); fr.alpha_composite(im, (W//2 - im.width//2 + sx, 1700 - im.height//2))
    if t >= 2.05:
        a = pop((t - 2.05)/0.3); s_ = a*pulso; im = P2.resize((max(1, int(P2.width*s_)), max(1, int(P2.height*s_)))); fr.alpha_composite(im, (W//2 - im.width//2, 1700 - im.height//2))
    fr.save(f'{S}/ov/o{k:04d}.png')

v = (f"[0:v]scale={W}:{H},setsar=1,setpts=PTS/{VEL},fps=30,eq=contrast=1.06:saturation=1.12:brightness=0.01,split[a][b];"
     "[b]eq=brightness=-0.30:saturation=0.25,gblur=sigma=8[fundo];"
     "[1:v]format=gray,scale=1080:1920[m];[a][m]alphamerge[frente];[fundo][frente]overlay=0:0,"
     "vignette=angle=0.55[vb];[4:v]format=rgba[ov];[vb][ov]overlay=0:0:shortest=1,format=yuv420p[vout]")
a = (f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0,apad,atrim=0:{DUR},asetpts=N/SR/TB[voz];"
     f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45,atrim=0:{DUR},afade=t=out:st={DUR-0.35}:d=0.35,asetpts=N/SR/TB[bat];"
     "[voz][bat]amix=inputs=2:duration=first:normalize=0[aout]")
run(['-i', f'{S}/limpo.mov', '-loop', '1', '-i', f'{S}/mascara.png', '-i', f'{F0}/audio-enviado.m4a', '-i', f'{S}/batida.wav', '-framerate', '30', '-i', f'{S}/ov/o%04d.png',
     '-filter_complex', v + ';' + a, '-map', '[vout]', '-map', '[aout]', '-t', str(DUR), '-ar', '48000', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
     '-c:a', 'pcm_s16le', f'{S}/pre.mov'])
run(['-i', f'{S}/pre.mov', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT])
print('ok', DUR)
