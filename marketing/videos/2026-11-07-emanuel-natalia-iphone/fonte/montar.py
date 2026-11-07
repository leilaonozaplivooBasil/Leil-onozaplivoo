# Vídeo Emanuel + Natália (IMG_7327) — feed do Insta e versão vendedores
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; MK = '/home/user/Leil-onozaplivoo/marketing'; A, B = 6.02, 40.2; dur = round(B - A, 2)
F = lambda p, t: ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-%s.otf' % p, t)
W, H = 1080, 1920; VERDE, OURO, NOITE, BR = (27,122,72), (245,196,81), (10,20,16), (255,255,255)
PROB = []
def pilula(d, y, t, f, cor, txt, raio):
    w = d.textlength(t, font=f)
    if w + 80 > W - 60: PROB.append(f'"{t}" não cabe')
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
# tempos do vídeo original (Whisper medium, conferido) — subtrai A
LEG = [(4.7, 7.7, 'eu me chamo', 'Emanuel'), (7.7, 10.0, 'e eu me chamo', 'Natália'),
       (10.0, 12.2, 'e nós viemos convidar você', None), (12.2, 13.95, 'a participar do leilão do', 'iPhone'),
       (13.95, 16.3, 'que encerra hoje', 'às 20h'), (16.3, 18.75, 'fala aí, Natália:', 'as características?'),
       (18.75, 20.6, 'lacrado', 'na caixa'), (20.6, 21.95, 'com', 'nota fiscal'), (21.95, 22.98, '1 ano de', 'garantia'),
       (22.98, 23.94, 'tu acredita nisso?', None), (23.94, 26.1, 'é mesmo!', None),
       (26.1, 28.7, 'gente, a Leilão no Zap é', 'fantástica, né?'), (28.7, 29.6, None, 'fantástica!'),
       (29.6, 33.2, 'comente agora', 'iPhone'), (33.2, 36.4, 'a gente te envia o link', 'pra dar seu lance'),
       (36.4, 40.2, 'vem pra', 'Leilão no Zap!')]
selo()
def render(saida, extra=None):
    ent = ['-i', f'{S}/base.mp4', '-loop', '1', '-t', f'{dur}', '-i', f'{S}/selo.png']; vf = "[0:v][1:v]overlay=0:0[b0]"; n = 0
    leg = list(LEG)
    if extra: leg = [l for l in leg if l[0] < 29.6] + extra
    for j, (a, b, t, dd) in enumerate(leg):
        legenda(t, dd, f'l{j}'); ent += ['-loop', '1', '-t', f'{dur}', '-i', f'{S}/l{j}.png']
        vf += f";[b{j}][{2+j}:v]overlay=0:0:enable='between(t,{round(a-A,2)},{round(b-A,2)})'[b{j+1}]"; n = j + 1
    subprocess.run(['ffmpeg','-v','error','-y'] + ent + ['-i', f'{S}/audio.wav', '-filter_complex', vf, '-map', f'[b{n}]', '-map', f'{len(leg)+2}:a', '-t', f'{dur}',
        '-c:v','libx264','-crf','18','-preset','medium','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart', saida], check=True)
render(f'{S}/feed.mp4')
# vendedores (WhatsApp): sem "comente", chama pro link
render(f'{S}/vendedores.mp4', [(29.6, 33.2, 'é agora, iPhone!', 'dá seu lance'), (33.2, 36.4, 'o link tá aqui', 'na mensagem'), (36.4, 40.2, 'vem pra', 'Leilão no Zap!')])
if PROB: print('PROBLEMAS', PROB); sys.exit(1)
print('ok')
