# Assinatura sonora v8 (29/10/2026, ideia do Luiz): "BUM BUM BUM, Leilão no Zap" — batidas graves de cinema, com eco,
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


def montar(nome, batidas, v0):
    dur = v0 + len(voz) / SR + 0.45
    sil = [v0 + s / VEL for s in (0.0, 0.22, 0.43, 0.57)]
    mel = [(t0, nota(fq, 0.55 if i < 3 else 0.9)) for i, (t0, fq) in enumerate(zip(sil, MEL))]
    tambor = abafar(eco(mix(batidas, dur)))
    # a voz fica na frente: o eco do último BUM abaixa quando ela entra
    env = np.ones(len(tambor)); i = int(v0 * SR); env[i:] = np.maximum(0.35, np.exp(-(np.arange(len(env) - i) / SR) * 6))
    salvar(nome, tambor * env + mix([(v0, voz * 0.95)] + mel, dur))


MEL = [523.25, 659.25, 783.99, 1046.5]
# A: três BUM iguais e espaçados (bum · bum · BUM)
montar('opcao-A-bum-bum-bum', [(0.0, bum(0.8, 0.7)), (0.22, bum(0.88, 0.7)), (0.44, bum(1.0, 1.1, 90, 38))], 0.80)
# B: dois rápidos e um maior (bum-bum · BUM), o "tudum" com uma batida a mais
montar('opcao-B-bumbum-BUM', [(0.0, bum(0.75, 0.55)), (0.14, bum(0.85, 0.55)), (0.40, bum(1.0, 1.2, 88, 36))], 0.78)
print('ok')
