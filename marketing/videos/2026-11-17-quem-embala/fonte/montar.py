# "Do clique até a sua casa" (17/11): pedido no sistema → etiqueta → embalagem acelerada → o Angel mostra o pacote e fala.
# Partes aceleradas sem o som original (só a trilha); a fala final em velocidade normal, com legenda.
# Privacidade: a lista de pedidos e a etiqueta são borradas (nomes e endereços de clientes nunca aparecem).
# Áudio: fala -16 LUFS; trilha 20 dB abaixo da fala por baixo dela e no máximo -24 LUFS sozinha.
# Uso: montar.py <pasta_dos_mp4_720> <trilha.mp3> <saida.mp4>
import os, sys, subprocess
IN, TRILHA, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
TMP = os.path.join(os.path.dirname(SAIDA), 'tmp-embala'); os.makedirs(TMP, exist_ok=True)
def run(*a): subprocess.run(a, check=True)
BASE = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,format=yuv420p'
BORRA = lambda y: f"split[a][b];[b]crop=iw:ih*{1-y:.2f}:0:ih*{y:.2f},boxblur=28:3[bb];[a][bb]overlay=0:H*{y:.2f}"
# (arquivo, início, fim, velocidade, filtro extra, texto na tela)
PARTES = [
 ('IMG_5763', 4.3, 6.8, 1.0, '', ''),                                   # gancho: o pacote pronto, ele sorrindo
 ('IMG_5291', 0.0, 6.0, 3.0, BORRA(0.36), '1. o seu pedido cai aqui'),
 ('IMG_5297', 0.0, 15.6, 4.0, BORRA(0.56), '2. a etiqueta sai na hora'),
 ('IMG_5757', 0.0, 21.7, 6.0, '', '3. tudo bem protegido'),
 ('IMG_5758', 0.0, 47.5, 8.0, '', ''),
 ('IMG_5759', 0.0, 15.7, 6.0, '', '4. caixa fechada'),
 ('IMG_5760', 0.0, 10.2, 6.0, '', '5. papel pardo e capricho'),
 ('IMG_5761', 0.0, 6.3, 6.0, '', ''),
 ('IMG_5762', 0.0, 8.3, 6.0, '', ''),
 ('IMG_5763', 0.0, 4.3, 3.0, '', ''),
 ('IMG_5764', 0.2, 10.85, 1.0, '', 'FALA'),
]
segs = []; t = 0.0; legendas = []; fala_ini = None
for i, (n, a, b, v, extra, txt) in enumerate(PARTES):
    out = f'{TMP}/p{i:02d}.mp4'; vf = f"trim={a}:{b},setpts=(PTS-STARTPTS)/{v},{BASE}" + (f',{extra}' if extra else '')
    run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{IN}/{n}.mp4', '-filter_complex', f'[0:v]{vf}[v]', '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', out)
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
    if txt == 'FALA': fala_ini = t
    elif txt: legendas.append((t, t + min(d, 3.2), txt))
    segs.append(out); t += d
total = t
open(f'{TMP}/lista.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/lista.txt', '-c', 'copy', f'{TMP}/video.mp4')

# legendas: gancho, passos e a fala do Angel (tempos da fala relativos ao corte 0.2 s)
def ts(x): return f'0:{int(x // 60):02d}:{x % 60:05.2f}'
FALA = [(0.07, 1.65, 'e o seu produto chega na sua casa'), (2.47, 3.81, 'e o responsável é o…'), (3.81, 5.6, 'Angel!'),
        (5.6, 8.15, 'pra precisar, estamos aqui: equipe Leilão no Zap'), (8.37, 10.6, 'é isso, família Leilão no Zap!')]
ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', '', '[V4+ Styles]',
 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
 'Style: G,Inter Display Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,8,3,8,60,60,330,1',
 'Style: P,Inter Display Black,70,&H0026411B,&H00FFFFFF,&H0051C4F5,&H0051C4F5,0,0,0,0,100,100,0,0,3,18,0,8,60,60,300,1',
 'Style: L,Inter Display Black,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,2,70,70,560,1', '', '[Events]',
 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
 r'Dialogue: 0,0:00:00.00,0:00:02.50,G,,0,0,0,,quem embala\N{\c&H51C4F5&}o seu pedido?']
for s, e, txt in legendas: ass.append(f'Dialogue: 0,{ts(s)},{ts(e)},P,,0,0,0,,{txt}')
for s, e, txt in FALA:
    txt = txt.replace('Leilão no Zap', r'{\c&H51C4F5&}Leilão no Zap{\c&HFFFFFF&}').replace('Angel!', r'{\c&H51C4F5&}Angel!{\c&HFFFFFF&}')
    ass.append(f'Dialogue: 0,{ts(fala_ini + s)},{ts(fala_ini + e)},L,,0,0,0,,{txt}')
open(f'{TMP}/leg.ass', 'w').write('\n'.join(ass) + '\n')

# áudio: fala do Angel tratada a -16 LUFS; trilha -24 LUFS e abaixa 20 dB por baixo da fala
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', '0.2', '-to', '10.85', '-i', f'{IN}/IMG_5764.mp4', '-vn', '-af',
    'highpass=f=90,equalizer=f=3200:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9', '-ar', '48000', '-ac', '2', f'{TMP}/fala.wav')
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-stream_loop', '-1', '-i', TRILHA, '-t', f'{total:.3f}', '-af', f'loudnorm=I=-24:TP=-3,afade=t=out:st={total - 1.2:.3f}:d=1.2', '-ar', '48000', '-ac', '2', f'{TMP}/trilha.wav')
fi = fala_ini
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{TMP}/trilha.wav', '-i', f'{TMP}/fala.wav', '-filter_complex',
    f"[0:a]volume='if(gte(t,{fi - .3:.2f}),0.32,1)':eval=frame[m];[1:a]adelay={int(fi * 1000)}|{int(fi * 1000)},apad[f];[m][f]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84[a]",
    '-map', '[a]', '-ar', '48000', f'{TMP}/mix.wav')
run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{TMP}/mix.wav', '-filter_complex',
    f"[0:v]ass={TMP}/leg.ass:fontsdir=/usr/share/fonts/opentype/inter[v]", '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA)
print('ok', SAIDA, round(total, 2), 'fala começa em', round(fala_ini, 2))
