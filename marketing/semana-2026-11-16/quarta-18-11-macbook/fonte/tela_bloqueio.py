# Arte da TARDE (qua 18/11) do MacBook: imita a TELA DE BLOQUEIO do celular cheia de notificações do Leilão no Zap.
# Ninguém resiste a notificação: hora grande, 4 avisos empilhados (lance subiu, 1º lance até 19h, quantos na disputa, martelo 20h),
# o MacBook de "papel de parede" e "deslize pra dar seu lance". Uso: tela_bloqueio.py <lance_antes> <lance_agora> <pessoas> <hora HH:MM> <horas_p_19h>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ) + '/visual'; MK = '/home/user/Leil-onozaplivoo/marketing'
ANTES, AGORA, PESSOAS, HORA, FALTA = sys.argv[1:6]; VEND = len(sys.argv) > 6 and sys.argv[6] == 'vendedor'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
W, H = 1080, 1920; BR, VERM, AMA, OURO = (255, 255, 255), (255, 59, 48), (255, 204, 0), (245, 196, 81)
EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
def real(v): return f'{float(v):,.0f}'.replace(',', '.')
def emoji(ch, tam):
    c = Image.new('RGBA', (140, 140)); ImageDraw.Draw(c).text((70, 70), ch, font=EMO, embedded_color=True, anchor='mm')
    c = c.crop(c.getbbox()); c.thumbnail((tam, tam), Image.LANCZOS); return c
# papel de parede: o MacBook grande, desfocado no fundo + nítido embaixo, num verde-noite
b = Image.new('RGBA', (W, H), (8, 26, 17, 255))
y, x = np.mgrid[0:H, 0:W]; g = np.clip(1 - np.hypot(x - W / 2, y - 1350) / 1200, 0, 1) ** 1.6
cor = np.zeros((H, W, 4), 'uint8'); cor[..., 0] = 40; cor[..., 1] = 160; cor[..., 2] = 95; cor[..., 3] = (g * 150).astype('uint8'); b.alpha_composite(Image.fromarray(cor))
mac = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA'); mac = mac.crop(mac.getbbox())
for cx, cy, r, c, a in ((W * .2, 700, 520, (120, 80, 230), 110), (W * .85, 1100, 560, (40, 190, 110), 120), (W / 2, 1500, 500, (150, 110, 255), 90)):
    gl = Image.new('RGBA', (W, H)); ImageDraw.Draw(gl).ellipse((cx - r, cy - r, cx + r, cy + r), fill=c + (a,)); b.alpha_composite(gl.filter(ImageFilter.GaussianBlur(170)))
MW = 600; m = mac.resize((MW, int(mac.height * MW / mac.width)), Image.LANCZOS); TOPO_MAC = 1300; BASE = TOPO_MAC + m.height
s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((W / 2 - MW * .47, BASE - 18, W / 2 + MW * .47, BASE + 22), fill=(0, 0, 0, 170)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
b.alpha_composite(m, ((W - MW) // 2, TOPO_MAC))
print('base mac', BASE)
d = ImageDraw.Draw(b)
# topo: cadeado, data e hora gigante
d.rounded_rectangle((W / 2 - 22, 118, W / 2 + 22, 150), 6, fill=BR); d.arc((W / 2 - 16, 92, W / 2 + 16, 128), 180, 360, fill=BR, width=6)
d.text((W / 2, 205), 'quarta-feira, 18 de novembro', font=F('SemiBold', 40), fill=(235, 240, 236), anchor='mm')
d.text((W / 2, 345), HORA, font=F('Bold', 230), fill=BR, anchor='mm')
# notificações (cartões "vidro")
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')
ic = LOGO.crop((0, 0, LOGO.height, LOGO.height)) if LOGO.width > LOGO.height else LOGO
ic = ic.resize((72, 72), Image.LANCZOS)
# texto com DESTAQUE nas palavras-chave (pedido do Emanuel): 'h' = marca-texto amarelo, 'v' = vermelho, 'b' = negrito branco
AMAC = (255, 214, 10)
def linha(d, x, y, partes, tam, peso_n='Medium'):
    x_ini = x
    for t, est in partes:
        f = F('Black' if est in 'hvb' else peso_n, tam); w = d.textlength(t, font=f)
        if est in 'hv' and x > x_ini: x += 12
        if est == 'h':
            d.rounded_rectangle((x - 6, y - tam * .62, x + w + 6, y + tam * .58), 10, fill=AMAC); d.text((x, y), t, font=f, fill=(20, 20, 20), anchor='lm')
        elif est == 'v':
            d.rounded_rectangle((x - 6, y - tam * .62, x + w + 6, y + tam * .58), 10, fill=VERM); d.text((x, y), t, font=f, fill=BR, anchor='lm')
        else: d.text((x, y), t, font=f, fill=BR, anchor='lm')
        x += w + (18 if est in 'hv' else 0)
NOTIF = [('🚨', [('O LANCE SUBIU!', 'v')], [('De R$ ' + real(ANTES) + ' pra ', 'n'), ('R$ ' + real(AGORA), 'h'), (' em poucas horas', 'n')], 'agora', True),
         ('⏰', [('Seu ', 'b'), ('1º LANCE', 'h'), ('só até ', 'b'), ('18H59', 'h')], [('Depois disso, quem não deu lance ', 'n'), ('fica de fora', 'b')], 'agora', False),
         ('👀', [(f'{PESSOAS} PESSOAS', 'h'), ('já na disputa', 'b')], [('MacBook Neo 13" · ', 'n'), ('novo e lacrado', 'b'), (', com nota', 'n')], 'há 2 min', False),
         ('🔨', [('O martelo bate ', 'b'), ('HOJE, ÀS 20H', 'h')], [('Quem der o ', 'n'), ('último lance', 'b'), (' leva o MacBook', 'n')], 'há 5 min', False)]
y0 = 470
for i, (e, t1, t2, quando, borda) in enumerate(NOTIF):
    h = 182; x0, x1 = 44, W - 44
    vidro = b.crop((x0, y0, x1, y0 + h)).filter(ImageFilter.GaussianBlur(30))
    camada = Image.new('RGBA', vidro.size, (255, 255, 255, 46)); vidro.alpha_composite(camada)
    mk = Image.new('L', vidro.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, vidro.width - 1, h - 1), 44, fill=255)
    b.paste(vidro, (x0, y0), mk); d = ImageDraw.Draw(b)
    if borda: d.rounded_rectangle((x0, y0, x1, y0 + h), 44, outline=VERM + (255,), width=5)
    im = Image.new('L', (72, 72), 0); ImageDraw.Draw(im).rounded_rectangle((0, 0, 71, 71), 18, fill=255)
    fundo_ic = Image.new('RGBA', (72, 72), (12, 40, 26, 255)); fundo_ic.alpha_composite(ic); b.paste(fundo_ic, (x0 + 30, y0 + 26), im); d = ImageDraw.Draw(b)
    d.text((x0 + 122, y0 + 46), 'LEILÃO NO ZAP', font=F('SemiBold', 30), fill=(230, 236, 232), anchor='lm'); d.text((x1 - 32, y0 + 46), quando, font=F('Medium', 30), fill=(215, 222, 218), anchor='rm')
    em = emoji(e, 58); b.alpha_composite(em, (x0 + 34, y0 + 104)); d = ImageDraw.Draw(b)
    linha(d, x0 + 128, y0 + 104, t1, 46); linha(d, x0 + 128, y0 + 152, t2, 33)
    y0 += h + 16
# rodapé: deslize pra dar seu lance + barrinha do iPhone
if VEND:
    d.text((W / 2, 1765), '↑  toque no link e dê seu lance', font=F('Bold', 46), fill=BR, anchor='mm')
    d.text((W / 2, 1825), 'o 1º lance só vale até as 18h59', font=F('SemiBold', 34), fill=AMAC, anchor='mm')
else:
    d.text((W / 2, 1760), '↑  deslize pra dar seu lance', font=F('SemiBold', 44), fill=BR, anchor='mm')
    d.text((W / 2, 1820), 'comenta LEILÃO que eu te mando o link', font=F('Medium', 32), fill=(215, 225, 218), anchor='mm')
d.rounded_rectangle((W / 2 - 140, 1880, W / 2 + 140, 1892), 6, fill=BR)
b.convert('RGB').save(f'{OUT}/V7-tarde-tela-de-bloqueio' + ('-VENDEDORES' if VEND else '-INSTAGRAM') + '.jpg', quality=94); print('ok')
