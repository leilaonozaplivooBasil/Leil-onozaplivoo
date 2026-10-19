"""Monta o vídeo feed 4:5 "Chegou no Zap!" a partir das cenas animadas, da voz, dos efeitos e das camadas de texto.
Uso: python3 montar.py cena3_com_boca.mp4 saida.mp4"""
import subprocess, sys
c3, out = sys.argv[1], sys.argv[2]
W,H=1080,1350
CROP="crop=1072:1340:0:294,scale=1080:1350,setsar=1,fps=30"
T1, T2, T3, TF = 2.6, 3.8, 9.15, 2.6           # durações das cenas e da tela final
s2, s3, sF = T1, T1+T2, T1+T2+T3
TOT = sF+TF
k = 1/1.035                                   # fala B acelerada 3,5%
B = lambda t: s3 + (t-3.34)*k                  # tempo da fala original -> linha do tempo
cam = [  # (camada, início, fim)
  ('notif', 0.25, 2.5), ('logo', s2, sF),
  ('leg1', s2+0.3, s3), ('leg2', s3, B(7.75)), ('data', B(4.5), B(7.78)),
  ('leg3', B(7.78), B(11.4)), ('lance', B(7.78), B(11.4)), ('leg4', B(11.4), sF), ('fim', sF, TOT)]
inp = ['-i','anim1.mp4','-i','anim2.mp4','-i',c3]
for n,_,_ in cam: inp += ['-loop','1','-i',f'camadas/{n}.png']
sfx = [('sfx/plim.mp3',0.25,1.0),('sfx/fita.mp3',s2,0.8),('sfx/brilho.mp3',s2+0.4,0.6),('sfx/martelo.mp3',B(3.824),0.9),
       ('sfx/pop.mp3',B(4.5),0.7),('sfx/pop.mp3',B(7.78),0.7),('sfx/whoosh.mp3',sF-0.15,0.6),('sfx/martelo.mp3',sF+0.1,0.6)]
ai = inp.count('-i')
inp += ['-i','voz-A.mp3','-i','voz-B2.mp3','-i','musica.wav']
for f,_,_ in sfx: inp += ['-i',f]
fc = [f"[0:v]trim=0:{T1},setpts=PTS-STARTPTS,{CROP}[v1]",
      f"[1:v]trim=0.2:{0.2+T2},setpts=PTS-STARTPTS,{CROP}[v2]",
      f"[2:v]trim=0:{T3},setpts=PTS-STARTPTS,{CROP},split[v3][v3b]",
      f"[v3b]trim={T3-0.04}:{T3},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={TF},trim=0:{TF},setpts=PTS-STARTPTS,zoompan=z='min(1+0.0009*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30[vf]",
      "[v1][v2][v3][vf]concat=n=4:v=1:a=0[b0]"]
prev='b0'
for i,(n,a,b) in enumerate(cam):
    fc.append(f"[{3+i}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,setpts=PTS+{a:.3f}/TB[L{i}]")
    fc.append(f"[{prev}][L{i}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[o{i}]"); prev=f"o{i}"
fc.append(f"color=white:s={W}x{H}:d={TOT},format=rgba,colorchannelmixer=aa=0.5[w]")
fc.append(f"[{prev}][w]overlay=enable='between(t,{B(3.824):.3f},{B(3.824)+0.1:.3f})'[vout]")
# áudio
fc.append(f"[{ai}:a]adelay={int((s2+0.3)*1000)}|{int((s2+0.3)*1000)},volume=1.0[va]")
fc.append(f"[{ai+1}:a]adelay={int(s3*1000)}|{int(s3*1000)},volume=1.0[vb]")
fc.append(f"[{ai+2}:a]atrim=0:{TOT},volume=0.16,afade=in:st=0:d=0.8,afade=out:st={TOT-1.2}:d=1.2[mu]")
mix=['[va]','[vb]','[mu]']
for j,(f,t,vol) in enumerate(sfx):
    fc.append(f"[{ai+3+j}:a]volume={vol},adelay={int(t*1000)}|{int(t*1000)}[s{j}]"); mix.append(f"[s{j}]")
fc.append(''.join(mix)+f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{TOT},alimiter=limit=0.95[aout]")
cmd=['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[vout]','-map','[aout]','-t',f'{TOT:.2f}',
     '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',out]
subprocess.run(cmd,check=True); print('ok', round(TOT,2), 's')
