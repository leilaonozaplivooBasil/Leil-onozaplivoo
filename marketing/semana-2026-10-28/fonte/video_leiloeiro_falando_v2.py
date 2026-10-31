# Vídeo do LEILOEIRO FALANDO v2 (31/10/2026, pedido da Natália): voz clonada de TODAS as falas oficiais do site (73 s,
# voz isolada), falas com mais ânimo, boca sincronizada em 3 cenas (praia, café e a chamada com o martelo na mão), legenda
# EMBAIXO (longe do rosto), cartão final com a foto real, o lance do sistema e o jingle oficial (3 batidas).
# Uso: python3 video_leiloeiro_falando_v2.py <lance> <n_lances> <praia.mp4> <cafe.mp4> <chamada.mp4> <saida.mp4> [<previa>]
import math, os, subprocess, sys, tempfile
from PIL import Image
from video_leila_maquina import bloco_texto, colar, janela, W, H, FPS
from video_desejo_notebook import TRILHA
from video_leiloeiro_notebook import cartao

ASSINATURA = '/home/user/Leil-onozaplivoo/marketing/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.wav'
FF, FP = 'ffmpeg', 'ffprobe'
# (zoom, y da legenda, [(linhas, início, fim)])
CENAS = [
    (1.33, 1590, [(['Não acredito que eu', '*arrematei* esse *notebook*!'], 0.1, 3.6), (['Olha que *maravilha*… agora eu', 'trabalho de frente pro *mar*!'], 3.8, 6.9)]),
    (1.33, 1590, [(['E no café também!', '*Core* *i3*, *8GB*, *SSD* *512GB*'], 0.1, 4.7), (['Eu trabalho de', '*onde* *eu* *quiser*!'], 4.9, 7.2)]),
    (1.00, 1610, [(['Atenção, atenção!', 'Os lances *JÁ* *COMEÇARAM*!'], 0.1, 3.6), (['O martelo bate', '*HOJE* *às* *18h*!'], 3.7, 6.4), (['Corre no *Leilão* *no* *Zap*', 'e dá o seu *lance*!'], 6.5, 9.7)]),
]


def dur(f):
    return float(subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)


def quadros(video, zoom):
    w, h = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    vf = f'fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},crop={W}:{H}:(iw-{W})/2:ih-{H}'
    p = subprocess.Popen([FF, '-v', 'error', '-i', video, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield Image.frombytes('RGB', (W, H), b)
    p.kill()


def montar(lance, n, clips, saida, previa=None):
    ds = [dur(c) for c in clips]
    CARD = 3.2
    T = sum(ds) + CARD
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'], stdin=subprocess.PIPE)
    amostras = []
    for (zoom, yleg, legs), clip, d in zip(CENAS, clips, ds):
        imgs = [(bloco_texto(l, 56, larg=940), a, b) for l, a, b in legs]
        q = None
        for i, q in enumerate(quadros(clip, zoom)):
            t = i / FPS
            if t >= d:
                break
            b = q.convert('RGBA')
            for img, a0, a1 in imgs:
                al = janela(t, a0, a1, ent=0.15, sai=0.12)
                colar(b, img, 540, yleg + (1 - al) * 20, 0.94 + 0.06 * al, al)
            fr = b.convert('RGB'); proc.stdin.write(fr.tobytes())
            if previa and i in (40, 140):
                amostras.append(fr)
    final = cartao(lance, n)
    martelo = bloco_texto(['Martelo *HOJE* *às* *18h*'], 54, larg=660)
    cta = bloco_texto(['Dê seu lance · *leilaonozap.net*'], 46, larg=820)
    ult = q.convert('RGBA')
    for i in range(int(CARD * FPS)):
        t = i / FPS
        b = ult.copy(); f = final.copy(); f.putalpha(int(255 * min(1, t / 0.3))); b.alpha_composite(f)
        colar(b, martelo, 540, 1600, 1 + 0.03 * math.sin(t * 6), janela(t, 0.3, 99, ent=0.25))
        colar(b, cta, 540, 1745, 1.0, janela(t, 0.6, 99, ent=0.25))
        fr = b.convert('RGB'); proc.stdin.write(fr.tobytes())
        if previa and i == 60:
            amostras.append(fr)
    proc.stdin.close(); proc.wait()
    if previa:
        os.makedirs(previa, exist_ok=True)
        c = Image.new('RGB', (300 * len(amostras), 533))
        for j, s in enumerate(amostras):
            c.paste(s.resize((300, 533)), (j * 300, 0))
        c.save(f'{previa}/tira.jpg', quality=88)
    tc = sum(ds)
    tj = tc + 0.25
    parts = [f'[{k}:a]atrim=0:{ds[k]},asetpts=PTS-STARTPTS,aresample=48000,afade=t=out:st={ds[k] - 0.08}:d=0.08[c{k}]' for k in range(3)]
    fil = parts + ['[c0][c1][c2]concat=n=3:v=0:a=1,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=120[voz]',
                   f'[3:a]aresample=48000,adelay={int(tj * 1000)}|{int(tj * 1000)},volume=1.7[jg]',
                   f'[4:a]atrim=0:{T},volume=0.13,afade=t=in:d=0.5,afade=t=out:st={tc - 0.4}:d=0.5,apad=whole_dur={T}[tr]',
                   '[voz]asplit[v1][vsc]', '[tr][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=10:release=300[trd]',
                   f'[v1][trd][jg]amix=inputs=3:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.2:LRA=9,aresample=48000[ao]']
    subprocess.run([FF, '-v', 'error', '-y', '-i', clips[0], '-i', clips[1], '-i', clips[2], '-i', ASSINATURA, '-i', TRILHA, '-i', f'{tmp}/v.mp4',
                    '-filter_complex', ';'.join(fil), '-map', '5:v', '-map', '[ao]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-t', f'{T:.2f}', '-movflags', '+faststart', saida], check=True)
    print('ok', round(T, 2))


if __name__ == '__main__':
    a = sys.argv
    montar(float(a[1]), int(a[2]), a[3:6], a[6], a[7] if len(a) > 7 else None)
