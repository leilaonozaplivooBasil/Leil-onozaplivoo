import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR = (27,122,72), (245,196,81), (10,20,16), (255,255,255)
def legenda(txt, dest, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Black', 58); fd = F('Black', 68); y = 1380
    if txt:
        w = d.textlength(txt, font=f); x0 = (W - w) / 2 - 34; d.rounded_rectangle((x0, y - 46, x0 + w + 68, y + 46), 46, fill=VERDE + (245,)); d.text((W/2, y), txt, font=f, fill=BR, anchor='mm'); y += 106
    if dest:
        t = dest.upper(); w = d.textlength(t, font=fd); x0 = (W - w) / 2 - 36; d.rounded_rectangle((x0, y - 50, x0 + w + 72, y + 50), 50, fill=OURO + (255,)); d.text((W/2, y), t, font=fd, fill=(10,60,32), anchor='mm')
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
def selo(nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
    d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
    f = F('Black', 34); t = 'IPHONE · MARTELO 20H'; w = d.textlength(t, font=f)
    d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=(243,91,18,240)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm')
    im.save(f'{S}/{nome}.png')
VIDEOS = {
 1: [(0.0, 1.56, 'bom dia, família', None), (1.56, 2.7, None, 'Leilão no Zap!'), (2.72, 5.16, 'já estamos aqui no', 'aquecimento'), (5.16, 7.3, 'para o leilão do', 'iPhone!')],
 2: [(0.0, 2.42, 'o lance atual está em', None), (2.42, 4.3, 'o lance atual está em', 'R$ 463'), (4.4, 6.7, 'quem vai ser o próximo', 'a dar o lance?'), (7.0, 8.2, 'estamos acompanhando', None), (8.2, 10.7, 'e vou colocar a', 'contagem regressiva')],
}
selo('selo')
musica = f'{MK}/marca/trilhas-base/pegada-orla/01-funky-house-quiosque.mp3'
for n, legs in VIDEOS.items():
    dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{S}/v{n}.mov']).decode().strip())
    ent = ['-i', f'{S}/v{n}.mov', '-i', f'{S}/voz{n}.mp3', '-i', musica, '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png']
    vf = "[0:v]fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,eq=saturation=1.08:contrast=1.04:brightness=0.01[b0];[b0][3:v]overlay=0:0[b1]"
    k = 1
    for j, (a, b, t, dd) in enumerate(legs):
        legenda(t, dd, f'l{n}_{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{n}_{j}.png']
        vf += f";[b{k}][{4+j}:v]overlay=0:0:enable='between(t,{a},{b})'[b{k+1}]"; k += 1
    af = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,equalizer=f=3500:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=8:release=200,loudnorm=I=-16:TP=-1.5:LRA=7,asplit[voz][vsc];"
          f"[2:a]aresample=48000,atrim=0:{dur},volume=0.10,afade=t=in:d=0.4,afade=t=out:st={dur-0.6}:d=0.6[m0];[m0][vsc]sidechaincompress=threshold=0.015:ratio=8:attack=15:release=300[m];"
          f"[voz][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.93[a]")
    subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', vf + f';[b{k}]null[v];' + af, '-map','[v]','-map','[a]','-t',f'{dur}','-c:v','libx264','-crf','17','-preset','slow','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart', f'{S}/STORY-praia-{n}.mp4'], check=True)
    print('ok', n, dur)
