# Assinatura sonora v9 (29/10/2026, Luiz): o MARTELO continua sendo a batida; a Netflix é só referência de peso e eco.
# Cada batida = martelo da oficial inteiro (madeira, na frente) + estrondo grave por baixo + eco de sala grande. Base v8 — batidas graves de cinema, com eco,
# na SENSAÇÃO da abertura da Netflix, mas som próprio (nada copiado). Voz e melodia da oficial (v7).
import os, sys, subprocess, numpy as np
AQ = os.path.dirname(os.path.abspath(__file__))
SR = 48000
sys.argv = [sys.argv[0]]
src = open(os.path.join(AQ, '..', 'OFICIAL', 'fonte-montar.py')).read()
src = src.split("P1, P2, P3, V0")[0]          # só as ferramentas (ler, voz, martelo, nota, mix...) da oficial
exec(compile(src, 'oficial', 'exec'))


def bum(forca=1.0, cauda=0.9, f0=95, f1=42):
    """Estrondo grave: corpo que desce de f0 para f1 Hz + baque de ar filtrado + um pouco da madeira do martelo."""
    n = int(SR * cauda); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 9)
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (3.2 / cauda))
    ar = np.random.default_rng(3).normal(0, 1, n) * np.exp(-tt * 45)
    ar = np.convolve(ar, np.ones(240) / 240, mode='same') * 4              # tira o chiado, fica só o "tum"
    mad = np.zeros(n); m = martelo(0.8, 1.0); mad[:len(m)] = m[:n] * 0.07
    ataque = 1 - np.exp(-tt * 900)
    return norm((corpo * 1.0 + ar * 0.6 + mad) * ataque) * forca


def abafar(x, corte=700):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (fr / corte) ** 6)
    return np.fft.irfft(X, len(x))


def eco(x, mix=0.35):
    y = x.copy()
    for atraso, g in ((0.043, 0.55), (0.071, 0.4), (0.113, 0.3), (0.167, 0.2), (0.241, 0.12)):
        d = int(SR * atraso); y[d:] += x[:-d] * g * mix
    return y


def batida(forca=1.0, tom=1.0, cauda=0.8):
    m = martelo(tom, 1.0)
    g = bum(1.0, cauda, 80, 40)
    return m, g, forca


def montar(nome, batidas, v0):
    dur = v0 + len(voz) / SR + 0.45
    sil = [v0 + s / VEL for s in (0.0, 0.22, 0.43, 0.57)]
    mel = [(t0, nota(fq, 0.55 if i < 3 else 0.9)) for i, (t0, fq) in enumerate(zip(sil, MEL))]
    madeira = mix([(t, b[0] * b[2]) for t, b in batidas], dur)
    peso = abafar(mix([(t, b[1] * b[2] * 0.75) for t, b in batidas], dur), 300)
    tambor = eco(madeira + peso, 0.45)
    # a voz fica na frente: o eco do último BUM abaixa quando ela entra
    env = np.ones(len(tambor)); i = int(v0 * SR); env[i:] = np.maximum(0.35, np.exp(-(np.arange(len(env) - i) / SR) * 6))
    salvar(nome, tambor * env + mix([(v0, voz * 0.95)] + mel, dur))


MEL = [523.25, 659.25, 783.99, 1046.5]
# A: o ritmo da oficial (aprovado), POC POC POC com peso de cinema
montar('opcao-A-martelo-ritmo-oficial', [(0.0, batida(0.82, 1.0)), (0.15, batida(0.9, 0.96)), (0.30, batida(1.0, 0.92, 1.1))], 0.60)
# B: dois rápidos e um maior (o "tudum" com uma batida a mais), com o martelo
montar('opcao-B-martelo-tudum', [(0.0, batida(0.78, 1.0, 0.6)), (0.13, batida(0.86, 0.96, 0.6)), (0.38, batida(1.0, 0.9, 1.2))], 0.72)
print('ok')
