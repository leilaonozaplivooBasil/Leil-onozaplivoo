import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; MK = '/home/user/Leil-onozaplivoo/marketing'; M = '/home/user/leilonozap/public/provas/murilo-full.mp4'
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR = (27,122,72), (245,196,81), (10,20,16), (255,255,255)
INI, FIM = 64.3, 78.4; dur = round(FIM - INI, 2)
def legenda(txt, dest, nome):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); f = F('Black', 56); fd = F('Black', 68); y = 1400
    if txt:
        while d.textlength(txt, font=f) > W - 160: f = F('Black', f.size - 2)
        w = d.textlength(txt, font=f); x0 = (W - w) / 2 - 34; d.rounded_rectangle((x0, y - 46, x0 + w + 68, y + 46), 46, fill=VERDE + (245,)); d.text((W/2, y), txt, font=f, fill=BR, anchor='mm'); y += 106
    if dest:
        t = dest.upper(); w = d.textlength(t, font=fd); x0 = (W - w) / 2 - 36; d.rounded_rectangle((x0, y - 50, x0 + w + 72, y + 50), 50, fill=OURO + (255,)); d.text((W/2, y), t, font=fd, fill=(10,60,32), anchor='mm')
    a = im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.45); s = Image.new('RGBA', (W, H), (0,0,0,0)); s.putalpha(a); Image.alpha_composite(s, im).save(f'{S}/{nome}.png')
im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
f = F('Black', 34); t = 'ARREMATOU POR R$ 4.640'; w = d.textlength(t, font=f)
d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=(243,91,18,240)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
LEG = [(64.3, 66.3, 'então assim, de repente', None), (66.3, 68.95, 'quando eu chegar em casa,', 'faço um videozinho'), (69.0, 72.25, 'vou indicando o leilão do sábado', 'pros meus amigos'),
       (72.3, 75.45, 'porque isso daqui foi', 'surreal!'), (75.5, 77.0, 'o preço que eu paguei', 'R$ 4.640'), (77.0, 78.4, 'foi surreal mesmo,', 'bem bacana!')]
ent = ['-ss', str(INI), '-t', str(dur), '-i', M, '-loop', '1', '-t', str(dur), '-i', f'{S}/selo.png']
vf = "[0:v]scale=1080:1920,crop=540:960:74:320,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,setsar=1,fps=30,eq=saturation=1.06:contrast=1.03[b0];[b0][1:v]overlay=0:0[b1]"
for j, (a, b, t, dd) in enumerate(LEG):
    legenda(t, dd, f'l{j}'); ent += ['-loop', '1', '-t', str(dur), '-i', f'{S}/l{j}.png']; vf += f";[b{j+1}][{2+j}:v]overlay=0:0:enable='between(t,{a-INI:.2f},{b-INI:.2f})'[b{j+2}]"
subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', vf, '-map', f'[b{len(LEG)+1}]', '-an', '-t', str(dur), '-c:v','libx264','-crf','17','-preset','slow','-pix_fmt','yuv420p', f'{S}/video.mp4'], check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss', str(INI), '-t', str(dur), '-i', M, '-vn', '-af', f'aresample=48000,aformat=channel_layouts=stereo,highpass=f=90,equalizer=f=3200:t=q:w=1.4:g=-2,acompressor=threshold=-22dB:ratio=2:attack=15:release=250,loudnorm=I=-16:TP=-3:LRA=9,aresample=48000,apad,atrim=0:{dur},afade=t=out:st={dur-0.3}:d=0.3', '-ar','48000', f'{S}/voz.wav'], check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i', f'{S}/video.mp4','-i', f'{S}/voz.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(dur),'-movflags','+faststart', f'{S}/MURILO-15s.mp4'], check=True)
print('ok', dur)
