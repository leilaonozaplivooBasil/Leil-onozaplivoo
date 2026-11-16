# Segunda 16/11 (plano do Emanuel, semana editorial): carrossel 1 "Como fazer o cadastro" + artes de interesse do MacBook de quarta.
# Estilo "vitrine limpa" (marca/PROMPT-MESTRE-ARTES-ESTATICAS.md): fundo de uma cor, texto verde-escuro, Inter Display, logo pequeno.
# Prints REAIS do site no celular (leilaonozap.net, 16/11). Sem link e sem %. Uso: artes_segunda.py <lance_atual>
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(AQ); MK = '/home/user/Leil-onozaplivoo/marketing'
LANCE = sys.argv[1] if len(sys.argv) > 1 else '397'
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO = (245, 196, 81); VERDE = (10, 61, 38); VERDE2 = (27, 122, 72); AREIA = (246, 239, 226); MENTA = (214, 236, 221); BRANCO = (255, 255, 255)

def cabe(d, txt, peso, tam, larg, minimo=30):
    while tam >= minimo:
        f = F(peso, tam)
        if d.textlength(txt, font=f) <= larg: return f
        tam -= 2
    raise SystemExit(f'NÃO CABE: {txt!r}')

def linhas(d, xy, txts, peso, tam, larg, cor, entre=1.12, anchor='la'):
    x, y = xy
    for t in txts:
        f = cabe(d, t, peso, tam, larg); d.text((x, y), t, font=f, fill=cor, anchor=anchor); y += int(f.size * entre)
    return y

def logo(b, x, y, larg=160):
    lg = Image.open(f'{MK}/marca/logo-horizontal-transparente.png').convert('RGBA'); lg.thumbnail((larg, 70))
    ImageDraw.Draw(b).rounded_rectangle((int(x) - 18, int(y) - 10, int(x) + lg.width + 18, int(y) + lg.height + 10), 22, fill=VERDE)
    b.alpha_composite(lg, (int(x), int(y))); return lg.size

def celular(b, print_, x, y, alt, alvo=None, seta_de=None):
    """Print real num aparelho simples; alvo = caixa (x,y,w,h) no print, ganha um aro dourado."""
    im = Image.open(f'{AQ}/prints/{print_}').convert('RGBA'); k = alt / im.height; w = int(im.width * k)
    tela = im.resize((w, alt), Image.LANCZOS); borda = 18; R = 54
    sombra = Image.new('RGBA', b.size); ImageDraw.Draw(sombra).rounded_rectangle((x - borda + 14, y - borda + 26, x + w + borda + 14, y + alt + borda + 26), R + 10, fill=(0, 0, 0, 70))
    b.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(b); d.rounded_rectangle((x - borda, y - borda, x + w + borda, y + alt + borda), R + 10, fill=(18, 22, 20))
    m = Image.new('L', (w, alt), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, alt), R, fill=255); b.paste(tela, (x, y), m)
    if alvo:
        ax, ay, aw, ah = [v * k for v in alvo]; p = 16
        caixa = (x + ax - p, y + ay - p, x + ax + aw + p, y + ay + ah + p)
        g = Image.new('RGBA', b.size); ImageDraw.Draw(g).rounded_rectangle(caixa, 30, outline=OURO + (255,), width=14); b.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
        ImageDraw.Draw(b).rounded_rectangle(caixa, 30, outline=OURO, width=7)
        return caixa
    return (x, y, x + w, y + alt)

def seta(b, de, ate):
    d = ImageDraw.Draw(b); d.line((de, ate), fill=VERDE, width=9)
    v = np.array(ate) - np.array(de); v = v / np.linalg.norm(v); n = np.array([-v[1], v[0]]); a = np.array(ate)
    d.polygon([tuple(a), tuple(a - v * 38 + n * 22), tuple(a - v * 38 - n * 22)], fill=VERDE)

def rodape(b, n, tot=6, fundo=AREIA):
    d = ImageDraw.Draw(b); logo(b, 88, 1250, 140)
    d.rounded_rectangle((W - 160, 1258, W - 70, 1308), 25, fill=VERDE); d.text((W - 115, 1283), f'{n}/{tot}', font=F('SemiBold', 28), fill=BRANCO, anchor='mm')

def passo(b, n, x=70, y=90):
    d = ImageDraw.Draw(b); d.ellipse((x, y, x + 96, y + 96), fill=OURO); d.text((x + 48, y + 50), str(n), font=F('Black', 58), fill=VERDE, anchor='mm')
    d.text((x + 122, y + 50), f'PASSO {n} DE 4', font=F('SemiBold', 30), fill=VERDE2, anchor='lm')

def salvar(b, nome):
    p = f'{OUT}/{nome}'; b.convert('RGB').save(p, quality=93); print('ok', p)

W, H = 1080, 1350
# 1 · capa
b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b)
linhas(d, (70, 110), ['Como fazer', 'o seu cadastro'], 'Black', 110, 940, VERDE, 1.02)
linhas(d, (70, 470), ['em 4 passos,', 'pelo celular.'], 'Medium', 56, 440, VERDE)
d.rounded_rectangle((70, 650, 450, 720), 35, fill=VERDE); d.text((260, 685), 'leva 1 minuto', font=F('SemiBold', 34), fill=OURO, anchor='mm')
celular(b, 'p3.png', 560, 420, 760)
d = ImageDraw.Draw(b); d.text((70, 1040), 'Arrasta pro lado', font=F('SemiBold', 38), fill=VERDE); seta(b, (370, 1062), (500, 1062)); rodape(b, 1)
salvar(b, 'carrossel-cadastro-1.jpg')

# 2 · passo 1: ícone de pessoa
b = Image.new('RGBA', (W, H), AREIA + (255,)); d = ImageDraw.Draw(b); passo(b, 1)
y = linhas(d, (70, 230), ['Abra o site pelo', 'link da nossa bio e', 'toque no bonequinho', 'lá em cima'], 'Black', 54, 420, VERDE, 1.1)
d.text((70, y + 30), 'é o botão de entrar', font=F('Medium', 32), fill=VERDE2)
c = celular(b, 'p1.png', 528, 230, 820, alvo=(834, 18, 132, 132)); rodape(b, 2)
salvar(b, 'carrossel-cadastro-2.jpg')

# 3 · passo 2: Criar Conta
b = Image.new('RGBA', (W, H), AREIA + (255,)); d = ImageDraw.Draw(b); passo(b, 2)
y = linhas(d, (70, 230), ['Na janela que', 'abrir, toque em', '"Criar Conta"'], 'Black', 58, 420, VERDE, 1.1)
d.text((70, y + 30), 'fica embaixo de', font=F('Medium', 32), fill=VERDE2); d.text((70, y + 76), '"Ainda não tem conta?"', font=F('Medium', 32), fill=VERDE2)
c = celular(b, 'p2.png', 528, 230, 820, alvo=(111, 1662, 948, 144)); seta(b, (380, y + 160), (c[0] - 6, (c[1] + c[3]) // 2)); rodape(b, 3)
salvar(b, 'carrossel-cadastro-3.jpg')

# 4 · passo 3: preencher
b = Image.new('RGBA', (W, H), AREIA + (255,)); d = ImageDraw.Draw(b); passo(b, 3)
y = linhas(d, (70, 230), ['Preencha', 'os seus dados'], 'Black', 58, 420, VERDE, 1.1)
for t in ['Nome completo', 'E-mail', 'Telefone', 'CPF', 'Senha']:
    y += 22; d.ellipse((70, y + 12, 92, y + 34), fill=OURO); d.text((112, y), t, font=F('SemiBold', 40), fill=VERDE); y += 46
d.rounded_rectangle((70, y + 40, 480, y + 200), 22, fill=MENTA)
linhas(d, (95, y + 62), ['Tem Gmail? Use', '"Inscrever-se no Google"', 'que é mais rápido'], 'Medium', 30, 370, VERDE)
celular(b, 'p3.png', 528, 230, 820, alvo=(123, 1011, 924, 144)); rodape(b, 4)
salvar(b, 'carrossel-cadastro-4.jpg')

# 5 · passo 4: Criar Conta
b = Image.new('RGBA', (W, H), AREIA + (255,)); d = ImageDraw.Draw(b); passo(b, 4)
y = linhas(d, (70, 230), ['Toque em', '"Criar Conta"', 'e pronto!'], 'Black', 58, 420, VERDE, 1.1)
linhas(d, (70, y + 30), ['O endereço de entrega', 'só é pedido na hora', 'de receber o produto.'], 'Medium', 32, 420, VERDE2)
c = celular(b, 'p4b.png', 528, 230, 820, alvo=(123, 1614, 924, 144)); seta(b, (380, y + 180), (c[0] - 6, (c[1] + c[3]) // 2)); rodape(b, 5)
salvar(b, 'carrossel-cadastro-5.jpg')

# 6 · final
b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b)
y = linhas(d, (W // 2, 170), ['Pronto!', 'Você já entra', 'nos leilões.'], 'Black', 100, 900, VERDE, 1.08, 'ma')
d.line((W // 2 - 90, y + 40, W // 2 + 90, y + 40), fill=VERDE, width=6)
y = linhas(d, (W // 2, y + 100), ['Salva este post', 'pra não esquecer.'], 'Medium', 60, 900, VERDE, 1.12, 'ma')
d.rounded_rectangle((110, y + 70, W - 110, y + 300), 34, fill=VERDE)
linhas(d, (W // 2, y + 105), ['Ficou com dúvida?', 'Chama a gente no', 'WhatsApp oficial.'], 'SemiBold', 50, 760, OURO, 1.12, 'ma')
rodape(b, 6); salvar(b, 'carrossel-cadastro-6.jpg')

# Artes de interesse do MacBook (quarta 18/11, 20h). Foto original do produto (site), fundo branco tirado.
def macbook(alt):
    im = Image.open(f'{AQ}/fotos/macbook-neo-foto-c.webp').convert('RGB'); a = np.asarray(im).astype(float)
    dist = np.clip((255 - a.min(axis=2)) / 22, 0, 1); al = Image.fromarray((dist * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    p = im.convert('RGBA'); p.putalpha(al); p = p.crop(al.getbbox()); return p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
def pousa(b, p, x, base):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((x + p.width * .06, base - 18, x + p.width * .94, base + 18), fill=(0, 0, 0, 80))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(20))); b.alpha_composite(p, (int(x), int(base - p.height)))

b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b)
d.text((70, 110), 'O notebook que', font=F('Black', 76), fill=VERDE); d.text((70, 198), 'eu queria:', font=F('Medium', 76), fill=VERDE)
p = macbook(470); pousa(b, p, (W - p.width) // 2, 860); d = ImageDraw.Draw(b)
d.text((70, 930), 'Lance atual:', font=F('Medium', 56), fill=VERDE)
d.text((70, 1040), 'R$', font=F('Black', 80), fill=VERDE); d.text((190, 985), LANCE, font=F('Black', 220), fill=VERDE)
d.ellipse((800, 330, 1010, 540), fill=MENTA); d.text((905, 405), 'QUARTA', font=F('Black', 38), fill=VERDE2, anchor='mm'); d.text((905, 460), 'ÀS 20H', font=F('Black', 44), fill=VERDE2, anchor='mm')
logo(b, W - 210, 1250, 140); d = ImageDraw.Draw(b); d.text((70, 1285), 'MacBook Neo 13" · quarta, 18/11, às 20h', font=F('SemiBold', 32), fill=VERDE, anchor='lm')
salvar(b, 'arte-macbook-feed.jpg')

W, H = 1080, 1920
b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b); logo(b, (W - 170) // 2, 150, 170); d = ImageDraw.Draw(b)
d.text((W // 2, 330), 'O notebook que', font=F('Black', 92), fill=VERDE, anchor='ma'); d.text((W // 2, 435), 'eu queria:', font=F('Medium', 92), fill=VERDE, anchor='ma')
p = macbook(560); pousa(b, p, (W - p.width) // 2, 1180); d = ImageDraw.Draw(b)
d.text((W // 2, 1260), 'Lance atual:', font=F('Medium', 64), fill=VERDE, anchor='ma')
fR, fN = F('Black', 96), F('Black', 260); wr, wn = d.textlength('R$ ', font=fR), d.textlength(LANCE, font=fN); x0 = (W - wr - wn) / 2
d.text((x0, 1530), 'R$', font=fR, fill=VERDE, anchor='ls'); d.text((x0 + wr, 1530), LANCE, font=fN, fill=VERDE, anchor='ls')
d.rounded_rectangle((W // 2 - 300, 1620, W // 2 + 300, 1710), 45, fill=VERDE); d.text((W // 2, 1665), 'quarta, 18/11, às 20h', font=F('SemiBold', 44), fill=OURO, anchor='mm')
salvar(b, 'arte-macbook-story.jpg')
