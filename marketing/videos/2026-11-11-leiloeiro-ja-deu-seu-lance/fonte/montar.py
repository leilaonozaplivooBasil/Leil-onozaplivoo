# Vídeo 10 s "JÁ DEU O SEU LANCE?" — leiloeiro falando (clipes oficiais do site, voz e boca sincronizadas) + iPhone 18 de hoje.
# Clipes de public/leilao20 vêm com a máscara ao lado (metade esquerda = cor, direita = alfa). Sem créditos de IA.
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
S, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-09/quarta-11-11-iphone18/fonte')
import importlib.util
spec = importlib.util.spec_from_file_location('A', '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-09/quarta-11-11-iphone18/fonte/artes_hoje_lib.py'); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
W, H, FPS = 1080, 1920, 30
def run(a): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + a, check=True)
FUNDO = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-09/quarta-11-11-iphone18/fonte/fundo-texto.jpg'
PODIO = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-09/quarta-11-11-iphone18/fonte/fundo-podio.jpg'
def fundo(path, nome):
    sc = Image.open(path).convert('RGB'); e = H/sc.height; sc = sc.resize((round(sc.width*e), H), Image.LANCZOS); x = (sc.width-W)//2
    sc.crop((x, 0, x+W, H)).save(f'{S}/{nome}.png'); return f'{S}/{nome}.png'
def camada(nome, desenho):
    b = Image.new('RGBA', (W, H), (0,0,0,0)); desenho(b); b.save(f'{S}/{nome}.png'); return f'{S}/{nome}.png'
fT = fundo(FUNDO, 'bgT'); fP = fundo(PODIO, 'bgP')
SEG = []
# 1 — "Ei, você tá aí?" (vídeo do palco do site, 0–1,7 s), corte vertical com zoom chegando
t1 = camada('t1', lambda b: (A.logo(b), A.OURO_T(b, (W/2, 1560), 'EI, VOCÊ TÁ AÍ?', A.F('Black', 120))))
run(['-ss', '0', '-t', '1.7', '-i', f'{S}/fala.mp4', '-i', t1, '-filter_complex',
     f"[0:v]crop=460:624:90:0,scale=1080:1466:flags=lanczos,scale=w='trunc(1080*(1.0+0.06*t)/2)*2':h=-2:eval=frame,crop=1080:1466,pad=1080:1920:0:120:color=0x06100b,fps={FPS}[v];[v][1:v]overlay=0:0,format=yuv420p[o]",
     '-map', '[o]', '-map', '0:a', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', f'{S}/seg1.mov']); SEG.append('seg1')
def leiloeiro(clip, bg, txt, nome, x, y, alt):
    run(['-loop', '1', '-i', bg, '-i', f'{S}/{clip}.mp4', '-i', txt, '-filter_complex',
         f"[1:v]split[a][b];[a]crop=iw/2:ih:0:0[c];[b]crop=iw/2:ih:iw/2:0,format=gray[m];[c][m]alphamerge,scale=-2:{alt}:flags=lanczos[p];"
         f"[0:v][p]overlay={x}:{y}:shortest=1[s];[s][2:v]overlay=0:0,fps={FPS},format=yuv420p[o]",
         '-map', '[o]', '-map', '1:a', '-t', '2.83', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', f'{S}/{nome}.mov']); SEG.append(nome)
# 2 — "Segura essa emoção!" + JÁ DEU O SEU LANCE?
def d2(b):
    A.logo(b); A.T(b, (W/2, 330), 'JÁ DEU O', A.F('Black', 150), A.BR); A.OURO_T(b, (W/2, 500), 'SEU LANCE?', A.F('Black', 170))
    A.pil(b, W/2, 650, 'O LEILÃO ACABA HOJE À NOITE', A.F('Black', 44))
leiloeiro('personagem-empurra-segura-emocao', fT, camada('t2', d2), 'seg2', '130', 'H-h', 1500)
# 3 — "Vamos ver o que sai! Bora!" + as 3 cores do iPhone 18 no pódio, leiloeiro no canto
def d3(b):
    A.logo(b); A.T(b, (W/2, 300), 'iPHONE 18', A.F('Black', 150), A.BR); A.OURO_T(b, (W/2, 450), 'PRO MAX', A.F('Black', 150))
    A.pil(b, W/2, 590, 'LACRADO · VOCÊ ESCOLHE A COR', A.F('Black', 40))
    base = int(0.765*H)+6; A.luz(b, W/2, base-300, 280)
    A.poe(b, A.fone('glacial', 400), W/2-230, base-30, False); A.poe(b, A.fone('silver', 400), W/2+230, base-30, False); A.poe(b, A.fone('bordo', 540), W/2, base)
    A.pil(b, W/2, 1700, 'LANCE INICIAL  R$ 197,00', A.F('Black', 46), fundo=A.FLOR, cor=A.BR, borda=A.OURO, h=96)
leiloeiro('personagem-empurra-vamos-ver', fP, camada('t3', d3), 'seg3', 'W-w+10', '1230', 520)
# 4 — final: ACABA HOJE ÀS 20H + botão (2,64 s, música e o "toc")
def d4(b):
    A.logo(b); A.T(b, (W/2, 520), 'ACABA', A.F('Black', 200), A.BR); A.OURO_T(b, (W/2, 720), 'HOJE ÀS 20H', A.F('Black', 160))
    A.pil(b, W/2, 900, 'QUEM DER MAIS, LEVA', A.F('Black', 52), fundo=A.FLOR, cor=A.OURO, borda=A.OURO)
    A.poe(b, A.fone('bordo', 520), W/2, 1520); A.luz(b, W/2, 1250, 220, 70)
    A.pil(b, W/2, 1700, 'DÊ SEU LANCE · leilaonozap.net', A.F('Black', 44), fundo=A.OURO, cor=A.NOITE, borda=None, h=108)
run(['-loop', '1', '-t', '2.64', '-i', fT, '-loop', '1', '-t', '2.64', '-i', camada('t4', d4), '-f', 'lavfi', '-t', '2.64', '-i', 'anullsrc=r=48000:cl=stereo', '-filter_complex',
     f"[1:v]scale=w='trunc(1080*(1.12-0.12*min(1\\,t/0.35))/2)*2':h=-2:eval=frame,crop=1080:1920:(iw-1080)/2:(ih-1920)/2[t];[0:v][t]overlay=0:0,fps={FPS},format=yuv420p[o]",
     '-map', '[o]', '-map', '2:a', '-t', '2.64', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-c:a', 'pcm_s16le', f'{S}/seg4.mov']); SEG.append('seg4')
# junta com flash/zoom nas viradas, música de auditório baixinha por baixo (ducking na voz)
open(f'{S}/lista.txt', 'w').write(''.join(f"file '{S}/{s}.mov'\n" for s in SEG))
run(['-f', 'concat', '-safe', '0', '-i', f'{S}/lista.txt', '-c', 'copy', f'{S}/base.mov'])
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{S}/base.mov'], capture_output=True, text=True).stdout)
viradas = [1.7, 4.53, 7.36]
fl = ','.join(f"eq=brightness='0.5*max(0\\,1-(t-{v})/0.12)*gte(t\\,{v})':eval=frame" for v in viradas)
run(['-i', f'{S}/base.mov', '-stream_loop', '-1', '-i', f'{S}/musica.mp3', '-filter_complex',
     f"[0:v]{fl},fade=t=out:st={dur-0.3}:d=0.3[v];[0:a]asplit[vz][sc];[1:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.30,afade=t=out:st={dur-0.8}:d=0.8[m];"
     "[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=300[md];[vz][md]amix=inputs=2:duration=first:normalize=0,volume=1.25[a]",
     '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', f'{OUT}/REELS-STORY-leiloeiro-ja-deu-seu-lance-10s.mp4'])
print('ok', round(dur, 2), A.PROB)
