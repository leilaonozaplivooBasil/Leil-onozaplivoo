# Vídeo "A cara de quem viu…" (28/10/2026): Leila (imagens oficiais) + máquina de lavar, sem fala, 14 s, 9:16.
# Mesmo verde tom sobre tom das artes do grupo. Benefícios da descrição do produto no site; lance atual lido na hora.
# Uso: python3 video_leila_maquina.py <lance_agora> <saida.mp4> [<pasta_quadros_previa>]
import math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter
import vendedores3 as v3
v3.H = 1920  # o fundo facetado em 9:16
from vendedores3 import fundo_facetado, texto_em_arco
from vendedores2 import (F, real, camada_texto, vidro, recortar, ic_cronometro, ic_martelo, LIMA, LIMA_ESC, CREME,
                         FUNDO_ESC, BRANCO, FOTO)
from kit import AQUI, SITE, logo as _logo

W, H, FPS, DUR = 1080, 1920, 30, 14.0
MARTELO = '/home/user/Leil-onozaplivoo/marketing/videos/flamengo-hoje-18h/sfx/martelo.mp3'
WHOOSH = '/home/user/Leil-onozaplivoo/marketing/videos/flamengo-hoje-18h/sfx/whoosh.mp3'
POP = '/home/user/Leil-onozaplivoo/marketing/videos/flamengo-hoje-18h/sfx/pop.mp3'
TRILHA = '/home/user/leilonozap/public/duda/trilhas/divertido.mp3'


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def janela(t, a, b, ent=0.25, sai=0.25):
    """0→1 entrando em a, 1 até b, 1→0 saindo depois de b."""
    if t < a or t > b + sai:
        return 0.0
    if t < a + ent:
        return ease((t - a) / ent)
    if t > b:
        return 1 - ease((t - b) / sai)
    return 1.0


def com_alfa(img, a):
    if a >= 0.999:
        return img
    r = img.copy()
    r.putalpha(r.split()[-1].point(lambda v: int(v * a)))
    return r


def leila(nome, altura):
    im = Image.open(f'{SITE}/leila-recorte/{nome}.webp').convert('RGBA')
    im.putalpha(im.split()[-1].filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.2)))  # tira o contorno branco
    return im.resize((int(im.width * altura / im.height), altura), Image.LANCZOS)


def pilula(texto_forte, texto, larg=540):
    """Pílula de benefício: ícone redondo lima + duas linhas."""
    im = Image.new('RGBA', (larg + 40, 170), (0, 0, 0, 0))
    vidro(im, (10, 10, larg + 10, 150), borda=LIMA, raio=40)
    d = ImageDraw.Draw(im)
    d.ellipse((30, 38, 114, 122), fill=LIMA)
    d.line((52, 82, 66, 98, 94, 62), fill=FUNDO_ESC, width=10, joint='curve')
    d.text((134, 58), texto_forte, font=F('Black', 40), fill=LIMA, anchor='lm')
    d.text((134, 106), texto, font=F('Bold', 30), fill=BRANCO, anchor='lm')
    return im


def bloco_texto(linhas, tam, cor=BRANCO, destaque=LIMA, larg=980):
    """Texto centralizado em várias linhas; *palavra* em lima. Fundo de vidro escuro atrás."""
    f = F('Black', tam)
    d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    alt = int(tam * 1.18)
    im = Image.new('RGBA', (larg, alt * len(linhas) + 70), (0, 0, 0, 0))
    vidro(im, (0, 0, larg, im.height), borda=LIMA, raio=46)
    d = ImageDraw.Draw(im)
    y = 35
    for lin in linhas:
        pal = lin.split(' ')
        w = d0.textlength(lin.replace('*', ''), font=f)
        x = (larg - w) / 2
        for i, p in enumerate(pal):
            s = p.replace('*', '') + (' ' if i < len(pal) - 1 else '')
            d.text((x, y + alt / 2), s, font=f, fill=destaque if '*' in p else cor, anchor='lm')
            x += d0.textlength(s, font=f)
        y += alt
    return im


def colar(base, img, cx, cy, escala=1.0, a=1.0):
    if a <= 0.001:
        return
    if abs(escala - 1) > 0.002:
        img = img.resize((max(1, int(img.width * escala)), max(1, int(img.height * escala))), Image.BILINEAR)
    base.alpha_composite(com_alfa(img, a), (int(cx - img.width / 2), int(cy - img.height / 2)))


def montar(lance, saida, previa=None):
    fundo = fundo_facetado()
    _logo(fundo, y=60, largura=250)
    # peças prontas
    surpresa = leila('surpresa', 1000)
    apresenta = leila('apresenta', 980)
    piscada = leila('piscada', 900)
    maq = recortar(FOTO)
    maq_g = maq.resize((int(maq.width * 760 / maq.height), 760), Image.LANCZOS)
    brilho = Image.new('RGBA', (maq_g.width + 300, maq_g.height + 300), LIMA + (0,))
    m = Image.new('L', brilho.size, 0)
    m.paste(maq_g.split()[-1].point(lambda v: 210 if v > 20 else 0), (150, 150))
    brilho.putalpha(m.filter(ImageFilter.GaussianBlur(55)))
    gancho = bloco_texto(['Quando você descobre', 'quanto tá a *máquina*', '*de* *lavar* hoje…'], 74)
    nome = bloco_texto(['Máquina de lavar *Panasonic* *15* *kg*'], 50, larg=900)
    titulo_b = camada_texto('OLHA O QUE ELA FAZ', F('Black', 76), BRANCO, relevo=6)
    beneficios = [pilula('15 kg', 'cabe edredom e muita roupa'), pilula('Vários programas', 'um pra cada tipo de roupa'),
                  pilula('Economiza', 'água e tempo'), pilula('Novinha', 'direto de fábrica')]
    lance_txt = camada_texto(real(lance), F('Black', 150), ((235, 255, 150), LIMA_ESC), relevo=12, brilho=LIMA)
    rot_lance = camada_texto('LANCE ATUAL', F('Black', 64), BRANCO, relevo=5)
    martelo = bloco_texto(['Martelo *hoje* *às* *18h*'], 54, larg=720)
    final = bloco_texto(['Comenta *QUARTA*', 'que eu te mando o link'], 70)

    os.makedirs(previa, exist_ok=True) if previa else None
    tmp = tempfile.mkdtemp()
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{tmp}/v.mp4'],
                            stdin=subprocess.PIPE)
    marcas_previa = {1.2: '1', 3.2: '2', 7.9: '3', 10.8: '4', 13.0: '5'}
    for n in range(int(DUR * FPS)):
        t = n / FPS
        b = fundo.copy()
        # cena 1 (0–2.2): Leila surpresa + gancho
        a = janela(t, 0.0, 2.0, ent=0.18, sai=0.3)
        if a:
            esc = 0.86 + 0.14 * ease(t / 0.3) + 0.02 * max(0, t - 0.3)
            colar(b, surpresa, 540, H - surpresa.height * esc / 2 + (1 - a) * 300, esc, 1)
        colar(b, gancho, 540, 470, 1.0, janela(t, 0.05, 3.8, ent=0.3, sai=0.3))
        # máquina: entra no centro (2.0) e vai para a direita (4.0)
        if t >= 2.0:
            k = ease((t - 2.0) / 0.45)
            mv = ease((t - 4.0) / 0.5) if t >= 4.0 else 0
            esc = (0.55 + 0.45 * k) * (1 - 0.22 * mv)
            cx = 540 + 220 * mv
            cy = 1150 - 390 * mv
            a_m = 1 - janela(t, 12.0, 14.5, ent=0.3, sai=0.1) if t >= 12.0 else 1
            colar(b, brilho, cx, cy, esc, a_m * k)
            colar(b, maq_g, cx, cy + 4 * math.sin(t * 3), esc, a_m * k)
        colar(b, nome, 540, 1620, 1.0, janela(t, 2.4, 3.9, ent=0.25, sai=0.25))
        # cena 3 (4–12): Leila apresentando à esquerda + benefícios + lance
        a = janela(t, 4.1, 11.9, ent=0.35, sai=0.3)
        if a:
            colar(b, apresenta, apresenta.width / 2 - 60 - (1 - a) * 500, H - apresenta.height / 2, 1.0, 1)
        colar(b, titulo_b, 540, 300, 1.0, janela(t, 4.2, 8.9, ent=0.3, sai=0.3))
        for i, p in enumerate(beneficios):
            ini = 4.7 + i * 1.0
            aa = janela(t, ini, 8.9, ent=0.3, sai=0.3)
            colar(b, p, 790 + (1 - aa) * 300, 1150 + i * 160, 1.0, aa)
        aa = janela(t, 9.1, 11.9, ent=0.3, sai=0.3)
        if aa:
            colar(b, rot_lance, 780, 1170, 1.0, aa)
            pulso = 1 + 0.04 * math.sin((t - 9.1) * 6)
            colar(b, lance_txt, 780, 1335, (0.7 + 0.3 * ease((t - 9.1) / 0.35)) * pulso, aa)
            colar(b, martelo, 780, 1530, 1.0, janela(t, 9.5, 11.9, ent=0.3, sai=0.3))
            ic = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
            ic_cronometro(ImageDraw.Draw(ic), 80, 90, 52, LIMA)
            colar(b, ic, 780, 300 + 0, 1.0, 0)  # (reservado)
        # cena 4 (12–14): Leila piscando + chamada
        a = janela(t, 12.0, 14.0, ent=0.3, sai=0.01)
        if a:
            colar(b, piscada, 540, H - piscada.height / 2 + (1 - a) * 300, 1.0, 1)
            colar(b, final, 540, 560, 0.9 + 0.1 * a, a)
        quadro = b.convert('RGB')
        proc.stdin.write(quadro.tobytes())
        if previa:
            for tm, nome_q in marcas_previa.items():
                if abs(t - tm) < 0.5 / FPS:
                    quadro.save(f'{previa}/q{nome_q}.jpg', quality=88)
    proc.stdin.close()
    proc.wait()
    # som: trilha + 3 marteladas na abertura, whoosh na troca, pops nos benefícios, martelada no fim
    sfx = [(MARTELO, 0.0), (MARTELO, 0.45), (MARTELO, 0.9), (WHOOSH, 1.95), (WHOOSH, 3.95)] + \
          [(POP, 4.7 + i) for i in range(4)] + [(WHOOSH, 9.0), (MARTELO, 12.0)]
    ent = ['-i', f'{tmp}/v.mp4', '-i', TRILHA] + sum([['-i', s] for s, _ in sfx], [])
    filtros = [f'[1:a]atrim=0:{DUR},volume=0.8,afade=t=in:d=0.3,afade=t=out:st={DUR - 1.2}:d=1.2[tr]']
    nomes = ['[tr]']
    for i, (s, ini) in enumerate(sfx):
        vol = 3.5 if s == MARTELO else 1.6
        filtros.append(f'[{i + 2}:a]adelay={int(ini * 1000)}|{int(ini * 1000)},volume={vol}[s{i}]')
        nomes.append(f'[s{i}]')
    filtros.append(''.join(nomes) + f'amix=inputs={len(nomes)}:normalize=0:duration=first,atrim=0:{DUR},loudnorm=I=-13:TP=-1.2:LRA=9,aresample=48000[ao]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ent + ['-filter_complex', ';'.join(filtros), '-map', '0:v', '-map', '[ao]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(DUR), '-movflags', '+faststart', saida],
                   check=True)


if __name__ == '__main__':
    montar(float(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
