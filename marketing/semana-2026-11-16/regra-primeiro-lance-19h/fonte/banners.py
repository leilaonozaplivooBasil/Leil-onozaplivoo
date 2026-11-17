# REGRA NOVA (17/11): o primeiro lance de cada pessoa vai até 1 h antes do fechamento. Leilão do MacBook Neo (qua 18/11, fecha 20h)
# → primeiro lance até as 19h. Quem já deu lance segue disputando até o fim. No site a regra vale (por enquanto) para leilões de MacBook
# (src/lib/prazoDoPrimeiroLance.js). Dois estilos × quatro formatos. Sem link e sem %.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
BR, OURO, OURO2, VERDE, VERDE2, ESC, LAR, CREME = (255, 255, 255), (245, 196, 81), (246, 214, 140), (10, 61, 38), (27, 122, 72), (5, 28, 17), (240, 96, 40), (214, 230, 218)
MAC = Image.open(f'{MK}/semana-2026-11-16/segunda-16-11/fonte/fotos/apple-silver-frente.png').convert('RGBA')
LOGO = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA')

def cabe(d, t, peso, tam, larg):
    while d.textlength(t, font=F(peso, tam)) > larg and tam > 20: tam -= 2
    return F(peso, tam)
def fundo_escuro(W, H, cx, cy):
    y, x = np.mgrid[0:H, 0:W]; dd = np.clip(np.hypot(x - cx, (y - cy)) / max(W, H) * 1.3, 0, 1) ** 1.2
    a = np.array((22, 82, 52))[None, None] * (1 - dd[..., None]) + np.array(ESC)[None, None] * dd[..., None]
    return Image.fromarray(a.astype('uint8')).convert('RGBA')
def relogio(b, cx, cy, r, cor_aro=OURO, fundo=ESC, ponteiro=BR):
    d = ImageDraw.Draw(b); g = Image.new('RGBA', b.size); ImageDraw.Draw(g).ellipse((cx - r * 1.25, cy - r * 1.25, cx + r * 1.25, cy + r * 1.25), fill=cor_aro + (70,)); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(r * .25)))
    d = ImageDraw.Draw(b); d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fundo, outline=cor_aro, width=max(4, r // 14))
    for k in range(12):
        an = k / 12 * 2 * np.pi; r1, r2 = r * .80, r * (.92 if k % 3 else .70)
        d.line((cx + r1 * np.sin(an), cy - r1 * np.cos(an), cx + r2 * np.sin(an), cy - r2 * np.cos(an)), fill=cor_aro, width=max(3, r // 26))
    # 19h: ponteiro das horas no 7, minutos no 12
    an = 7 / 12 * 2 * np.pi; d.line((cx, cy, cx + r * .48 * np.sin(an), cy - r * .48 * np.cos(an)), fill=ponteiro, width=max(6, r // 11))
    d.line((cx, cy, cx, cy - r * .70), fill=ponteiro, width=max(4, r // 16)); d.ellipse((cx - r * .07, cy - r * .07, cx + r * .07, cy + r * .07), fill=cor_aro)
def pil(d, cx, cy, t, f, fundo, cor, pad=32):
    w = d.textlength(t, font=f); h = f.size + 28
    d.rounded_rectangle((cx - w / 2 - pad, cy - h / 2, cx + w / 2 + pad, cy + h / 2), h / 2, fill=fundo); d.text((cx, cy), t, font=f, fill=cor, anchor='mm')
def logo(b, x, y, larg):
    lg = LOGO.copy(); lg.thumbnail((larg, larg)); b.alpha_composite(lg, (int(x - lg.width / 2), int(y))); return lg.height
def mac(larg):
    return MAC.resize((larg, int(MAC.height * larg / MAC.width)), Image.LANCZOS)
def poe(b, p, x, base):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((x - p.width * .46, base - 14, x + p.width * .46, base + 16), fill=(0, 0, 0, 150)); b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    b.alpha_composite(p, (int(x - p.width / 2), int(base - p.height)))
def salvar(b, nome): b.convert('RGB').save(f'{OUT}/{nome}', quality=94); print('ok', nome)

# ---------- ESTILO A · escuro com relógio (impacto) ----------
def estilo_a(W, H, nome, s):
    b = fundo_escuro(W, H, W / 2, H * s['rel_y']); d = ImageDraw.Draw(b); u = s['u']
    logo(b, W / 2, s['logo'], int(150 * u))
    d = ImageDraw.Draw(b); pil(d, W / 2, s['pil'], 'ATENÇÃO: A REGRA MUDOU', F('Black', int(40 * u)), LAR, BR)
    f = cabe(d, 'PRIMEIRO LANCE', 'Black', int(118 * u), W * .9); d.text((W / 2, s['t1']), 'PRIMEIRO LANCE', font=f, fill=BR, anchor='mm')
    relogio(b, W / 2 - (s['rel_r'] * 1.15 if s.get('lado') else 0), s['rel_cy'], s['rel_r'])
    d = ImageDraw.Draw(b); fx = F('Black', int(s['hora_tam']))
    if s.get('lado'):
        d.text((W / 2 + s['rel_r'] * .25, s['rel_cy']), 'ATÉ AS', font=F('Black', int(56 * u)), fill=OURO2, anchor='ls')
        d.text((W / 2 + s['rel_r'] * .2, s['rel_cy'] + s['hora_tam'] * .82), '19H', font=fx, fill=OURO, anchor='ls')
    else:
        d.text((W / 2, s['ate']), 'ATÉ AS 19H', font=fx, fill=OURO, anchor='mm')
    y = s['corpo']
    for t, cor, peso in (('Quem não der o primeiro lance', BR, 'Bold'), ('até as 19h fica de fora do leilão.', BR, 'Bold'), ('Vale para clientes novos e antigos.', CREME, 'Medium')):
        f = cabe(d, t, peso, int(46 * u), W * .88); d.text((W / 2, y), t, font=f, fill=cor, anchor='mm'); y += f.size * 1.3
    d.rounded_rectangle((W * .07, s['box'], W * .93, s['box'] + s['box_h']), int(34 * u), fill=(4, 22, 13), outline=OURO, width=3)
    t1 = 'JÁ VALE AMANHÃ'; t2 = 'MacBook Neo · quarta, 18/11 · fecha às 20h'
    d.text((W / 2, s['box'] + s['box_h'] * .34), t1, font=F('Black', int(44 * u)), fill=OURO, anchor='mm')
    f = cabe(d, t2, 'SemiBold', int(38 * u), W * .8); d.text((W / 2, s['box'] + s['box_h'] * .70), t2, font=f, fill=BR, anchor='mm')
    salvar(b, nome)

estilo_a(1080, 1920, 'A-story-status-1080x1920.jpg', dict(u=1.0, rel_y=.40, logo=110, pil=270, t1=420, rel_cy=760, rel_r=230, hora_tam=190, ate=1150, corpo=1300, box=1520, box_h=230))
estilo_a(1080, 1350, 'A-feed-1080x1350.jpg', dict(u=.9, rel_y=.40, logo=50, pil=180, t1=300, rel_cy=560, rel_r=170, lado=True, hora_tam=170, corpo=850, box=1080, box_h=200))
estilo_a(1080, 1080, 'A-whatsapp-1080x1080.jpg', dict(u=.82, rel_y=.40, logo=36, pil=140, t1=240, rel_cy=440, rel_r=140, lado=True, hora_tam=150, corpo=680, box=860, box_h=180))

# site: horizontal 1920x1080 (relógio à esquerda, texto à direita)
W, H = 1920, 1080; b = fundo_escuro(W, H, 520, 540); relogio(b, 520, 560, 300); d = ImageDraw.Draw(b)
logo(b, 1340, 70, 170); d = ImageDraw.Draw(b); pil(d, 1340, 250, 'ATENÇÃO: A REGRA MUDOU', F('Black', 42), LAR, BR)
d.text((1340, 390), 'PRIMEIRO LANCE', font=F('Black', 112), fill=BR, anchor='mm'); d.text((1340, 530), 'ATÉ AS 19H', font=F('Black', 150), fill=OURO, anchor='mm')
for i, (t, cor) in enumerate((('Quem não der o primeiro lance até as 19h', BR), ('fica de fora do leilão. Vale para novos e antigos.', CREME))):
    d.text((1340, 660 + i * 62), t, font=F('Bold' if i == 0 else 'Medium', 44), fill=cor, anchor='mm')
d.rounded_rectangle((900, 820, 1780, 980), 34, fill=(4, 22, 13), outline=OURO, width=3)
d.text((1340, 870), 'JÁ VALE AMANHÃ', font=F('Black', 44), fill=OURO, anchor='mm'); d.text((1340, 930), 'MacBook Neo · quarta, 18/11 · fecha às 20h', font=F('SemiBold', 38), fill=BR, anchor='mm')
salvar(b, 'A-site-1920x1080.jpg')

# ---------- ESTILO B · vitrine limpa (dourado + produto real) ----------
def estilo_b(W, H, nome, s):
    b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b); u = s['u']
    pil(d, W / 2, s['pil'], 'REGRA NOVA', F('Black', int(42 * u)), VERDE, OURO)
    f = cabe(d, 'Deu o primeiro lance', 'Black', int(96 * u), W * .9); d.text((W / 2, s['t1']), 'Deu o primeiro lance', font=f, fill=VERDE, anchor='mm')
    f2 = cabe(d, 'até as 19h?', 'Black', int(150 * u), W * .9); d.text((W / 2, s['t2']), 'até as 19h?', font=f2, fill=VERDE, anchor='mm')
    d.text((W / 2, s['t3']), 'Então você está no páreo.', font=F('Medium', int(48 * u)), fill=VERDE2, anchor='mm')
    poe(b, mac(int(W * s['mac'])), W / 2, s['mac_base']); d = ImageDraw.Draw(b)
    y = s['corpo']
    for t, peso in (('Depois das 19h, só continua', 'SemiBold'), ('quem já tiver dado lance.', 'SemiBold')):
        f = cabe(d, t, peso, int(44 * u), W * .86); d.text((W / 2, y), t, font=f, fill=VERDE, anchor='mm'); y += f.size * 1.25
    d.rounded_rectangle((W * .08, s['box'], W * .92, s['box'] + s['box_h']), int(30 * u), fill=VERDE)
    t2 = 'MacBook Neo · quarta, 18/11 · fecha às 20h'
    f = cabe(d, t2, 'Black', int(40 * u), W * .78); d.text((W / 2, s['box'] + s['box_h'] / 2), t2, font=f, fill=OURO, anchor='mm')
    lg = LOGO.copy(); lg.thumbnail((int(140 * u), int(140 * u))); d.rounded_rectangle((W / 2 - lg.width / 2 - 24, s['logo'] - 12, W / 2 + lg.width / 2 + 24, s['logo'] + lg.height + 12), 22, fill=VERDE)
    b.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(s['logo']))); salvar(b, nome)

estilo_b(1080, 1920, 'B-story-status-1080x1920.jpg', dict(u=1.0, pil=200, t1=340, t2=480, t3=600, mac=.74, mac_base=1220, corpo=1330, box=1480, box_h=130, logo=1680))
estilo_b(1080, 1350, 'B-feed-1080x1350.jpg', dict(u=.9, pil=100, t1=205, t2=320, t3=420, mac=.54, mac_base=880, corpo=960, box=1080, box_h=110, logo=1225))
estilo_b(1080, 1080, 'B-whatsapp-1080x1080.jpg', dict(u=.78, pil=70, t1=155, t2=250, t3=335, mac=.40, mac_base=700, corpo=760, box=860, box_h=95, logo=985))

# site: faixa fina 1920x500 (para o topo da página)
W, H = 1920, 500; b = fundo_escuro(W, H, 300, 250); relogio(b, 260, 250, 170); d = ImageDraw.Draw(b)
d.text((520, 150), 'REGRA NOVA: PRIMEIRO LANCE ATÉ AS 19H', font=cabe(d, 'REGRA NOVA: PRIMEIRO LANCE ATÉ AS 19H', 'Black', 76, 1330), fill=OURO, anchor='lm')
d.text((520, 250), 'Quem não der o primeiro lance até as 19h fica de fora do leilão.', font=F('Bold', 44), fill=BR, anchor='lm')
d.text((520, 320), 'Vale para clientes novos e antigos.', font=F('Medium', 36), fill=CREME, anchor='lm'); d.text((520, 385), 'Já vale amanhã: MacBook Neo · quarta, 18/11 · fecha às 20h', font=F('Black', 38), fill=OURO2, anchor='lm')
logo(b, 1800, 40, 140); salvar(b, 'A-site-faixa-1920x500.jpg')
