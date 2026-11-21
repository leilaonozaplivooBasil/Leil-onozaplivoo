# Novelinha "O GALPÃO" EP. 01 — PCX em 48 vezes (21/11). 4 takes do Drive (IMG_7707, 7712, 7713, 7714) com transição
# entre as cenas, título fixo, legenda das falas, selo do lance e card final. Uso: montar.py <lance_agora>
import os, sys, subprocess, json
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/novela'; IN = S + '/in'; T = S + '/tmp'; os.makedirs(T, exist_ok=True)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '922'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H, X = 1080, 1920, 0.35   # X = duração da transição
VE, VM, MENTA, BR = (10, 61, 38), (27, 122, 72), (214, 236, 221), (255, 255, 255)
def sh(c): subprocess.run(c, shell=True, check=True)
# cenas: (arquivo, início, fim, transição que ENTRA nesta cena)
CENAS = [('IMG_7707', 0.00, 8.70, None), ('IMG_7712', 0.70, 12.30, 'smoothleft'), ('IMG_7713', 0.85, 13.20, 'zoomin'), ('IMG_7714', 0.90, 5.20, 'slideup')]
# legendas no tempo LOCAL de cada take (a partir da transcrição)
LEG = {
 'IMG_7707': [(0.0, 1.1, 'Amiga,'), (1.4, 3.9, 'vou comprar minha Honda PCX 160'), (3.9, 6.2, 'em 48 vezes!'), (6.2, 8.6, 'Mas o Emanuel não sabe, hein?')],
 'IMG_7712': [(1.1, 3.2, 'Tu vai comprar o quê?'), (3.2, 4.4, '48 vezes?!'), (4.6, 5.7, 'Eu quero muito!'), (6.0, 8.3, 'Não, 48 vezes não! Você vai comprar no Leilão no Zap.'), (8.3, 10.8, 'Eu já falei isso mil vezes pra você!'), (10.9, 12.2, 'Eu quero, eu quero!')],
 'IMG_7713': [(1.0, 3.9, 'Aqui, ó, só no Leilão no Zap'), (3.9, 7.6, 'você consegue comprar produtos novos com esse desconto'), (7.6, 9.6, 'e o lance da moto está em R$ 822'), (9.7, 11.1, 'Você vai comprar pra mim?'), (11.3, 12.5, 'Poxa, amor!')],
 'IMG_7714': [(1.2, 2.5, 'Vocês vão perder, hein?'), (2.5, 4.5, 'Tá todo mundo dando lance!')],
}
def png(nome, desenha):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); desenha(ImageDraw.Draw(im), im); im.save(f'{T}/{nome}.png'); return f'{T}/{nome}.png'
def caixa(d, cx, cy, linhas, f, fundo, cor, px=34, py=18, raio=26):
    ws = [d.textlength(l, font=f) for l in linhas]; lh = f.size * 1.18; w = max(ws) + 2 * px; h = lh * len(linhas) + 2 * py
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), raio, fill=fundo)
    for i, l in enumerate(linhas): d.text((cx, cy - h / 2 + py + lh * (i + .5)), l, font=f, fill=cor, anchor='mm')
def quebra(t, f, d, larg=900):
    ps, ls, cur = t.split(), [], ''
    for p in ps:
        tt = (cur + ' ' + p).strip()
        if d.textlength(tt, font=f) > larg and cur: ls.append(cur); cur = p
        else: cur = tt
    return ls + [cur]
TIT = png('titulo', lambda d, im: (caixa(d, W / 2, 190, ['ELA IA PARCELAR A MOTO', 'EM 48 VEZES'], F('Black', 64), VE, BR, 40, 22, 34), caixa(d, W / 2, 330, ['O GALPÃO · EP. 01'], F('Bold', 30), MENTA, VE, 26, 10, 22)))
# 1) cortar cada cena (vídeo + áudio da fala tratado à parte)
dur = []
for i, (n, a, b, _) in enumerate(CENAS):
    sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {IN}/{n}.mp4 -vf "fps=30,format=yuv420p" -an -c:v libx264 -preset veryfast -crf 16 {T}/v{i}.mp4')
    sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {IN}/{n}.mp4 -vn -af "highpass=f=90,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80" -ar 48000 -ac 2 {T}/a{i}.wav')
    dur.append(b - a)
# 2) juntar com transições (xfade no vídeo, acrossfade na voz)
ini = [0.0]
for i in range(1, len(CENAS)): ini.append(ini[-1] + dur[i - 1] - X)
total = ini[-1] + dur[-1]
ent = ''.join(f'-i {T}/v{i}.mp4 ' for i in range(len(CENAS))); fc = ''; ult = '[0:v]'
for i in range(1, len(CENAS)):
    fc += f'{ult}[{i}:v]xfade=transition={CENAS[i][3]}:duration={X}:offset={ini[i]:.3f}[x{i}];'; ult = f'[x{i}]'
sh(f'ffmpeg -nostdin -v error -y {ent} -filter_complex "{fc[:-1]}" -map "{ult}" -c:v libx264 -preset veryfast -crf 16 {T}/junto.mp4')
ae = ''.join(f'-i {T}/a{i}.wav ' for i in range(len(CENAS))); fa = ''; ult = '[0:a]'
for i in range(1, len(CENAS)): fa += f'{ult}[{i}:a]acrossfade=d={X}[y{i}];'; ult = f'[y{i}]'
sh(f'ffmpeg -nostdin -v error -y {ae} -filter_complex "{fa[:-1]}" -map "{ult}" {T}/voz_raw.wav')
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz_raw.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 {T}/voz.wav')
# 3) card final (2 s) + música
CARD = 2.0
def card(d, im):
    d.rectangle((0, 0, W, H), fill=VM)
    d.text((W / 2, 620), 'HOJE · 20H', font=F('Black', 150), fill=BR, anchor='mm')
    d.text((W / 2, 760), 'Honda PCX 160 vai a leilão', font=F('Medium', 52), fill=MENTA, anchor='mm')
    caixa(d, W / 2, 1000, ['Comenta MOTO'], F('Black', 96), BR, VE, 50, 26, 40)
    d.text((W / 2, 1130), 'que eu te mando o link', font=F('Medium', 46), fill=MENTA, anchor='mm')
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 300)); x = (W - lg.width) // 2
    d.rounded_rectangle((x - 26, 1430, x + lg.width + 26, 1430 + lg.height + 28), 40, fill=VE); im.alpha_composite(lg, (x, 1444))
png('card', card)
sh(f'ffmpeg -nostdin -v error -y -loop 1 -framerate 30 -t {CARD} -i {T}/card.png -vf "format=yuv420p" -c:v libx264 -preset veryfast -crf 16 {T}/card.mp4')
TT = total + CARD - X
# 4) camadas: título, legendas, selo do lance (aparece quando o Emanuel fala o valor), logo
camadas = [(TIT, 0, total - 0.1)]
k = 0
for i, (n, a, b, _) in enumerate(CENAS):
    for (s, e, t) in LEG[n]:
        if e <= a or s >= b: continue
        s2, e2 = max(s, a) - a + ini[i], min(e, b) - a + ini[i]
        def leg(d, im, t=t):
            f = F('Black', 54); ls = quebra(t, f, d, 880); caixa(d, W / 2, 1520, ls, f, (255, 255, 255, 238), VE, 30, 16, 24)
        camadas.append((png(f'leg{k}', leg), s2, e2)); k += 1
i3 = 2; t822 = 7.6 - CENAS[i3][1] + ini[i3]
def selo(d, im):
    caixa(d, W / 2, 1300, ['JÁ SUBIU!', f'LANCE AGORA: R$ {int(float(LANCE)):,}'.replace(',', '.')], F('Black', 50), VM, BR, 36, 18, 30)
camadas.append((png('selo', selo), t822 + 1.4, ini[i3] + dur[i3] - X))
ent = f'-i {T}/junto.mp4 -i {T}/card.mp4 ' + ''.join(f'-loop 1 -framerate 30 -i {c[0]} ' for c in camadas)
fc = f'[0:v][1:v]xfade=transition=fade:duration={X}:offset={total - X:.3f}[b0];'; ult = '[b0]'
for j, (_, s, e) in enumerate(camadas):
    fc += f"{ult}[{j + 2}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})':shortest=0[c{j}];"; ult = f'[c{j}]'
sh(f'ffmpeg -nostdin -v error -y {ent} -filter_complex "{fc[:-1]}" -map "{ult}" -t {TT:.3f} -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p {T}/video_sem_som.mp4')
# música da playlist do Santana: 2 cópias emendadas (a faixa tem ~32 s), bem baixa por baixo da fala, sobe no card
MUS = f'{MK}/marca/trilhas-base/pegada-orla/04-funky-soul-house.mp3'
sh(f'ffmpeg -nostdin -v error -y -i {MUS} -i {MUS} -filter_complex "[0:a][1:a]acrossfade=d=1.5,atrim=0:{TT:.3f},asetpts=N/SR/TB" -ar 48000 -ac 2 {T}/mus_longa.wav')
vol = f"volume='if(lt(t,{total - X:.2f}),0.07,0.30)':eval=frame"
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz.wav -i {T}/mus_longa.wav -filter_complex "[0:a]apad,atrim=0:{TT:.3f}[v];[1:a]{vol},afade=t=out:st={TT - 0.8:.2f}:d=0.8[m];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TT:.3f},asetpts=N/SR/TB" -ar 48000 {T}/mix.wav')
final = f'{OUT}/NOVELINHA-EP01-PCX-48-vezes.mp4'
sh(f'ffmpeg -nostdin -v error -y -i {T}/video_sem_som.mp4 -i {T}/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "{final}"')
print('ok', final, round(TT, 2), 'cenas em', [round(x, 2) for x in ini], 'selo em', round(t822 + 1.4, 2))
