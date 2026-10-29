# Assinatura sonora v10 "estúdio" (29/10/2026): o MARTELO com peso de cinema (referência de sensação: abertura da Netflix,
# pedida pelo Luiz), mixado como em estúdio. Batida em 4 camadas (estalo, madeira, corpo, grave de impacto), cada golpe
# levemente diferente (mão humana); reverb de sala grande em ESTÉREO por convolução; voz com presença, compressão e
# um toque de sala; melodia como sino suave aberto no estéreo; master com cola, limitador e -14 LUFS (padrão Instagram).
import os, sys, subprocess, wave, numpy as np
AQ = os.path.dirname(os.path.abspath(__file__))
SR = 48000
src = open(os.path.join(AQ, '..', 'OFICIAL', 'fonte-montar.py')).read().split("P1, P2, P3, V0")[0]
exec(compile(src, 'oficial', 'exec'))          # ler(), voz, base (amostra do martelo), nota(), norm()
rng = np.random.default_rng(29)


def fft_filtro(x, lo=None, hi=None, ordem=4):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9
    if hi: X *= 1 / np.sqrt(1 + (f / hi) ** (2 * ordem))
    if lo: X *= 1 / np.sqrt(1 + (lo / f) ** (2 * ordem))
    return np.fft.irfft(X, len(x))


def env(n, ataque, queda):
    t = np.arange(n) / SR
    return (1 - np.exp(-t / ataque)) * np.exp(-t / queda)


def golpe(forca=1.0, tom=1.0, peso=1.0):
    n = int(SR * 1.4); t = np.arange(n) / SR
    # 1) estalo: o "toc" que faz reconhecer o martelo (ruído curtinho, faixa 1,5–6 kHz)
    est = fft_filtro(rng.normal(0, 1, n), 1500, 6000) * env(n, 0.0004, 0.012)
    # 2) madeira: a amostra do martelo da oficial, com o tom do golpe
    idx = np.arange(0, len(base) - 1, tom); mad = np.zeros(n); m = np.interp(idx, np.arange(len(base)), base)[:n]; mad[:len(m)] = m
    # 3) corpo: ressonância da mesa (≈190 Hz) — dá o "peso" de madeira maciça
    corpo = np.sin(2 * np.pi * 190 * tom * t) * env(n, 0.001, 0.07) + 0.5 * np.sin(2 * np.pi * 290 * tom * t) * env(n, 0.001, 0.04)
    # 4) grave de impacto: desce de 110 para 42 Hz (o "tum" de cinema), cauda maior no golpe final
    f = 42 + 68 * np.exp(-t * 14)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.18 * peso)
    sub = np.tanh(sub * 1.6) / np.tanh(1.6)                      # leve saturação: o grave aparece até em celular
    g = est * 0.35 + norm(mad) * 0.9 + corpo * 0.45 + sub * 0.85 * peso
    return norm(g) * forca


def resposta_sala(seg=1.6, pre=0.022):
    """Impulso de sala grande, estéreo (L e R diferentes), agudos morrendo antes dos graves."""
    n = int(SR * seg); t = np.arange(n) / SR
    canais = []
    for semente in (1, 2):
        r = np.random.default_rng(semente).normal(0, 1, n) * np.exp(-t * 6.9 / seg)
        brilho = fft_filtro(r, 2500, None) * np.exp(-t * 14)        # agudo some rápido
        r = fft_filtro(r, 120, 2500) + brilho * 0.4
        r = np.concatenate([np.zeros(int(SR * pre)), r])
        canais.append(r / np.sqrt((r ** 2).sum()))
    return canais


def convolver(x, ir):
    n = len(x) + len(ir) - 1; N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]


def compressor(x, limiar=0.25, razao=3.0, ataque=0.003, solta=0.12):
    a, r = np.exp(-1 / (SR * ataque)), np.exp(-1 / (SR * solta)); e = 0.0; g = np.ones_like(x)
    ab = np.abs(x)
    for i in range(len(x)):
        e = a * e + (1 - a) * ab[i] if ab[i] > e else r * e + (1 - r) * ab[i]
        if e > limiar: g[i] = (limiar + (e - limiar) / razao) / e
    return x * g


def coloca(trilha, t0, s, ganho=1.0):
    i = int(t0 * SR); n = min(len(s), len(trilha) - i); trilha[i:i + n] += s[:n] * ganho


def voz_estudio():
    v = voz.copy()
    v = fft_filtro(v, 90, None, 2)                                  # tira o ronco
    X = np.fft.rfft(v); f = np.fft.rfftfreq(len(v), 1 / SR)
    X *= 1 + 0.6 * np.exp(-((f - 3200) / 1400) ** 2)                # presença (inteligível no celular)
    X *= 1 + 0.25 * np.exp(-((f - 180) / 90) ** 2)                  # corpo da voz
    X *= 1 - 0.35 * np.exp(-((f - 7200) / 1500) ** 2)               # tira o chiado do "s"
    v = np.fft.irfft(X, len(v))
    return compressor(norm(v) * 0.9, 0.22, 3.5, 0.002, 0.09)


def montar(nome, golpes, v0):
    dur = v0 + len(voz) / SR + 0.55
    n = int(dur * SR)
    bat = np.zeros(n)
    for t0, g in golpes:
        coloca(bat, t0, g)
    irL, irR = resposta_sala(1.7)
    salaL, salaR = convolver(bat, irL), convolver(bat, irR)
    # a sala abaixa quando a voz entra (a voz fica na frente)
    duck = np.ones(n); i = int(v0 * SR); duck[i:] = 0.45 + 0.55 * np.exp(-(np.arange(n - i) / SR) * 2.5)
    vz = np.zeros(n); coloca(vz, v0, voz_estudio())
    irvL, irvR = resposta_sala(0.6, 0.012)
    vzL = vz + convolver(vz, irvL) * 0.10; vzR = vz + convolver(vz, irvR) * 0.10
    sil = [v0 + s / VEL for s in (0.0, 0.22, 0.43, 0.57)]
    mel = [523.25, 659.25, 783.99, 1046.5]
    sino = np.zeros(n)
    for k, (t0, fq) in enumerate(zip(sil, mel)):
        coloca(sino, t0, nota(fq, 0.6 if k < 3 else 1.1, 0.22))
    sinoL, sinoR = np.roll(sino, int(SR * 0.008)), sino               # sino levemente aberto no estéreo
    L = bat * 1.0 + salaL * 0.42 * duck + vzL * 1.05 + sinoL * 0.55
    R = bat * 1.0 + salaR * 0.42 * duck + vzR * 1.05 + sinoR * 0.55
    est = np.stack([L, R], 1)
    est = est / np.abs(est).max() * 0.9
    fade = int(SR * 0.18); est[-fade:] *= np.linspace(1, 0, fade)[:, None]
    tmp = os.path.join(AQ, '_tmp.wav')
    with wave.open(tmp, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((est * 32767).astype(np.int16).tobytes())
    for ext, extra in (('wav', []), ('mp3', ['-b:a', '320k']), ('m4a', ['-c:a', 'aac', '-b:a', '256k'])):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af',
                        'acompressor=threshold=-14dB:ratio=2:attack=10:release=150:makeup=1.5,alimiter=limit=0.89:level=false,loudnorm=I=-14:TP=-1:LRA=7',
                        '-ar', '48000'] + extra + [os.path.join(AQ, f'{nome}.{ext}')], check=True)
    os.remove(tmp)


# A: ritmo da oficial aprovada (toc toc TOC), cada golpe um pouco mais grave e forte
montar('Jingle-v10-A-martelo-ritmo-oficial', [(0.00, golpe(0.80, 1.00, 0.55)), (0.15, golpe(0.88, 0.97, 0.65)), (0.30, golpe(1.00, 0.93, 1.4))], 0.62)
# B: o "tudum" com uma batida a mais (toc-toc · TOC), o último grande e ecoando
montar('Jingle-v10-B-martelo-tudum', [(0.00, golpe(0.78, 1.00, 0.55)), (0.13, golpe(0.86, 0.97, 0.65)), (0.40, golpe(1.00, 0.91, 1.6))], 0.78)
print('ok')
