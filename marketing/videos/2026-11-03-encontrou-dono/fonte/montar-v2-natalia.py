# "Encontrou dono" v2 — Natália abre e fecha, as 5 entregas reais no meio, transições suaves, jingle no fim
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; P = '/home/user/leilonozap/public/provas'; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, FLORESTA, BRANCO = (27,122,72), (245,196,81), (10,20,16), (0,45,27), (255,255,255)
T = 0.3
# arquivo, início, fim, recorte, volume (LUFS medido → -16; None = som ambiente baixo), legendas [(ini,fim,texto,destaque)], rótulo de produto
PARTES = [
  (f'{S}/ini.mov', 0.55, 5.00, '800:1422:187:380', -28.4, [(0.8, 2.75, 'Sabe o que esses produtos', 'têm em comum?'), (2.9, 4.9, 'Todos já encontraram', 'dono')], None),
  (f'{P}/cliente-full.mp4', 5.5, 8.5, '928:1650:76:0', None, [], 'Mais um entregue'),
  (f'{P}/herbert-full.mp4', 8.5, 11.5, None, None, [], 'Ar-condicionado'),
  (f'{P}/matheus-video-full.mp4', 13.0, 16.0, None, None, [], 'PlayStation 5'),
  (f'{P}/lucas-full.mp4', 4.8, 7.0, None, None, [], 'Scooter elétrica'),
  (f'{P}/murilo-full.mp4', 82.5, 86.5, '568:1010:90:320', -24.0, [(82.6, 84.6, 'Tudo lacrado, tudo', 'certinho'), (84.6, 86.5, 'E foi o', 'iPhone 17 Pro Max')], None),
  (f'{S}/ini.mov', 7.35, 11.75, '800:1422:187:380', -28.4, [(7.55, 9.35, 'E amanhã chega', 'mais um'), (9.45, 11.6, 'Alguém arrematou', 'no sábado')], None),
  (f'{S}/fim.mov', 0.55, 5.75, None, -32.0, [(0.7, 2.3, 'Quer saber', 'quem foi?'), (2.6, 5.6, 'Segue a gente que amanhã', 'eu te mostro')], None),
]
def run(c): subprocess.run(c, check=True)
def quebra(d, txt, f, larg):
    l, a = [], ''
    for p in txt.split():
        t = (a + ' ' + p).strip()
        if d.textlength(t, font=f) > larg and a: l.append(a); a = p
        else: a = t
    return l + ([a] if a else [])
def legenda(txt, dest, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Black', 58); fd = F('Black', 66); y = 1430
    for l in quebra(d, txt, f, W - 220):
        w = d.textlength(l, font=f); x0 = (W - w) / 2 - 34; d.rounded_rectangle((x0, y - 46, x0 + w + 68, y + 46), 46, fill=VERDE + (245,)); d.text((W/2, y), l, font=f, fill=BRANCO, anchor='mm'); y += 104
    if dest:
        t = dest.upper(); w = d.textlength(t, font=fd); x0 = (W - w) / 2 - 36; d.rounded_rectangle((x0, y - 49, x0 + w + 72, y + 49), 49, fill=OURO + (255,)); d.text((W/2, y), t, font=fd, fill=(10,60,32), anchor='mm')
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def rotulo(txt, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Black', 56); w = d.textlength(txt, font=f); x0 = (W - w)/2 - 40
    d.rounded_rectangle((x0, 1560, x0 + w + 80, 1666), 53, fill=VERDE + (245,)); d.text((W/2, 1613), txt, font=f, fill=BRANCO, anchor='mm'); im.save(f'{S}/{nome}.png')
logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((300, 110))
selo = Image.new('RGBA', (W, H), (0,0,0,0)); ds = ImageDraw.Draw(selo); ds.rounded_rectangle((40, 276, 80 + logo.width, 304 + logo.height), 30, fill=NOITE + (150,)); selo.alpha_composite(logo, (60, 290)); selo.save(f'{S}/selo.png')
fe = Image.new('RGB', (W, H), NOITE); dd = ImageDraw.Draw(fe)
for y in range(H): dd.line((0, y, W, y), fill=tuple(int(NOITE[i] + (FLORESTA[i] - NOITE[i]) * y / H) for i in range(3)))
fe = fe.convert('RGBA'); lg = logo.copy(); lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((720, 260)); fe.alpha_composite(lg, ((W - lg.width)//2, 720)); fe.convert('RGB').save(f'{S}/fecho.png')
partes, durs = [], []
for k, (arq, ini, fim, rec, lufs, legs, rot) in enumerate(PARTES):
    dur = round(fim - ini, 3); ovs = ['selo']
    for j, (a, b, txt, dest) in enumerate(legs): legenda(txt, dest, f'l{k}_{j}'); ovs.append((f'l{k}_{j}', a - ini, b - ini))
    if rot: rotulo(rot, f'r{k}'); ovs.append((f'r{k}', 0.25, dur))
    vf = f"[0:v]scale=1080:1920" + (f",crop={rec},scale=1080:1920:flags=lanczos" if rec else "") + ",setsar=1,fps=30,eq=saturation=1.05[b0]"
    ent = ['-ss', str(ini), '-t', str(dur), '-i', arq]
    for n, o in enumerate(ovs):
        nome = o if isinstance(o, str) else o[0]; ent += ['-loop', '1', '-t', str(dur), '-i', f'{S}/{nome}.png']
        cond = '' if isinstance(o, str) else f":enable='between(t,{o[1]:.2f},{o[2]:.2f})'"
        vf += f";[b{n}][{n+1}:v]overlay=0:0{cond}[b{n+1}]"
    vol = f"volume={-16 - lufs:.1f}dB,acompressor=threshold=-18dB:ratio=3:attack=8:release=200" if lufs is not None else "volume=0.25"
    vf += f";[b{len(ovs)}]null[v];[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,{vol}[a]"
    out = f'{S}/p{k}.mp4'; run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', vf, '-map','[v]','-map','[a]','-t',str(dur),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k', out])
    partes.append(out); durs.append(dur)
FECHO = 2.4
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(FECHO),'-i',f'{S}/fecho.png','-f','lavfi','-t',str(FECHO),'-i','anullsrc=r=48000:cl=stereo','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','18','-c:a','aac','-shortest',f'{S}/pfim.mp4'])
todos = partes + [f'{S}/pfim.mp4']; durs.append(FECHO)
ent = sum([['-i', p] for p in todos], []); fc, ac = [], []; acc = durs[0]; va, aa = '[0:v]', '[0:a]'
for n in range(1, len(todos)):
    off = acc - T; fx = 'fadeblack' if n == len(todos) - 1 else 'fade'
    fc.append(f"{va}[{n}:v]xfade=transition={fx}:duration={T}:offset={off:.3f}[vx{n}]"); ac.append(f"{aa}[{n}:a]acrossfade=d={T}:c1=tri:c2=tri[ax{n}]")
    va, aa = f'[vx{n}]', f'[ax{n}]'; acc = off + durs[n]
run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', ';'.join(fc + ac), '-map', va, '-map', aa, '-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k', f'{S}/junto.mp4'])
total = acc; tj = total - FECHO + 0.25
musica = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/encontrou/musica.mp3'
jingle = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
af = (f"[0:a]asplit[voz][vsc];[1:a]aloop=loop=1:size=1200000,atrim=0:{tj},volume=0.45,afade=t=in:d=0.3,afade=t=out:st={tj-0.6}:d=0.6[m0];[m0][vsc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[m];"
      f"[2:a]adelay={int(tj*1000)}|{int(tj*1000)}[j];[voz][m][j]amix=inputs=3:normalize=0:duration=first,volume=3dB,alimiter=limit=0.93[a]")
run(['ffmpeg','-v','error','-y','-i',f'{S}/junto.mp4','-i',musica,'-i',jingle,'-filter_complex',af,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{total:.2f}','-movflags','+faststart',f'{S}/REELS-encontrou-dono-v2.mp4'])
print('ok', round(total, 2))
