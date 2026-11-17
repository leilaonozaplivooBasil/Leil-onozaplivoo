# "Hoje a gente tá no galpão" (17/11): chegada → produtos da loja → produtos sendo testados → tour acelerado →
# fala final "tudo que está no site está aqui". Partes aceleradas só com a trilha; a fala final em velocidade normal.
# Áudio: fala -16 LUFS; trilha -24 LUFS e 20 dB abaixo por baixo da fala. Uso: montar.py <pasta_mp4_720> <trilha> <saida>
import os, sys, subprocess
IN, TRILHA, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
TMP = os.path.join(os.path.dirname(SAIDA), 'tmp-galpao'); os.makedirs(TMP, exist_ok=True)
def run(*a): subprocess.run(a, check=True)
BASE = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p'
PARTES = [('IMG_5754', 1.5, 6.5, 2.0, ''), ('IMG_5755', 0.0, 18.0, 3.0, 'os produtos da loja'),
          ('IMG_3471', 0.0, 9.5, 3.0, 'e os que estão sendo testados'), ('IMG_3472', 0.0, 11.2, 3.0, ''), ('IMG_3470', 0.0, 8.2, 3.0, ''),
          ('IMG_5756', 0.0, 24.0, 4.0, 'tem de tudo um pouco'), ('IMG_5754', 15.0, 54.6, 5.0, '')]  # 17/11: a Natália pediu para tirar a fala final
segs = []; t = 0.0; leg = []; fala_ini = 0
for i, (n, a, b, v, txt) in enumerate(PARTES):
    out = f'{TMP}/p{i:02d}.mp4'
    run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{IN}/{n}.mp4', '-filter_complex', f'[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{v},{BASE}[v]',
        '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
    if txt == 'FALA': fala_ini = t
    elif txt: leg.append((t, t + min(d, 3.4), txt))
    segs.append(out); t += d
total = t
open(f'{TMP}/lista.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/lista.txt', '-c', 'copy', f'{TMP}/video.mp4')
def ts(x): return f'0:{int(x // 60):02d}:{x % 60:05.2f}'
ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', '', '[V4+ Styles]',
 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
 'Style: G,Inter Display Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,8,3,8,60,60,330,1',
 'Style: P,Inter Display Black,66,&H0026411B,&H00FFFFFF,&H0051C4F5,&H0051C4F5,0,0,0,0,100,100,0,0,3,18,0,8,60,60,300,1',
 'Style: L,Inter Display Black,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,2,70,70,560,1', '', '[Events]',
 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
 r'Dialogue: 0,0:00:00.00,0:00:02.50,G,,0,0,0,,hoje a gente\N{\c&H51C4F5&}tá no galpão']
for s, e, txt in leg: ass.append(f'Dialogue: 0,{ts(s)},{ts(e)},P,,0,0,0,,{txt}')
open(f'{TMP}/leg.ass', 'w').write('\n'.join(ass) + '\n')
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-stream_loop', '-1', '-i', TRILHA, '-t', f'{total:.3f}', '-af', f'loudnorm=I=-24:TP=-3,afade=t=out:st={total - 1.0:.3f}:d=1.0', '-ar', '48000', '-ac', '2', f'{TMP}/trilha.wav')
import shutil; shutil.copy(f'{TMP}/trilha.wav', f'{TMP}/mix.wav')
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{TMP}/mix.wav', '-filter_complex', f"[0:v]ass={TMP}/leg.ass:fontsdir=/usr/share/fonts/opentype/inter[v]",
    '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA)
print('ok', SAIDA, round(total, 2), 'fala em', round(fala_ini, 2))
