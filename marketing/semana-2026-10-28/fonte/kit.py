# Molde visual da semana (briefing Duda, 27/10/2026): verde-escuro, verde, preto e toque de dourado.
# Texto na tela SEMPRE na mesma fonte, no mesmo lugar (faixa verde-escura em y=1250..1560), formato 9:16.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = '/home/user/leilonozap/public/marca/agentes'
FONTE = '/usr/share/fonts/opentype/inter/InterDisplay-%s.otf'

VERDE_ESCURO = (8, 38, 25)
VERDE = (34, 139, 76)
VERDE_CLARO = (205, 235, 214)
DOURADO = (232, 186, 74)
BRANCO = (255, 255, 255)
W, H = 1080, 1920
FAIXA = (60, 1250, 1020, 1560)   # o lugar fixo do texto em todo stories


def fonte(peso, tam):
    return ImageFont.truetype(FONTE % peso, tam)


def fundo(w=W, h=H, brilho=(540, 760)):
    """Degradê verde-escuro com um brilho suave atrás do personagem/produto."""
    im = Image.new('RGB', (w, h))
    px = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        c = tuple(int(a + (b - a) * t) for a, b in zip((14, 64, 40), (4, 20, 12)))
        px.line([(0, y), (w, y)], fill=c)
    luz = Image.new('L', (w, h), 0)
    ImageDraw.Draw(luz).ellipse((brilho[0] - 420, brilho[1] - 420, brilho[0] + 420, brilho[1] + 420), fill=120)
    luz = luz.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', (w, h), (46, 150, 88)), im, luz)
    return im.convert('RGBA')


def recorte(caminho, altura):
    im = Image.open(caminho).convert('RGBA')
    return im.resize((int(im.width * altura / im.height), altura), Image.LANCZOS)


def leiloeiro(nome, altura):
    return recorte(f'{SITE}/leiloeiro/{nome}.webp', altura)


def leila(nome, altura):
    return recorte(f'{SITE}/leila-recorte/{nome}.webp', altura)


def sombra(im, base, xy, raio=30, forca=140):
    a = im.split()[-1].point(lambda v: forca if v > 10 else 0)
    s = Image.new('RGBA', im.size, (0, 0, 0, 0))
    s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(s, (xy[0] + 10, xy[1] + 24))
    base.alpha_composite(im, xy)


def logo(base, y=110, largura=360, x=None):
    lg = Image.open(f'{AQUI}/logo.png').convert('RGBA')
    lg = lg.resize((largura, int(lg.height * largura / lg.width)), Image.LANCZOS)
    base.alpha_composite(lg, ((base.width - largura) // 2 if x is None else x, y))


def selo(base, texto, y, cor=DOURADO, tam=34, x=None):
    """Etiqueta em pílula com contorno dourado (ex.: 'QUARTA · DIA DE LEILÃO')."""
    d = ImageDraw.Draw(base)
    f = fonte('Black', tam)
    w = d.textlength(texto, font=f)
    x = (base.width - w) / 2 if x is None else x
    d.rounded_rectangle((x - 30, y - 14, x + w + 30, y + tam + 18), radius=40, fill=(0, 0, 0, 150), outline=cor, width=3)
    d.text((x, y), texto, font=f, fill=cor)


def _linhas(d, texto, f, larg):
    """Quebra por palavra; *palavra* sai dourada."""
    pal = texto.split(' ')
    out, atual = [], []
    for p in pal:
        teste = ' '.join(atual + [p]).replace('*', '')
        if atual and d.textlength(teste, font=f) > larg:
            out.append(atual)
            atual = [p]
        else:
            atual.append(p)
    if atual:
        out.append(atual)
    return out


def texto_rico(d, xy_centro, texto, f, larg, cor=BRANCO, destaque=DOURADO, entre=1.12):
    linhas = _linhas(d, texto, f, larg)
    alt = f.size * entre
    y = xy_centro[1] - alt * len(linhas) / 2
    for lin in linhas:
        limpo = ' '.join(lin).replace('*', '')
        x = xy_centro[0] - d.textlength(limpo, font=f) / 2
        for i, p in enumerate(lin):
            c = destaque if '*' in p else cor
            s = p.replace('*', '') + (' ' if i < len(lin) - 1 else '')
            d.text((x, y), s, font=f, fill=c)
            x += d.textlength(s, font=f)
        y += alt
    return y


def faixa(base, titulo, sub=None, caixa=FAIXA, opaco=235, tam=74):
    """A faixa fixa: título grande (palavra entre *asteriscos* sai dourada) e uma linha de apoio."""
    x0, y0, x1, y1 = caixa
    camada = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    d.rounded_rectangle(caixa, radius=40, fill=VERDE_ESCURO + (opaco,))
    d.rounded_rectangle((x0 + 40, y0, x1 - 40, y0 + 8), radius=4, fill=DOURADO + (255,))
    base.alpha_composite(camada)
    d = ImageDraw.Draw(base)
    larg = x1 - x0 - 90
    while tam > 56 and len(_linhas(ImageDraw.Draw(base), titulo.upper(), fonte('Black', tam), larg)) > 2:
        tam -= 6
    f, fs = fonte('Black', tam), fonte('Bold', 40)
    alt_t = len(_linhas(d, titulo.upper(), f, larg)) * tam * 1.12
    alt_s = len(_linhas(d, sub, fs, larg)) * 40 * 1.25 + 26 if sub else 0
    topo = (y0 + y1) / 2 - (alt_t + alt_s) / 2 + 6
    texto_rico(d, ((x0 + x1) / 2, topo + alt_t / 2), titulo.upper(), f, larg)
    if sub:
        texto_rico(d, ((x0 + x1) / 2, topo + alt_t + 26 + (alt_s - 26) / 2), sub, fs, larg, cor=VERDE_CLARO, entre=1.25)


def cartao_foto(base, caminho, caixa, raio=36):
    """Foto real do produto num cartão branco arredondado (as fotos vêm com fundo branco)."""
    x0, y0, x1, y1 = caixa
    w, h = x1 - x0, y1 - y0
    card = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    ft = Image.open(caminho).convert('RGB')
    esc = min((w - 60) / ft.width, (h - 60) / ft.height)
    ft = ft.resize((int(ft.width * esc), int(ft.height * esc)), Image.LANCZOS)
    card.paste(ft, ((w - ft.width) // 2, (h - ft.height) // 2))
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=raio, fill=255)
    card.putalpha(m)
    s = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle((x0 + 8, y0 + 26, x1 + 8, y1 + 26), radius=raio, fill=(0, 0, 0, 150))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(26)))
    base.alpha_composite(card, (x0, y0))
    ImageDraw.Draw(base).rounded_rectangle(caixa, radius=raio, outline=DOURADO, width=4)


def preco(base, xy, rotulo, valor, cor_valor=BRANCO, riscado=False, tam=64):
    d = ImageDraw.Draw(base)
    d.text(xy, rotulo, font=fonte('Bold', 34), fill=VERDE_CLARO)
    fv = fonte('Black', tam)
    d.text((xy[0], xy[1] + 44), valor, font=fv, fill=cor_valor)
    if riscado:
        w = d.textlength(valor, font=fv)
        yy = xy[1] + 44 + tam * 0.58
        d.line((xy[0] - 4, yy, xy[0] + w + 4, yy), fill=(230, 80, 70), width=7)


def sobreposicao(titulo, sub=None, topo=None):
    """PNG transparente 9:16 para colar por cima do vídeo que a equipe grava (mesma faixa, mesmo lugar)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if topo:
        selo(im, topo, 150)
    faixa(im, titulo, sub)
    return im


def salvar(im, caminho, fundo_preto=False):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    if caminho.endswith('.png'):
        im.save(caminho, optimize=True)
    else:
        im.convert('RGB').save(caminho, quality=93)
