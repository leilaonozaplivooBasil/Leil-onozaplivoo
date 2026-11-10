# Vídeo animado do banner "Leilão da Felicidade" (sem créditos de IA): zoom lento no palco, confete, balão que salta,
# título que entra com brilho dourado, botão que pulsa e a voz oficial do leiloeiro (v3). A boca do leiloeiro fica parada.
# Uso: animar.py <cena.png> <voz.mp3> <musica.mp3> <saida.mp4>
import sys, os, math, random, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
cena, voz, musica, out = sys.argv[1:5]; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H, FPS, DUR = 1920, 1080, 30, 7.0
BR, OURO, NEON, ESC, VERDE = (255,255,255), (245,196,81), (61,220,132), (8,30,24), (27,122,72)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
def camada(): return Image.new('RGBA', (W, H), (0,0,0,0))
def cabe(d, t, f, maxw):
    while d.textlength(t, font=f) > maxw: f = ImageFont.truetype(f.path, f.size - 2)
    return f
X, MAXW = 1020, 820
# fundo grande (para o zoom) + sombra do lado do texto
base = Image.open(cena).convert('RGB').resize((round(W*1.08), round(H*1.08)), Image.LANCZOS)
g = Image.new('L', (W, 1)); [g.putpixel((x, 0), int(125*min(1, max(0, (x-880)/420))**1.3)) for x in range(W)]
sombra = Image.new('RGBA', (W, H), (6,14,12,0)); sombra.putalpha(g.resize((W, H)))
# camadas
logo = camada(); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((360, 130)); logo.alpha_composite(lg, (X + (MAXW - lg.width)//2 + 60, 70))
bal = camada(); d = ImageDraw.Draw(bal); bx0, by0, bx1, by1 = 905, 245, 1560, 455
sh = camada(); ImageDraw.Draw(sh).rounded_rectangle((bx0+6, by0+14, bx1+6, by1+14), 40, fill=(0,0,0,110)); bal.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
d.rounded_rectangle((bx0, by0, bx1, by1), 40, fill=BR); d.polygon([(bx0+8, by0+110), (bx0-40, by0+150), (bx0+10, by0+158)], fill=BR)
f = F('Bold', 44)
for i, partes in enumerate([[('Eii, vem conhecer o', ESC)], [('Leilão da Felicidade', VERDE), (',', ESC)], [('aqui você ganha ', ESC), ('ou ganha!', VERDE)]]):
    x = bx0 + 44
    for t, cor in partes: d.text((x, by0 + 34 + i*56), t, font=f, fill=cor); x += d.textlength(t, font=f)
kick = camada(); d = ImageDraw.Draw(kick); k = ' '.join('SEJA BEM-VINDO AO'); d.text((X+60, 540), k, font=cabe(d, k, F('Bold', 30), MAXW), fill=NEON)
def titulo(t, y, cor):
    c = camada(); d = ImageDraw.Draw(c); fo = cabe(d, t, F('Black', 150), MAXW)
    gl = camada(); ImageDraw.Draw(gl).text((X+60, y), t, font=fo, fill=cor+(160,)); c.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
    d.text((X+60, y), t, font=fo, fill=cor); m = camada(); ImageDraw.Draw(m).text((X+60, y), t, font=fo, fill=(255,255,255,255))
    return c, m.split()[3]
t1, _ = titulo('LEILÃO DA', 590, BR); t2, m2 = titulo('FELICIDADE', 735, OURO)
linha = camada(); ImageDraw.Draw(linha).line((X+64, 905, X+230, 905), fill=NEON, width=5)
bot = camada(); d = ImageDraw.Draw(bot); fb = F('Black', 42); tb = 'QUERO CONHECER  →'; wb = d.textlength(tb, font=fb)
BX = (X+60, 935, X+60+wb+110, 1035)
gl = camada(); ImageDraw.Draw(gl).rounded_rectangle(BX, 50, fill=NEON+(200,)); bot.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
d.rounded_rectangle(BX, 50, fill=NEON); d.text((BX[0]+55, 985), tb, font=fb, fill=ESC, anchor='lm')
# confete
random.seed(7); CONF = [(random.uniform(0, W), random.uniform(-H, H), random.uniform(60, 140), random.uniform(0, 6.28), random.choice([OURO, (255,220,120), (255,240,200), NEON])) for _ in range(90)]
def eo(x): x = max(0, min(1, x)); return 1 - (1 - x)**3
def pop(x):  # salto com leve passada do ponto
    x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
def alfa(img, a):
    if a >= 1: return img
    c = img.copy(); c.putalpha(c.split()[3].point(lambda v: int(v*a))); return c
def escala(img, s, cx, cy):
    if abs(s-1) < 1e-3: return img
    if s <= 0.01: return camada()
    w, h = round(W*s), round(H*s); r = img.resize((w, h), Image.BILINEAR); c = camada()
    ox, oy = round(cx - cx*s), round(cy - cy*s)
    big = camada(); big.paste(r, (ox, oy), r) if True else None
    return big
tmp = tempfile.mkdtemp()
for n in range(int(DUR*FPS)):
    t = n / FPS
    z = 1.0 + 0.06*(t/DUR); cw = round(base.width/z); ch = round(cw*H/W)
    x0 = (base.width-cw)//2; y0 = (base.height-ch)//2
    fr = base.crop((x0, y0, x0+cw, y0+ch)).resize((W, H), Image.BILINEAR).convert('RGBA')
    fr.alpha_composite(sombra)
    cf = camada(); dc = ImageDraw.Draw(cf)
    for (x0, y0, v, ph, cor) in CONF:
        y = (y0 + v*t*1.6) % (H + 60) - 30; x = x0 + 18*math.sin(ph + t*2.2); s = 5 + 3*abs(math.sin(ph + t*5))
        dc.rectangle((x, y, x+s, y+9), fill=cor + (210,))
    fr.alpha_composite(cf)
    fr.alpha_composite(alfa(logo, eo((t-0.1)/0.5)))
    if t >= 0.25: fr.alpha_composite(escala(bal, pop((t-0.25)/0.45), bx0-30, by0+150))
    if t >= 1.0: fr.alpha_composite(alfa(kick, eo((t-1.0)/0.4)))
    for c, t0 in ((t1, 1.2), (t2, 1.5)):
        if t >= t0:
            a = eo((t-t0)/0.45); sl = camada(); sl.alpha_composite(alfa(c, a), (round(-80*(1-a)), 0)); fr.alpha_composite(sl)
    if t >= 2.2:  # brilho passando no FELICIDADE
        px = X + 60 + (t - 2.2) % 2.6 / 1.2 * 1100 - 200
        g2 = Image.new('L', (W, H), 0); ImageDraw.Draw(g2).polygon([(px, 720), (px+90, 720), (px-10, 880), (px-100, 880)], fill=200)
        g2 = Image.composite(g2.filter(ImageFilter.GaussianBlur(10)), Image.new('L', (W, H), 0), m2)
        br = Image.new('RGBA', (W, H), (255,255,240,0)); br.putalpha(g2); fr.alpha_composite(br)
    if t >= 1.9: fr.alpha_composite(alfa(linha, eo((t-1.9)/0.3)))
    if t >= 2.4:
        s = pop((t-2.4)/0.4) * ((1 + 0.05*max(0, math.sin((t-4.6)*6.0))) if t > 4.6 else 1)
        fr.alpha_composite(escala(bot, s, (BX[0]+BX[2])/2, (BX[1]+BX[3])/2))
    fr.convert('RGB').save(f'{tmp}/f{n:04d}.jpg', quality=92)
# áudio: voz entra em 0,35 s; música de auditório baixinha por baixo, com ducking
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/f%04d.jpg', '-i', voz, '-i', musica, '-filter_complex',
    f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=350:all=1,apad=whole_dur={DUR},volume=1.15,asplit[v][sc];"
    f"[2:a]atrim=0.5:{DUR+0.5},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.32,afade=t=in:d=0.4,afade=t=out:st={DUR-1.0}:d=1.0[m];"
    "[m][sc]sidechaincompress=threshold=0.04:ratio=4:attack=20:release=350[md];[v][md]amix=inputs=2:duration=first:normalize=0[a]",
    '-map', '0:v', '-map', '[a]', '-t', str(DUR), '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print('ok')
