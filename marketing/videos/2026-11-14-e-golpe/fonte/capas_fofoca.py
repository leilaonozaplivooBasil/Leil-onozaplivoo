# 20 capas "estilo fofoca" para o É golpe? completo (17/11). Quadros dos vídeos originais (sem legenda queimada).
# Molde da "Fofoca do escritório": topo escuro, logo, pílula laranja, título branco + linha amarela, pílula verde embaixo.
# Uso: capas_fofoca.py <pasta_dos_1080> <video_final> <saida>
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
IN, FINAL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
MK = '/home/user/Leil-onozaplivoo/marketing'; F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
LARANJA, AMARELO, VERDE, BRANCO, ESC = (240, 96, 40), (245, 196, 81), (27, 122, 72), (255, 255, 255), (5, 28, 17)
QUADROS = {'A': ('IMG_7490', 6.56), 'B': ('IMG_7490', 2.78), 'C': ('IMG_7490', 10.26), 'D': ('IMG_7492', 11.6), 'E': ('IMG_7492', 16.6),
           'F': ('IMG_7492', 35.7), 'G': ('IMG_7492', 37.2), 'H': ('IMG_7492', 45.3), 'I': ('IMG_7492', 1.3), 'J': (None, 3.0)}
CAPAS = [('J', 'FOFOCA DO ESCRITÓRIO', 'MANDARAM ISSO', 'PRA GENTE', 'é golpe?'),
         ('A', 'FOFOCA DO ESCRITÓRIO', 'PERGUNTARAM SE', 'A GENTE É GOLPE', 'olha a resposta'),
         ('F', 'FOFOCA DO ESCRITÓRIO', 'O GABRIEL', 'É GOLPE?', 'ele respondeu'),
         ('G', 'EXPOSED', 'ELE JUROU', 'QUE NÃO É GOLPE', 'e ainda chegou cedo'),
         ('D', 'FOFOCA DO ESCRITÓRIO', 'A IARA', 'CONTOU TUDO', 'a diretora de logística'),
         ('E', 'FOFOCA DO ESCRITÓRIO', 'ELAS ENTREGAM', 'EM MÃO?!', 'olha o que ela disse'),
         ('B', 'TODO DIA ALGUÉM PERGUNTA', 'É GOLPE', 'OU NÃO É?', 'a gente respondeu'),
         ('C', 'FOFOCA DO ESCRITÓRIO', 'O GOLPE TÁ AÍ…', 'CAI QUEM QUER', 'foi isso que ele disse'),
         ('H', 'FLAGRA', 'SAEM DEPOIS', 'DAS 21H', 'isso é golpe?'),
         ('I', 'FOMOS INVESTIGAR', 'É GOLPE', 'OU NÃO É?', 'abrimos as portas'),
         ('A', 'FOFOCA BOMBA', 'DESCOBRIMOS QUEM', 'ESTÁ POR TRÁS', 'do Leilão no Zap'),
         ('F', 'FOFOCA DO ESCRITÓRIO', 'PERGUNTEI PRO GABRIEL', 'SE ELE É GOLPE', 'olha a cara dele'),
         ('J', 'TÁ TODO MUNDO', 'PERGUNTANDO…', 'É GOLPE?', 'chegou a resposta'),
         ('D', 'FOFOCA DO ESCRITÓRIO', 'A EMOÇÃO DE QUEM', 'ARREMATOU', 'ela contou'),
         ('H', 'BASTIDOR', 'O QUE NINGUÉM', 'TE MOSTRA', 'o Leilão no Zap por dentro'),
         ('B', 'FOFOCA DO ESCRITÓRIO', 'ELE JURA', 'QUE NÃO É GOLPE', 'e você, acredita?'),
         ('G', 'FOFOCA DO ESCRITÓRIO', 'QUE HORAS ELE', 'CHEGOU AQUI?', 'você não vai acreditar'),
         ('I', 'VEM COMIGO', 'É GOLPE?', '', 'eu te mostro tudo'),
         ('C', 'EXPOSED', 'LEILÃO NO ZAP', 'É GOLPE?', 'assiste até o fim'),
         ('E', 'FOFOCA DO ESCRITÓRIO', 'A RESPOSTA', 'QUE VOCÊ PEDIU', 'é golpe ou não é?')]

def quadro(k):
    nome, t = QUADROS[k]; src = FINAL if nome is None else os.path.join(IN, nome + '_1080.mp4'); p = os.path.join(OUT, f'.q_{k}.png')
    if not os.path.exists(p): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', src, '-frames:v', '1', '-vf', 'scale=1080:1920', p], check=True)
    return Image.open(p).convert('RGBA')
def cabe(d, t, peso, tam, larg):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 40: tam -= 4
    return F(peso, tam)
def pilula(d, cy, t, f, fundo, cor):
    w = d.textlength(t, font=f); h = f.size + 34
    d.rounded_rectangle((540 - w / 2 - 34, cy - h / 2, 540 + w / 2 + 34, cy + h / 2), h / 2, fill=fundo); d.text((540, cy), t, font=f, fill=cor, anchor='mm')
def contorno(d, xy, t, f, cor):
    for dx, dy in ((0, 7), (3, 5), (-3, 5)): d.text((xy[0] + dx, xy[1] + dy), t, font=f, fill=(0, 0, 0, 170), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')

grade = []
for i, (k, pil, l1, l2, sub) in enumerate(CAPAS, start=1):
    b = quadro(k)
    if QUADROS[k][0] is None:  # print das mensagens: desce a conversa e deixa o topo limpo para o título
        nb = Image.new('RGBA', (1080, 1920), ESC + (255,)); nb.alpha_composite(b.crop((0, 0, 1080, 1360)), (0, 560)); b = nb
    g = np.zeros((1920, 1080, 4), np.uint8); g[..., :3] = ESC; g[:820, :, 3] = (np.linspace(1, 0, 820) ** 1.2 * 235)[:, None].astype(np.uint8)
    b.alpha_composite(Image.fromarray(g)); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((170, 70)); b.alpha_composite(lg, ((1080 - lg.width) // 2, 70))
    d = ImageDraw.Draw(b); pilula(d, 210, pil, F('Black', 38), LARANJA, BRANCO)
    f1 = cabe(d, l1, 'Black', 128, 980); contorno(d, (540, 335), l1, f1, BRANCO); y = 335 + f1.size * .55
    if l2: f2 = cabe(d, l2, 'Black', 128, 980); contorno(d, (540, y + f2.size * .55), l2, f2, AMARELO); y += f2.size * 1.1
    pilula(d, y + 70, sub, F('Bold', 42), VERDE, BRANCO)
    d.text((1040, 1880), f'{i:02d}', font=F('Bold', 34), fill=(255, 255, 255, 160), anchor='rs')
    nome = f'{OUT}/capa-{i:02d}.jpg'; b.convert('RGB').save(nome, quality=92); grade.append(b.convert('RGB').resize((216, 384)))
s = Image.new('RGB', (216 * 5, 384 * 4))
for i, im in enumerate(grade): s.paste(im, ((i % 5) * 216, (i // 5) * 384))
s.save(f'{OUT}/TODAS-as-20-capas.jpg', quality=90); print('ok')
