# Reels iPhone 17 Pro Max — versão "prompt mestre": gente real o tempo todo, voz real do Murilo, preço FINAL, câmera de celular
import subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; FIM = sys.argv[2] if len(sys.argv) > 2 else 'feed'
M = '/home/user/leilonozap/public/provas/murilo-full.mp4'; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf' % p, t)
W, H = 1080, 1920; OURO = (245,196,81); VERDE = (27,122,72); NOITE = (10,20,16)
T = 0.25
# trecho do vídeo do Murilo (início, fim), legendas da fala [(ini, fim, texto, palavra em dourado)], textos de cima [(ini, fim, texto)]
CENAS = [
  (84.75, 86.75, [(84.9, 86.6, 'e foi o 17 pro max!', '17 pro max!')], [(84.75, 86.75, 'esse iphone encontrou dono')]),
  (24.9, 31.8, [(25.0, 26.4, 'fiquei meio desconfiado...', None), (26.4, 28.0, 'mas quando vi todo mundo', None), (28.0, 29.2, 'dando lance, dando lance', None), (30.0, 31.7, 'falei: não, vou com tudo', 'com tudo')], [(24.9, 27.5, 'no começo ele desconfiou')]),
  (51.95, 61.1, [(52.0, 53.35, 'aí eu falei:', None), (53.35, 54.5, 'agora é meu, agora é meu', None), (54.5, 56.5, 'cruzando os dedos...', None), (56.6, 59.2, 'dou-lhe uma, duas, três...', None), (59.3, 61.0, 'arrematado!', 'arrematado!')], []),
  (79.85, 84.95, [(79.9, 81.8, 'tudo certinho, tudo lacrado', 'lacrado'), (83.1, 84.9, 'tudo certinho, tá?', None)], [(79.85, 84.95, '__preco__')]),
  (86.6, 89.8, '__vo1__', [(86.6, 89.8, 'sábado · 20h · iphone 17 pro max')]),
  (44.0, 46.8, '__vo2__', [(44.0, 46.8, 'sábado · 20h · iphone 17 pro max')]),
]
def run(c): subprocess.run(c, check=True)
def contorno(d, xy, t, f, cor, w=5):
    for dx in range(-w, w+1, 2):
        for dy in range(-w, w+1, 2):
            if dx*dx + dy*dy <= w*w: d.text((xy[0]+dx, xy[1]+dy), t, font=f, fill=(0,0,0,255), anchor='mm')
    d.text(xy, t, font=f, fill=cor, anchor='mm')
def legenda(txt, dest, nome):   # legenda de criador: minúscula, branca com contorno, palavra-chave dourada
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('ExtraBold', 64 if txt != 'arrematado!' else 104)
    y = 1450
    if dest and dest in txt:
        a = txt[:txt.index(dest)]; b = txt[txt.index(dest)+len(dest):]
        wa, wd, wb = d.textlength(a, font=f), d.textlength(dest, font=f), d.textlength(b, font=f); x0 = W/2 - (wa+wd+wb)/2
        contorno(d, (x0 + wa/2, y), a, f, (255,255,255,255)); contorno(d, (x0 + wa + wd/2, y), dest, f, OURO + (255,)); contorno(d, (x0 + wa + wd + wb/2, y), b, f, (255,255,255,255))
    else: contorno(d, (W/2, y), txt, f, (255,255,255,255))
    im.save(f'{S}/{nome}.png')
def caixa_ig(txt, nome, y=420):   # texto "do Instagram": caixa branca arredondada, letra preta
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    if txt == '__preco__':
        f1, f2 = F('Bold', 54), F('ExtraBold', 74)
        for (t, f, fundo, cor, yy) in (('na loja: R$ 8.404', f1, (255,255,255,235), (40,40,40), 380), ('ele pagou: R$ 4.640', f2, OURO + (255,), (10,40,22), 500)):
            w = d.textlength(t, font=f); d.rounded_rectangle((W/2 - w/2 - 30, yy - f.size*0.85, W/2 + w/2 + 30, yy + f.size*0.85), 22, fill=fundo); d.text((W/2, yy), t, font=f, fill=cor, anchor='mm')
        d.line((W/2 - d.textlength('na loja: R$ 8.404', font=f1)/2 + 190, 382, W/2 + d.textlength('na loja: R$ 8.404', font=f1)/2, 382), fill=(200,40,40), width=6)
    else:
        f = F('Bold', 56); w = d.textlength(txt, font=f)
        d.rounded_rectangle((W/2 - w/2 - 30, y - 48, W/2 + w/2 + 30, y + 48), 22, fill=(255,255,255,235)); d.text((W/2, y), txt, font=f, fill=(30,30,30), anchor='mm')
    im.save(f'{S}/{nome}.png')
partes, durs = [], []
VO = {'feed': [(0.16, 1.3, 'e sábado tem mais!', 'sábado'), (1.4, 3.1, 'outro iphone 17 pro max', None), (3.1, 4.06, 'às 20h', '20h'), (4.1, 5.6, 'comenta IPHONE aí embaixo!', 'IPHONE')],
      'vendedores': [(0.04, 1.31, 'e sábado tem mais!', 'sábado'), (1.39, 3.18, 'outro iphone 17 pro max', None), (3.2, 4.17, 'às 20h', '20h'), (4.2, 5.25, 'me chama no whatsapp!', 'whatsapp!')]}[FIM]
mudo = set()
for k, (ini, fim, legs, tops) in enumerate(CENAS):
    dur = round(fim - ini, 3); ovs = []
    if legs in ('__vo1__', '__vo2__'):
        mudo.add(k); legs = []
    for j, (a, b, t, dd) in enumerate(legs): legenda(t, dd, f'l{k}_{j}'); ovs.append((f'l{k}_{j}', a - ini, b - ini))
    for j, (a, b, t) in enumerate(tops): caixa_ig(t, f't{k}_{j}'); ovs.append((f't{k}_{j}', a - ini + 0.1, b - ini))
    # recorte do meio do corpo pra cima (sem a legenda queimada do vídeo do site) + leve balanço de câmera na mão
    vf = ("[0:v]scale=1080:1920,crop=568:1010:60:320,scale=1134:2016:flags=lanczos,"
          "crop=1080:1920:x='27+14*sin(t*1.7)+6*sin(t*3.1)':y='48+12*sin(t*1.3+1)+5*cos(t*2.7)',setsar=1,fps=30,eq=saturation=1.05:contrast=1.03[b0]")
    ent = ['-ss', str(ini), '-t', str(dur), '-i', M]
    for n, (nome, a, b) in enumerate(ovs):
        ent += ['-loop', '1', '-t', str(dur), '-i', f'{S}/{nome}.png']; vf += f";[b{n}][{n+1}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[b{n+1}]"
    vf += f";[b{len(ovs)}]null[v];[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=90," + ("volume=0" if k in mudo else "volume=7dB,acompressor=threshold=-20dB:ratio=3:attack=8:release=200") + "[a]"
    out = f'{S}/p{k}.mp4'; run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', vf, '-map','[v]','-map','[a]','-t',str(dur),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k', out])
    partes.append(out); durs.append(dur)
# fecho: 2 s, dia e hora (o convite já foi dito na cena anterior)
FECHO = 2.0
fe = Image.new('RGB', (W, H), NOITE); d = ImageDraw.Draw(fe)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((640, 230)); fe.paste(lg, ((W - lg.width)//2, 300), lg)
d.text((W/2, 660), 'iphone 17 pro max', font=F('Bold', 60), fill=(220,235,225), anchor='mm')
d.text((W/2, 770), 'sábado · 20h', font=F('ExtraBold', 96), fill=OURO, anchor='mm')
d.text((W/2, 890), 'comenta IPHONE' if FIM == 'feed' else 'me chama no whatsapp', font=F('Bold', 54), fill=(255,255,255), anchor='mm')
lei = Image.open(f'{MK}/marca/leiloeiro-aponta-moeda-recorte.png').convert('RGBA'); lei.thumbnail((900, 960)); fe.paste(lei, ((W - lei.width)//2 + 30, H - lei.height + 40), lei)
fe.save(f'{S}/fecho-{FIM}.png')
run(['ffmpeg','-v','error','-y','-loop','1','-t',str(FECHO),'-i',f'{S}/fecho-{FIM}.png','-f','lavfi','-t',str(FECHO),'-i','anullsrc=r=48000:cl=stereo','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','18','-c:a','aac','-shortest',f'{S}/pfim.mp4'])
todos = partes + [f'{S}/pfim.mp4']; durs.append(FECHO)
ent = sum([['-i', p] for p in todos], []); fc, ac = [], []; acc = durs[0]; va, aa = '[0:v]', '[0:a]'
for n in range(1, len(todos)):
    off = acc - T
    fc.append(f"{va}[{n}:v]xfade=transition=fade:duration={T}:offset={off:.3f}[vx{n}]"); ac.append(f"{aa}[{n}:a]acrossfade=d={T}:c1=tri:c2=tri[ax{n}]")
    va, aa = f'[vx{n}]', f'[ax{n}]'; acc = off + durs[n]
run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', ';'.join(fc + ac), '-map', va, '-map', aa, '-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k', f'{S}/junto.mp4'])
total = acc; tj = total - FECHO + 0.15
k5 = min(mudo); t_vo = sum(durs[:k5]) - k5*T + 0.1
vo_ovs = []
for j, (a, b, t, dd) in enumerate(VO): legenda(t, dd, f'vo{j}'); vo_ovs.append((f'vo{j}', t_vo + a, t_vo + b))
ent2 = ['-i', f'{S}/junto.mp4'] + sum([['-loop','1','-t',f'{total:.2f}','-i',f'{S}/{n}.png'] for n,_,_ in vo_ovs], [])
fc2 = ''.join(f"{'[0:v]' if i==0 else f'[w{i}]'}[{i+1}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[w{i+1}];" for i,(n,a,b) in enumerate(vo_ovs)).rstrip(';')
run(['ffmpeg','-v','error','-y'] + ent2 + ['-filter_complex', fc2, '-map', f'[w{len(vo_ovs)}]', '-map', '0:a', '-t', f'{total:.2f}', '-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy', f'{S}/junto2.mp4'])
tj = max(tj, t_vo + 5.75)
# música: bem de fundo na fala (~8%), sobe no "arrematado!" e no fecho
inicio_c3 = durs[0] + durs[1] - 2*T; t_arr = inicio_c3 + (59.3 - 51.95)
musica = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/joao/musicaE.mp3'
jingle = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
vol = f"if(between(t,{t_arr:.2f},{t_arr+1.8:.2f}),0.75,0.11)"
pocpoc = f'{MK}/marca/assinatura-sonora/OFICIAL/apoio-so-pocpoc.mp3'
af = (f"[0:a]anull[voz];[3:a]adelay={int(t_vo*1000)}|{int(t_vo*1000)},volume=1.6[vo];[4:a]atrim=0:0.6,adelay={int((t_arr-0.05)*1000)}|{int((t_arr-0.05)*1000)},volume=1.2[poc];[1:a]aloop=loop=1:size=1500000,atrim=0:{tj},volume='{vol}':eval=frame,afade=t=in:d=0.2,afade=t=out:st={tj-0.4}:d=0.4[m];"
      f"[2:a]adelay={int(tj*1000)}|{int(tj*1000)},volume=1.1[j];[voz][vo][poc][m][j]amix=inputs=5:normalize=0:duration=first,alimiter=limit=0.93[a]")
run(['ffmpeg','-v','error','-y','-i',f'{S}/junto2.mp4','-i',musica,'-i',jingle,'-i',f'{S}/vo-{FIM}.mp3','-i',pocpoc,'-filter_complex',af,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',f'{total:.2f}','-movflags','+faststart',f'{S}/REELS-iphone-natural-{FIM}.mp4'])
print('ok', FIM, round(total, 2), 'arrematado em', round(t_arr, 2))
