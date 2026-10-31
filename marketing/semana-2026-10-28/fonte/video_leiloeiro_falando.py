# Vídeo do LEILOEIRO FALANDO com a voz oficial (31/10/2026): cenas da praia e do café com boca sincronizada
# (voz clonada da fala oficial do vídeo de boas-vindas da roleta) → cartão "os lances já começaram" com a foto REAL do
# notebook, lance do sistema, a fala da chamada e o jingle oficial (3 batidas). 9:16 para status e Reels.
# Uso: python3 video_leiloeiro_falando.py <lance> <n_lances> <cena1.mp4> <cena2.mp4> <fala3.mp3> <saida.mp4> [<previa>]
import math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
from video_leila_maquina import bloco_texto, colar, janela, W, H, FPS, WHOOSH, POP
from video_desejo_notebook import TRILHA
from video_leiloeiro_notebook import cartao
from video_leila_maquina import bloco_texto as bt

ASSINATURA = '/home/user/Leil-onozaplivoo/marketing/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.wav'
FF, FP = 'ffmpeg', 'ffprobe'
LEG = {  # legendas por cena: (linhas, início, fim) em segundos da cena
    0: [(['Não acredito que eu', '*arrematei* esse *notebook*!'], 0.1, 3.4), (['Olha que *maravilha*… agora eu', 'trabalho de frente pro *mar*!'], 3.7, 6.4)],
    1: [(['E no café também!', '*Core* *i3*, *8GB*, *SSD* *512GB*'], 0.1, 5.0), (['Agora eu trabalho de', '*onde* *eu* *quiser*!'], 5.2, 8.3)],
}


def dur(f):
    return float(subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)


def quadros(video, zoom):
    """Lê a cena já no 9:16 cheio, ampliada e presa embaixo (some a faixa lisa do topo da imagem original)."""
    w, h = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    vf = f'fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},crop={W}:{H}:(iw-{W})/2:ih-{H}'
    p = subprocess.Popen([FF, '-v', 'error', '-i', video, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield Image.frombytes('RGB', (W, H), b)


def montar(lance, n, c1, c2, f3, saida, previa=None):
    d1, d2, d3 = dur(c1), min(dur(c2), 8.45), dur(f3)
    fim_card = d3 + 2.2
    T = d1 + d2 + fim_card
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'], stdin=subprocess.PIPE)
    k = 0
    salvos = []
    for idx, (clip, limite) in enumerate(((c1, d1), (c2, d2))):
        legs = [(bt(l, 64), a, b) for l, a, b in LEG[idx]]
        for i, q in enumerate(quadros(clip, 1.27)):
            t = i / FPS
            if t >= limite:
                break
            b = q.convert('RGBA')
            for img, a0, a1 in legs:
                al = janela(t, a0, a1, ent=0.2, sai=0.15)
                colar(b, img, 540, 320 + (1 - al) * 25, 0.93 + 0.07 * al, al)
            if idx == 0 and t < 0.25:  # entra do preto
                b = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), b, t / 0.25)
            fr = b.convert('RGB'); proc.stdin.write(fr.tobytes()); k += 1
            if previa and i in (45, 150):
                salvos.append(fr)
    final = cartao(lance, n)
    martelo = bloco_texto(['Martelo *HOJE* *às* *18h*'], 54, larg=660)
    cta = bloco_texto(['Dê seu lance · *leilaonozap.net*'], 46, larg=820)
    ult = q.convert('RGBA')
    for i in range(int(fim_card * FPS)):
        t = i / FPS
        b = ult.copy()
        a = min(1, t / 0.4)
        f = final.copy(); f.putalpha(int(255 * a)); b.alpha_composite(f)
        colar(b, martelo, 540, 1600, 1 + 0.03 * math.sin(t * 6), janela(t, 0.5, 99, ent=0.3))
        colar(b, cta, 540, 1745, 1.0, janela(t, 1.0, 99, ent=0.3))
        fr = b.convert('RGB'); proc.stdin.write(fr.tobytes())
        if previa and i == 90:
            salvos.append(fr)
    proc.stdin.close(); proc.wait()
    if previa:
        os.makedirs(previa, exist_ok=True)
        c = Image.new('RGB', (360 * len(salvos), 640))
        for j, s in enumerate(salvos):
            c.paste(s.resize((360, 640)), (j * 360, 0))
        c.save(f'{previa}/tira.jpg', quality=88)
    # som: voz das cenas + fala da chamada + jingle no fim; trilha baixinha por baixo, abaixando quando há voz
    t2, t3 = d1, d1 + d2
    tj = t3 + d3 + 0.15
    fil = [f'[0:a]atrim=0:{d1},asetpts=PTS-STARTPTS[a1]', f'[1:a]atrim=0:{d2},asetpts=PTS-STARTPTS,afade=t=out:st={d2 - 0.12}:d=0.12[a2]',
           f'[a1][a2]concat=n=2:v=0:a=1,aresample=48000[cen]', f'[2:a]aresample=48000,adelay={int(t3 * 1000)}|{int(t3 * 1000)}[f3]',
           '[cen][f3]amix=inputs=2:normalize=0:duration=longest,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=120[voz]',
           f'[3:a]aresample=48000,adelay={int(tj * 1000)}|{int(tj * 1000)},volume=1.6[jg]',
           f'[4:a]atrim=0:{T},volume=0.14,afade=t=in:d=0.6,afade=t=out:st={tj - 0.6}:d=0.6,apad=whole_dur={T}[tr]',
           f'[voz]asplit[v1][vsc]', '[tr][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=10:release=300[trd]',
           f'[v1][trd][jg]amix=inputs=3:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.2:LRA=9,aresample=48000[ao]']
    subprocess.run([FF, '-v', 'error', '-y', '-i', c1, '-i', c2, '-i', f3, '-i', ASSINATURA, '-i', TRILHA, '-i', f'{tmp}/v.mp4',
                    '-filter_complex', ';'.join(fil), '-map', '5:v', '-map', '[ao]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-t', f'{T:.2f}', '-movflags', '+faststart', saida], check=True)
    print('ok', round(T, 2))


if __name__ == '__main__':
    a = sys.argv
    montar(float(a[1]), int(a[2]), a[3], a[4], a[5], a[6], a[7] if len(a) > 7 else None)
