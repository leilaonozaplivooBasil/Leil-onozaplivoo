# Novelinha "O GALPÃO" EP. 01 — PCX em 48 vezes (21/11), versão 2 com as regras do curso (Natália, 21/11):
# até 30 s · algo muda a cada ≤5 s (jump cut + zoom no rosto de quem fala, enquadramento da cintura pra cima) ·
# "desenhar": falou da moto, a moto aparece · título nos 3 primeiros segundos · um pedido só no fim · transição entre cenas.
# Uso: montar.py <lance_agora>
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/novela'; IN = S + '/in'; T = S + '/tmp'; os.makedirs(T, exist_ok=True)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); MK = '/home/user/Leil-onozaplivoo/marketing'
PCX = MK + '/semana-2026-11-16/sabado-21-11-pcx/fonte/fotos/pcx-plataforma-lado.webp'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '922'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H, X = 1080, 1920, 0.35
VE, VM, MENTA, BR = (10, 61, 38), (27, 122, 72), (214, 236, 221), (255, 255, 255)
def sh(c): subprocess.run(c, shell=True, check=True)
# cada cena = lista de trechos (início, fim, zoom, foco_x, foco_y) no tempo do take; entre trechos = corte seco; entre cenas = transição
CENAS = [
 ('IMG_7707', None, [(1.35, 4.60, 1.00, .40, .45), (4.60, 8.55, 1.45, .32, .30)]),                      # ela no telefone (abre, depois fecha no rosto)
 ('IMG_7712', 'smoothleft', [(1.05, 4.35, 1.35, .74, .38), (4.65, 5.65, 1.45, .28, .45), (6.00, 10.80, 1.30, .92, .38)]),  # Emanuel / ela / Emanuel
 ('IMG_7713', 'zoomin', [(0.95, 3.85, 1.15, .50, .45), (7.50, 9.60, 1.30, .45, .40), (9.95, 12.70, 1.10, .50, .45)]),       # mostra o celular / lance / abraço
 ('IMG_7714', 'slideup', [(0.90, 4.60, 1.20, .48, .45)]),                                                 # Natália passa com a caixa
]
LEG = {
 'IMG_7707': [(1.4, 3.9, 'Vou comprar minha Honda PCX 160'), (3.9, 6.2, 'em 48 vezes!'), (6.2, 8.6, 'Mas o Emanuel não sabe, hein?')],
 'IMG_7712': [(1.1, 3.2, 'Tu vai comprar o quê?'), (3.2, 4.4, '48 vezes?!'), (4.6, 5.7, 'Eu quero muito!'), (6.0, 8.3, 'Não, 48 vezes não! Você vai comprar no Leilão no Zap.'), (8.3, 10.8, 'Eu já falei isso mil vezes pra você!')],
 'IMG_7713': [(1.0, 3.9, 'Aqui, ó: só no Leilão no Zap'), (7.5, 9.6, 'e o lance da moto está em R$ 822'), (9.9, 11.1, 'Você vai comprar pra mim?'), (11.3, 12.6, 'Poxa, amor!')],
 'IMG_7714': [(1.2, 2.5, 'Vocês vão perder, hein?'), (2.5, 4.5, 'Tá todo mundo dando lance!')],
}
# "desenhar": a moto aparece quando é citada (tempo do take)
MOTO_EM = {'IMG_7707': [(2.5, 4.3)], 'IMG_7713': [(7.6, 9.6)]}
def png(nome, desenha):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); desenha(ImageDraw.Draw(im), im); im.save(f'{T}/{nome}.png'); return f'{T}/{nome}.png'
def caixa(d, cx, cy, linhas, f, fundo, cor, px=34, py=18, raio=26):
    ws = [d.textlength(l, font=f) for l in linhas]; lh = f.size * 1.18; w = max(ws) + 2 * px; h = lh * len(linhas) + 2 * py
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), raio, fill=fundo)
    for i, l in enumerate(linhas): d.text((cx, cy - h / 2 + py + lh * (i + .5)), l, font=f, fill=cor, anchor='mm')
def quebra(t, f, d, larg=880):
    ls, cur = [], ''
    for p in t.split():
        tt = (cur + ' ' + p).strip()
        if d.textlength(tt, font=f) > larg and cur: ls.append(cur); cur = p
        else: cur = tt
    return ls + [cur]
# 1) recortar os trechos com zoom (enquadramento da cintura pra cima no rosto de quem fala) + leve aproximação contínua
ini_cena, dur_cena, mapa = [], [], {}   # mapa[take] = [(a, b, t0_saida)]
for ci, (n, _, tre) in enumerate(CENAS):
    parts = []; t_local = 0.0; mapa[n] = []
    for ti, (a, b, z, fx, fy) in enumerate(tre):
        d = b - a
        vf = (f"scale=w='trunc({W}*{z}*(1+0.025*t)/2)*2':h=-2:eval=frame,"
              f"crop={W}:{H}:x='min(max(0,iw*{fx}-{W}/2),iw-{W})':y='min(max(0,ih*{fy}-{H}/2),ih-{H})',fps=30,setsar=1,format=yuv420p")
        sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {IN}/{n}.mp4 -vf "{vf}" -an -c:v libx264 -preset veryfast -crf 16 {T}/c{ci}_{ti}.mp4')
        sh(f'ffmpeg -nostdin -v error -y -ss {a} -to {b} -i {IN}/{n}.mp4 -vn -af "highpass=f=90,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03" -ar 48000 -ac 2 {T}/c{ci}_{ti}.wav')
        parts.append(ti); mapa[n].append((a, b, t_local)); t_local += d
    lista = '|'.join(f'{T}/c{ci}_{ti}.mp4' for ti in parts)
    with open(f'{T}/l{ci}.txt', 'w') as fh: fh.write(''.join(f"file '{T}/c{ci}_{ti}.mp4'\n" for ti in parts))
    with open(f'{T}/la{ci}.txt', 'w') as fh: fh.write(''.join(f"file '{T}/c{ci}_{ti}.wav'\n" for ti in parts))
    sh(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i {T}/l{ci}.txt -c:v libx264 -preset veryfast -crf 16 {T}/v{ci}.mp4')
    sh(f'ffmpeg -nostdin -v error -y -f concat -safe 0 -i {T}/la{ci}.txt {T}/a{ci}.wav')
    dur_cena.append(t_local)
    ini_cena.append(0.0 if ci == 0 else ini_cena[-1] + dur_cena[-2] - X)
total = ini_cena[-1] + dur_cena[-1]
def saida(n, t):   # tempo do take -> tempo no vídeo final (None se o trecho foi cortado)
    ci = [c[0] for c in CENAS].index(n)
    for a, b, t0 in mapa[n]:
        if a <= t <= b: return ini_cena[ci] + t0 + (t - a)
    return None
def faixas(n, s, e):  # devolve os pedaços (s2,e2) no vídeo final de um intervalo do take
    ci = [c[0] for c in CENAS].index(n); r = []
    for a, b, t0 in mapa[n]:
        s1, e1 = max(s, a), min(e, b)
        if e1 - s1 > 0.15: r.append((ini_cena[ci] + t0 + s1 - a, ini_cena[ci] + t0 + e1 - a))
    return r
# 2) juntar cenas com transição
ent = ''.join(f'-i {T}/v{i}.mp4 ' for i in range(len(CENAS))); fc = ''; ult = '[0:v]'
for i in range(1, len(CENAS)): fc += f'{ult}[{i}:v]xfade=transition={CENAS[i][1]}:duration={X}:offset={ini_cena[i]:.3f}[x{i}];'; ult = f'[x{i}]'
sh(f'ffmpeg -nostdin -v error -y {ent} -filter_complex "{fc[:-1]}" -map "{ult}" -c:v libx264 -preset veryfast -crf 16 {T}/junto.mp4')
ae = ''.join(f'-i {T}/a{i}.wav ' for i in range(len(CENAS))); fa = ''; ult = '[0:a]'
for i in range(1, len(CENAS)): fa += f'{ult}[{i}:a]acrossfade=d={X}[y{i}];'; ult = f'[y{i}]'
sh(f'ffmpeg -nostdin -v error -y {ae} -filter_complex "{fa[:-1]}" -map "{ult}" {T}/voz_raw.wav')
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz_raw.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 {T}/voz.wav')
# 3) card final
CARD = 2.0
def card(d, im):
    d.rectangle((0, 0, W, H), fill=VM)
    d.text((W / 2, 560), 'HOJE · 20H', font=F('Black', 150), fill=BR, anchor='mm')
    m = Image.open(PCX).convert('RGBA'); m = m.crop(m.getbbox()); m = m.resize((760, int(m.height * 760 / m.width)), Image.LANCZOS); im.alpha_composite(m, ((W - 760) // 2, 660))
    d = ImageDraw.Draw(im); caixa(d, W / 2, 1260, ['Comenta MOTO'], F('Black', 96), BR, VE, 50, 26, 40)
    d.text((W / 2, 1390), 'que eu te mando o link', font=F('Medium', 46), fill=MENTA, anchor='mm')
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 300)); x = (W - lg.width) // 2
    d.rounded_rectangle((x - 26, 1560, x + lg.width + 26, 1560 + lg.height + 28), 40, fill=VE); im.alpha_composite(lg, (x, 1574))
png('card', card)
sh(f'ffmpeg -nostdin -v error -y -loop 1 -framerate 30 -t {CARD} -i {T}/card.png -vf "format=yuv420p" -c:v libx264 -preset veryfast -crf 16 {T}/card.mp4')
TT = total + CARD - X
# 4) camadas
TIT = png('titulo', lambda d, im: (caixa(d, W / 2, 190, ['ELA IA PARCELAR A MOTO', 'EM 48 VEZES'], F('Black', 64), VE, BR, 40, 22, 34), caixa(d, W / 2, 330, ['O GALPÃO · EP. 01'], F('Bold', 30), MENTA, VE, 26, 10, 22)))
camadas = [(TIT, 0, total - 0.1)]; k = 0
for n, lst in LEG.items():
    for (s, e, t) in lst:
        for (s2, e2) in faixas(n, s, e):
            def leg(d, im, t=t): f = F('Black', 54); caixa(d, W / 2, 1560, quebra(t, f, d), f, (255, 255, 255, 238), VE, 30, 16, 24)
            camadas.append((png(f'leg{k}', leg), s2, e2)); k += 1
def moto_card(d, im):
    d.rounded_rectangle((170, 1000, W - 170, 1480), 44, fill=MENTA + (250,))
    m = Image.open(PCX).convert('RGBA'); m = m.crop(m.getbbox()); m = m.resize((580, int(m.height * 580 / m.width)), Image.LANCZOS); im.alpha_composite(m, ((W - 580) // 2, 1030))
    d = ImageDraw.Draw(im); d.text((W / 2, 1440), 'Honda PCX 160', font=F('Black', 48), fill=VE, anchor='mm')
MC = png('moto', moto_card)
for n, lst in MOTO_EM.items():
    for (s, e) in lst:
        for (s2, e2) in faixas(n, s, e): camadas.append((MC, s2, e2))
def selo(d, im): caixa(d, W / 2, 660, ['JÁ SUBIU!', f'LANCE AGORA: R$ {int(float(LANCE)):,}'.replace(',', '.')], F('Black', 50), VM, BR, 36, 18, 30)
t_sel = saida('IMG_7713', 8.9); camadas.append((png('selo', selo), t_sel, ini_cena[2] + dur_cena[2] - X))
ent = f'-i {T}/junto.mp4 -i {T}/card.mp4 ' + ''.join(f'-loop 1 -framerate 30 -i {c[0]} ' for c in camadas)
fc = f'[0:v][1:v]xfade=transition=fade:duration={X}:offset={total - X:.3f}[b0];'; ult = '[b0]'
for j, (_, s, e) in enumerate(camadas): fc += f"{ult}[{j + 2}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})':shortest=0[c{j}];"; ult = f'[c{j}]'
sh(f'ffmpeg -nostdin -v error -y {ent} -filter_complex "{fc[:-1]}" -map "{ult}" -t {TT:.3f} -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p {T}/video_sem_som.mp4')
MUS = f'{MK}/marca/trilhas-base/pegada-orla/04-funky-soul-house.mp3'
sh(f'ffmpeg -nostdin -v error -y -i {MUS} -af "atrim=0:{TT:.3f},asetpts=N/SR/TB" -ar 48000 -ac 2 {T}/mus.wav')
vol = f"volume='if(lt(t,{total - X:.2f}),0.07,0.30)':eval=frame"
sh(f'ffmpeg -nostdin -v error -y -i {T}/voz.wav -i {T}/mus.wav -filter_complex "[0:a]apad,atrim=0:{TT:.3f}[v];[1:a]{vol},afade=t=out:st={TT - 0.8:.2f}:d=0.8[m];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TT:.3f},asetpts=N/SR/TB" -ar 48000 {T}/mix.wav')
final = f'{OUT}/NOVELINHA-EP01-PCX-48-vezes.mp4'
sh(f'ffmpeg -nostdin -v error -y -i {T}/video_sem_som.mp4 -i {T}/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "{final}"')
print('ok', round(TT, 2), 'cenas', [round(x, 2) for x in ini_cena], [round(x, 2) for x in dur_cena], 'selo', round(t_sel, 2))
