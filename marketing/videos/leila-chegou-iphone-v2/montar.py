"""Monta o vídeo feed 4:5 "Chegou no Zap!" v2 — Leila fiel, um só cenário, voz real dela.
Cena A (Kling): notificação -> surpresa -> abre a caixa -> tira o iPhone laranja.
Cena B (OmniHuman): Leila fala com a voz clonada, segurando o iPhone.
Uso: python3 montar.py cenaA.mp4 cenaB.mp4 saida.mp4 [corteA] [inicioA]"""
import subprocess, sys
a, b, out = sys.argv[1:4]
TA = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0   # quanto da cena A usar
A0 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0   # de onde começar a cena A
V1 = '../leila-chegou-iphone/'                          # camadas, efeitos e música da v1
W, H = 1080, 1350
def crop(src):  # 9:16 -> 4:5 centrado no rosto
    return f"scale={W}:-2,crop={W}:{H}:0:(ih-{H})*0.42,setsar=1,fps=30"
dur = lambda f: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
TB = dur(b); TF = 2.6
sB, sF = TA, TA + TB
TOT = sF + TF
V = lambda t: sB + t                                    # tempo da fala -> linha do tempo
cam = [('notif', 0.4, 3.2),
       ('leg1', V(0.1), V(3.1)), ('leg2', V(3.15), V(7.08)), ('data', V(4.15), V(7.08)),
       ('leg3', V(7.1), V(10.95)), ('lance', V(7.1), V(10.95)), ('leg4', V(11.0), sF),
       ('logo', sB, sF), ('fim', sF, TOT)]
inp = ['-i', a, '-i', b]
for n, _, _ in cam: inp += ['-loop', '1', '-i', f'{V1}camadas/{n}.png']
sfx = [('plim', 0.4, 1.0), ('fita', TA*0.45, 0.8), ('brilho', TA-1.6, 0.7), ('whoosh', sB-0.1, 0.5),
       ('pop', V(4.15), 0.7), ('pop', V(7.1), 0.7), ('martelo', V(3.6), 0.8), ('whoosh', sF-0.15, 0.6), ('martelo', sF+0.1, 0.6)]
ai = inp.count('-i')
inp += ['-i', b, '-i', V1+'musica.wav']
for f, _, _ in sfx: inp += ['-i', f'{V1}sfx/{f}.mp3']
fc = [f"[0:v]trim={A0}:{A0+TA},setpts=PTS-STARTPTS,{crop(0)}[va]",
      f"[1:v]setpts=PTS-STARTPTS,{crop(1)},split[vb][vb2]",
      f"[vb2]trim={TB-0.05}:{TB},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={TF},trim=0:{TF},setpts=PTS-STARTPTS,"
      f"zoompan=z='min(1+0.0009*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30[vf]",
      "[va][vb][vf]concat=n=3:v=1:a=0[b0]"]
prev = 'b0'
for i, (n, s, e) in enumerate(cam):
    fc.append(f"[{2+i}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,setpts=PTS+{s:.3f}/TB[L{i}]")
    fc.append(f"[{prev}][L{i}]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[o{i}]"); prev = f"o{i}"
fc.append(f"[{prev}]null[vout]")
fc.append(f"[{ai}:a]adelay={int(sB*1000)}|{int(sB*1000)},volume=1.0[vz]")
fc.append(f"[{ai+1}:a]atrim=0:{TOT},volume=0.14,afade=in:st=0:d=0.8,afade=out:st={TOT-1.2}:d=1.2[mu]")
mix = ['[vz]', '[mu]']
for j, (f, t, vol) in enumerate(sfx):
    fc.append(f"[{ai+2+j}:a]volume={vol},adelay={int(t*1000)}|{int(t*1000)}[s{j}]"); mix.append(f"[s{j}]")
fc.append(''.join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{TOT},alimiter=limit=0.95[aout]")
cmd = ['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]', '-t', f'{TOT:.2f}',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print('ok', round(TOT, 2), 's')
