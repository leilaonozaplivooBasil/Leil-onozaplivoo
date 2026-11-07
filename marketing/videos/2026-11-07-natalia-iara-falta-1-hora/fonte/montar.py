# Vídeos Natália + Iara (IMG_4931 e IMG_4932) — "falta 1 hora" pro martelo do iPhone. Stories e vendedores.
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR = (27,122,72), (245,196,81), (10,20,16), (255,255,255)
PROB = []
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 2*raio > W - 60: PROB.append(f'"{t}" não cabe')
    x0 = (W - w) / 2 - raio + 8; d.rounded_rectangle((x0, y - raio, x0 + w + 2*raio - 16, y + raio), raio, fill=cor); d.text((W/2, y), t, font=f, fill=txt, anchor='mm')
def legenda(txt, dest, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); y = 1430
    if txt: pilula(d, y, txt, F('Black', 56), VERDE + (245,), BR, 46); y += 106
    if dest: pilula(d, y, dest.upper(), F('Black', 66), OURO + (255,), (10,60,32), 50)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def selo():
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
    d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
    f = F('Black', 34); t = 'IPHONE · MARTELO 20H'; w = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=(243,91,18,240)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
VIDEOS = {
 'IMG_4931': dict(A=1.4, B=17.45, musica='03-piano-house', saida='STORY-VENDEDORES-1-voce-acredita-falta-1-hora', LEG=[
   (1.4, 3.2, 'Natália, você acredita', None), (3.2, 5.4, 'que falta 1 hora pro', 'leilão do iPhone?'),
   (5.4, 6.85, 'ai, meu Deus, sério?', None), (6.85, 8.9, 'menos de', '1 hora!'), (8.9, 10.55, 'como você está se sentindo?', None),
   (10.55, 12.0, 'nossa, eu estou', 'muito ansiosa'), (12.0, 12.75, 'e vocês?', None),
   (12.75, 14.1, 'ansiosa pra saber', None), (14.1, 16.4, 'quem vai ser o arrematante', 'dessa noite'), (16.4, 17.45, None, 'muita emoção!')]),
 'IMG_4932': dict(A=0.6, B=25.4, musica='04-funky-soul-house', saida='STORY-VENDEDORES-2-o-que-falta-clica-no-link', LEG=[
   (0.6, 2.6, 'Iara, você não vai', 'acreditar'), (2.6, 3.85, 'pleno sábado,', None), (3.85, 5.8, 'menos de 1 hora pra', 'acabar o leilão'),
   (5.8, 8.2, 'galera inteira', 'trabalhando'), (8.2, 9.4, 'atendendo todo mundo', None), (9.4, 10.7, 'o que que falta?', None),
   (10.7, 13.0, 'Iara, o que será que', 'esse pessoal'), (13.0, 14.9, 'tá esperando pra', 'arrematar o iPhone?'),
   (14.9, 16.9, 'clicar no link e', 'participar!'), (16.9, 17.9, 'clica, gente!', None), (17.9, 18.95, 'o que vocês estão esperando?', None),
   (18.95, 21.8, 'se tiver dúvida,', 'chama no direct'), (21.8, 23.2, 'entendeu, Iara?', None), (23.2, 23.7, 'entendi!', None),
   (23.7, 25.4, 'então tá bom,', 'vamos lá, pessoal!')]),
}
# zoom de 18% preso no topo: o bolo de fio preto do chão (sempre abaixo da linha 1700) sai do quadro (pedido da Natália)
TM = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
selo(); OUT = sys.argv[2]
SO = sys.argv[3:] or list(VIDEOS)
for v, c in VIDEOS.items():
    if v not in SO: continue
    A, B = c['A'], c['B']; dur = round(B - A, 2)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(A),'-to',str(B),'-i',f'{S}/in/{v}.mov','-an','-vf',f'{TM},scale=1276:2266:flags=lanczos,crop=1080:1920:98:0,fps=30,eq=saturation=1.05','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',f'{S}/{v}-base.mp4'], check=True)
    # voz já tratada num wav separado (regra: nada de loudnorm junto com amix)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(A),'-to',str(B),'-i',f'{S}/{v}-voz_ok.wav','-af','afade=t=in:d=0.04',f'{S}/{v}-voz_c.wav'], check=True)
    m = f'{MK}/marca/trilhas-base/pegada-orla/{c["musica"]}.mp3'
    subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','-1','-i',m,'-i',f'{S}/{v}-voz_c.wav','-filter_complex',
        f"[0:a]atrim=0:{dur},asetpts=N/SR/TB,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.26,afade=t=in:d=0.6,afade=t=out:st={dur-1.5}:d=1.5[m];"
        "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];"
        "[v][md]amix=inputs=2:duration=first:normalize=0,volume=1.41", '-ar','48000',f'{S}/{v}-audio.wav'], check=True)
    ent = ['-i', f'{S}/{v}-base.mp4', '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png']; vf = "[0:v][1:v]overlay=0:0[b0]"
    for j, (a, b, t, dd) in enumerate(c['LEG']):
        legenda(t, dd, f'{v}-l{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/{v}-l{j}.png']
        vf += f";[b{j}][{2+j}:v]overlay=0:0:enable='between(t,{round(a-A,2)},{round(b-A-0.04,2)})'[b{j+1}]"
    n = len(c['LEG'])
    subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-i', f'{S}/{v}-audio.wav', '-filter_complex', vf, '-map', f'[b{n}]', '-map', f'{n+2}:a', '-t', f'{dur}',
        '-c:v','libx264','-crf','18','-preset','medium','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart', f'{OUT}/{c["saida"]}.mp4'], check=True)
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok')
