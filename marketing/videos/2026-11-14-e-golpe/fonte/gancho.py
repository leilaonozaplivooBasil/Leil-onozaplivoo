# Gancho do vídeo "É GOLPE?": chuva de mensagens (4 prints REAIS com nome/número borrados + balões estilo WhatsApp SEM
# nome/número, com as dúvidas que a equipe recebe), cada vez mais rápido, com "plim"; congela e corta para
# "TODO DIA A GENTE RECEBE ESSA PERGUNTA." com a martelada. Uso: gancho.py <saida.mp4>
import sys, os, math, random, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]; F0 = os.path.dirname(os.path.abspath(__file__)); MK = '/home/user/Leil-onozaplivoo/marketing'
W, H, FPS = 1080, 1920, 30; OURO, NOITE, BR = (245, 196, 81), (8, 20, 14), (255, 255, 255)
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{p}.otf', t)
def arredonda(im, r=34):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width-1, im.height-1), r, fill=255); o = im.convert('RGBA'); o.putalpha(m); return o
def balao(txt, hora):
    f = F('Regular', 46); fh = F('Regular', 26); d0 = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    w = int(d0.textlength(txt, font=f)) + 150; im = Image.new('RGBA', (w, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w-1, 119), 30, fill=(32, 44, 51, 255)); d.text((34, 58), txt, font=f, fill=(233, 237, 239), anchor='lm')
    d.text((w-22, 96), hora, font=fh, fill=(140, 150, 155), anchor='rm'); return im
reais = [arredonda(Image.open(f'{F0}/prints/{n}.png')) for n in ('golpe', 'e-verdade', 'iphone-207', 'encaminhada-207')]
falsos_txt = [('Isso é golpe?', '19:02'), ('Funciona de verdade?', '10:41'), ('É real isso?', '21:15'), ('Já ganhou alguém mesmo?', '13:07'),
              ('Ninguém vende iPhone por 200...', '18:20'), ('Tô desconfiado', '09:33')]
estilo = [balao(t, h) for t, h in falsos_txt]
ordem = [reais[0], estilo[0], reais[1], estilo[1], reais[2], estilo[2], estilo[3], reais[3], estilo[4], estilo[5]]
# tempos de entrada: começa espaçado e acelera
T = []; t = 0.2; passo = 0.62
for _ in ordem: T.append(round(t, 3)); t += passo; passo = max(0.16, passo*0.80)
FIM_CHUVA = T[-1] + 0.6; CORTE = FIM_CHUVA + 0.12; DUR = CORTE + 1.8
random.seed(8); POS = []
for i, im in enumerate(ordem):
    s = min((W - 70)/im.width, 1.45*random.uniform(0.95, 1.05))
    POS.append((random.uniform(35, max(36, W - 35 - im.width*s)), 230 + (i*181) % 1420 + random.uniform(-30, 30), s, random.uniform(-7, 7)))
fundo = Image.new('RGBA', (W, H), (11, 20, 26, 255)); df = ImageDraw.Draw(fundo)
for k in range(260):  # padrão discreto de fundo de conversa
    x, y = random.uniform(0, W), random.uniform(0, H); df.ellipse((x-3, y-3, x+3, y+3), fill=(20, 32, 40, 255))
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((300, 110))
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
tmp = tempfile.mkdtemp()
for k in range(round(DUR*FPS)):
    t = k/FPS
    if t < CORTE:
        fr = fundo.copy(); tt = min(t, FIM_CHUVA)
        for im, t0, (x, y, s, r) in zip(ordem, T, POS):
            if tt < t0: continue
            a = pop((tt - t0)/0.22); sc = s*a
            if sc < 0.03: continue
            b = im.resize((max(1, int(im.width*sc)), max(1, int(im.height*sc))), Image.LANCZOS).rotate(r, resample=Image.BICUBIC, expand=True)
            sh = Image.new('RGBA', b.size, (0, 0, 0, 0)); sh.putalpha(b.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v*0.6)))
            fr.alpha_composite(sh, (int(x+8), int(y+14))); fr.alpha_composite(b, (int(x), int(y)))
        if t > FIM_CHUVA:  # congela e pisca
            fr.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(180*(t - FIM_CHUVA)/0.12))))
        sk = int(10*math.sin(t*60)*max(0, (t - 1.6)/(FIM_CHUVA - 1.6))) if t > 1.6 else 0  # tremor crescente
        out = Image.new('RGB', (W, H), (0, 0, 0)); out.paste(fr.convert('RGB'), (sk, -sk//2))
    else:
        tc = t - CORTE; fr = Image.new('RGBA', (W, H), NOITE + (255,)); d = ImageDraw.Draw(fr)
        g = Image.new('RGBA', (W, H)); ImageDraw.Draw(g).ellipse((W/2-500, H/2-500, W/2+500, H/2+500), fill=(27, 122, 72, 160)); fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(200)))
        a = min(1, tc/0.18); fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Black.otf', 92)
        for txt, y, cor in (('TODO DIA', 780, BR), ('A GENTE RECEBE', 890, BR), ('ESSA PERGUNTA.', 1010, OURO)):
            d.text((W/2, y), txt, font=fb, fill=cor + (int(255*a),), anchor='mm')
        fr.alpha_composite(lg, ((W - lg.width)//2, 1240))
        out = fr.convert('RGB')
    out.save(f'{tmp}/f{k:04d}.jpg', quality=92)
PLIM = f'{MK}/videos/leila-chegou-iphone/sfx/pop.mp3'; MART = f'{MK}/videos/leila-chegou-iphone/sfx/martelo.mp3'
ent = []; fc = []; mix = ''
for i, t0 in enumerate(T):
    ent += ['-i', PLIM]; fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,asetrate=48000*{1 + i*0.04:.2f},aresample=48000,volume=0.8,adelay={int(t0*1000)}:all=1[p{i}]"); mix += f'[p{i}]'
ent += ['-i', MART]; j = len(T); fc.append(f"[{j}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=4,adelay={int(CORTE*1000)}:all=1[m]"); mix += '[m]'
fc.append(f"{mix}amix=inputs={j+1}:duration=longest:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-14:TP=-1.5[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ent + ['-filter_complex', ';'.join(fc), '-map', '[a]', '-ar', '48000', f'{tmp}/a.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/f%04d.jpg', '-i', f'{tmp}/a.wav', '-map', '0:v', '-map', '1:a', '-t', str(DUR),
                '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT], check=True)
print('ok', round(DUR, 2), T)
