# Série JÁ ENCONTROU O DONO · EP. 03 (20/11): a Elisama, amiga do Murilo, buscou o iPhone 18 Pro Max (arrematado por R$ 7.750 em 11/11,
# conferido no sistema). Corta só as pausas e o "hoje tem MacBook" do fim. Chamada: sábado 21/11 21h tem outro iPhone 18 Pro Max.
# Uso: montar.py <proxy.mp4> <saida.mp4>
import sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PX, SAIDA = sys.argv[1:3]; MK = '/home/user/Leil-onozaplivoo/marketing'; W, H, FPS = 1080, 1920, 30
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
VERDE, OURO, AMA, NOITE, BR, VERM = (27, 122, 72), (245, 196, 81), (255, 214, 10), (10, 20, 16), (255, 255, 255), (222, 30, 38)
TRE = [(0.0, 6.75), (7.6, 27.4), (27.45, 42.62)]  # tira só a pausa e o "hoje tem MacBook" do fim (já passou)
# legenda (tempo original): texto em pedaços curtos, palavras-chave em amarelo
LEG = [(0.05, 2.5, 'ESTAMOS AQUI COM A ELISAMA'), (2.5, 4.0, 'AMIGA DO *MURILO*'), (3.9, 6.7, 'QUE ARREMATOU O *IPHONE 18 PRO MAX*'),
       (7.69, 9.6, 'ELISAMA, É DE *VERDADE?*'), (9.7, 10.6, 'É *GOLPE* OU NÃO É?'), (10.95, 12.0, 'NÃO É *GOLPE*, GENTE!'), (12.0, 15.4, 'TÔ AQUI *PESSOALMENTE*, NO RECREIO'),
       (15.87, 16.9, 'É *SUPER VERDADE*'), (17.1, 19.0, 'EU DESCONFIEI UM POUCO'), (19.0, 21.8, 'MAS QUANDO VI AQUI...'), (21.85, 23.4, 'CELULAR *LACRADO*'), (23.4, 25.6, 'COM *NOTA FISCAL* E TUDO'),
       (25.77, 26.7, 'ENTÃO É *VERDADE!*'), (27.43, 30.5, 'E A SENSAÇÃO DE SEGURAR'), (30.5, 32.5, 'UM IPHONE *ARREMATADO?*'), (33.03, 34.0, 'MUITO *FELIZ!*'),
       (34.0, 36.3, 'É DE ÚLTIMA EDIÇÃO, UM *18 PRO MAX*'), (36.9, 38.9, 'QUE ACABOU DE CHEGAR NO *MERCADO*'), (39.9, 41.5, 'TU INDICA PROS *AMIGOS?*'), (41.54, 42.6, '*INDICO!* SUPER.')]
SELO = [(3.9, 15.0, 'iPHONE 18 PRO MAX', 'arrematado pelo Murilo por', 'R$ 7.750')]
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((230, 90))
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def legenda(fr, to):
    for a, b, t in LEG:
        if a <= to < b:
            d = ImageDraw.Draw(fr); ws = [(w.replace('*', ''), 0) for w in t.split()]
            # junta palavras de um destaque com várias palavras (*R$ 6.370*)
            tam = 78
            while sum(d.textlength(w + ' ', font=F('Black', tam)) for w, _ in ws) > 980: tam -= 4
            f = F('Black', tam); x = W / 2 - sum(d.textlength(w + ' ', font=f) for w, _ in ws) / 2; y = 1500
            dest = False
            for w, k in ws:
                if w and t.count('*') and ('*' + w in t or w + '*' in t or ('*' in t and dest)): pass
                ww = d.textlength(w, font=f); kk = destaque(t, w)
                if kk: d.rounded_rectangle((x - 10, y - 52, x + ww + 10, y + 48), 14, fill=AMA)
                d.text((x, y), w, font=f, fill=NOITE if kk else BR, anchor='lm', stroke_width=0 if kk else 7, stroke_fill=(0, 0, 0))
                x += d.textlength(w + ' ', font=f)
            return
def destaque(t, w):
    import re
    for m in re.findall(r'\*([^*]+)\*', t):
        if w in [x.replace('*', '') for x in m.split()]: return True
    return False
def selo(fr, to):
    """etiqueta compacta no alto, na parede (acima da cabeça), para não cobrir o rosto"""
    for a, b, t1, t2, t3 in SELO:
        if a <= to < b and to > 3.2:
            k = ease((to - 3.2) / .35) * ease((b - to) / .3); d = ImageDraw.Draw(fr); f1, f2, f3 = F('Black', 40), F('Bold', 28), F('Black', 58)
            w = max(d.textlength(t1, font=f1), d.textlength(t2, font=f2), d.textlength(t3, font=f3)) + 70; x0 = -w + (w + 36) * k; y0 = 228
            d.rounded_rectangle((x0, y0, x0 + w, y0 + 182), 26, fill=VERDE); d.rounded_rectangle((x0 + w - 14, y0, x0 + w, y0 + 182), 7, fill=AMA)
            d.text((x0 + 30, y0 + 38), t1, font=f1, fill=BR, anchor='lm'); d.text((x0 + 30, y0 + 80), t2, font=f2, fill=(205, 235, 215), anchor='lm'); d.text((x0 + 30, y0 + 136), t3, font=f3, fill=AMA, anchor='lm')
def gancho(fr, tl):
    if tl > 3.0: return
    d = ImageDraw.Draw(fr); k = ease(tl / .25); f = F('Black', int(118 * (.8 + .2 * k)))
    t = 'JÁ ENCONTROU O DONO'; f = F('Black', int(76 * (.8 + .2 * k))); w = d.textlength(t, font=f); d.rounded_rectangle((W / 2 - w / 2 - 40, 240, W / 2 + w / 2 + 40, 350), 40, fill=VERDE); d.text((W / 2, 295), t, font=f, fill=BR, anchor='mm')
    f2 = F('Black', 40); t2 = 'EP. 03'; w2 = d.textlength(t2, font=f2); d.rounded_rectangle((W / 2 - w2 / 2 - 26, 368, W / 2 + w2 / 2 + 26, 432), 32, fill=AMA); d.text((W / 2, 400), t2, font=f2, fill=NOITE, anchor='mm')
def topo(fr):
    p = Image.new('RGBA', (W, H)); ImageDraw.Draw(p).rounded_rectangle((W / 2 - LOGO.width / 2 - 20, 110, W / 2 + LOGO.width / 2 + 20, 130 + LOGO.height), 26, fill=(10, 20, 16, 160))
    fr.alpha_composite(p); fr.alpha_composite(LOGO, (int(W / 2 - LOGO.width / 2), 120))
enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', SAIDA + '.v.mp4'], stdin=subprocess.PIPE)
tl = 0.0
for ti, (a, b) in enumerate(TRE):
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{a:.3f}', '-i', PX, '-t', f'{b - a:.3f}', '-vf', f'fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE); n = 0
    z0 = 1.0 if ti % 2 == 0 else 1.08   # alterna enquadramento a cada corte (dá ritmo de jump cut)
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        to = a + n / FPS; im = Image.frombytes('RGB', (W, H), buf); z = z0 + (.14 * (1 - ease(n / 7)) if ti else 0)
        cw, ch = W / z, H / z; x0 = (W - cw) / 2; y0 = (H - ch) * .35
        fr = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS).convert('RGBA')
        if ti and n < 3: fr = fr.filter(ImageFilter.BoxBlur(10 - 3 * n))
        if ti and n < 4: fr.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(170 * (1 - n / 4)))))
        topo(fr); selo(fr, to); legenda(fr, to); gancho(fr, tl)
        enc.stdin.write(fr.convert('RGB').tobytes()); n += 1; tl += 1 / FPS
    p.wait()
FIM = 4.0
for n in range(int(FIM * FPS)):
    t = n / FPS; fr = Image.new('RGBA', (W, H), NOITE + (255,)); g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((-200, 380, W + 200, 1500), fill=VERDE + (140,)); fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((440, 190)); fr.alpha_composite(lg, (int(W / 2 - lg.width / 2), 300))
    k = ease(t / .35); d = ImageDraw.Draw(fr)
    f = F('Black', 44); tx = 'JÁ ENCONTROU O DONO · EP. 03'; w = d.textlength(tx, font=f); d.rounded_rectangle((W / 2 - w / 2 - 34, 560, W / 2 + w / 2 + 34, 650), 45, fill=VERDE); d.text((W / 2, 606), tx, font=f, fill=BR, anchor='mm')
    d.text((W / 2, 800), 'O PRÓXIMO DONO', font=F('Black', int(100 * (.85 + .15 * k))), fill=BR, anchor='mm'); d.text((W / 2, 920), 'PODE SER VOCÊ', font=F('Black', int(100 * (.85 + .15 * k))), fill=OURO, anchor='mm')
    if t > .6:
        d.text((W / 2, 1070), 'sábado tem outro', font=F('SemiBold', 50), fill=BR, anchor='mm'); d.text((W / 2, 1150), 'iPHONE 18 PRO MAX', font=F('Black', 76), fill=AMA, anchor='mm')
    if t > 1.1:
        f = F('Black', 54); tx = 'Comenta EU QUERO'; w = d.textlength(tx, font=f); d.rounded_rectangle((W / 2 - w / 2 - 40, 1270, W / 2 + w / 2 + 40, 1376), 53, fill=AMA); d.text((W / 2, 1323), tx, font=f, fill=NOITE, anchor='mm')
        d.text((W / 2, 1440), 'que eu te envio o link', font=F('SemiBold', 44), fill=BR, anchor='mm')
    enc.stdin.write(fr.convert('RGB').tobytes())
enc.stdin.close(); enc.wait()
fc = ''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - .03:.3f}:d=0.03[a{i}];' for i, (a, b) in enumerate(TRE))
fc += ''.join(f'[a{i}]' for i in range(len(TRE))) + f'concat=n={len(TRE)}:v=0:a=1,loudnorm=I=-16:TP=-1.5,apad=pad_dur={FIM}[fala];'
fc += f'[1:a]aloop=-1:size=2e9,atrim=0:{tl + FIM:.3f},volume=0.07,afade=t=out:st={tl + FIM - 1:.3f}:d=1[tri];[2:a]adelay={int(tl * 1000)}|{int(tl * 1000)},volume=1.1[ass];[fala][tri][ass]amix=inputs=3:normalize=0:duration=first[mix]'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', PX, '-i', f'{MK}/marca/trilhas-base/trilha-house-brasileiro.mp3', '-i', f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3', '-i', SAIDA + '.v.mp4',
                '-filter_complex', fc, '-map', '3:v', '-map', '[mix]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', SAIDA], check=True)
print('ok', round(tl + FIM, 1))
