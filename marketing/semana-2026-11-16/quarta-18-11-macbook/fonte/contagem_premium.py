# Contagem do MacBook (qua 18/11) no estilo PREMIUM aprovado (dourado em degradê, MacBook herói, comparação de preço).
# 14h 6 HORAS · 17h FALTAM 2H PRO 1º LANCE · 18h30 ÚLTIMOS 30 MIN PRO 1º LANCE · 19h50 ÚLTIMOS 10 · 20h É AGORA
# Uso: contagem_premium.py <lance> [só: 14h,17h,...]
import os, sys
F0 = os.path.dirname(os.path.abspath(__file__))
src = open(f'{F0}/hoje_premium.py').read().split('b = fundo()\n# facho')[0]
sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:]; exec(src)
SO = sys.argv[2].split(',') if len(sys.argv) > 2 else None
AMA = (255, 210, 0)

def base_arte(topo, c_fundo=None):
    b = fundo()
    if c_fundo:
        t = Image.new('RGBA', (W, H), c_fundo + (110,)); b.alpha_composite(t)
    cone = Image.new('RGBA', (W, H)); ImageDraw.Draw(cone).polygon([(W / 2 - 60, -20), (W / 2 + 60, -20), (W / 2 + 420, 1260), (W / 2 - 420, 1260)], fill=OCLARO + (30,)); b.alpha_composite(cone.filter(ImageFilter.GaussianBlur(50)))
    lg = LOGO.copy(); lg.thumbnail((190, 190)); b.alpha_composite(lg, ((W - lg.width) // 2, 80)); d = ImageDraw.Draw(b)
    d.text((W / 2, 250), espac(topo), font=F('Medium', 32), fill=OCLARO, anchor='mm'); linha_ouro(b, W / 2 - 80, W / 2 + 80, 285); return b
def heroi(b, mw=620, base=1175):
    mm = MAC.resize((mw, int(MAC.height * mw / MAC.width)), Image.LANCZOS)
    brilho(b, (W / 2 - 480, base - 380, W / 2 + 480, base + 40), (120, 90, 220), 60, 110); brilho(b, (W / 2 - 520, base - 60, W / 2 + 520, base + 60), OURO, 80, 55)
    r = mm.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, mw, int(mm.height * .18))); gm = Image.linear_gradient('L').resize(r.size).point(lambda v: int((255 - v) * .22))
    r.putalpha(ImageChops.multiply(r.split()[3], gm)); b.alpha_composite(r, ((W - mw) // 2, base + 4)); b.alpha_composite(mm, ((W - mw) // 2, base - mm.height)); linha_ouro(b, 140, W - 140, base + 6, 170)
    ouro(b, (W / 2, 1245), 'MacBook Neo 13"', F('Bold', 60), glow=.2)
    ImageDraw.Draw(b).text((W / 2, 1305), 'Prateado  ·  Chip A18 Pro  ·  256GB  ·  novo e lacrado', font=F('Regular', 32), fill=CREME, anchor='mm')
def quadro_preco(b, y0=1370, sub='NO LEILÃO, O LANCE ESTÁ EM'):
    d = ImageDraw.Draw(b); d.rounded_rectangle((70, y0, W - 70, y0 + 330), 30, fill=(4, 20, 12, 235), outline=OURO, width=2)
    for i, (rot, val) in enumerate((('na Apple', 'R$ 8.499'), ('no Mercado Livre', 'a partir de R$ 6.099'))):
        cx = 70 + (W - 140) * (.27 + i * .46); d.text((cx, y0 + 50), rot, font=F('Medium', 30), fill=(170, 190, 178), anchor='mm'); d.text((cx, y0 + 98), val, font=F('Bold', 40 if i == 0 else 34), fill=BR, anchor='mm')
    linha_ouro(b, 130, W - 130, y0 + 145, 160); d.text((W / 2, y0 + 185), espac(sub), font=F('SemiBold', 28), fill=OCLARO, anchor='mm')
    fR, fN = F('Medium', 54), F('Black', 120); wr = d.textlength('R$ ', font=fR); wn = d.textlength(real(LANCE), font=fN); x0 = (W - wr - wn) / 2
    ouro(b, (x0, y0 + 305), 'R$', fR, anchor='ls', glow=0); ouro(b, (x0 + wr, y0 + 305), real(LANCE), fN, anchor='ls', glow=.35)
def tarja(b, t1, t2, y=1745, cor=VERM):
    d = ImageDraw.Draw(b); d.rounded_rectangle((70, y, W - 70, y + 100), 26, fill=cor)
    d.text((W / 2, y + 37), t1, font=F('Black', 46), fill=BR, anchor='mm'); d.text((W / 2, y + 80), t2, font=F('SemiBold', 28), fill=(255, 225, 225), anchor='mm')
def numero(b, n, rotulo, y_n=470, y_r=640):
    d = ImageDraw.Draw(b); ouro(b, (W / 2, y_n), n, F('Black', 260), glow=.45); d.text((W / 2 + 3, y_r + 6), rotulo, font=F('Black', 96), fill=(0, 0, 0, 150), anchor='mm'); d.text((W / 2, y_r), rotulo, font=F('Black', 96), fill=BR, anchor='mm')
def salva(b, n): b.convert('RGB').save(f'{OUT}/{n}.jpg', quality=95); print('ok', n)
def quer(h): return SO is None or h in SO

if quer('14h'):
    b = base_arte('O MARTELO BATE EM'); numero(b, '6', 'HORAS'); heroi(b); quadro_preco(b); tarja(b, '1º LANCE SÓ ATÉ AS 19H', 'depois disso, fica de fora'); salva(b, 'MAC-2-14h-faltam-6-horas-PREMIUM')
if quer('17h'):
    b = base_arte('ATENÇÃO À REGRA NOVA', (90, 10, 14)); d = ImageDraw.Draw(b)
    d.text((W / 2 + 3, 420 + 6), 'FALTAM 2 HORAS', font=F('Black', 120), fill=(0, 0, 0, 150), anchor='mm'); d.text((W / 2, 420), 'FALTAM 2 HORAS', font=F('Black', 120), fill=BR, anchor='mm')
    ouro(b, (W / 2, 565), 'pro seu 1º lance', F('Bold', 92), glow=.4); heroi(b); quadro_preco(b)
    tarja(b, 'ATÉ AS 19H OU FICA DE FORA', 'quem já deu lance segue até as 20h'); salva(b, 'MAC-3-17h-faltam-2h-pro-1o-lance-PREMIUM')
if quer('18h30'):
    b = base_arte('ÚLTIMA CHAMADA PRO 1º LANCE', (110, 10, 14)); numero(b, '30', 'MINUTOS'); heroi(b); quadro_preco(b)
    tarja(b, 'ÀS 19H FECHA A ENTRADA', 'deu lance até lá? continua até as 20h'); salva(b, 'MAC-4-18h30-ultimos-30-pro-1o-lance-PREMIUM')
if quer('19h50'):
    b = base_arte('RETA FINAL'); numero(b, '10', 'MINUTOS'); heroi(b); quadro_preco(b, sub='O LANCE AGORA ESTÁ EM')
    tarja(b, 'O MARTELO BATE ÀS 20H', 'quem já deu lance ainda pode cobrir', cor=(27, 122, 72)); salva(b, 'MAC-5-19h50-ultimos-10-PREMIUM')
if quer('20h'):
    b = base_arte('O MARTELO VAI BATER'); d = ImageDraw.Draw(b)
    d.text((W / 2 + 4, 440 + 8), 'É AGORA!', font=F('Black', 200), fill=(0, 0, 0, 160), anchor='mm'); d.text((W / 2, 440), 'É AGORA!', font=F('Black', 200), fill=BR, anchor='mm')
    ouro(b, (W / 2, 590), 'últimos segundos', F('Bold', 90), glow=.4); heroi(b); quadro_preco(b, sub='O LANCE AGORA ESTÁ EM')
    tarja(b, 'QUEM DÁ MAIS?', 'acompanhe ao vivo no site', cor=(27, 122, 72)); salva(b, 'MAC-6-20h-e-agora-PREMIUM')
