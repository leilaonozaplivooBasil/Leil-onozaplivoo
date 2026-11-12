# Vídeo curto (IMG_3291): foco na pessoa dançando e na TV com a roleta; parede, antena e fios escurecidos/sem cor nas bordas.
# Áudio: o som enviado (Deck_Boutique_Gourmet) + batida de funk sintetizada (batida_funk.py). Uso: montar.py <pasta-trabalho> <saida.mp4>
import sys, subprocess
from PIL import Image, ImageDraw, ImageFilter
S, OUT = sys.argv[1:3]; F0 = '/home/user/Leil-onozaplivoo/marketing/videos/2026-11-12-funk-tv-roleta/fonte'
W, H = 1080, 1920; VEL = 0.88; DUR = round(3.345/VEL, 2)
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
# máscara de foco: TV inteira + a pessoa (elipse), bordas bem suaves
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
d.rounded_rectangle((-20, 175, W+20, 935), 30, fill=255)
d.ellipse((190, 960, 890, 2060), fill=255)
m.filter(ImageFilter.GaussianBlur(70)).save(f'{S}/mascara.png')
subprocess.run(['python3', f'{F0}/batida_funk.py', f'{S}/batida.wav', str(DUR + 0.3), '130'], check=True)
tm = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
v = (f"[0:v]{tm},scale={W}:{H},setsar=1,setpts=PTS/{VEL},fps=30,eq=contrast=1.06:saturation=1.12:brightness=0.01,split[a][b];"
     "[b]eq=brightness=-0.30:saturation=0.25,gblur=sigma=8[fundo];"
     "[1:v]format=gray,scale=1080:1920[m];[a][m]alphamerge[frente];[fundo][frente]overlay=0:0,"
     "vignette=angle=0.55,format=yuv420p[vout]")
a = (f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.0,apad,atrim=0:{DUR},asetpts=N/SR/TB[voz];"
     f"[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45,atrim=0:{DUR},afade=t=out:st={DUR-0.35}:d=0.35,asetpts=N/SR/TB[bat];"
     "[voz][bat]amix=inputs=2:duration=first:normalize=0[aout]")
run(['-i', f'{F0}/v.mov', '-loop', '1', '-i', f'{S}/mascara.png', '-i', f'{F0}/audio-enviado.m4a', '-i', f'{S}/batida.wav',
     '-filter_complex', v + ';' + a, '-map', '[vout]', '-map', '[aout]', '-t', str(DUR), '-ar', '48000', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
     '-c:a', 'pcm_s16le', f'{S}/pre.mov'])
run(['-i', f'{S}/pre.mov', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT])
print('ok', DUR)
