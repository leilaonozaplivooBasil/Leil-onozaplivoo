# "É golpe?" completo (17/11): entrada (chuva de mensagens) + IMG_7490 + IMG_7492, sem pausas e respirações, sem cortar falas.
# Cortes = trechos de silêncio medidos pela energia do som (abaixo de 30% entre o piso e a fala, por 0,2 s ou mais),
# com 60 ms de folga de cada lado. Legenda queimada (palavras do Whisper conferidas à mão). Áudio: voz tratada e -16 LUFS.
# Uso: montar_completo.py <pasta_com_os_movs> <saida.mp4>
import sys, os, subprocess, wave, json
import numpy as np
IN, SAIDA = sys.argv[1], sys.argv[2]
AQ = os.path.dirname(os.path.abspath(__file__)); GANCHO = os.path.join(os.path.dirname(AQ), 'GANCHO-e-golpe-chuva-de-mensagens.mp4')
TMP = os.path.join(os.path.dirname(SAIDA), 'tmp-golpe'); os.makedirs(TMP, exist_ok=True)
run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def pausas(wav, minimo=.28, folga=.06):
    w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    hop = int(sr * .02); n = len(x) // hop; db = np.array([20 * np.log10(np.sqrt(np.mean(x[i*hop:(i+1)*hop] ** 2)) + 1e-9) for i in range(n)])
    piso, fala = np.percentile(db, 10), np.percentile(db, 80); q = db < piso + (fala - piso) * .30; out = []; i = 0
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]: j += 1
            if (j - i) * .02 >= minimo: out.append((i * .02 + folga, j * .02 - folga))
            i = j
        else: i += 1
    return out, n * .02

def manter(wav, ini, fim):
    """trechos que ficam: [ini, fim] menos as pausas"""
    ps, _ = pausas(wav); seg = []; t = ini
    for a, b in ps:
        if b <= ini or a >= fim: continue
        a, b = max(a, ini), min(b, fim)
        if a > t: seg.append((t, a))
        t = max(t, b)
    if fim > t: seg.append((t, fim))
    return [(round(a, 3), round(b, 3)) for a, b in seg if b - a > .08]

# legendas no tempo ORIGINAL de cada vídeo (Whisper medium, revisado)
LEG = {
 'IMG_7490': [('todo dia a gente recebe', 1.62, 3.3), ('esse tipo de mensagem', 3.3, 5.4), ('mas o golpe tá aí', 6.88, 8.62),
              ('cai quem quer', 8.98, 9.9), ('o golpe tá aí', 10.14, 11.28), ('cai quem quer', 11.64, 12.7)],
 'IMG_7492': [('aqui vou mostrar pra vocês', 0, 1.82), ('se é golpe, galera', 1.82, 3.3), ('em pleno sábado trabalhando', 3.3, 5.14),
              ('e aí, comenta com a gente:', 5.14, 6.88), ('é golpe ou não é?', 6.88, 8.1), ('claro que não, né', 8.32, 9.28),
              ('a gente é super real', 9.28, 10.42), ('e como é que é a emoção', 10.42, 12.62), ('da galera que arrematou?', 12.62, 13.8),
              ('seus amigos, o pessoal', 13.8, 15.28), ('tu entrega os produtos?', 15.28, 17.3), ('já entreguei várias vezes', 17.58, 18.86),
              ('em mão, gente!', 18.86, 19.6), ('é muito legal', 19.6, 20.8), ('tem vários vídeos, né, Natália', 20.8, 23.9),
              ('a gente, prova social', 23.92, 26.0), ('eles ficam encantados', 26.08, 28.4), ('aqui, gente, olha só', 28.54, 30.74),
              ('que legal!', 30.74, 31.42), ('e a Iara é diretora', 31.42, 33.32), ('de logística', 33.32, 34.28), ('agora o Gabriel', 34.28, 35.2),
              ('Gabriel, tu é golpe, Gabriel?', 35.2, 37.0), ('eu não sou golpe, não', 37.04, 38.5), ('que horas tu chegou', 39.06, 39.88),
              ('aqui pra trabalhar?', 39.88, 40.84), ('cheguei cedo', 40.84, 41.8), ('e que horas tu vai sair daqui?', 42.18, 43.4),
              ('vai embora depois das 21 horas', 44.12, 46.88), ('galera, respondendo WhatsApp', 46.88, 48.66), ('fazendo cadastro', 48.66, 49.9),
              ('estamos esperando vocês', 50.4, 52.28), ('Leilão no Zap', 52.28, 53.64), ('não é golpe!', 53.64, 54.6)],
}
CLIPES = [('IMG_7490', 1.28, 12.80), ('IMG_7492', 0.0, 54.66)]   # 7490: tira o "1, 2, 3" da contagem antes de gravar

def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h}:{m:02d}:{s:05.2f}'
ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', 'WrapStyle: 0', '',
       '[V4+ Styles]', 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       'Style: L,Inter Display Black,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,2,70,70,560,1', '',
       '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']

partes = []; t_saida = 5.5; plano = {}
partes.append(['-i', GANCHO])
filt = ['[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v0]', '[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]']; rot = ['[v0][a0]']; k = 1
for idx, (nome, ini, fim) in enumerate(CLIPES, start=1):
    wav = os.path.join(IN, nome + '.wav'); seg = manter(wav, ini, fim); plano[nome] = seg
    partes.append(['-i', os.path.join(IN, nome + '_1080.mp4')])
    for a, b in seg:
        d = b - a; f = .015
        filt.append(f'[{idx}:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=30,format=yuv420p[v{k}]')
        filt.append(f'[{idx}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d={f},afade=t=out:st={d - f:.3f}:d={f}[a{k}]')
        rot.append(f'[v{k}][a{k}]'); k += 1
    # remapeia as legendas: tempo original -> tempo no vídeo final
    def mapa(t):
        acc = t_saida
        for a, b in seg:
            if t < a: return acc
            if t <= b: return acc + (t - a)
            acc += b - a
        return acc
    for txt, s, e in LEG[nome]:
        s2, e2 = mapa(s), mapa(e)
        if e2 - s2 < .25: continue
        txt = txt.replace('golpe', r'{\c&H51C4F5&}golpe{\c&HFFFFFF&}').replace('Zap', r'{\c&H51C4F5&}Zap{\c&HFFFFFF&}')
        ass.append(f'Dialogue: 0,{ts(s2)},{ts(e2)},L,,0,0,0,,{txt}')
    t_saida += sum(b - a for a, b in seg)
open(f'{TMP}/leg.ass', 'w').write('\n'.join(ass) + '\n')
filt.append(''.join(rot) + f'concat=n={k}:v=1:a=1[vc][ac]')
filt.append(f"[vc]ass={TMP}/leg.ass:fontsdir=/usr/share/fonts/opentype/inter[vo]")
cmd = ['ffmpeg', '-y', '-v', 'error', '-filter_complex_threads', '1', '-threads', '2']
for p in partes: cmd += p
cmd += ['-filter_complex', ';'.join(filt), '-map', '[vo]', '-map', '[ac]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-c:a', 'pcm_s16le', f'{TMP}/bruto.mkv']
subprocess.run(cmd, check=True)
# voz: graves sujos fora, presença, compressor; volume final -16 LUFS num passe à parte (regra de áudio da marca)
run('ffmpeg', '-y', '-i', f'{TMP}/bruto.mkv', '-vn', '-af', 'highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,alimiter=limit=0.95', f'{TMP}/voz.wav')
run('ffmpeg', '-y', '-i', f'{TMP}/voz.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9', '-ar', '48000', f'{TMP}/voz_n.wav')
run('ffmpeg', '-y', '-i', f'{TMP}/bruto.mkv', '-i', f'{TMP}/voz_n.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA)
json.dump(plano, open(f'{TMP}/cortes.json', 'w')); print('ok', SAIDA, 'duração', round(t_saida, 2))
