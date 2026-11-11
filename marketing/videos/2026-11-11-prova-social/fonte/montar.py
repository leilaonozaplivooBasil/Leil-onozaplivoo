# Vídeo de PROVA SOCIAL (11/11): gancho "SERÁ QUE CHEGA MESMO?" + 8 provas reais (prints de WhatsApp, vídeos e fotos de quem recebeu)
# + fechamento "TUDO REAL. TUDO ENTREGUE." com a assinatura sonora oficial. Sem link e sem % (regra do Instagram até 29/11).
# Uso: montar.py <pasta-com-in/> <saida.mp4>
import sys, os, math, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S, OUT = sys.argv[1:3]; IN = f'{S}/in'; MK = '/home/user/Leil-onozaplivoo/marketing'
W, H, FPS = 1080, 1920, 30
VERDE, OURO, NOITE, BR, NEON, FOGO = (27,122,72), (245,196,81), (10,20,16), (255,255,255), (61,220,132), (243,91,18)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
PROB = []
def cabe(d, t, f, maxw):
    while d.textlength(t, font=f) > maxw: f = ImageFont.truetype(f.path, f.size - 2)
    return f
def eo(x): x = max(0, min(1, x)); return 1 - (1 - x)**3
def pop(x): x = max(0, min(1, x)); return 1 + 2.7*(x-1)**3 + 1.7*(x-1)**2 if x > 0 else 0
def cover(im, w=W, h=H):
    r = max(w/im.width, h/im.height); im = im.resize((round(im.width*r), round(im.height*r)), Image.LANCZOS)
    x, y = (im.width-w)//2, (im.height-h)//2; return im.crop((x, y, x+w, y+h))
def fundo_borrado(im):
    b = cover(im.convert('RGB'), W//4, H//4).filter(ImageFilter.GaussianBlur(10)).resize((W, H))
    return Image.blend(b, Image.new('RGB', (W, H), NOITE), 0.45)
def frames_video(arq, ini, dur, modo='cover'):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ini), '-t', str(dur + 0.2), '-i', arq, '-vf', f'fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', arq], capture_output=True, text=True).stdout.strip().split(','))
    n = len(p) // (w*h*3); fr = [Image.frombytes('RGB', (w, h), p[i*w*h*3:(i+1)*w*h*3]) for i in range(n)]
    return fr
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((250, 92))
def pilula(d, cx, cy, t, f, fundo, cor, r):
    w = d.textlength(t, font=f)
    if w + 2*r > W - 40: PROB.append(f'"{t}" não cabe')
    d.rounded_rectangle((cx-w/2-r, cy-r, cx+w/2+r, cy+r), r, fill=fundo); d.text((cx, cy+2), t, font=f, fill=cor, anchor='mm')
def check(d, cx, cy, s, cor):
    d.line([(cx-s*0.45, cy), (cx-s*0.12, cy+s*0.35), (cx+s*0.5, cy-s*0.4)], fill=cor, width=max(4, int(s*0.2)), joint='curve')
def camada_topo(fr, n_prova, t):
    d = ImageDraw.Draw(fr)
    sh = Image.new('L', (1, 330)); [sh.putpixel((0, y), int(150*(1-y/330))) for y in range(330)]
    s = Image.new('RGBA', (W, 330), NOITE+(0,)); s.putalpha(sh.resize((W, 330))); fr.alpha_composite(s)
    fr.alpha_composite(LOGO, (48, 210))
    if n_prova:
        f = F('Black', 38); t_ = f'PROVA {n_prova} DE 8'; w = d.textlength(t_, font=f)
        d.rounded_rectangle((W-60-w-60, 222, W-60, 292), 35, fill=FOGO); d.text((W-60-(w+60)/2, 258), t_, font=f, fill=BR, anchor='mm')
def rotulo(fr, t_cena, titulo):
    if t_cena < 0.18: return
    a = pop((t_cena-0.18)/0.4); lay = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(lay)
    f = cabe(d, titulo, F('Black', 74), W-260); w = d.textlength(titulo, font=f); r = 58; cx, cy = W/2 + 34, 1500
    d.rounded_rectangle((cx-w/2-r-70, cy-r, cx+w/2+r, cy+r), r, fill=OURO+(255,))
    d.ellipse((cx-w/2-r-60, cy-46, cx-w/2-r+32, cy+46), fill=VERDE); check(d, cx-w/2-r-14, cy+2, 50, BR)
    d.text((cx-10, cy+3), titulo, font=f, fill=(10,60,32), anchor='mm')
    sm = lay.split()[3].filter(ImageFilter.GaussianBlur(16)).point(lambda v: v*0.5); sd = Image.new('RGBA', (W, H), (0,0,0,0)); sd.putalpha(sm)
    lay = Image.alpha_composite(sd, lay)
    if a < 0.999:
        lw, lh = max(1, round(W*a)), max(1, round(H*a)); r_ = lay.resize((lw, lh)); lay = Image.new('RGBA', (W, H), (0,0,0,0)); lay.paste(r_, (round(cx - cx*a), round(cy - cy*a)), r_)
    fr.alpha_composite(lay)
def foto_kb(im, t, dur, alvo, z1):
    # foto inteira encaixada (com fundo borrado), aproximando devagar do ponto 'alvo' (fração da imagem)
    base = fundo_borrado(im).convert('RGBA'); r = min(W*0.94/im.width, H*0.80/im.height)
    fw, fh = round(im.width*r), round(im.height*r); fg = im.convert('RGB').resize((fw, fh), Image.LANCZOS)
    ox, oy = (W-fw)//2, (H-fh)//2 + 40
    cv = base.copy(); m = Image.new('L', (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw, fh), 34, fill=255)
    sh = Image.new('RGBA', (W, H), (0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((ox+8, oy+18, ox+fw+8, oy+fh+18), 34, fill=(0,0,0,150)); cv.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    cv.paste(fg, (ox, oy), m)
    z = 1 + (z1-1)*eo(t/dur)*0.9 + (z1-1)*0.1*(t/dur)
    px, py = ox + alvo[0]*fw, oy + alvo[1]*fh
    cw, ch = W/z, H/z; x0 = min(max(0, px - cw/2), W-cw); y0 = min(max(0, py - ch/2), H-ch)
    return cv.crop((round(x0), round(y0), round(x0+cw), round(y0+ch))).resize((W, H), Image.BILINEAR)
# ---- cenas: (tipo, fonte, duração, rótulo, extra)
CENAS = [('gancho', 'v1.mp4', 2.1, None, 0.0),
         ('video', 'v1.mp4', 2.6, 'ENTREGA CHEGANDO', 2.0),
         ('foto', 'f1.jpg', 2.8, 'PS5 CHEGOU CERTINHO', (0.38, 0.70, 1.55)),
         ('video', 'v3.mp4', 2.2, 'CAIXA NA PORTA', 0.6),
         ('foto', 'f2.jpg', 2.8, 'iPHONE NA MÃO', (0.32, 0.74, 1.55)),
         ('video', 'v4.mp4', 2.2, 'PATINETE ELÉTRICO', 0.3),
         ('foto', 'f3.jpg', 2.6, 'E JÁ MANDOU FOTO', (0.40, 0.25, 1.6)),
         ('video_h', 'v2.mp4', 2.4, 'TV NOVA NO JOGO', 3.0),
         ('foto', 'f4.jpg', 2.8, 'NOTEBOOK DELL', (0.62, 0.50, 1.25)),
         ('fim', None, 4.2, None, None)]
tmp = tempfile.mkdtemp(); n = 0; CORTES = []; t_glob = 0.0; n_prova = 0
gancho_bg = None
for tipo, src, dur, rot, ex in CENAS:
    CORTES.append(t_glob); nf = round(dur*FPS)
    if tipo in ('video', 'video_h'): fr_v = frames_video(f'{IN}/{src}', ex, dur)
    if tipo == 'gancho': fr_v = frames_video(f'{IN}/{src}', ex, dur)
    if tipo == 'foto': im = Image.open(f'{IN}/{src}')
    if tipo not in ('gancho', 'fim'): n_prova += 1
    for k in range(nf):
        t = k / FPS
        if tipo == 'gancho':
            b = fundo_borrado(fr_v[min(k, len(fr_v)-1)]).convert('RGBA'); d = ImageDraw.Draw(b)
            sx = round(10*math.sin(t*55)*max(0, 1-t/0.5))
            for txt, y, f, cor, t0 in (('SERÁ QUE', 760, F('Black', 150), BR, 0.0), ('CHEGA MESMO?', 920, F('Black', 150), OURO, 0.25)):
                if t >= t0:
                    a = pop((t-t0)/0.35); ff = ImageFont.truetype(f.path, max(10, round(cabe(d, txt, f, W-80).size*a)))
                    d.text((W/2+sx+6, y+8), txt, font=ff, fill=(0,0,0), anchor='mm'); d.text((W/2+sx, y), txt, font=ff, fill=cor, anchor='mm')
            if t >= 1.05: pilula(d, W/2, 1120, 'olha o que chegou essa semana', F('Bold', 48), VERDE, BR, 42)
            fr = b
        elif tipo in ('video', 'video_h'):
            v = fr_v[min(k, len(fr_v)-1)]
            if tipo == 'video':
                fr = cover(v).convert('RGBA')
            else:
                fr = fundo_borrado(v).convert('RGBA'); r = W*1.0/v.width; vv = v.resize((W, round(v.height*r)), Image.LANCZOS)
                z = 1.0 + 0.05*t/dur; vv = vv.resize((round(vv.width*z), round(vv.height*z))); fr.paste(vv, ((W-vv.width)//2, (H-vv.height)//2 - 60))
            camada_topo(fr, n_prova, t); rotulo(fr, t, rot)
        elif tipo == 'foto':
            fr = foto_kb(im, t, dur, ex[:2], ex[2]).convert('RGBA'); camada_topo(fr, n_prova, t); rotulo(fr, t, rot)
        else:  # fim
            fr = Image.new('RGBA', (W, H), NOITE+(255,)); g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((-200, 300, W+200, 1500), fill=110)
            gl = Image.new('RGBA', (W, H), VERDE+(0,)); gl.putalpha(g.filter(ImageFilter.GaussianBlur(160))); fr.alpha_composite(gl); d = ImageDraw.Draw(fr)
            for txt, y, cor, t0 in (('TUDO REAL.', 640, BR, 0.0), ('TUDO ENTREGUE.', 790, OURO, 0.3)):
                if t >= t0:
                    a = pop((t-t0)/0.35); f = cabe(d, txt, F('Black', 150), W-80); ff = ImageFont.truetype(f.path, max(10, round(f.size*a)))
                    d.text((W/2+6, y+8), txt, font=ff, fill=(0,0,0), anchor='mm'); d.text((W/2, y), txt, font=ff, fill=cor, anchor='mm')
            if t >= 0.9: pilula(d, W/2, 960, 'o próximo pode ser você', F('Bold', 52), VERDE, BR, 44)
            if t >= 1.4:
                s = pop((t-1.4)/0.4) * (1 + 0.04*max(0, math.sin((t-2.2)*7)) if t > 2.2 else 1)
                lay = Image.new('RGBA', (W, H), (0,0,0,0)); dl = ImageDraw.Draw(lay); f = F('Black', 66); tx = 'COMENTA  EU QUERO'; w = dl.textlength(tx, font=f)
                dl.rounded_rectangle((W/2-w/2-70, 1140, W/2+w/2+70, 1260), 60, fill=NEON); dl.text((W/2, 1202), tx, font=f, fill=NOITE, anchor='mm')
                if s < 0.999:
                    r_ = lay.resize((max(1, round(W*s)), max(1, round(H*s)))); lay = Image.new('RGBA', (W, H), (0,0,0,0)); lay.paste(r_, (round(W/2*(1-s)), round(1200*(1-s))), r_)
                fr.alpha_composite(lay)
            if t >= 2.6:  # logo entra no "Leilão no Zap!" da assinatura (que começa em 2,0 s do fim)
                lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((420, 160)); a = eo((t-2.6)/0.3)
                lg.putalpha(lg.split()[3].point(lambda v: int(v*a))); fr.alpha_composite(lg, ((W-lg.width)//2, 1400))
        # transição: punch + flash nos primeiros quadros de cada cena
        if k < 6 and n > 0:
            a = 1 - k/6; z = 1 + 0.10*a; c = fr.resize((round(W*z), round(H*z))); x0, y0 = (c.width-W)//2, (c.height-H)//2; fr = c.crop((x0, y0, x0+W, y0+H))
            fl = Image.new('RGBA', (W, H), (255,255,255,int(150*a*a))); fr.alpha_composite(fl)
        fr.convert('RGB').save(f'{tmp}/f{n:05d}.jpg', quality=92); n += 1
    t_glob += nf / FPS
dur = n / FPS
# ---- áudio: música (pegada orla, brazilian bass) + whoosh em cada corte + pop no rótulo + assinatura sonora oficial no fim
SFX = f'{MK}/videos/leila-chegou-iphone/sfx'; ASS = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
ent = ['-i', f'{MK}/marca/trilhas-base/pegada-orla/05-brazilian-bass.mp3']; fc = []; mix = ['[m]']
t_ass = CORTES[-1] + 2.0
fc.append(f"[0:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55,afade=t=in:d=0.3,afade=t=out:st={t_ass-0.6}:d=1.0[m]")
k = 1
for i, c in enumerate(CORTES[1:]):
    ent += ['-i', f'{SFX}/whoosh.mp3']; fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.5,adelay={int(max(0,c-0.12)*1000)}:all=1[w{i}]"); mix.append(f'[w{i}]'); k += 1
for i, (c, cen) in enumerate(zip(CORTES, CENAS)):
    if cen[3]:
        ent += ['-i', f'{SFX}/pop.mp3']; fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45,adelay={int((c+0.2)*1000)}:all=1[p{i}]"); mix.append(f'[p{i}]'); k += 1
ent += ['-i', ASS]; fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(t_ass*1000)}:all=1[as]"); mix.append('[as]')
fc.append(''.join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,asetpts=N/SR/TB,apad,atrim=0:{dur}[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ent + ['-filter_complex', ';'.join(fc), '-map', '[a]', '-ar', '48000', f'{tmp}/mix.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/mix.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '48000', f'{tmp}/audio.wav'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/f%05d.jpg', '-i', f'{tmp}/audio.wav', '-map', '0:v', '-map', '1:a', '-t', f'{dur}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT], check=True)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', round(dur, 2), [round(c, 2) for c in CORTES])
