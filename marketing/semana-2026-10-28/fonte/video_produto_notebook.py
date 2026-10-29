# Vídeo do notebook SÓ COM A FOTO REAL (29/10/2026) — pedido da Natália: nada de pessoas nem cenário criado por IA.
# "Câmera" passeando pela foto oficial do leilão (logo Dell → tela → notebook inteiro com os pontos fortes) sobre o verde da
# marca, com um brilho passando na tampa; fecha no cartão final aprovado e na assinatura sonora oficial. 15 s, 9:16.
# Uso: DIA=quinta|sexta|sabado python3 video_produto_notebook.py <lance> <saida.mp4> [<pasta_previa>]
import math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from video_leila_maquina import bloco_texto, pilula, colar, janela, ease, W, H, FPS, WHOOSH, POP
from video_desejo_notebook import cartao_final, TRILHA, ASSINATURA, QUANDO
from stories_notebook import fundo
from vendedores2 import recortar
from arte_do_dia import LIMA
from kit import AQUI, logo as _logo

DUR = 15.0
NOTE = recortar(f'{AQUI}/f-007-notebook-1000.png')


def brilho(img, fase):
    """Faixa de luz diagonal passando por cima do produto (só onde há produto)."""
    if not 0 < fase < 1:
        return img
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w]
    pos = (xx + yy * 0.6) / (w + h * 0.6)
    faixa = np.clip(1 - np.abs(pos - (fase * 1.4 - 0.2)) / 0.06, 0, 1) * 0.55
    a = np.array(img.split()[-1]).astype(float) / 255
    luz = Image.fromarray((faixa * a * 255).astype('uint8'))
    out = img.copy()
    camada = Image.new('RGBA', img.size, (255, 255, 255, 0))
    camada.putalpha(luz)
    out.alpha_composite(camada)
    return out


def camera(base, largura, u, v, cx=540, cy=900, fase_brilho=None):
    """Desenha o notebook com 'largura' px de largura, com o ponto (u, v) da foto no ponto (cx, cy) da tela."""
    k = largura / NOTE.width
    x0, y0 = cx - u * NOTE.width * k, cy - v * NOTE.height * k
    # recorta só a parte visível antes de ampliar (mais rápido e mais nítido)
    sx0, sy0 = max(0, -x0 / k), max(0, -y0 / k)
    sx1, sy1 = min(NOTE.width, (W - x0) / k), min(NOTE.height, (H - y0) / k)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    parte = NOTE.crop((int(sx0), int(sy0), int(math.ceil(sx1)), int(math.ceil(sy1))))
    parte = parte.resize((max(1, int(parte.width * k)), max(1, int(parte.height * k))), Image.BICUBIC)
    if fase_brilho is not None:
        parte = brilho(parte, fase_brilho)
    base.alpha_composite(parte, (int(x0 + int(sx0) * k), int(y0 + int(sy0) * k)))


def brilho_chao(base, cx, cy, larg, a):
    g = Image.new('L', (W, H), 0)
    ImageDraw.Draw(g).ellipse((cx - larg * 0.55, cy - 120, cx + larg * 0.55, cy + 120), fill=int(150 * a))
    c = Image.new('RGBA', (W, H), (110, 230, 90, 0))
    c.putalpha(g.filter(ImageFilter.GaussianBlur(70)))
    base.alpha_composite(c)


def montar(lance, saida, previa=None):
    fundo_v = fundo()
    _logo(fundo_v, y=140, largura=230)
    t1 = bloco_texto(['Ele pode ser *seu*…'], 76, larg=820)
    t2 = bloco_texto(['Tela *Full* *HD* de 15,6"', 'pra estudar, trabalhar', 'e maratonar *sua* *série*'], 62)
    t3 = bloco_texto(['OLHA O QUE *ELE* *TEM*'], 64, larg=820)
    pilulas = [pilula('Core i3', 'rápido pro dia a dia', 500), pilula('8GB de memória', 'abre tudo junto', 500),
               pilula('SSD 512GB', 'liga em segundos', 500), pilula('Windows 11', 'pronto pra usar', 500)]
    final = cartao_final(lance)
    martelo = bloco_texto([QUANDO], 50, larg=640)
    cta = bloco_texto(['Dá seu *lance* no *link*'], 52, larg=720)
    if previa:
        os.makedirs(previa, exist_ok=True)
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'],
                            stdin=subprocess.PIPE)
    marcas = {1.8: '1', 5.5: '2', 9.8: '3', 13.0: '4'}
    for n in range(int(DUR * FPS)):
        t = n / FPS
        b = fundo_v.copy()
        # A (0–3.8): bem de perto no logo Dell da tampa, abrindo devagar, com brilho passando
        a = janela(t, 0.0, 3.5, ent=0.01, sai=0.35)
        if a:
            k = ease(t / 3.5)
            camada = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            camera(camada, 3200 - 900 * k, 0.68, 0.245, cy=820, fase_brilho=(t - 0.6) / 2.2)
            colar(b, camada, W / 2, H / 2, 1.0, a)
            colar(b, t1, 540, 1560 + (1 - janela(t, 0.5, 3.4, ent=0.35)) * 40, 1.0, janela(t, 0.5, 3.3, ent=0.35, sai=0.3))
        # B (3.5–7.6): passeando pela tela
        a = janela(t, 3.5, 7.3, ent=0.35, sai=0.35)
        if a:
            k = ease((t - 3.5) / 3.8)
            camada = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            camera(camada, 2100 + 250 * k, 0.30 + 0.16 * k, 0.60, cy=820)
            colar(b, camada, W / 2, H / 2, 1.0, a)
            colar(b, t2, 540, 1560, 1.0, janela(t, 3.9, 7.2, ent=0.35, sai=0.3))
        # C (7.3–11.3): o notebook inteiro subindo, com luz no chão, e os pontos fortes
        a = janela(t, 7.3, 11.0, ent=0.4, sai=0.35)
        if a:
            k = ease((t - 7.3) / 0.8)
            camada = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            brilho_chao(camada, 540, 1110, 900, k)
            camera(camada, 820 + 60 * ease((t - 7.3) / 3.7), 0.5, 0.5, cy=830 + (1 - k) * 120,
                   fase_brilho=(t - 8.0) / 1.6)
            colar(b, camada, W / 2, H / 2, 1.0, a)
            colar(b, t3, 540, 360, 1.0, janela(t, 7.5, 10.9, ent=0.3, sai=0.3))
            for i, p in enumerate(pilulas):
                ai = janela(t, 8.0 + i * 0.55, 10.9, ent=0.3, sai=0.3)
                colar(b, p, 540 + (1 - ai) * 300 * (1 if i % 2 else -1), 1340 + i * 150, 1.0, ai)
        # D (11.1–15): cartão final aprovado
        a = janela(t, 11.1, 16, ent=0.45, sai=0.01)
        if a:
            f = final.copy()
            f.putalpha(int(255 * a))
            b.alpha_composite(f)
            colar(b, martelo, 540, 1650, 1.0, janela(t, 11.7, 16, ent=0.3))
            colar(b, cta, 540, 1770, 1 + 0.03 * math.sin(t * 6), janela(t, 12.3, 16, ent=0.3))
        quadro = b.convert('RGB')
        proc.stdin.write(quadro.tobytes())
        if previa:
            for tm, nq in marcas.items():
                if abs(t - tm) < 0.5 / FPS:
                    quadro.save(f'{previa}/q{nq}.jpg', quality=88)
    proc.stdin.close()
    proc.wait()
    sfx = [(WHOOSH, 3.4), (WHOOSH, 7.2)] + [(POP, 8.0 + i * 0.55) for i in range(4)] + [(WHOOSH, 11.0)]
    ent = ['-i', f'{tmp}/v.mp4', '-i', TRILHA, '-i', ASSINATURA] + sum([['-i', s] for s, _ in sfx], [])
    fil = [f'[1:a]atrim=0:{DUR},volume=0.9,afade=t=in:d=0.5,afade=t=out:st=11.8:d=0.9,apad=whole_dur={DUR}[tr]',
           '[2:a]adelay=12700|12700,volume=2.2[as]']
    nomes = ['[tr]', '[as]']
    for i, (s, ini) in enumerate(sfx):
        fil.append(f'[{i + 3}:a]adelay={int(ini * 1000)}|{int(ini * 1000)},volume=1.4[s{i}]')
        nomes.append(f'[s{i}]')
    fil.append(''.join(nomes) + f'amix=inputs={len(nomes)}:normalize=0:duration=first,atrim=0:{DUR},'
               'loudnorm=I=-13:TP=-1.2:LRA=9,aresample=48000[ao]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ent + ['-filter_complex', ';'.join(fil), '-map', '0:v', '-map', '[ao]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(DUR), '-movflags', '+faststart', saida],
                   check=True)


if __name__ == '__main__':
    montar(float(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
