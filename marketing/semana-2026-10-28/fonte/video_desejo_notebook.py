# Vídeo de DESEJO do notebook (29/10/2026): a pessoa se imagina com o produto (praia, quiosque, café) e fecha no
# cartão verde com a foto REAL do notebook, o lance do sistema e a assinatura sonora oficial. 15 s, 9:16.
# Cenas geradas por IA são ilustrativas (o selo "cenas ilustrativas" aparece nelas); o produto real só no cartão final.
# Uso: DIA=quinta|sexta|sabado python3 video_desejo_notebook.py <lance> <saida.mp4> [<pasta_previa>]
import math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
from video_leila_maquina import bloco_texto, colar, janela, ease, W, H, FPS
from stories_notebook import fundo
from notebook_dia import FOTO, NOME, SPEC, vidro
from arte_do_dia import LIMA, BRANCO, F, real, produto
from vendedores2 import ic_martelo
from kit import logo as _logo

DUR = 15.0
CENAS = '/home/user/Leil-onozaplivoo/marketing/semana-2026-10-28/notebook/cenas-desejo/ia'
TRILHA = '/home/user/leilonozap/public/duda/trilhas/brasileira.mp3'
ASSINATURA = '/home/user/Leil-onozaplivoo/marketing/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.wav'
DIA = os.environ.get('DIA', 'quinta')
QUANDO = {'quinta': 'Martelo *sábado* *às* *18h*', 'sexta': 'Martelo *amanhã* *às* *18h*', 'sabado': 'Martelo *hoje* *às* *18h*'}[DIA]

# (arquivo, início, fim, zoom de/para, foco y) — fotos com zoom lento, trocando com fusão
TOMADAS = [('cena-002.jpg', 0.0, 4.2, (1.00, 1.10), 0.45), ('cena-000.jpg', 3.8, 7.9, (1.08, 1.00), 0.40),
           ('cena-001.jpg', 7.5, 11.4, (1.00, 1.09), 0.55)]
FRASES = [(['Imagina abrir o *seu*', '*notebook* aqui…'], 0.4, 3.7), (['de frente pro *mar*,', 'com água de coco'], 4.2, 7.4),
          (['ou no seu *café*', '*favorito*'], 7.9, 10.9)]


def foto(arq):
    im = Image.open(f'{CENAS}/{arq}').convert('RGB')
    e = max(W / im.width, H / im.height)
    return im.resize((int(im.width * e) + 1, int(im.height * e) + 1), Image.LANCZOS)


def quadro_foto(im, z, fy):
    w, h = int(W / z), int(H / z)
    x = (im.width - w) // 2
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h)).resize((W, H), Image.BILINEAR)


def cartao_final(lance):
    b = fundo()
    _logo(b, y=140, largura=230)
    d = ImageDraw.Draw(b)
    d.text((W / 2, 400), 'AGORA PODE', font=F('Black', 92), fill=BRANCO, anchor='mm')
    d.text((W / 2, 500), 'SER O SEU', font=F('Black', 92), fill=LIMA, anchor='mm')
    produto(b, FOTO, 540, 1120, 470)
    vidro(b, (190, 1170, 890, 1400), raio=30)
    d = ImageDraw.Draw(b)
    ic_martelo(d, 330, 1200, 48, LIMA)
    d.text((395, 1226), 'LANCE ATUAL', font=F('Black', 40), fill=LIMA, anchor='lm')
    d.text((540, 1325), real(lance), font=F('Black', 120), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1480), NOME, font=F('Black', 56), fill=BRANCO, anchor='mm')
    d.text((W / 2, 1542), SPEC, font=F('Black', 34), fill=LIMA, anchor='mm')
    return b


def montar(lance, saida, previa=None):
    fotos = {a: foto(a) for a, *_ in TOMADAS}
    frases = [(bloco_texto(l, 72), a, b) for l, a, b in FRASES]
    selo_ia = Image.new('RGBA', (300, 50), (0, 0, 0, 0))
    ImageDraw.Draw(selo_ia).text((150, 25), 'cenas ilustrativas', font=F('Bold', 26), fill=(255, 255, 255, 170), anchor='mm')
    final = cartao_final(lance)
    martelo = bloco_texto([QUANDO], 50, larg=640)
    cta = bloco_texto(['Dá seu *lance* no *link*'], 52, larg=720)
    if previa:
        os.makedirs(previa, exist_ok=True)
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'],
                            stdin=subprocess.PIPE)
    marcas = {2.0: '1', 6.0: '2', 9.5: '3', 12.5: '4', 14.5: '5'}
    for n in range(int(DUR * FPS)):
        t = n / FPS
        b = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        for arq, a0, a1, (z0, z1), fy in TOMADAS:
            al = janela(t, a0, a1 - 0.4, ent=0.4 if a0 else 0.01, sai=0.4)
            if al > 0:
                k = (t - a0) / (a1 - a0)
                q = quadro_foto(fotos[arq], z0 + (z1 - z0) * k, fy).convert('RGBA')
                q.putalpha(int(255 * al))
                b.alpha_composite(q)
        if t < 11.4:
            colar(b, selo_ia, W - 170, H - 60, 1.0, 1.0)
        for img, a0, a1 in frases:
            al = janela(t, a0, a1, ent=0.35, sai=0.3)
            colar(b, img, 540, 380 + (1 - al) * 40, 1.0, al)
        # cartão final (11.1–15)
        al = janela(t, 11.1, 16, ent=0.45, sai=0.01)
        if al:
            f = final.copy()
            f.putalpha(int(255 * al))
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
    filtro = (f'[1:a]atrim=0:{DUR},volume=0.9,afade=t=in:d=0.5,afade=t=out:st=12.4:d=1.0[tr];'
              f'[2:a]adelay=13200|13200,volume=2.2[as];[tr][as]amix=inputs=2:normalize=0:duration=first,atrim=0:{DUR},'
              f'loudnorm=I=-13:TP=-1.2:LRA=9,aresample=48000[ao]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/v.mp4', '-i', TRILHA, '-i', ASSINATURA, '-filter_complex', filtro,
                    '-map', '0:v', '-map', '[ao]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(DUR),
                    '-movflags', '+faststart', saida], check=True)


if __name__ == '__main__':
    montar(float(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
