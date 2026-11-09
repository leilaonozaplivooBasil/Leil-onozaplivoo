# "Como foi sábado" — leilão do iPhone 17 Pro Max (07/11) até o martelo. Imagens da TV sem borrar (pedido da Natália, 09/11); áudio só com trechos sem nome.
import subprocess, sys, pillow_heif
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
pillow_heif.register_heif_opener()
S = sys.argv[1]; OUT = sys.argv[2]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR, FOGO = (27,122,72), (245,196,81), (10,20,16), (255,255,255), (243,91,18)
PROB = []
def run(a): subprocess.run(['ffmpeg','-v','error','-y'] + a, check=True)
def foto(src, dst, dur, zoom_in=True):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB'); e = max(W/im.width, H/im.height)*1.08
    im = im.resize((round(im.width*e), round(im.height*e)), Image.LANCZOS); x = (im.width-W)//2; y = (im.height-H)//2
    big = im.crop((x-0 if x>=0 else 0, y, x+W, y+H)) if False else im
    big.save(f'{S}/tmp_foto.png')
    z = "1.0+0.0018*on" if zoom_in else "1.08-0.0018*on"
    run(['-loop','1','-i',f'{S}/tmp_foto.png','-vf',f"scale={big.width*2}:-2,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(dur*30)}:s={W}x{H}:fps=30,format=yuv420p",'-t',str(dur),'-c:v','libx264','-crf','16','-preset','fast',dst])
def corte(src, a, b, dst, crop=None, extra=None):
    c = f'crop={crop},' if crop else ''          # só a tela da TV (sem os produtos embaixo)
    x = f',{extra}' if extra else ''              # trecho de longe ampliado: desfoque p/ nenhum nome de cliente ficar legível
    run(['-ss',str(a),'-to',str(b),'-i',src,'-an','-vf',f'{c}scale={W}:{H}:flags=lanczos{x},fps=30,format=yuv420p','-c:v','libx264','-crf','16','-preset','fast',dst])
# --- vídeo (sem áudio) ---
V = [('clip', f'{S}/v4934_sdr.mp4', 0.0, 2.6), ('clip', f'{S}/v4934_sdr.mp4', 5.7, 6.9),   # a equipe na mesa atendendo (IMG_4934, no lugar da 1ª foto)
     ('clip', f'{S}/efb_n.mp4', 1.3, 4.6, '956:1700:0:0'), ('clip', f'{S}/efb_n.mp4', 10.1, 13.4, '788:1400:50:0'),
     ('clip', f'{S}/efb_n.mp4', 17.0, 18.5, '788:1400:150:0'), ('clip', f'{S}/efb_n.mp4', 20.9, 24.6, '788:1400:250:0'),
     ('clip', f'{S}/v4947_sdr.mp4', 0.0, 3.5, '900:1600:100:0'),
     ('clip', f'{S}/v4951_sdr.mp4', 0.0, 3.2, '500:889:170:400'), ('clip', f'{S}/v4951_sdr.mp4', 3.2, 8.4, '480:853:80:560'),
     ('clip', f'{S}/v4951_sdr.mp4', 8.4, 12.4, '900:1600:0:100'), ('foto', f'{S}/in/f4916.jpg', 3.2)]
partes, t, inicio = [], 0.0, []
for i, v in enumerate(V):
    dst = f'{S}/p{i}.mp4'
    if v[0] == 'foto': foto(v[1], dst, v[2], zoom_in=(i == 0)); d = v[2]
    else: corte(v[1], v[2], v[3], dst, v[4] if len(v) > 4 else None, v[5] if len(v) > 5 else None); d = round(v[3]-v[2], 3)
    inicio.append(t); partes.append(dst); t = round(t + d, 3)
DUR = t
open(f'{S}/lista.txt','w').write(''.join(f"file '{p}'\n" for p in partes))
run(['-f','concat','-safe','0','-i',f'{S}/lista.txt','-c','copy',f'{S}/base.mp4'])
# --- vozes: só trechos SEM nome de cliente (nomes falados ficam de fora) ---
VOZES = [(f'{S}/in/vEFB9.mp4', 1.4, 3.05, inicio[2]+0.1), (f'{S}/in/vEFB9.mp4', 10.15, 12.72, inicio[3]+0.05),
         (f'{S}/in/vEFB9.mp4', 17.1, 18.4, inicio[4]+0.1),
         (f'{S}/in/v4947.mov', 0.0, 3.46, inicio[6]), (f'{S}/in/v4951.mov', 1.75, 8.4, inicio[7]+1.75)]   # sem o "tem gente com dinheiro, não vai não" (pedido 09/11)
ent, fc, lbl = [], '', []
for j, (src, a, b, at) in enumerate(VOZES):
    ent += ['-ss', str(a), '-to', str(b), '-i', src]
    fc += (f"[{j}:a]asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=mono,highpass=f=90,lowpass=f=10500,equalizer=f=3200:t=q:w=1.4:g=-3,"
           f"deesser=i=0.5,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=180:makeup=2,afade=t=in:d=0.05,afade=t=out:st={round(b-a-0.08,3)}:d=0.08,adelay={int(at*1000)}[v{j}];")
    lbl.append(f'[v{j}]')
ent += ['-f', 'lavfi', '-t', str(DUR), '-i', 'anullsrc=r=48000:cl=mono']; lbl.append(f'[{len(VOZES)}:a]')   # silêncio desde o 0: segura cada voz no tempo certo
fc += ''.join(lbl) + f"amix=inputs={len(lbl)}:normalize=0,asetpts=N/SR/TB,apad=whole_dur={DUR},atrim=0:{DUR}[vz]"
run(ent + ['-filter_complex', fc, '-map', '[vz]', '-ar', '48000', f'{S}/vozes_raw.wav'])
run(['-i', f'{S}/vozes_raw.wav', '-af', 'loudnorm=I=-17:TP=-3:LRA=10', '-ar', '48000', f'{S}/vozes_n.wav'])   # wav separado (regra)
run(['-i', f'{S}/vozes_n.wav', '-af', f'apad=whole_dur={DUR},atrim=0:{DUR}', '-ar', '48000', f'{S}/vozes.wav'])   # completa com silêncio até o fim do vídeo
m = f'{MK}/marca/trilhas-base/pegada-orla/03-piano-house.mp3'
run(['-stream_loop','-1','-i',m,'-i',f'{S}/vozes.wav','-filter_complex',
     f"[0:a]atrim=0:{DUR},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.32,afade=t=in:d=1,afade=t=out:st={DUR-2.5}:d=2.5[m];"
     "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350[md];"
     "[md][v]amix=inputs=2:duration=first:normalize=0,volume=1.3", '-ar', '48000', f'{S}/audio.wav'])
# --- camadas de texto ---
def pilula(d, cx, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(f'"{t}" não cabe')
    d.rounded_rectangle((cx-w/2-raio+8, y-raio, cx+w/2+raio-8, y+raio), raio, fill=cor); d.text((cx, y), t, font=f, fill=txt, anchor='mm')
def camada(nome, linhas):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for kind, y, t in linhas:
        if kind == 'v': pilula(d, W/2, y, t, F('Black', 56), VERDE+(245,), BR, 46)
        elif kind == 'o': pilula(d, W/2, y, t.upper(), F('Black', 66), OURO+(255,), (10,60,32), 50)
        elif kind == 'f': pilula(d, W/2, y, t.upper(), F('Black', 44), FOGO+(245,), BR, 38)
        elif kind == 'big':
            f = F('Black', 400); s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).text((W/2, y+14), t, font=f, fill=(0,0,0,170), anchor='mm')
            im.alpha_composite(s.filter(ImageFilter.GaussianBlur(18))); d.text((W/2, y), t, font=f, fill=BR, anchor='mm')
        elif kind == 'arr':
            x0, y0, x1, y1 = 110, y, 970, y+420
            s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).rounded_rectangle((x0, y0+16, x1, y1+16), 40, fill=(0,0,0,150)); im.alpha_composite(s.filter(ImageFilter.GaussianBlur(24)))
            d.rounded_rectangle((x0, y0, x1, y1), 40, fill=(8,40,24,240), outline=OURO+(255,), width=5)
            d.text((W/2, y0+95), 'ARREMATADO!', font=F('Black', 104), fill=OURO, anchor='mm')
            d.text((W/2, y0+235), t, font=F('Black', 150), fill=BR, anchor='mm')
            d.text((W/2, y0+350), 'na loja, ele custava R$ 9.464', font=F('Bold', 44), fill=(200,230,210), anchor='mm')
    a = im.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: v*0.4); sh = Image.new('RGBA', (W, H)); sh.putalpha(a)
    Image.alpha_composite(sh, im).save(f'{S}/{nome}.png')
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
s = Image.new('RGBA', (W, H)); ds = ImageDraw.Draw(s); ds.rounded_rectangle((40, 250, 80+lg.width, 278+lg.height), 30, fill=NOITE+(150,)); s.alpha_composite(lg, (60, 264)); s.save(f'{S}/selo.png')
I = inicio
CAM = [  # (início, fim, nome, linhas)
 (0.0, I[2], 'c0', [('f', 1390, 'sábado de leilão'), ('v', 1500, 'a galera atendendo'), ('o', 1606, 'até as 21h!')]),
 (I[2], I[3], 'c2', [('v', 1500, 'tudo ao vivo, sem corte'), ('o', 1606, 'o lance subindo…')]),
 (I[3], I[4], 'c3', [('v', 1500, 'pegando'), ('o', 1606, 'fogo!')]),
 (I[4], I[5], 'c4', [('o', 1606, 'guerra de lances!')]),
 (I[5], I[6], 'c5', [('v', 1500, 'e aí,'), ('o', 1606, 'quem dá mais?')]),
 (I[6], I[7], 'c6', [('v', 1500, 'chegou em'), ('o', 1606, 'R$ 4.720!')]),
 (I[7], I[7]+3.0, 'c7', [('f', 1500, 'contagem ao vivo, na tela da TV')]),   # o 3-2-1 é o do próprio site, sem número por cima
 (I[7]+3.0, I[9], 'c8', [('o', 1606, 'fechou!')]),
 (I[9]+2.2, I[10], 'c9', [('arr', 1040, 'R$ 6.370')]),
 (I[10], DUR, 'c10', [('v', 1430, 'obrigado, galera!'), ('f', 1540, 'quarta tem iPhone 18 Pro Max'), ('o', 1650, 'quarta · 20h')]),
]
ent = ['-i', f'{S}/base.mp4', '-loop', '1', '-t', str(DUR), '-i', f'{S}/selo.png']; vf = f"[0:v][1:v]overlay=0:0:enable='between(t,0,{I[10]-0.04})'[b0]"   # a foto final já tem a logo do site
for j, (a, b, nome, linhas) in enumerate(CAM):
    camada(nome, linhas); ent += ['-loop', '1', '-t', str(DUR), '-i', f'{S}/{nome}.png']
    vf += f";[b{j}][{2+j}:v]overlay=0:0:enable='between(t,{round(a,3)},{round(b-0.04,3)})'[b{j+1}]"
n = len(CAM)
vf += f";[b{n}]fade=t=in:st=0:d=0.4,fade=t=out:st={DUR-0.6}:d=0.6[vout]"
run(ent + ['-i', f'{S}/audio.wav', '-filter_complex', vf, '-map', '[vout]', '-map', f'{2+n}:a', '-t', str(DUR),
     '-c:v','libx264','-crf','20','-preset','medium','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart', f'{OUT}/REELS-como-foi-sabado-ate-o-martelo.mp4'])
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok', DUR, [round(x,2) for x in inicio])
