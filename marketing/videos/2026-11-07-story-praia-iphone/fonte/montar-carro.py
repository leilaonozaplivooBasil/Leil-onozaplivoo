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
im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((280, 104))
d.rounded_rectangle((40, 250, 80 + lg.width, 278 + lg.height), 30, fill=NOITE + (150,)); im.alpha_composite(lg, (60, 264))
f = F('Black', 34); t = 'IPHONE · MARTELO 20H'; w = d.textlength(t, font=f)
d.rounded_rectangle((W - 60 - w - 56, 270, W - 60, 340), 35, fill=(243,91,18,240)); d.text((W - 60 - (w + 56) / 2, 305), t, font=f, fill=BR, anchor='mm'); im.save(f'{S}/selo.png')
LEG = [(0.0, 1.36, 'eu não acredito...', None), (1.36, 3.25, 'que tu não deu', 'lance ainda?!'), (3.3, 5.6, 'já está em', 'R$ 800'), (5.8, 7.2, 'não perde', 'tempo!'), (7.25, 8.9, 'o iPhone pode ser', 'seu'), (8.9, 10.83, 'hoje, hein?', 'martelo às 20h')]
dur = 10.83
ent = ['-i', f'{S}/base.mp4', '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png']
vf = "[0:v][1:v]overlay=0:0[b0]"
for j, (a, b, t, dd) in enumerate(LEG):
    legenda(t, dd, f'l{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{j}.png']; vf += f";[b{j}][{2+j}:v]overlay=0:0:enable='between(t,{a},{b})'[b{j+1}]"
subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-filter_complex', vf, '-map', f'[b{len(LEG)}]', '-t', f'{dur}', '-c:v','libx264','-crf','17','-preset','slow','-profile:v','high','-pix_fmt','yuv420p', f'{S}/video.mp4'], check=True)
print('ok')
