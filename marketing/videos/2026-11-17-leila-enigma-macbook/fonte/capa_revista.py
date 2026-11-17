# Capa no clima da capa de revista do momento (17/11, pedido da Natália): fundo branco, quadradinho vermelho no topo com
# "Leilão no Zap" (o NOSSO nome, nunca o logo/título da revista), manchete preta condensada, círculo de ícones preto e vermelho
# (pôster nosso, gerado no Gamma) e o MacBook (ou o logo) no centro. Uso: capa_revista.py
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
ANTON = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/fonts/package/files/anton-latin-400-normal.woff'
SER, SERB, SERI = ('/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf', '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf', '/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf')
A = lambda t: ImageFont.truetype(ANTON, t); S = lambda f, t: ImageFont.truetype(f, t)
BRANCO, PRETO, VERM = (247, 245, 240), (17, 17, 17), (214, 30, 38)
POSTER = Image.open(f'{AQ}/poster.jpg').convert('RGB')
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')

def cabe(d, t, fn, tam, larg):
    while d.textlength(t, font=fn(tam)) > larg and tam > 20: tam -= 2
    return fn(tam)
def capa(W, H, nome, centro='mac', topo=0):
    b = Image.new('RGBA', (W, H), BRANCO + (255,)); d = ImageDraw.Draw(b); y = topo + int(H * .045)
    # quadradinho vermelho com o nosso nome
    bw, bh = int(W * .25), int(W * .115); d.rectangle((W / 2 - bw / 2, y, W / 2 + bw / 2, y + bh), fill=VERM)
    d.text((W / 2, y + bh * .32), 'Leilão', font=S(SER, int(bh * .36)), fill=BRANCO, anchor='mm'); d.text((W / 2, y + bh * .70), 'no Zap', font=S(SER, int(bh * .36)), fill=BRANCO, anchor='mm')
    y += bh + int(W * .03)
    f = cabe(d, 'O ENIGMA DE QUARTA', A, 220, W * .94); d.text((W / 2, y), 'O ENIGMA DE QUARTA', font=f, fill=PRETO, anchor='mt'); y += int(f.size * 1.18)
    linhas = [[('MacBook Neo ', SERB), ('Novo e lacrado', SERI), (' · Nota fiscal ', SER), ('Com garantia', SERI)],
              [('Regra nova ', SERB), ('1º lance só até as 19h', SERI), (' · Martelo ', SER), ('quarta, 20h', SERI)]]
    for ln in linhas:
        tam = int(W * .031); tot = sum(d.textlength(t, font=S(fn, tam)) for t, fn in ln); x = (W - tot) / 2
        for t, fn in ln: d.text((x, y), t, font=S(fn, tam), fill=PRETO); x += d.textlength(t, font=S(fn, tam))
        y += int(tam * 1.35)
    # círculo do pôster
    c = POSTER.crop((0, int(POSTER.height * .25), POSTER.width, int(POSTER.height * .25) + POSTER.width))
    dia = int(min(W * .96, H - y - H * .03)); c = c.resize((dia, dia), Image.LANCZOS)
    m = Image.new('L', (dia, dia), 0); ImageDraw.Draw(m).ellipse((0, 0, dia, dia), fill=255); cy = y + int(H * .015)
    b.paste(c, ((W - dia) // 2, cy), m); d = ImageDraw.Draw(b)
    # retângulo central (branco com borda vermelha) e o conteúdo
    rw, rh = int(dia * .52), int(dia * .30); cx0, cy0 = W / 2 - rw / 2, cy + dia * .47 - rh / 2
    d.rectangle((cx0, cy0, cx0 + rw, cy0 + rh), fill=BRANCO, outline=VERM, width=max(4, W // 200))
    if centro == 'mac':
        mw = int(rw * .86); mm = MAC.resize((mw, int(MAC.height * mw / MAC.width)), Image.LANCZOS); b.alpha_composite(mm, (int(W / 2 - mw / 2), int(cy0 + rh / 2 - mm.height / 2)))
    else:
        lg = LOGO.copy(); lg.thumbnail((int(rw * .80), int(rh * .70))); fundo = Image.new('RGBA', (int(rw - 12), int(rh - 12)), (10, 61, 38, 255)); b.alpha_composite(fundo, (int(cx0 + 6), int(cy0 + 6)))
        b.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(cy0 + rh / 2 - lg.height / 2)))
    b.convert('RGB').save(f'{OUT}/{nome}', quality=94); print('ok', nome)

capa(1080, 1920, 'CAPA-revista-macbook-1080x1920.jpg', 'mac', topo=120)
capa(1080, 1920, 'CAPA-revista-logo-1080x1920.jpg', 'logo', topo=120)
capa(1080, 1350, 'CAPA-revista-macbook-feed-1080x1350.jpg', 'mac')
