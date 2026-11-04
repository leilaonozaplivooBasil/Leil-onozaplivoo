# Reels do leilão do iPhone 17 Pro Max (sábado 07/11, 20h) — voz do Leiloeiro, fotos reais do anúncio, prova do Murilo
import subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = sys.argv[1]; FIM = sys.argv[2]   # 'feed' ou 'vendedores'
MK = '/home/user/Leil-onozaplivoo/marketing'; PROVA = '/home/user/leilonozap/public/provas/murilo-full.mp4'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H, FPS = 1080, 1920, 30
NOITE, FLORESTA, VERDE, OURO, LIMA, BRANCO = (0,24,13), (0,45,27), (27,122,72), (245,196,81), (63,208,126), (255,255,255)
def fundo():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.clip(1 - np.sqrt(((xx - W/2)/W)**2 + ((yy - H*0.42)/H)**2) * 1.6, 0, 1)
    c = np.array(NOITE, np.float32)[None,None] + (np.array(FLORESTA, np.float32) - np.array(NOITE, np.float32))[None,None] * g[...,None] * 1.4
    return Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).convert('RGBA')
BG = fundo()
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); LOGO.thumbnail((300, 110))
def recorte(p):
    im = Image.open(p).convert('RGBA'); bb = im.split()[3].getbbox(); return im.crop(bb)
FRENTE = recorte(f'{D}/rec1.png'); CAMERA = recorte(f'{D}/rec2.png')
def sombra_txt(d, xy, t, f, cor, anchor='mm'):
    for dx, dy in ((0,4),(2,5),(-2,5)): d.text((xy[0]+dx, xy[1]+dy), t, font=f, fill=(0,0,0,140), anchor=anchor)
    d.text(xy, t, font=f, fill=cor, anchor=anchor)
def pilula(d, cx, cy, t, f, fundo_c, texto_c, pad=40):
    w = d.textlength(t, font=f); h = f.size
    d.rounded_rectangle((cx - w/2 - pad, cy - h*0.8, cx + w/2 + pad, cy + h*0.8), int(h*0.8), fill=fundo_c); d.text((cx, cy), t, font=f, fill=texto_c, anchor='mm')
def entra(t, ini, dur=0.35):  # 0→1 com freio
    x = min(1, max(0, (t - ini) / dur)); return 1 - (1 - x) ** 3
def produto(img, alvo_h, t, ini, cx=W/2, cy=H*0.47, zoom=0.06, dur=3.0):
    q = entra(t, ini, 0.45); s = (0.86 + 0.14*q) * (1 + zoom * min(1, (t-ini)/dur))
    im = img.copy(); r = alvo_h * s / im.height; im = im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
    flut = math.sin((t-ini) * 2.2) * 10
    halo = Image.new('RGBA', (W, H), (0,0,0,0)); dh = ImageDraw.Draw(halo)
    dh.ellipse((cx - im.width*0.7, cy - im.height*0.55, cx + im.width*0.7, cy + im.height*0.55), fill=(63,208,126,55)); halo = halo.filter(ImageFilter.GaussianBlur(90))
    return halo, im, (int(cx - im.width/2), int(cy - im.height/2 + flut)), q
def quadro(t):
    c = BG.copy()
    if t < 5.35:      # cena 1: o iPhone entra
        halo, im, pos, q = produto(FRENTE, 820, t, 0.0, cy=H*0.56)
        c.alpha_composite(halo); a = im.copy(); a.putalpha(a.split()[3].point(lambda v: int(v*q))); c.alpha_composite(a, pos)
        d = ImageDraw.Draw(c); k = entra(t, 0.9)
        if k > 0:
            sombra_txt(d, (W/2, 330 - 30*(1-k)), 'IPHONE 17 PRO MAX', F('Black', 92), BRANCO + (int(255*k),))
            sombra_txt(d, (W/2, 430 - 30*(1-k)), '256 GB · Prateado', F('Bold', 54), LIMA + (int(255*k),))
        k = entra(t, 1.5)
        if k > 0: pilula(d, W/2, 1640 + 40*(1-k), 'LEILÃO NO SÁBADO', F('Black', 52), VERDE + (int(240*k),), BRANCO + (int(255*k),))
    elif t < 7.45:    # cena 2: preço de loja (dado do comparador, Mercado Livre)
        halo, im, pos, q = produto(CAMERA, 720, t, 5.35, cy=H*0.62, zoom=0.10, dur=2.0)
        c.alpha_composite(halo); c.alpha_composite(im, pos); d = ImageDraw.Draw(c)
        sombra_txt(d, (W/2, 300), 'NA LOJA', F('Black', 70), BRANCO)
        k = entra(t, 5.55); f = F('Black', 130); txt = 'R$ 9.464'
        if k > 0:
            sombra_txt(d, (W/2, 440), txt, f, (255,255,255,int(255*k)))
            w = d.textlength(txt, font=f); x0 = W/2 - w/2 - 20
            d.line((x0, 450, x0 + (w + 40) * entra(t, 6.2, 0.3), 450), fill=(243,91,18,255), width=14)
    elif t < 10.55:   # cena 3: lance inicial
        halo, im, pos, q = produto(FRENTE, 760, t, 7.45, cy=H*0.62, zoom=0.05)
        c.alpha_composite(halo); c.alpha_composite(im, pos); d = ImageDraw.Draw(c)
        sombra_txt(d, (W/2, 300), 'AQUI O LANCE COMEÇOU EM', F('Black', 60), BRANCO)
        k = entra(t, 8.7, 0.25); f = F('Black', int(170 * (0.7 + 0.3*k)))
        if k > 0: pilula(d, W/2, 470, 'R$ 197', f, OURO + (255,), (10,60,32,255), pad=50)
    else:             # cena 5: chamada final
        d = ImageDraw.Draw(c); c.alpha_composite(LOGO.resize((420, int(LOGO.height*420/LOGO.width))), (int(W/2 - 210), 300))
        im = FRENTE.copy(); r = 520 / im.height; im = im.resize((int(im.width*r), 520), Image.LANCZOS); c.alpha_composite(im, (int(W/2 - im.width/2), 520))
        k = entra(t, 13.85); sombra_txt(d, (W/2, 1170 + 30*(1-k)), 'SÁBADO · 20H', F('Black', 110), BRANCO + (int(255*k),))
        k = entra(t, 15.6); sombra_txt(d, (W/2, 1300 + 30*(1-k)), 'o martelo bate', F('Bold', 66), LIMA + (int(255*k),))
        k = entra(t, 16.9)
        if k > 0:
            chamada = 'COMENTA "IPHONE"' if FIM == 'feed' else 'ME CHAMA NO WHATSAPP'
            pilula(d, W/2, 1480 + 30*(1-k), chamada, F('Black', 56), VERDE + (int(245*k),), BRANCO + (int(255*k),))
            sub = 'que a gente te explica como dar lance' if FIM == 'feed' else 'que eu te explico como dar lance'
            d.text((W/2, 1590 + 30*(1-k)), sub, font=F('SemiBold', 42), fill=(200,230,210,int(255*k)), anchor='mm')
    return c.convert('RGB')
T_PROVA = (10.55, 13.85); TOTAL = 20.4
# cenas desenhadas → vídeo
p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',f'{D}/cenas.mp4'], stdin=subprocess.PIPE)
for n in range(int(TOTAL*FPS)):
    t = n / FPS
    p.stdin.write((quadro(t) if not (T_PROVA[0] <= t < T_PROVA[1]) else Image.new('RGB',(W,H))).tobytes())
p.stdin.close(); p.wait()
# a prova: Murilo com o iPhone lacrado (recorte limpo, sem a TV com %)
pil = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(pil); pilula(d, W/2, 1560, 'O ÚLTIMO JÁ ENCONTROU DONO', F('Black', 50), OURO + (255,), (10,60,32,255)); c2 = Image.new('RGBA',(W,H)); c2.alpha_composite(LOGO,(60,260)); c2.alpha_composite(pil); c2.save(f'{D}/prova_txt.png')
dp = T_PROVA[1] - T_PROVA[0]
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/cenas.mp4','-ss','82.6','-t',str(dp),'-i',PROVA,'-loop','1','-t',str(dp),'-i',f'{D}/prova_txt.png',
  '-filter_complex', f"[1:v]scale=1080:1920,crop=568:1010:90:320,scale=1080:1920:flags=lanczos,setsar=1,fps=30,setpts=PTS-STARTPTS+{T_PROVA[0]}/TB[pv];[pv][2:v]overlay=0:0[pt];[0:v][pt]overlay=0:0:enable='between(t,{T_PROVA[0]},{T_PROVA[1]})':eof_action=pass[v]",
  '-map','[v]','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',f'{D}/video_mudo.mp4'], check=True)
# som: voz do Leiloeiro + música que abaixa na fala + fala real do Murilo baixinha + jingle
musica = f'/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/joao/musicaC.mp3'
jingle = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
tj = 18.5
af = (f"[1:a]adelay=200|200,volume=1.5,asplit[voz][vsc];[2:a]atrim=0:{tj+0.3},volume=0.5,afade=t=in:d=0.3,afade=t=out:st={tj-0.4}:d=0.7[m0];[m0][vsc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[m];"
      f"[3:a]atrim=0:{dp},asetpts=PTS-STARTPTS,volume=0.35,adelay={int(T_PROVA[0]*1000)}|{int(T_PROVA[0]*1000)}[mu];[4:a]adelay={int(tj*1000)}|{int(tj*1000)},volume=1.1[j];"
      f"[voz][m][mu][j]amix=inputs=4:normalize=0,apad=whole_dur={TOTAL},loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{D}/video_mudo.mp4','-i',f'{D}/voz.mp3','-i',musica,'-ss','82.6','-i',PROVA,'-i',jingle,'-filter_complex',af,
  '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(TOTAL),'-movflags','+faststart',f'{D}/REELS-iphone-sabado-{FIM}.mp4'], check=True)
print('ok', FIM)
