# Estilo "vitrine limpa" (referência Mercado Livre, 04/11): fundo de UMA cor, produto real recortado e grande,
# no máximo 2 frases curtas, preço como herói. Ouro da marca + verde-escuro (o par equivalente ao amarelo+azul deles).
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from kit import logo, salvar
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
OUT = '/home/user/Leil-onozaplivoo/marketing/marca/estilo-vitrine/exemplos'
W, H = 1080, 1350
F = lambda p, t: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/InterDisplay-{p}.otf', t)
OURO = (245, 196, 81); VERDE = (10, 61, 38); VERDE2 = (27, 122, 72); AREIA = (246, 239, 226); MENTA = (214, 236, 221)

def prod(nome, alt, sombra=True):
    p = Image.open(f'{I}/{nome}').convert('RGBA'); p = p.crop(p.getbbox())
    return p.resize((int(p.width * alt / p.height), alt), Image.LANCZOS)
def pousa(b, p, x, y_base, forca=90):
    s = Image.new('RGBA', b.size); ImageDraw.Draw(s).ellipse((x + p.width * .08, y_base - 16, x + p.width * .92, y_base + 16), fill=(0, 0, 0, forca))
    b.alpha_composite(s.filter(ImageFilter.GaussianBlur(18))); b.alpha_composite(p, (int(x), int(y_base - p.height)))
def marca_dagua(b, txt, cor):
    m = Image.new('RGBA', b.size); d = ImageDraw.Draw(m); f = F('Black', 330)
    for k, t in enumerate(txt): d.text((W / 2, 120 + k * 330), t, font=f, fill=cor + (22,), anchor='mt')
    b.alpha_composite(m)

# 1 · carrossel em 2 metades ("o que eu queria" x "o que eu paguei")
def ex1():
    b = Image.new('RGBA', (W, H), OURO + (255,)); d = ImageDraw.Draw(b)
    d.line((0, H // 2, W, H // 2), fill=(255, 250, 235), width=8)
    d.text((70, 150), 'O que eu queria', font=F('Black', 64), fill=VERDE); d.text((70, 225), 'ganhar de Natal:', font=F('Medium', 64), fill=VERDE)
    pousa(b, prod('c-iphone.png', 540), 600, 640, 70)
    d = ImageDraw.Draw(b)
    d.text((W - 70, 870), 'Onde o lance', font=F('Black', 70), fill=VERDE, anchor='ra'); d.text((W - 70, 950), 'começa:', font=F('Medium', 70), fill=VERDE, anchor='ra')
    d.text((70, 1090), 'R$', font=F('Black', 70), fill=VERDE); d.text((175, 1035), '197', font=F('Black', 230), fill=VERDE)
    logo(b, y=1240, largura=170, x=W - 240); d = ImageDraw.Draw(b)
    d.text((70, 1290), 'iPhone 17 Pro Max · sábado às 20h', font=F('SemiBold', 30), fill=VERDE)
    d.rounded_rectangle((W - 150, 40, W - 50, 96), 28, fill=(0, 0, 0, 60)); d.text((W - 100, 68), '1/5', font=F('SemiBold', 30), fill=(255, 255, 255), anchor='mm')
    salvar(b, f'{OUT}/1-carrossel-queria-x-paguei.jpg')

# 2 · número gigante como herói + 3 produtos em blocos (dia de leilões)
def ex2():
    b = Image.new('RGBA', (W, H), OURO + (255,)); marca_dagua(b, ['HOJE', 'TEM', 'LEILÃO'], VERDE); d = ImageDraw.Draw(b)
    d.text((W / 2, 130), 'ÀS QUINTAS', font=F('Black', 92), fill=VERDE, anchor='mt'); d.text((W / 2, 228), 'TEM 5 LEILÕES', font=F('Medium', 76), fill=VERDE, anchor='mt')
    # blocos (pódios lisos da mesma cor, um tom abaixo)
    def bloco(x0, x1, y0, y1):
        d.rectangle((x0, y0, x1, y1), fill=(228, 178, 64)); d.polygon([(x0, y0), (x0 + 40, y0 - 30), (x1 + 40, y0 - 30), (x1, y0)], fill=(250, 210, 110)); d.polygon([(x1, y0), (x1 + 40, y0 - 30), (x1 + 40, y1 - 30), (x1, y1)], fill=(210, 160, 50))
    bloco(90, 420, 900, 1010); bloco(400, 720, 820, 1010); bloco(680, 990, 930, 1010)
    pousa(b, prod('c-headset.png', 380), 70, 905, 60); pousa(b, prod('c-relogio.png', 360), 450, 825, 60); pousa(b, prod('c-camera.png', 360), 770, 935, 60)
    d = ImageDraw.Draw(b)
    d.text((110, 1075), 'LANCE', font=F('Medium', 52), fill=VERDE); d.text((110, 1135), 'DESDE', font=F('Medium', 52), fill=VERDE)
    d.text((330, 1050), 'R$', font=F('Black', 80), fill=VERDE); d.text((450, 1015), '7,97', font=F('Black', 210), fill=VERDE)
    logo(b, y=1235, largura=160, x=W // 2 - 80); d = ImageDraw.Draw(b)
    # selo redondo
    d.ellipse((800, 330, 1010, 540), fill=MENTA); d.text((905, 405), 'É HOJE', font=F('Black', 40), fill=VERDE2, anchor='mm'); d.text((905, 460), '12H-20H', font=F('Black', 40), fill=VERDE2, anchor='mm')
    salvar(b, f'{OUT}/2-numero-heroi-5-leiloes.jpg')

# 3 · um produto, fundo areia, uma frase e o preço
def ex3():
    b = Image.new('RGBA', (W, H), AREIA + (255,)); d = ImageDraw.Draw(b); logo(b, y=60, largura=170, x=70); d = ImageDraw.Draw(b)
    d.text((70, 250), 'Cuidar de quem', font=F('Black', 80), fill=VERDE); d.text((70, 340), 'você ama', font=F('Medium', 80), fill=VERDE); d.text((70, 430), 'custa pouco.', font=F('Medium', 80), fill=VERDE2)
    pousa(b, prod('c-pressao2.png', 520), 330, 1060, 80)
    d = ImageDraw.Draw(b)
    d.text((70, 1120), 'Medidor de pressão de pulso', font=F('SemiBold', 36), fill=VERDE)
    d.text((70, 1170), 'lance desde', font=F('Medium', 40), fill=VERDE2); d.text((300, 1150), 'R$ 7,97', font=F('Black', 96), fill=VERDE)
    d.text((W - 70, 1290), 'martelo hoje às 12h', font=F('SemiBold', 30), fill=VERDE2, anchor='rm')
    salvar(b, f'{OUT}/3-um-produto-uma-frase.jpg')

ex1(); ex2(); ex3(); print('ok')
