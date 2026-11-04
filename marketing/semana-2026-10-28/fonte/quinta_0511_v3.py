# Quinta 05/11 v3: visual "anúncio 3D" (referência da Natália): cenário com pódio neon + produto REAL recortado,
# título grande com contorno e painel de lance embaixo. Cenários feitos por IA sem produto; o produto é a foto original.
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from kit import logo, fonte, salvar, DOURADO, VERDE_ESCURO, BRANCO
from pecas import real
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-05/quinta-05-11/feed-v3'
W, H = 1080, 1350
HORA = sys.argv[1] if len(sys.argv) > 1 else '8H'
LIMA = (150, 240, 90); NEON = (60, 220, 110)

def cena(nome): return Image.open(f'{I}/{nome}').convert('RGBA').resize((W, H), Image.LANCZOS)

def poe_produto(b, nome, cx, base_y, alt, brilho=NEON):
    p = Image.open(f'{I}/{nome}').convert('RGBA'); bb = p.getbbox(); p = p.crop(bb)
    p = p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
    x, y = int(cx - p.width / 2), int(base_y - p.height)
    a = p.split()[-1]
    g = Image.new('RGBA', (W, H)); gl = Image.new('RGBA', p.size, brilho + (255,)); gl.putalpha(a)
    g.alpha_composite(gl, (x, y)); g = g.filter(ImageFilter.GaussianBlur(28))
    g.putalpha(g.split()[-1].point(lambda v: min(255, int(v * 1.3))))
    b.alpha_composite(g)
    s = Image.new('RGBA', (W, H)); ImageDraw.Draw(s).ellipse((cx - p.width * .45, base_y - 22, cx + p.width * .45, base_y + 22), fill=(0, 0, 0, 200))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    b.alpha_composite(p, (x, y))

def titulo(b, linhas, y, tam=104, larg=1000):
    d = ImageDraw.Draw(b)
    for txt, cor in linhas:
        f = fonte('Black', tam)
        while d.textlength(txt, font=f) > larg: tam -= 4; f = fonte('Black', tam)
        sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).text((W / 2 + 6, y + 10), txt, font=f, fill=(0, 0, 0, 200), anchor='mt')
        b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(b)
        if cor == 'grad':
            m = Image.new('L', (W, H)); ImageDraw.Draw(m).text((W / 2, y), txt, font=f, fill=255, anchor='mt', stroke_width=0)
            gr = Image.new('RGBA', (W, H))
            gd = ImageDraw.Draw(gr)
            for yy in range(y, y + tam + 20):
                t = (yy - y) / (tam + 20); gd.line((0, yy, W, yy), fill=tuple(int(a + (c - a) * t) for a, c in zip((215, 255, 120), (40, 190, 90))) + (255,))
            d.text((W / 2, y), txt, font=f, fill=(0, 0, 0, 0), anchor='mt', stroke_width=7, stroke_fill=(6, 40, 20))
            b.alpha_composite(Image.composite(gr, Image.new('RGBA', (W, H), (0, 0, 0, 0)), m))
        else:
            d.text((W / 2, y), txt, font=f, fill=cor, anchor='mt', stroke_width=7, stroke_fill=(6, 40, 20))
        y += int(tam * 1.0)
    return y

def sub(b, txt, y, tam=42, cor=BRANCO):
    d = ImageDraw.Draw(b); d.text((W / 2, y), txt, font=fonte('Black', tam), fill=cor, anchor='mt', stroke_width=5, stroke_fill=(6, 40, 20))

def painel(b, nome, loja, lance, rotulo='Lance:', rodape=None, y0=1070):
    vid = Image.new('RGBA', (W, H)); vd = ImageDraw.Draw(vid)
    vd.rounded_rectangle((50, y0, W - 50, H - 40), 40, fill=(4, 22, 12, 225), outline=NEON + (255,), width=4)
    gl = vid.filter(ImageFilter.GaussianBlur(18)); b.alpha_composite(gl); b.alpha_composite(vid)
    d = ImageDraw.Draw(b)
    d.ellipse((90, y0 + 26, 140, y0 + 76), fill=NEON); d.line((103, y0 + 52, 113, y0 + 63, 129, y0 + 40), fill=BRANCO, width=6)
    d.text((158, y0 + 51), nome, font=fonte('Black', 40), fill=BRANCO, anchor='lm')
    f = fonte('Black', 92); d.text((90, y0 + 98), rotulo, font=fonte('Black', 64), fill=BRANCO)
    x = 90 + d.textlength(rotulo + ' ', font=fonte('Black', 64))
    d.text((x, y0 + 80), real(lance), font=f, fill=LIMA, stroke_width=3, stroke_fill=(6, 40, 20))
    d.text((90, y0 + 192), rodape or f'Na loja {real(loja)}  ·  martelo hoje às {HORA}', font=fonte('Bold', 34), fill=(205, 235, 214))

def logo_topo(b, y=36, pilula=False):
    if pilula:
        s_ = Image.new('RGBA', (W, H)); ImageDraw.Draw(s_).rounded_rectangle((395, y - 12, 685, y + 122), 34, fill=(6, 40, 20, 235)); b.alpha_composite(s_)
    logo(b, y=y, largura=250)

def a1():
    b = cena('s-luxo.png'); poe_produto(b, 'c-relogio.png', 540, 1010, 540, brilho=(235, 190, 90)); logo_topo(b)
    y = titulo(b, [('ELEGÂNCIA', BRANCO), ('NO PULSO', 'grad')], 175, 112); sub(b, 'achadinho do dia', y + 6, 40, DOURADO)
    painel(b, 'Relógio EYT ouro rosa', 108.75, 7.97); salvar(b, f'{OUT}/01-relogio.jpg')

def a2():
    b = cena('s-saude.png'); poe_produto(b, 'c-pressao2.png', 540, 1010, 430); logo_topo(b, pilula=True)
    y = titulo(b, [('CUIDE DE QUEM', BRANCO), ('VOCÊ AMA', 'grad')], 175, 104); sub(b, 'pressão medida em casa, sem fila', y + 6, 40)
    painel(b, 'Medidor de pressão de pulso', 56.21, 7.97); salvar(b, f'{OUT}/02-medidor-pressao.jpg')

def a3():
    b = cena('s-verde3.png'); poe_produto(b, 'c-camera.png', 540, 990, 560); logo_topo(b)
    y = titulo(b, [('ENXERGA ONDE', BRANCO), ('A MÃO NÃO ALCANÇA', 'grad')], 175, 100); sub(b, 'motor · ralo · parede', y + 6, 40, DOURADO)
    painel(b, 'Câmera endoscópica com LED', 96.84, 7.97); salvar(b, f'{OUT}/03-camera-endoscopica.jpg')

def a4():
    b = cena('s-pet.png'); poe_produto(b, 'c-tapete.png', 540, 965, 520, brilho=(255, 255, 255)); logo_topo(b, pilula=True)
    y = titulo(b, [('SEU PET', BRANCO), ('AGRADECE!', 'grad')], 175, 116); sub(b, '30 unidades · 60 x 60 cm', y + 6, 40)
    painel(b, 'Tapete higiênico pet', 68.71, 7.97); salvar(b, f'{OUT}/04-tapete-pet.jpg')

def a5():
    b = cena('s-gamer.png'); poe_produto(b, 'c-headset.png', 540, 975, 560, brilho=(230, 60, 60)); logo_topo(b)
    y = titulo(b, [('QUANTO VOCÊ', BRANCO), ('DARIA NELE?', 'grad')], 175, 112); sub(b, 'comenta seu lance aqui embaixo', y + 6, 40, DOURADO)
    painel(b, 'Headset gamer Flakes', 99.96, 7.97); salvar(b, f'{OUT}/05-headset-gamer.jpg')

def a6():
    b = cena('s-verde1.png'); poe_produto(b, 'c-iphone.png', 560, 1010, 560); logo_topo(b)
    y = titulo(b, [('SÁBADO TEM', BRANCO), ('iPHONE!', 'grad')], 175, 112); sub(b, 'o último saiu por R$ 4.640 no leilão de 24/10', y + 6, 36, DOURADO)
    painel(b, 'iPhone 17 Pro Max 256GB', 9464.78, 197, rotulo='Lance inicial:', rodape=f'Na loja {real(9464.78)}  ·  martelo sábado às 20h')
    salvar(b, f'{OUT}/06-sabado-iphone.jpg')

for f, h in ((a1, '12H'), (a2, '14H'), (a3, '16H'), (a4, '18H'), (a5, '20H'), (a6, '')):
    HORA = h; f()
print('ok')
