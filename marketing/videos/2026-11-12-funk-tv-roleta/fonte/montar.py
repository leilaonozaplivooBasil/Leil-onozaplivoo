# Vídeo curto (IMG_3291): foco na pessoa dançando e na TV com a roleta; parede, antena e fios escurecidos/sem cor nas bordas.
# Áudio: o som enviado (Deck_Boutique_Gourmet) + batida de funk sintetizada no tempo da voz (129 bpm, 1º tempo em 0,19 s).
# Fio da parede apagado antes (tirar_fio.py -> <pasta>/limpo.mov). Tela: 'ATENÇÃO!!' (verde, sem fita) e depois 'VEM QUE VEM!' palavra por palavra, na batida, nas cores da marca.
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
# letreiros quadro a quadro: ATENÇÃO!! (verde) e depois VEM · QUE · VEM! entrando uma palavra por batida
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO, VERDE, NOITE, BR = (245, 196, 81), (27, 122, 72), (8, 30, 20), (255, 255, 255)
import os; os.makedirs(f'{S}/ov', exist_ok=True)
def sombra(im, r=16, a=0.55):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v*a)))
    o = Image.new('RGBA', (im.width, im.height + 12), (0, 0, 0, 0)); o.alpha_composite(sh, (0, 12)); o.alpha_composite(im); return o
def placa_atencao():
    f = F('Black', 118); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = d0.textlength('ATENÇÃO!!', font=f); h = 178; ic = 150
    im = Image.new('RGBA', (int(w + 110 + ic), h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 20, im.width-1, 20+h), 44, fill=VERDE, outline=OURO, width=6)
    cx, cy, r = 40 + ic/2 - 8, 20 + h/2 + 6, 58
    d.polygon([(cx, cy-r), (cx+r*1.12, cy+r*0.82), (cx-r*1.12, cy+r*0.82)], fill=OURO); d.text((cx, cy+14), '!', font=F('Black', 66), fill=NOITE, anchor='mm')
    d.text((60 + ic + w/2 - 10, 20 + h/2 + 4), 'ATENÇÃO!!', font=f, fill=BR, anchor='mm')
    return sombra(im)
def palavra(t, cor_txt, fundo, tam):
    f = F('Black', tam); d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1))); w = d0.textlength(t, font=f); h = int(tam*1.25)
    im = Image.new('RGBA', (int(w + 70), h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 15, im.width-1, 15+h), 34, fill=fundo); d.text((im.width/2, 15 + h/2 + 4), t, font=f, fill=cor_txt, anchor='mm')
    return sombra(im, 14)
PA = placa_atencao()
VEM1, QUE, VEM2 = palavra('VEM', OURO, VERDE, 150), palavra('QUE', BR, NOITE, 110), palavra('VEM!', NOITE, OURO, 170)
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
def poe(fr, im, cx, cy, s_, rot=0):
    if s_ <= 0.02: return
    r = im.resize((max(1, int(im.width*s_)), max(1, int(im.height*s_))), Image.LANCZOS)
    if rot: r = r.rotate(rot, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(r, (int(cx - r.width/2), int(cy - r.height/2)))
TV1, TV2, TV3 = T1 + 4*BAT, T1 + 5*BAT, T1 + 6*BAT  # 2,05 · 2,51 · 2,97 s: uma palavra por batida
for k in range(round(DUR*30)):
    t = k/30; fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fase = ((t - T1) % BAT)/BAT if t >= T1 else 1; pulso = 1 + 0.06*max(0, 1 - fase*4)
    if T1 <= t < TV1 - 0.05:
        sx = int(12*math.sin(t*70)*max(0, 1 - (t-T1)/0.4)); sai = max(0, (t - (TV1 - 0.2))/0.15)
        poe(fr, PA, W/2 + sx, 1700, pop((t - T1)/0.3)*pulso*(1 - sai))
    if t >= TV1:
        poe(fr, VEM1, W/2 - 255, 1640, pop((t - TV1)/0.28)*(pulso if t >= TV3 else 1), -6)
    if t >= TV2:
        poe(fr, QUE, W/2 + 250, 1610, pop((t - TV2)/0.28)*(pulso if t >= TV3 else 1), 5)
    if t >= TV3:
        poe(fr, VEM2, W/2 + 10, 1790, pop((t - TV3)/0.3)*pulso, -3)
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
