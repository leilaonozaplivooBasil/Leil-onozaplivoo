# Reels "Encontrou dono" — 5 entregas reais (provas do site) + fecho com a voz do Leiloeiro + jingle oficial
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; PROVAS = '/home/user/leilonozap/public/provas'; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920
NOITE, FLORESTA, VIVO, OURO, LIMA, BRANCO = (0,24,13), (0,45,27), (1,132,67), (208,172,81), (63,208,126), (255,255,255)
CLIPES = [  # arquivo, início, duração, rótulo
  ('cliente-full', 5.5, 3.0, 'Mais um entregue'),
  ('herbert-full', 8.5, 3.0, 'Ar-condicionado 12.000 BTUs'),
  ('matheus-video-full', 13.0, 3.0, 'PlayStation 5'),
  ('lucas-full', 4.8, 2.1, 'Scooter elétrica'),
  ('murilo-full', 82.5, 4.0, 'iPhone 17 Pro Max'),
]
def sombra_texto(d, xy, txt, f, cor, anchor='mm', s=6):
    for dx in range(-s, s+1, 2):
        for dy in range(-s, s+1, 2):
            d.text((xy[0]+dx, xy[1]+dy), txt, font=f, fill=(0,0,0,170), anchor=anchor)
    d.text(xy, txt, font=f, fill=cor, anchor=anchor)
def pilula(txt, nome, y=1650):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Bold', 52)
    w = d.textlength(txt, font=f); x0 = (W-w)/2-40
    d.rounded_rectangle((x0, y-50, x0+w+80, y+50), 50, fill=VIVO+(240,))
    d.text((W/2, y), txt, font=f, fill=BRANCO, anchor='mm'); im.save(f'{S}/{nome}.png')
def legenda_murilo(l1, l2, destaque, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((-40, 1395, W+40, 1800), 34, fill=(63,200,120,255))
    f = F('Black', 72); y = 1530 if l2 else 1597
    for i, linha in enumerate([l1] + ([l2] if l2 else [])):
        yy = y + i*130; w = d.textlength(linha, font=f); x = (W-w)/2
        if destaque in linha:
            a = linha.index(destaque); xa = x + d.textlength(linha[:a], font=f); wa = d.textlength(destaque, font=f)
            d.rounded_rectangle((xa-12, yy-52, xa+wa+12, yy+52), 14, fill=(20,20,20))
            d.text((x, yy), linha[:a], font=f, fill=(15,15,15), anchor='lm'); d.text((xa, yy), destaque, font=f, fill=(245,196,81), anchor='lm')
            d.text((xa+wa, yy), linha[a+len(destaque):], font=f, fill=(15,15,15), anchor='lm')
        else: d.text((x, yy), linha, font=f, fill=(15,15,15), anchor='lm')
    im.save(f'{S}/{nome}.png')
def gancho():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 760), fill=(0,0,0,0))
    g = Image.new('RGBA', (W, H), (0,0,0,0)); dg = ImageDraw.Draw(g)
    for y in range(0, 900):  # degradê escuro no topo para o texto respirar
        dg.line((0, y, W, y), fill=(0,24,13, int(200*(1-y/900))))
    im = Image.alpha_composite(im, g); d = ImageDraw.Draw(im)
    sombra_texto(d, (W/2, 300), 'TODOS ESSES JÁ', F('Black', 84), BRANCO)
    sombra_texto(d, (W/2, 420), 'ENCONTRARAM', F('Black', 108), LIMA)
    sombra_texto(d, (W/2, 560), 'DONO.', F('Black', 150), LIMA)
    im.save(f'{S}/gancho.png')
def fecho(etapa):
    im = Image.new('RGB', (W, H), NOITE); d = ImageDraw.Draw(im)
    for y in range(H): d.line((0, y, W, y), fill=tuple(int(NOITE[i]+(FLORESTA[i]-NOITE[i])*y/H) for i in range(3)))
    im = im.convert('RGBA')
    logo = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); logo.thumbnail((620, 220))
    im.alpha_composite(logo, ((W-logo.width)//2, 120))
    lei = Image.open(f'{MK}/marca/leiloeiro-aponta-moeda-recorte.png').convert('RGBA'); lei.thumbnail((1250, 1250))
    im.alpha_composite(lei, ((W-lei.width)//2 + 30, H-lei.height+130))
    d = ImageDraw.Draw(im)
    if etapa >= 1:
        sombra_texto(d, (W/2, 430), 'E amanhã chega', F('Black', 112), BRANCO, s=4)
        sombra_texto(d, (W/2, 560), 'mais um.', F('Black', 124), LIMA, s=4)
    if etapa >= 2:
        sombra_texto(d, (W/2, 690), 'Alguém arrematou no sábado...', F('Bold', 64), OURO, s=4)
    if etapa >= 3:
        f = F('Black', 56); t = 'SEGUE PRA VER QUEM É'
        w = d.textlength(t, font=f)
        d.rounded_rectangle(((W-w)/2-44, 770, (W+w)/2+44, 870), 50, fill=VIVO)
        d.text((W/2, 820), t, font=f, fill=BRANCO, anchor='mm')
        d.text((W/2, 925), '@leilaonozapoficial', font=F('SemiBold', 44), fill=BRANCO, anchor='mm')
    im.convert('RGB').save(f'{S}/fecho{etapa}.png')
def run(c): subprocess.run(c, check=True)
gancho(); [pilula(r, f'pil{i}', 1290 if a.startswith('murilo') else 1650) for i, (a, _, _, r) in enumerate(CLIPES)]
legenda_murilo('Tudo lacrado, gente,', 'tudo certinho.', 'lacrado,', 'leg1'); legenda_murilo('E foi o 17 Pro Max!', '', '17 Pro Max!', 'leg2'); [fecho(e) for e in (1, 2, 3)]
# 1) cortes, cada um em 1080x1920, 30 fps, com leve zoom de entrada
partes = []
for i, (arq, ini, dur, _) in enumerate(CLIPES):
    out = f'{S}/c{i}.mp4'; ov = [f'{S}/pil{i}.png'] + ([f'{S}/gancho.png'] if i == 0 else []) + ([f'{S}/leg1.png', f'{S}/leg2.png'] if arq.startswith('murilo') else [])
    pre = "[0:v]scale=1080:1920,crop=720:1280:30:400,scale=1080:1920:flags=lanczos,setsar=1," if arq.startswith('murilo') else "[0:v]scale=1080:1920,setsar=1,"
    vf = (pre + f"fps=30,zoompan=z='1.06-0.06*on/({dur}*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[b];"
          f"[b][1:v]overlay=0:0:enable='gte(t,0.25)'[v1]")
    if i == 0: vf += ";[v1][2:v]overlay=0:0[v]"
    elif arq.startswith('murilo'): vf += ";[v1][2:v]overlay=0:0:enable='lt(t,2.15)'[v2];[v2][3:v]overlay=0:0:enable='gte(t,2.15)'[v]"
    else: vf = vf.replace('[v1]', '[v]')
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(ini), '-t', str(dur), '-i', f'{PROVAS}/{arq}.mp4'] + sum([['-loop', '1', '-t', str(dur), '-i', o] for o in ov], [])
    cmd += ['-filter_complex', vf, '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-shortest', out]
    run(cmd); partes.append((out, dur))
# 2) fecho: 3 etapas que aparecem no ritmo da fala (voz 5,9 s) + logo segurando no jingle
voz = f'{S}/voz.mp3'
tempos = [(1, 1.9), (2, 1.8), (3, 4.2)]  # total 7,9 s: voz 5,9 + jingle 1,75 + respiro
for e, d in tempos:
    run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(d), '-i', f'{S}/fecho{e}.png', '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '19', f'{S}/f{e}.mp4'])
with open(f'{S}/lista.txt', 'w') as l:
    for p, _ in partes: l.write(f"file '{p}'\n")
    for e, _ in tempos: l.write(f"file '{S}/f{e}.mp4'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{S}/lista.txt', '-an', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', f'{S}/video-mudo.mp4'])
t_clipes = sum(d for _, d in partes); t_total = t_clipes + sum(d for _, d in tempos)
t_murilo = t_clipes - partes[-1][1]; t_voz = t_clipes + 0.15; t_jingle = t_voz + 5.95
# 3) áudio: música animada (abaixa na fala do Murilo e na voz do Leiloeiro), fala real do Murilo, voz do Leiloeiro, jingle inteiro no fim
musica = f'{S}/musica.mp3'; jingle = f'{MK}/marca/assinatura-sonora/OFICIAL/assinatura-sonora-leilao-no-zap-OFICIAL.mp3'
af = (f"[1:a]atrim=0:{t_jingle},volume='if(between(t,{t_murilo},{t_clipes}),0.35,if(gte(t,{t_voz}),0.22,0.9))':eval=frame,afade=t=out:st={t_jingle-0.8}:d=0.8[m];"
      f"[2:a]atrim={82.5}:{86.5},asetpts=PTS-STARTPTS,volume=1.6,adelay={int(t_murilo*1000)}|{int(t_murilo*1000)}[mu];"
      f"[3:a]volume=1.5,adelay={int(t_voz*1000)}|{int(t_voz*1000)}[vz];"
      f"[4:a]volume=1.1,adelay={int(t_jingle*1000)}|{int(t_jingle*1000)}[jg];"
      f"[m][mu][vz][jg]amix=inputs=4:normalize=0,apad=whole_dur={t_total},alimiter=limit=0.95[a]")
run(['ffmpeg', '-v', 'error', '-y', '-i', f'{S}/video-mudo.mp4', '-i', musica, '-i', f'{PROVAS}/murilo-full.mp4', '-i', voz, '-i', jingle,
     '-filter_complex', af, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', str(t_total), '-movflags', '+faststart', f'{S}/REELS-encontrou-dono.mp4'])
print('ok', t_total, t_murilo, t_voz, t_jingle)
