# Assinatura sonora v4 (29/10/2026, pedido do Luiz): TRÊS batidas e martelo mais GRAVE. Base: v3 do Leilão NoZap (28/10/2026): POC POC + "Leilão no Zap!" (voz oficial do Leiloeiro, vídeo da roleta).
# Melhorias: martelada encorpada (madeira + grave + estalo), 2ª batida mais grave e mais forte (sensação de "fechou"),
# mini-melodia de 4 notas casada com as sílabas Lei-lão-no-Zap (vira a "melodia da marca"), cauda curta de ambiente,
# volume no padrão do Instagram (-14 LUFS). Gera 4 cortes: completa, sem melodia, só POC POC e instrumental.
import subprocess, numpy as np, wave, os
SR = 48000
AQ = os.path.dirname(os.path.abspath(__file__))
VID = '/home/user/leilonozap/public/leilao20/video1-v2-leve.mp4'
MART = '/home/user/Leil-onozaplivoo/marketing/videos/flamengo-hoje-18h/sfx/martelo.mp3'


def ler(arq, ini=None, fim=None, filtro=None):
    cmd = ['ffmpeg', '-v', 'error', '-y']
    if ini is not None:
        cmd += ['-ss', str(ini), '-to', str(fim)]
    cmd += ['-i', arq, '-vn', '-ac', '1', '-ar', str(SR)]
    if filtro:
        cmd += ['-af', filtro]
    cmd += ['-f', 'f32le', '/tmp/claude-0/a.raw']
    subprocess.run(cmd, check=True)
    return np.fromfile('/tmp/claude-0/a.raw', dtype=np.float32).astype(float)


def norm(x):
    return x / (np.abs(x).max() + 1e-9)


# voz: "Leilão no Zap" (2,85–3,95 s do vídeo da roleta), 25% mais rápida, com corpo e presença
VEL = 1.25
voz = norm(ler(VID, 2.85, 3.95, f'afade=t=in:d=0.012,afade=t=out:st=1.0:d=0.1,atempo={VEL},highpass=f=70,'
                                  'acompressor=threshold=-20dB:ratio=4:attack=3:release=80,equalizer=f=200:t=q:w=1:g=2,'
                                  'equalizer=f=3200:t=q:w=1.2:g=2.5'))

# martelada: madeira (amostra) + grave (corpo) + estalo (ataque)
base = norm(ler(MART, filtro='lowpass=f=1800,equalizer=f=120:t=q:w=1:g=6'))[:int(SR * 0.32)]
t = np.arange(int(SR * 0.32)) / SR
grave = np.sin(2 * np.pi * 58 * t) * np.exp(-t * 18)
estalo = np.random.default_rng(1).normal(0, 1, len(t)) * np.exp(-t * 260)


def martelo(tom=1.0, forca=1.0):
    m = base * 1.0 + grave * 1.1 + estalo * 0.06
    if tom != 1.0:  # muda a altura sem mudar o caráter (2ª batida mais grave = "fechou")
        idx = np.arange(0, len(m) - 1, tom)
        m = np.interp(idx, np.arange(len(m)), m)
    return norm(m) * forca


def nota(f, dur=0.5, amp=0.28):
    tt = np.arange(int(SR * dur)) / SR
    env = np.exp(-tt * 7) * (1 - np.exp(-tt * 600))
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 14) + 0.12 * np.sin(2 * np.pi * 4.01 * f * tt) * np.exp(-tt * 30)
    return amp * s * env


def ambiente(x, mix=0.18):
    """Cauda curta de 'sala' (3 reflexões amortecidas), só para não terminar seco."""
    y = x.copy()
    for atraso, g in ((0.031, 0.5), (0.057, 0.33), (0.089, 0.2)):
        d = int(SR * atraso)
        y[d:] += x[:-d] * g * mix * 3
    return y


def mix(eventos, dur):
    out = np.zeros(int(SR * dur))
    for t0, s in eventos:
        i = int(t0 * SR)
        n = min(len(s), len(out) - i)
        out[i:i + n] += s[:n]
    return out


def salvar(nome, x):
    x = ambiente(x)
    x = x / (np.abs(x).max() + 1e-9) * 0.95
    fade = int(SR * 0.06)
    x[-fade:] *= np.linspace(1, 0, fade)
    with wave.open('/tmp/claude-0/s.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/claude-0/s.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=7',
                    '-ar', '48000', '-ac', '2', '-b:a', '256k', f'{AQ}/{nome}.mp3'], check=True)


P1, P2, P3, V0 = 0.0, 0.15, 0.30, 0.53           # 1ª batida, 2ª batida, início da voz (o ritmo já aprovado)
# sílabas na voz acelerada (do reconhecimento de voz: Lei 0,00 · lão ~0,22 · no 0,43 · Zap 0,57 s, divididos por 1,25)
SIL = [V0 + s / VEL for s in (0.0, 0.22, 0.43, 0.57)]
MEL = [523.25, 659.25, 783.99, 1046.5]  # dó-mi-sol-dó (sobe e "abre", sensação de conquista)
dur = V0 + len(voz) / SR + 0.30
pocpoc = [(P1, martelo(0.78, 0.8)), (P2, martelo(0.74, 0.88)), (P3, martelo(0.64, 1.0))]
melodia = [(t0, nota(f, 0.55 if i < 3 else 0.9)) for i, (t0, f) in enumerate(zip(SIL, MEL))]

salvar('1-ASSINATURA-COMPLETA-pocpoc-leilao-no-zap-com-melodia', mix(pocpoc + [(V0, voz * 0.95)] + melodia, dur))
salvar('2-assinatura-sem-melodia', mix(pocpoc + [(V0, voz)], dur))
salvar('3-so-pocpoc-transicao', mix(pocpoc, 0.75))
salvar('4-instrumental-pocpoc-e-melodia-sem-voz', mix(pocpoc + [(t0, nota(f, 0.6 if i < 3 else 1.0, 0.5)) for i, (t0, f) in enumerate(zip(SIL, MEL))], dur + 0.2))
print('ok', round(dur, 2))
