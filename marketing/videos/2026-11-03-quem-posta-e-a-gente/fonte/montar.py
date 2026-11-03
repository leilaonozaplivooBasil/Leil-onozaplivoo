# Reels "Quem posta é a gente" — Natália e João (marketing) + legenda no padrão da Duda + trilha + jingle
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920
VERDE, OURO, NOITE, FLORESTA, BRANCO = (27,122,72), (245,196,81), (10,20,16), (0,45,27), (255,255,255)
# arquivo, início, fim, legendas [(ini, fim, texto, destaque)] em tempo do clipe
CLIPES = [  # arquivo, início, fim, legendas, volume medido (LUFS) → cada fala vai para o mesmo nível
  ('v1', 0.55, 4.30, [(0.7, 2.05, 'Sabe quem posta tudo', None), (2.05, 4.3, 'que aparece aqui no', 'Instagram?')], -31.0),
  ('v2', 0.80, 2.10, [(0.9, 2.1, 'Eu sou o', 'João')], -21.7),
  ('v3', 0.60, 3.65, [(0.7, 1.9, 'E eu sou a Natália', None), (1.9, 3.65, 'do marketing do', 'Leilão no Zap')], -28.2),
  ('v6', 2.25, 8.30, [(2.4, 3.7, 'Esse é o nosso escritório', None), (3.7, 5.2, 'bem em frente pra', 'praia')], -19.8),
  ('v4', 0.45, 5.80, [(0.6, 3.2, 'Daqui a gente acompanha cada leilão', None), (3.3, 5.8, 'e cada entrega que chega na', 'casa de vocês')], -33.4),
  ('v5', 0.70, 4.70, [(0.86, 2.2, 'Tem alguma', 'dúvida?'), (2.2, 4.7, 'Comenta aqui que a gente', 'responde')], -28.0),
]
ALVO = -16.0
def run(c): subprocess.run(c, check=True)
def quebra(d, txt, f, larg):
    linhas, atual = [], ''
    for p in txt.split():
        t = (atual + ' ' + p).strip()
        if d.textlength(t, font=f) > larg and atual: linhas.append(atual); atual = p
        else: atual = t
    return linhas + ([atual] if atual else [])
def legenda(txt, dest, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Black', 58); fd = F('Black', 64)
    linhas = quebra(d, txt, f, W - 220); y = 1430
    for l in linhas:
        w = d.textlength(l, font=f); x0 = (W - w) / 2 - 34
        d.rounded_rectangle((x0, y - 46, x0 + w + 68, y + 46), 46, fill=VERDE + (245,))
        d.text((W / 2, y), l, font=f, fill=BRANCO, anchor='mm'); y += 104
    if dest:
        t = dest.upper(); w = d.textlength(t, font=fd); x0 = (W - w) / 2 - 36
        d.rounded_rectangle((x0, y - 48, x0 + w + 72, y + 48), 48, fill=OURO + (255,))
        d.text((W / 2, y), t, font=fd, fill=(10,60,32), anchor='mm')
    sh = im.copy().split()[3].filter(ImageFilter.GaussianBlur(14)); sombra = Image.new('RGBA', (W, H), (0,0,0,0)); sombra.putalpha(sh.point(lambda a: a * 0.45))
    out = Image.alpha_composite(sombra, im); out.save(f'{S}/{nome}.png')
def selo():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((300, 110))
    x, y = 60, 290
    d.rounded_rectangle((x - 20, y - 14, x + logo.width + 20, y + logo.height + 14), 30, fill=NOITE + (150,))
    im.alpha_composite(logo, (x, y)); im.save(f'{S}/selo.png')
def fecho():
    im = Image.new('RGB', (W, H), NOITE); d = ImageDraw.Draw(im)
    for y in range(H): d.line((0, y, W, y), fill=tuple(int(NOITE[i] + (FLORESTA[i] - NOITE[i]) * y / H) for i in range(3)))
    im = im.convert('RGBA'); logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((720, 260))
    im.alpha_composite(logo, ((W - logo.width) // 2, 640)); d = ImageDraw.Draw(im)
    d.text((W / 2, 1010), 'Comenta sua dúvida aqui', font=F('Black', 66), fill=BRANCO, anchor='mm')
    t = 'A GENTE RESPONDE'; f = F('Black', 58); w = d.textlength(t, font=f)
    d.rounded_rectangle(((W - w) / 2 - 44, 1080, (W + w) / 2 + 44, 1180), 50, fill=VERDE); d.text((W / 2, 1130), t, font=f, fill=BRANCO, anchor='mm')
    d.text((W / 2, 1260), '@leilaonozapoficial', font=F('SemiBold', 46), fill=(200, 230, 210), anchor='mm')
    im.convert('RGB').save(f'{S}/fecho.png')
selo(); fecho()
partes = []; t_total = 0
for k, (arq, ini, fim, legs, lufs) in enumerate(CLIPES):
    dur = round(fim - ini, 3); ovs = []
    for j, (a, b, txt, dest) in enumerate(legs):
        nome = f'leg{k}_{j}'; legenda(txt, dest, nome); ovs.append((nome, max(0, a - ini), min(dur, b - ini)))
    hdr = 'zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.18:saturation=1.1,' if arq == 'v6' else ''
    fc = f"[0:v]{hdr}scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,eq=saturation=1.06[b0];[b0][1:v]overlay=0:0[b1]"
    entradas = ['-ss', str(ini), '-t', str(dur), '-i', f'{S}/{arq}.mov', '-loop', '1', '-t', str(dur), '-i', f'{S}/selo.png']
    for n, (nome, a, b) in enumerate(ovs):
        entradas += ['-loop', '1', '-t', str(dur), '-i', f'{S}/{nome}.png']
        fc += f";[b{n+1}][{n+2}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[b{n+2}]"
    fc += f";[b{len(ovs)+1}]null[v];[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,volume={ALVO-lufs:.1f}dB,acompressor=threshold=-18dB:ratio=3:attack=8:release=200:makeup=1,afade=t=in:d=0.06,afade=t=out:st={dur-0.18:.2f}:d=0.18[a]"
    out = f'{S}/p{k}.mp4'
    run(['ffmpeg', '-v', 'error', '-y'] + entradas + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(dur), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', out])
    partes.append(out); t_total += dur
FECHO = 2.6
run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(FECHO), '-i', f'{S}/fecho.png', '-f', 'lavfi', '-t', str(FECHO), '-i', 'anullsrc=r=48000:cl=stereo',
     '-vf', 'fps=30,format=yuv420p,fade=t=in:d=0.25', '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-shortest', f'{S}/pfim.mp4'])
with open(f'{S}/lista.txt', 'w') as l:
    for p in partes + [f'{S}/pfim.mp4']: l.write(f"file '{p}'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{S}/lista.txt', '-c', 'copy', f'{S}/junto.mp4'])
total = t_total + FECHO; tj = t_total + 0.3
jingle = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
musica = f'{S}/musica.mp3'
af = (f"[0:a]anull[voz];[1:a]atrim=0:{t_total},volume=0.13,afade=t=in:d=0.4,afade=t=out:st={t_total-0.6}:d=0.6[m];"
      f"[2:a]volume=1.0,adelay={int(tj*1000)}|{int(tj*1000)}[j];[voz][m][j]amix=inputs=3:normalize=0:duration=first,volume=4dB,alimiter=limit=0.93[a]")
run(['ffmpeg', '-v', 'error', '-y', '-i', f'{S}/junto.mp4', '-i', musica, '-i', jingle, '-filter_complex', af, '-map', '0:v', '-map', '[a]',
     '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(total), '-movflags', '+faststart', f'{S}/REELS-quem-posta-e-a-gente.mp4'])
print('ok', round(total, 2))
