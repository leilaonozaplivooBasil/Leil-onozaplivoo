# Já encontrou o dono EP. 04 (23/11): depoimento de quem arrematou um iPhone (IMG_3630, 22 s, HDR → SDR).
# Corta o "boa noite, meus amigos" (regra do curso: nada de "oi gente"), cortes secos com zoom alternado a cada trecho,
# título nos 3 primeiros segundos, legenda, música baixa, card final. Uso: montar.py
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/iphone3630'; T = S + '/tmp'; os.makedirs(T, exist_ok=True)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920; VE, VM, MENTA, BR = (10, 61, 38), (27, 122, 72), (214, 236, 221), (255, 255, 255)
def sh(c): subprocess.run(c, shell=True, check=True)
TRE = [(3.25, 8.60, 1.00), (9.60, 13.60, 1.14), (13.70, 18.80, 1.00), (19.00, 21.70, 1.16)]
LEG = [(3.3, 6.3, 'Acabei de arrematar um iPhone'), (6.3, 8.6, 'no Leilão!'), (9.6, 11.55, 'Pensei que fosse alguma coisa…'), (11.55, 13.6, 'mas é uma coisa séria.'),
       (13.7, 17.5, 'Levou uma semana pra entregar o iPhone.'), (17.5, 18.8, 'Entregue!'), (19.0, 21.7, 'Aí, filha, pra você!')]
def png(n, f):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); f(ImageDraw.Draw(im), im); im.save(f'{T}/{n}.png'); return f'{T}/{n}.png'
def caixa(d, cx, cy, ls, f, fu, co, px=34, py=18, r=26):
    ws = [d.textlength(l, font=f) for l in ls]; lh = f.size * 1.18; w = max(ws) + 2 * px; h = lh * len(ls) + 2 * py
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), r, fill=fu)
    for i, l in enumerate(ls): d.text((cx, cy - h / 2 + py + lh * (i + .5)), l, font=f, fill=co, anchor='mm')
def quebra(t, f, d, L=880):
    ls, c = [], ''
    for p in t.split():
        tt = (c + ' ' + p).strip()
        if d.textlength(tt, font=f) > L and c: ls.append(c); c = p
        else: c = tt
    return ls + [c]
# trechos com zoom alternado (corte seco)
mapa = []; t0 = 0
for i, (a, b, z) in enumerate(TRE):
    vf = f"scale=w='trunc({W}*{z}*(1+0.012*t)/2)*2':h=-2:eval=frame,crop={W}:{H}:x='(iw-{W})/2':y='(ih-{H})*0.35',fps=30,setsar=1,format=yuv420p"
    sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {S}/sdr.mp4 -vf "{vf}" -an -c:v libx264 -preset veryfast -crf 16 {T}/v{i}.mp4')
    sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {S}/sdr.mp4 -vn -af "highpass=f=90,afftdn=nf=-25,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.03:.3f}:d=0.03" -ar 48000 -ac 2 {T}/a{i}.wav')
    mapa.append((a, b, t0)); t0 += b - a
TOT = t0
open(f'{T}/lv.txt', 'w').write(''.join(f"file '{T}/v{i}.mp4'\n" for i in range(len(TRE))))
open(f'{T}/la.txt', 'w').write(''.join(f"file '{T}/a{i}.wav'\n" for i in range(len(TRE))))
sh(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i {T}/lv.txt -c:v libx264 -preset veryfast -crf 16 {T}/junto.mp4')
sh(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i {T}/la.txt {T}/voz_raw.wav')
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz_raw.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 {T}/voz.wav')
def faixas(s, e):
    r = []
    for a, b, o in mapa:
        s1, e1 = max(s, a), min(e, b)
        if e1 - s1 > .15: r.append((o + s1 - a, o + e1 - a))
    return r
CARD, X = 2.2, 0.3
def card(d, im):
    d.rectangle((0, 0, W, H), fill=VM)
    caixa(d, W / 2, 520, ['JÁ ENCONTROU O DONO · EP. 04'], F('Black', 40), MENTA, VE, 30, 12, 26)
    d.text((W / 2, 700), 'Pensou que era', font=F('Medium', 64), fill=MENTA, anchor='mm'); d.text((W / 2, 800), 'brincadeira.', font=F('Medium', 64), fill=MENTA, anchor='mm')
    d.text((W / 2, 950), 'Virou presente', font=F('Black', 96), fill=BR, anchor='mm'); d.text((W / 2, 1060), 'da filha.', font=F('Black', 96), fill=BR, anchor='mm')
    caixa(d, W / 2, 1270, ['Segue pra ver o próximo'], F('Black', 54), BR, VE, 44, 22, 36)
    d.text((W / 2, 1390), '#EncontrouDono', font=F('Bold', 42), fill=MENTA, anchor='mm')
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 280)); x = (W - lg.width) // 2
    d.rounded_rectangle((x - 26, 1560, x + lg.width + 26, 1560 + lg.height + 28), 40, fill=VE); im.alpha_composite(lg, (x, 1574))
png('card', card)
sh(f'ffmpeg -nostdin -v error -y -loop 1 -framerate 30 -t {CARD} -i {T}/card.png -vf format=yuv420p -c:v libx264 -preset veryfast -crf 16 {T}/card.mp4')
TT = TOT + CARD - X
TIT = png('tit', lambda d, im: (caixa(d, W / 2, 190, ['ELE ACHOU QUE', 'ERA GOLPE'], F('Black', 72), VE, BR, 44, 22, 34), caixa(d, W / 2, 345, ['JÁ ENCONTROU O DONO · EP. 04'], F('Bold', 30), MENTA, VE, 26, 10, 22)))
cam = [(TIT, 0, TOT - .1)]; k = 0
for s, e, t in LEG:
    for s2, e2 in faixas(s, e):
        def lg(d, im, t=t): f = F('Black', 56); caixa(d, W / 2, 1560, quebra(t, f, d), f, (255, 255, 255, 240), VE, 30, 16, 24)
        cam.append((png(f'l{k}', lg), s2, e2)); k += 1
ent = f'-i {T}/junto.mp4 -i {T}/card.mp4 ' + ''.join(f'-loop 1 -framerate 30 -i {c[0]} ' for c in cam)
fc = f'[0:v][1:v]xfade=transition=fade:duration={X}:offset={TOT - X:.3f}[b0];'; u = '[b0]'
for j, (_, s, e) in enumerate(cam): fc += f"{u}[{j + 2}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})':shortest=0[c{j}];"; u = f'[c{j}]'
sh(f'ffmpeg -nostdin -v error -y {ent} -filter_complex "{fc[:-1]}" -map "{u}" -t {TT:.3f} -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p {T}/vs.mp4')
MUS = f'{MK}/marca/trilhas-base/pegada-orla/03-piano-house.mp3'
vol = f"volume='if(lt(t,{TOT - X:.2f}),0.07,0.30)':eval=frame"
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz.wav -i {MUS} -filter_complex "[0:a]apad,atrim=0:{TT:.3f}[v];[1:a]atrim=0:{TT:.3f},asetpts=N/SR/TB,{vol},afade=t=out:st={TT - .8:.2f}:d=0.8[m];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TT:.3f},asetpts=N/SR/TB" -ar 48000 {T}/mix.wav')
fin = f'{OUT}/JA-ENCONTROU-O-DONO-EP04-iPhone-presente-da-filha.mp4'
sh(f'ffmpeg -nostdin -v error -y -i {T}/vs.mp4 -i {T}/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "{fin}"')
print('ok', round(TT, 2))
