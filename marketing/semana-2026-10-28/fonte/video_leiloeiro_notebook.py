# Vídeo do LEILOEIRO com o notebook (31/10/2026): praia com água de coco → café trabalhando → chamada "os lances já
# começaram, martelo hoje às 18h". Cenas geradas com a imagem oficial do Leiloeiro como referência (Gamma), falas em
# balão (a voz oficial ainda não está no gerador de vídeo), cartão final com a foto REAL do produto, lance do sistema e
# o jingle oficial (3 batidas). 9:16, serve para status do WhatsApp e Reels.
# Uso: python3 video_leiloeiro_notebook.py <lance> <n_lances> <saida.mp4> [<pasta_previa>]
import math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
from video_leila_maquina import bloco_texto, colar, janela, ease, W, H, FPS, WHOOSH, POP
from video_desejo_notebook import quadro_foto, TRILHA
from stories_notebook import fundo, titulo
from notebook_dia import FOTO, NOME, SPEC, vidro
from arte_do_dia import LIMA, BRANCO, F, real, produto
from vendedores2 import ic_martelo
from kit import logo as _logo

DUR = 16.0
CENAS = '/home/user/Leil-onozaplivoo/marketing/semana-2026-10-28/notebook/video-leiloeiro-veo/cenas'
ASSINATURA = '/home/user/Leil-onozaplivoo/marketing/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.wav'
# (arquivo, início, fim, zoom de/para) — foco embaixo: corta a faixa lisa de céu/parede do topo da imagem
TOMADAS = [('cena-000.jpg', 0.0, 6.0, (1.26, 1.36)), ('cena-001.jpg', 5.6, 11.4, (1.36, 1.26))]
FALAS = [(['Não acredito que', 'eu *arrematei* esse', '*notebook*!'], 0.5, 2.9), (['Olha que *maravilha*…', 'trabalhando de frente', 'pro *mar*!'], 3.1, 5.5),
         (['E no café também.', '*Core* *i3*, *8GB*, *SSD* *512GB*'], 6.2, 8.6), (['Agora eu trabalho de', '*onde* *eu* *quiser*!'], 8.8, 11.0)]


def foto(arq):
    im = Image.open(f'{CENAS}/{arq}').convert('RGB')
    e = max(W / im.width, H / im.height)
    return im.resize((int(im.width * e) + 1, int(im.height * e) + 1), Image.LANCZOS)


def cartao(lance, n):
    b = fundo()
    _logo(b, y=140, largura=230)
    d = ImageDraw.Draw(b)
    titulo(d, 'OS LANCES', 'JÁ COMEÇARAM', 400, 104)
    produto(b, FOTO, 540, 1080, 420)
    vidro(b, (190, 1110, 890, 1340), raio=30)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 330, 1140, 48, LIMA)
    d.text((395, 1166), 'LANCE ATUAL', font=F('Black', 40), fill=LIMA, anchor='lm')
    d.text((540, 1265), real(lance), font=F('Black', 120), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1410), NOME, font=F('Black', 56), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1468), SPEC + (f'  ·  {n} lances' if n else ''), font=F('Black', 30), fill=LIMA, anchor='mm')
    return b


def montar(lance, n, saida, previa=None):
    fotos = {a: foto(a) for a, *_ in TOMADAS}
    falas = [(bloco_texto(l, 66), a, b) for l, a, b in FALAS]
    final = cartao(lance, n)
    martelo = bloco_texto(['Martelo *HOJE* *às* *18h*'], 54, larg=660)
    cta = bloco_texto(['Dê seu lance · *leilaonozap.net*'], 46, larg=820)
    if previa:
        os.makedirs(previa, exist_ok=True)
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'],
                            stdin=subprocess.PIPE)
    marcas = {1.8: '1', 4.4: '2', 7.4: '3', 9.8: '4', 14.0: '5'}
    for k in range(int(DUR * FPS)):
        t = k / FPS
        b = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        for arq, a0, a1, (z0, z1) in TOMADAS:
            al = janela(t, a0, a1 - 0.4, ent=0.4 if a0 else 0.01, sai=0.4)
            if al > 0:
                q = quadro_foto(fotos[arq], z0 + (z1 - z0) * (t - a0) / (a1 - a0), 1.0).convert('RGBA')
                q.putalpha(int(255 * al))
                b.alpha_composite(q)
        for img, a0, a1 in falas:
            al = janela(t, a0, a1, ent=0.25, sai=0.2)
            colar(b, img, 540, 330 + (1 - al) * 30, 0.92 + 0.08 * al, al)
        al = janela(t, 11.1, 17, ent=0.45, sai=0.01)
        if al:
            f = final.copy(); f.putalpha(int(255 * al)); b.alpha_composite(f)
            colar(b, martelo, 540, 1600, 1 + 0.03 * math.sin(t * 6), janela(t, 11.7, 17, ent=0.3))
            colar(b, cta, 540, 1745, 1.0, janela(t, 12.3, 17, ent=0.3))
        q = b.convert('RGB')
        proc.stdin.write(q.tobytes())
        if previa:
            for tm, nq in marcas.items():
                if abs(t - tm) < 0.5 / FPS:
                    q.save(f'{previa}/q{nq}.jpg', quality=88)
    proc.stdin.close(); proc.wait()
    sfx = [(POP, a) for _, a, _ in FALAS] + [(WHOOSH, 5.5), (WHOOSH, 11.0)]
    ent = ['-i', f'{tmp}/v.mp4', '-i', TRILHA, '-i', ASSINATURA] + sum([['-i', s] for s, _ in sfx], [])
    fil = [f'[1:a]atrim=0:{DUR},volume=0.85,afade=t=in:d=0.5,afade=t=out:st=13.0:d=0.8,apad=whole_dur={DUR}[tr]',
           '[2:a]adelay=13700|13700,volume=2.0[as]']
    nomes = ['[tr]', '[as]']
    for i, (s, ini) in enumerate(sfx):
        fil.append(f'[{i + 3}:a]adelay={int(ini * 1000)}|{int(ini * 1000)},volume=1.3[s{i}]'); nomes.append(f'[s{i}]')
    fil.append(''.join(nomes) + f'amix=inputs={len(nomes)}:normalize=0:duration=first,atrim=0:{DUR},loudnorm=I=-14:TP=-1.2:LRA=9,aresample=48000[ao]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ent + ['-filter_complex', ';'.join(fil), '-map', '0:v', '-map', '[ao]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(DUR), '-movflags', '+faststart', saida], check=True)


if __name__ == '__main__':
    montar(float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
