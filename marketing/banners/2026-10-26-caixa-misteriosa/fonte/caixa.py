"""Caixa misteriosa: 4 artes 1080x1080 para o card do leilão.
O Leiloeiro é sempre o recorte oficial (a-caixa.webp), sem nenhuma alteração por IA: só trocamos a caixa de papelão
por uma caixa desenhada aqui, e a mão dele volta por cima."""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

S = 2                      # supersample
W = 1080 * S
FONTE = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FONTE_B = '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
RECORTE = '/home/user/leilonozap/public/marca/agentes/leiloeiro/a-caixa.webp'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

VERDE_A = np.array([38, 176, 104]); VERDE_B = np.array([10, 92, 50])
OURO = [(255, 236, 160), (245, 196, 81), (201, 142, 30)]


def grad_v(w, h, c0, c1):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(c0)[None, None, :] * (1 - t) + np.array(c1)[None, None, :] * t
    return np.repeat(a, w, axis=1)


def ouro(w, h, vertical=True):
    """gradiente dourado metálico com brilho."""
    n = h if vertical else w
    t = np.linspace(0, 1, n)
    c = np.zeros((n, 3))
    for i in range(3):
        c[:, i] = np.interp(t, [0, .22, .45, .7, 1], [OURO[2][i], OURO[0][i], OURO[1][i], OURO[2][i] * .95, OURO[1][i]])
    if vertical:
        a = np.repeat(c[:, None, :], w, axis=1)
    else:
        a = np.repeat(c[None, :, :], h, axis=0)
    return Image.fromarray(a.clip(0, 255).astype('uint8'))


def interrogacao(img, cx, cy, tam, alfa=255):
    """'?' dourado com contorno verde-escuro e sombra."""
    f = ImageFont.truetype(FONTE, tam)
    camada = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(camada)
    d.text((cx, cy), '?', font=f, anchor='mm', fill=255)
    sombra = camada.filter(ImageFilter.GaussianBlur(tam * .04))
    sombra = ImageChops.offset(sombra, int(tam * .03), int(tam * .05))
    img.paste((4, 40, 22), (0, 0), sombra.point(lambda v: v * .7 * alfa / 255))
    cont = camada.filter(ImageFilter.MaxFilter(max(3, int(tam * .035) | 1)))
    img.paste((6, 52, 28), (0, 0), cont.point(lambda v: v * alfa / 255))
    g = ouro(img.size[0], img.size[1])
    # gradiente só na altura do '?'
    bb = camada.getbbox()
    if bb:
        g = ouro(img.size[0], bb[3] - bb[1] + 2)
        gg = Image.new('RGB', img.size, OURO[1]); gg.paste(g, (0, bb[1]))
        img.paste(gg, (0, 0), camada.point(lambda v: v * alfa / 255))


def padrao(img, cor, alfa, tam, seed):
    rnd = random.Random(seed)
    f = ImageFont.truetype(FONTE, tam)
    lay = Image.new('L', img.size, 0); d = ImageDraw.Draw(lay)
    for y in range(-tam, img.size[1] + tam, int(tam * 1.4)):
        for x in range(-tam, img.size[0] + tam, int(tam * 1.4)):
            d.text((x + (tam * .7 if (y // int(tam * 1.4)) % 2 else 0), y), '?', font=f, fill=alfa, anchor='mm')
    img.paste(cor, (0, 0), lay)


def face_frente(w, h, escuro=1.0, faixa_tampa=True, fita=True, int_q=True, seed=1):
    a = grad_v(w, h, VERDE_A * escuro, VERDE_B * escuro)
    # brilho diagonal suave
    yy, xx = np.mgrid[0:h, 0:w]
    sheen = np.exp(-(((xx / w) - (yy / h) * .6 - .15) ** 2) / .02) * 28 * escuro
    a = a + sheen[..., None]
    img = Image.fromarray(a.clip(0, 255).astype('uint8'))
    padrao(img, tuple(int(c * escuro) for c in (60, 200, 125)), 22, int(h * .11), seed)
    d = ImageDraw.Draw(img)
    tampa = int(h * .2)
    if faixa_tampa:
        # tampa um pouco mais clara, com sombra embaixo
        ov = Image.fromarray(grad_v(w, tampa, VERDE_A * escuro * 1.12, VERDE_A * escuro * .88).clip(0, 255).astype('uint8'))
        img.paste(ov, (0, 0))
        sh = Image.new('L', (w, h), 0); ImageDraw.Draw(sh).rectangle([0, tampa, w, tampa + int(h * .05)], fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(h * .02))
        img.paste((3, 30, 16), (0, 0), sh)
        # filete dourado na borda da tampa
        g = ouro(w, max(4, int(h * .022)))
        img.paste(g, (0, tampa - g.size[1]))
    if fita:
        fw = int(w * .13)
        g = ouro(fw, tampa, vertical=False)
        img.paste(g, (w // 2 - fw // 2, 0))
    if int_q:
        interrogacao(img, w // 2, int(tampa + (h - tampa) * .52), int((h - tampa) * .78))
    # borda escura nas laterais (oclusão)
    vin = Image.new('L', (w, h), 0); ImageDraw.Draw(vin).rectangle([0, 0, w, h], outline=110, width=int(w * .012))
    img.paste((4, 36, 20), (0, 0), vin.filter(ImageFilter.GaussianBlur(w * .01)))
    return img


def face_topo(w, h, fita=True):
    a = grad_v(w, h, VERDE_A * 1.18, VERDE_A * 1.0)
    img = Image.fromarray(a.clip(0, 255).astype('uint8'))
    padrao(img, (90, 220, 150), 18, int(h * .16), 3)
    if fita:
        fw = int(w * .13); fh = int(h * .2)
        img.paste(ouro(fw, h, vertical=False), (w // 2 - fw // 2, 0))
        img.paste(ouro(w, fh), (0, h // 2 - fh // 2))
    vin = Image.new('L', (w, h), 0); ImageDraw.Draw(vin).rectangle([0, 0, w, h], outline=90, width=int(w * .012))
    img.paste((8, 60, 32), (0, 0), vin.filter(ImageFilter.GaussianBlur(w * .01)))
    return img


def face_dentro(w, h):
    """interior da caixa aberta: paredes escuras e um brilho dourado no fundo."""
    a = np.zeros((h, w, 3)); a[:] = (6, 40, 22)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2)
    glow = np.exp(-r ** 2 / .06)
    a = a * (1 - glow[..., None]) + np.array([255, 226, 140])[None, None] * glow[..., None]
    img = Image.fromarray(a.clip(0, 255).astype('uint8'))
    return img


def coef(src, dst):
    """coeficientes de Image.PERSPECTIVE que levam dst (saída) -> src (textura)."""
    m = []; b = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(m, float), np.array(b, float)).tolist()


def colar_quad(canvas, tex, quad, luz=1.0):
    """quad: TL, TR, BR, BL na tela."""
    w, h = tex.size
    t = tex
    if luz != 1.0:
        t = Image.fromarray((np.asarray(tex).astype(float) * luz).clip(0, 255).astype('uint8'))
    c = coef([(0, 0), (w, 0), (w, h), (0, h)], quad)
    warped = t.convert('RGBA').transform(canvas.size, Image.PERSPECTIVE, c, Image.BICUBIC)
    mask = Image.new('L', canvas.size, 0); ImageDraw.Draw(mask).polygon(quad, fill=255)
    warped.putalpha(mask)
    canvas.alpha_composite(warped)


def aresta(canvas, p, q, cor=(190, 255, 210, 150), larg=3):
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).line([p, q], fill=cor, width=larg * S)
    canvas.alpha_composite(lay.filter(ImageFilter.GaussianBlur(S * .6)))


def laco(canvas, cx, cy, tam):
    """laço dourado (duas alças e um nó) em pé sobre a tampa."""
    k = 3
    L = Image.new('RGBA', (int(tam * 3) * k, int(tam * 2) * k), (0, 0, 0, 0))
    ox, oy = L.size[0] // 2, int(L.size[1] * .68)
    def alca(lado):
        a = Image.new('L', L.size, 0); d = ImageDraw.Draw(a)
        lw, lh = tam * .95 * k, tam * .62 * k
        d.ellipse([ox - lw / 2, oy - lh / 2, ox + lw / 2, oy + lh / 2], fill=255)
        d.ellipse([ox - lw * .28, oy - lh * .22, ox + lw * .28, oy + lh * .22], fill=0)
        a = a.rotate(lado * 28, center=(ox, oy), resample=Image.BICUBIC)
        a = ImageChops.offset(a, int(lado * tam * .42 * k), int(-tam * .24 * k))
        return a
    for lado in (-1, 1):
        m = alca(lado)
        g = ouro(L.size[0], L.size[1]).convert('RGBA')
        sh = m.filter(ImageFilter.GaussianBlur(k * 3))
        L.paste((120, 80, 10, 255), (0, 0), ImageChops.offset(sh, 0, k * 4).point(lambda v: v * .5))
        L.paste(g, (0, 0), m)
        # contorno escuro
        cont = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(5)), m)
        L.paste((150, 100, 20, 255), (0, 0), cont)
    # nó
    d = ImageDraw.Draw(L)
    r = tam * .2 * k
    no = Image.new('L', L.size, 0); ImageDraw.Draw(no).ellipse([ox - r, oy - r * 1.1, ox + r, oy + r * .9], fill=255)
    L.paste(ouro(L.size[0], L.size[1]).convert('RGBA'), (0, 0), no)
    hl = Image.new('L', L.size, 0); ImageDraw.Draw(hl).ellipse([ox - r * .5, oy - r * .8, ox, oy - r * .3], fill=170)
    L.paste((255, 250, 220, 255), (0, 0), hl.filter(ImageFilter.GaussianBlur(k * 2)))
    L = L.resize((L.size[0] // k, L.size[1] // k), Image.LANCZOS)
    canvas.alpha_composite(L, (int(cx - L.size[0] / 2), int(cy - L.size[1] * .68)))


def brilhos(canvas, n, area, seed, tam=(6, 20), cor=(255, 230, 150)):
    rnd = random.Random(seed)
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = area
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1); s = rnd.uniform(*tam) * S
        a = rnd.randint(150, 255)
        d.polygon([(x, y - s), (x + s * .22, y - s * .22), (x + s, y), (x + s * .22, y + s * .22), (x, y + s), (x - s * .22, y + s * .22), (x - s, y), (x - s * .22, y - s * .22)], fill=cor + (a,))
    glow = lay.filter(ImageFilter.GaussianBlur(S * 4))
    canvas.alpha_composite(glow); canvas.alpha_composite(lay)


def fundo(seed=0, cx=.5, cy=.45):
    yy, xx = np.mgrid[0:W, 0:W] / W
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    base = np.array([10, 20, 16]); meio = np.array([22, 96, 58])
    t = np.clip(1 - r / .62, 0, 1) ** 1.6
    a = base * (1 - t[..., None]) + meio * t[..., None]
    img = Image.fromarray(a.clip(0, 255).astype('uint8')).convert('RGBA')
    # '?' flutuando bem apagados
    rnd = random.Random(seed)
    lay = Image.new('L', img.size, 0); d = ImageDraw.Draw(lay)
    for _ in range(14):
        s = rnd.randint(50, 130) * S
        f = ImageFont.truetype(FONTE, s)
        x, y = rnd.uniform(0, W), rnd.uniform(0, W)
        if abs(x / W - cx) < .28 and abs(y / W - cy) < .3: continue
        d.text((x, y), '?', font=f, fill=rnd.randint(18, 40), anchor='mm')
    img.paste((63, 208, 126, 255), (0, 0), lay.filter(ImageFilter.GaussianBlur(S * 1.5)))
    return img


def raios(canvas, origem, alvo_ang, abertura, alcance, alfa=120, n=9, seed=4):
    rnd = random.Random(seed)
    lay = Image.new('L', canvas.size, 0); d = ImageDraw.Draw(lay)
    ox, oy = origem
    for i in range(n):
        ang = alvo_ang + (i / (n - 1) - .5) * abertura + rnd.uniform(-.04, .04)
        lw = rnd.uniform(.03, .07)
        p1 = (ox + math.cos(ang - lw) * alcance, oy + math.sin(ang - lw) * alcance)
        p2 = (ox + math.cos(ang + lw) * alcance, oy + math.sin(ang + lw) * alcance)
        d.polygon([(ox, oy), p1, p2], fill=rnd.randint(int(alfa * .5), alfa))
    # some com a distância
    yy, xx = np.mgrid[0:canvas.size[1], 0:canvas.size[0]]
    fade = np.clip(1 - np.sqrt((xx - ox) ** 2 + (yy - oy) ** 2) / alcance, 0, 1)
    m = (np.asarray(lay).astype(float) * fade).astype('uint8')
    m = Image.fromarray(m).filter(ImageFilter.GaussianBlur(S * 6))
    canvas.paste((255, 228, 140, 255), (0, 0), m) if False else canvas.alpha_composite(Image.merge('RGBA', [Image.new('L', canvas.size, 255), Image.new('L', canvas.size, 228), Image.new('L', canvas.size, 140), m]))


def brilho_redondo(canvas, c, raio, cor=(255, 225, 130), alfa=200):
    lay = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(lay).ellipse([c[0] - raio, c[1] - raio, c[0] + raio, c[1] + raio], fill=alfa)
    lay = lay.filter(ImageFilter.GaussianBlur(raio * .5))
    canvas.alpha_composite(Image.merge('RGBA', [Image.new('L', canvas.size, v) for v in cor] + [lay]))


def sombra_chao(canvas, cx, cy, rx, ry, alfa=170):
    lay = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(lay).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=alfa)
    lay = lay.filter(ImageFilter.GaussianBlur(ry * .6))
    canvas.alpha_composite(Image.merge('RGBA', [Image.new('L', canvas.size, 0)] * 3 + [lay]))


def titulo(canvas, texto, y, tam, cor=(255, 255, 255), sub=None):
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(FONTE, tam * S)
    sh = Image.new('L', canvas.size, 0); ImageDraw.Draw(sh).text((W // 2, y), texto, font=f, anchor='mm', fill=200)
    canvas.alpha_composite(Image.merge('RGBA', [Image.new('L', canvas.size, 0)] * 3 + [sh.filter(ImageFilter.GaussianBlur(S * 6))]))
    d.text((W // 2, y), texto, font=f, anchor='mm', fill=cor)


# ---------- montagem da caixa ----------
TEX_F = face_frente(1000, 800)
TEX_F_ABERTA = face_frente(1000, 800, faixa_tampa=False, fita=False)
TEX_L = face_frente(800, 800, escuro=.72, fita=True, seed=2)
TEX_T = face_topo(1000, 800)
TEX_IN = face_dentro(1000, 800)
TEX_L_ABERTA = face_frente(800, 800, escuro=.72, faixa_tampa=False, fita=False, seed=2)


def lerp(p, q, t): return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def caixa(canvas, F, T, L, lado='dir', aberta=False, tampa_dy=0, tampa_rot=0, laco_tam=None):
    """F: frente (TL,TR,BR,BL). T: topo (TL atrás-esq, TR atrás-dir, BR=frente-dir, BL=frente-esq). L: lateral visível (TL,TR,BR,BL)."""
    colar_quad(canvas, TEX_L_ABERTA if aberta else TEX_L, L, luz=.95)
    colar_quad(canvas, TEX_F_ABERTA if aberta else TEX_F, F)
    if not aberta:
        colar_quad(canvas, TEX_T, T, luz=1.08)
    else:
        colar_quad(canvas, TEX_IN, T)
    # arestas de luz
    aresta(canvas, F[0], F[1]); aresta(canvas, F[0], F[3], cor=(150, 240, 190, 90))
    if lado == 'dir': aresta(canvas, F[1], F[2], cor=(160, 245, 200, 110))
    else: aresta(canvas, F[0], F[3], cor=(160, 245, 200, 110))
    if not aberta:
        aresta(canvas, T[0], T[1], cor=(200, 255, 220, 120))
        cx = sum(p[0] for p in T) / 4; cy = sum(p[1] for p in T) / 4
        laco(canvas, cx, cy, laco_tam or abs(F[1][0] - F[0][0]) * .42)
    else:
        # tampa solta no ar: topo + faixa da frente (20% da altura)
        h = .2
        fb = [F[0], F[1], lerp(F[1], F[2], h), lerp(F[0], F[3], h)]
        lb = [L[0], L[1], lerp(L[1], L[2], h), lerp(L[0], L[3], h)]
        cxm = sum(p[0] for p in T) / 4; cym = sum(p[1] for p in T) / 4
        ang = math.radians(tampa_rot)
        def mv(p):
            x, y = p[0] - cxm, p[1] - cym
            return (cxm + x * math.cos(ang) - y * math.sin(ang), cym + x * math.sin(ang) + y * math.cos(ang) - tampa_dy)
        lid = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        tf = Image.new('RGB', (1000, 160)); tf.paste(TEX_F.crop((0, 0, 1000, 160)))
        tl = Image.new('RGB', (800, 160)); tl.paste(TEX_L.crop((0, 0, 800, 160)))
        colar_quad(lid, tl, [mv(p) for p in lb], luz=.95)
        colar_quad(lid, tf, [mv(p) for p in fb])
        colar_quad(lid, TEX_T, [mv(p) for p in T], luz=1.08)
        aresta(lid, mv(F[0]), mv(F[1]))
        aresta(lid, mv(T[0]), mv(T[1]), cor=(200, 255, 220, 120))
        tc = mv((cxm, cym))
        laco(lid, tc[0], tc[1], laco_tam or abs(F[1][0] - F[0][0]) * .42)
        sh = lid.getchannel('A').filter(ImageFilter.GaussianBlur(S * 10))
        return lid, sh
    return None, None


def projetar(dim, yaw, pitch, escala, centro, dist=6.0):
    w, h, d = dim
    pts = {}
    for nx, sx in (('l', -1), ('r', 1)):
        for ny, sy in (('b', -1), ('t', 1)):
            for nz, sz in (('k', -1), ('f', 1)):
                x, y, z = sx * w / 2, sy * h / 2, sz * d / 2
                x, z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)
                y, z = y * math.cos(pitch) - z * math.sin(pitch), y * math.sin(pitch) + z * math.cos(pitch)
                f = dist / (dist - z)
                pts[nx + ny + nz] = (centro[0] + x * f * escala, centro[1] - y * f * escala)
    return pts


def caixa_3d(canvas, dim, yaw, pitch, escala, centro):
    p = projetar(dim, yaw, pitch, escala, centro)
    F = [p['ltf'], p['rtf'], p['rbf'], p['lbf']]
    T = [p['ltk'], p['rtk'], p['rtf'], p['ltf']]
    if yaw < 0:  # gira para mostrar a lateral direita
        L = [p['rtf'], p['rtk'], p['rbk'], p['rbf']]; lado = 'dir'
    else:
        L = [p['ltk'], p['ltf'], p['lbf'], p['lbk']]; lado = 'esq'
    caixa(canvas, F, T, L, lado=lado)
    return p


def leiloeiro():
    im = Image.open(RECORTE).convert('RGBA')
    k = 1.5 * S
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    off = ((W - im.width) // 2, W - im.height)
    return im, k, off


MAO = [(330, 489), (324, 495), (325, 505), (331, 516), (338, 523), (343, 530), (330, 540), (318, 547), (308, 552), (303, 558),
       (302, 567), (306, 572), (304, 580), (305, 590), (310, 597), (320, 604), (345, 612), (430, 640), (430, 470), (352, 485), (345, 488), (338, 487)]


def arte_leiloeiro(aberta, nome):
    can = fundo(seed=7 if not aberta else 9, cy=.5)
    per, k, off = leiloeiro()
    if aberta:
        brilho_redondo(can, (off[0] + 210 * k, off[1] + 410 * k), 230 * k * .9, alfa=120)
        raios(can, (off[0] + 205 * k, off[1] + 420 * k), -math.pi / 2, 2.6, 520 * k, alfa=210, n=13)
    can.alpha_composite(per, off)
    tp = lambda p: (off[0] + p[0] * k, off[1] + p[1] * k)
    e = 1.5
    F = [tp((62 - e, 430 - e)), tp((265 + e, 452 - e)), tp((267 + e, 612 + e)), tp((63 - e, 592 + e))]
    T = [tp((150 - e, 398 - e)), tp((352 + e, 417 - e)), F[1], F[0]]
    L = [F[1], T[1], tp((351 + e, 577)), F[2]]
    caixa_lay = Image.new('RGBA', can.size, (0, 0, 0, 0))
    lid, lid_sh = caixa(caixa_lay, F, T, L, aberta=aberta, tampa_dy=78 * k, tampa_rot=-10, laco_tam=105 * k)
    can.alpha_composite(caixa_lay)
    # a mão direita dele volta por cima da caixa
    m = Image.new('L', can.size, 0); ImageDraw.Draw(m).polygon([tp(p) for p in MAO], fill=255)
    m = ImageChops.multiply(m.filter(ImageFilter.GaussianBlur(S * .8)), Image.new('L', can.size, 0).__class__.paste(Image.new('L', can.size, 0), 0) or Image.new('L', can.size, 255)) if False else m.filter(ImageFilter.GaussianBlur(S * .8))
    mao = Image.new('RGBA', can.size, (0, 0, 0, 0)); mao.alpha_composite(per, off)
    a = ImageChops.multiply(mao.getchannel('A'), m); mao.putalpha(a)
    can.alpha_composite(mao)
    if aberta:
        boca = (sum(p[0] for p in T) / 4, sum(p[1] for p in T) / 4)
        raios(can, boca, -math.pi / 2, 1.4, 90 * k, alfa=170)
        brilho_redondo(can, boca, 85 * k, alfa=255)
        brilho_redondo(can, boca, 40 * k, cor=(255, 250, 225), alfa=255)
        sombra = Image.merge('RGBA', [Image.new('L', can.size, 0)] * 3 + [ImageChops.offset(lid_sh, 0, int(18 * k)).point(lambda v: v * .45)])
        can.alpha_composite(sombra)
        can.alpha_composite(lid)
        brilhos(can, 34, (off[0] + 20 * k, off[1] + 300 * k, off[0] + 540 * k, off[1] + 470 * k), 11, tam=(5, 16))
        # '?' saindo da caixa
        q = Image.new('RGB', can.size, (0, 0, 0)); qm = Image.new('L', can.size, 0)
        for (dx, dy, t, rot) in [(-165, -30, 70, -18), (175, -20, 56, 16), (-130, -120, 44, -10), (215, -100, 38, 14)]:
            lay = Image.new('RGB', (int(t * k * 1.6),) * 2, (0, 0, 0))
            interrogacao(lay, lay.width // 2, lay.height // 2, int(t * k))
            mk = Image.new('L', lay.size, 0); ImageDraw.Draw(mk).text((lay.width // 2, lay.height // 2), '?', font=ImageFont.truetype(FONTE, int(t * k)), anchor='mm', fill=255)
            mk = mk.filter(ImageFilter.MaxFilter(max(3, int(t * k * .035) | 1) + 2))
            lay = lay.rotate(rot, resample=Image.BICUBIC); mk = mk.rotate(rot, resample=Image.BICUBIC)
            pos = (int(boca[0] + dx * k - lay.width / 2), int(boca[1] + dy * k - lay.height / 2))
            rr = lay.convert('RGBA'); rr.putalpha(mk); can.alpha_composite(rr, pos)
    else:
        brilhos(can, 18, (60 * S, 120 * S, W - 60 * S, W - 200 * S), 5, tam=(4, 12))
    can.convert('RGB').resize((1080, 1080), Image.LANCZOS).save(f'{OUT}/{nome}', quality=93)


def arte_caixa(nome, yaw, pitch, escala, centro, texto, sub, seed):
    can = fundo(seed=seed, cy=centro[1] / W)
    # palco / spot de luz
    spot = Image.new('L', can.size, 0)
    ImageDraw.Draw(spot).polygon([(centro[0] - 120 * S, 0), (centro[0] + 120 * S, 0), (centro[0] + 420 * S, W), (centro[0] - 420 * S, W)], fill=55)
    can.alpha_composite(Image.merge('RGBA', [Image.new('L', can.size, v) for v in (200, 255, 220)] + [spot.filter(ImageFilter.GaussianBlur(40 * S))]))
    brilho_redondo(can, (centro[0], centro[1]), 330 * S, cor=(60, 210, 130), alfa=90)
    p = projetar((1.0, .78, 1.0), yaw, pitch, escala, centro)
    base_y = max(p['lbf'][1], p['rbf'][1], p['lbk'][1], p['rbk'][1])
    sombra_chao(can, centro[0], base_y + 4 * S, escala * .78, escala * .12, alfa=200)
    caixa_3d(can, (1.0, .78, 1.0), yaw, pitch, escala, centro)
    brilhos(can, 26, (90 * S, 160 * S, W - 90 * S, W - 140 * S), seed + 1)
    if texto:
        titulo(can, texto, 96 * S, 74)
    if sub:
        d = ImageDraw.Draw(can); f = ImageFont.truetype(FONTE_B, 40 * S)
        d.text((W // 2, W - 78 * S), sub, font=f, anchor='mm', fill=(245, 196, 81))
    can.convert('RGB').resize((1080, 1080), Image.LANCZOS).save(f'{OUT}/{nome}', quality=93)


if __name__ == '__main__':
    qual = sys.argv[2] if len(sys.argv) > 2 else 'todas'
    if qual in ('1', 'todas'): arte_leiloeiro(False, '1-leiloeiro-segurando.jpg')
    if qual in ('2', 'todas'): arte_caixa('2-caixa.jpg', -0.55, 0.42, 470 * S, (W // 2, 590 * S), 'CAIXA MISTERIOSA', 'Um produto surpresa para quem arrematar', 21)
    if qual in ('3', 'todas'): arte_caixa('3-caixa.jpg', 0.5, 0.3, 520 * S, (W // 2, 600 * S), 'O QUE TEM DENTRO?', 'Só quem arrematar vai saber', 31)
    if qual in ('4', 'todas'): arte_leiloeiro(True, '4-leiloeiro-abrindo.jpg')
