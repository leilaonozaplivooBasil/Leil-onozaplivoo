# Contagem regressiva do PS5 (sáb 14/11, martelo 20h) no estilo "elite": verde-escuro + dourado, letra fina, pouco texto.
# 6 artes, uma ideia diferente por horário: 10h HOJE · 14h 6 HORAS · 18h AQUECE O CONTROLE · 19h 60 MINUTOS · 19h50 ÚLTIMOS 10 · 20h É AGORA.
# Reaproveita os ajudantes de artes_elite.py. Uso: artes_contagem.py <pasta_saida> <lance> <n_pessoas> [só: 10h,14h,...]
import sys, os, math
F0 = os.path.dirname(os.path.abspath(__file__))
exec(open(f'{F0}/artes_elite.py').read().split('# ---------- 1) MONOLITO')[0])
SO = sys.argv[4].split(',') if len(sys.argv) > 4 else None
def rodape(b, y=1700, sub=None):
    ouro_txt(b, (W/2, y), f'lance atual  R$ {real(LANCE)}', F('Regular', 42), glow=0.2)
    texto(b, (W/2, y + 62), espac(sub or f'{NP} PESSOAS NA DISPUTA', 1), F('Light', 24), (196, 200, 190))
    logo(b, y + 105, 160)
def topo(b, t, y=170):
    texto(b, (W/2, y), espac(t, 1), F('Light', 30), OCLARO); linha_ouro(b, W/2-60, W/2+60, y + 38, 220)
def salva(b, nome): b.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=95); print('ok', nome)
def quer(h): return SO is None or h in SO
caixa = tom_quente(foto('ps5-caixa')); caixa = caixa.crop(caixa.getbbox())
# 10h — HOJE.
if quer('10h'):
    b = fundo(cy=H*0.62)
    cone = Image.new('RGBA', (W, H)); ImageDraw.Draw(cone).polygon([(W/2-50, -20), (W/2+50, -20), (W/2+300, 1500), (W/2-300, 1500)], fill=OCLARO+(40,)); b.alpha_composite(cone.filter(ImageFilter.GaussianBlur(45)))
    poeira(b, 45, 21); topo(b, 'SÁBADO É DIA DE LEILÃO')
    texto(b, (W/2, 470), 'Hoje.', F('Thin', 260), (244, 240, 230))
    ouro_txt(b, (W/2, 650), 'às 20h', F('ExtraLight', 110), glow=0.3)
    c = console.resize((round(console.width*700/console.height), 700), Image.LANCZOS); poe(b, c, W/2, 1500, 0.2); linha_ouro(b, 170, W-170, 1502, 150)
    rodape(b, 1640, f'A DISPUTA JÁ COMEÇOU · {NP} PESSOAS'); salva(b, 'PS5-HOJE-1-10h-hoje')
# 14h — 6 HORAS (anel de relógio fino, 6 de 12 marcas acesas)
if quer('14h'):
    b = fundo(cy=H*0.42); poeira(b, 40, 22); topo(b, 'O MARTELO BATE EM')
    CX, CY, R = W/2, 760, 330; an = Image.new('RGBA', (W, H)); da = ImageDraw.Draw(an)
    da.ellipse((CX-R, CY-R, CX+R, CY+R), outline=OURO+(60,), width=2)
    da.arc((CX-R, CY-R, CX+R, CY+R), -90, 90, fill=OURO+(230,), width=4)
    for i in range(12):
        a_ = math.radians(i*30-90); r1 = R-30; on = i < 6
        da.line((CX+r1*math.cos(a_), CY+r1*math.sin(a_), CX+(R-8)*math.cos(a_), CY+(R-8)*math.sin(a_)), fill=(OCLARO if on else OURO)+((240 if on else 90),), width=4 if on else 2)
    b.alpha_composite(an.filter(ImageFilter.GaussianBlur(6))); b.alpha_composite(an)
    ouro_txt(b, (CX, CY-40), '6', F('Thin', 360), glow=0.4)
    texto(b, (CX, CY+170), espac('HORAS', 2), F('Light', 40), (236, 232, 222))
    c = console.resize((round(console.width*430/console.height), 430), Image.LANCZOS); poe(b, c, W/2, 1540, 0.2); linha_ouro(b, 260, W-260, 1542, 140)
    rodape(b, 1650); salva(b, 'PS5-HOJE-2-14h-6-horas')
# 18h — AQUECE O CONTROLE (foto de estúdio do controle)
if quer('18h'):
    est = Image.open(f'{F0}/fotos/controle-estudio-gamma.jpg').convert('RGB'); r_ = max(W/est.width, H/est.height)
    est = est.resize((round(est.width*r_), round(est.height*r_)), Image.LANCZOS); xo, yo = (est.width-W)//2, (est.height-H)//2
    b = est.crop((xo, yo+40, xo+W, yo+H+40)).convert('RGBA'); poeira(b, 35, 23)
    topo(b, 'FALTAM 2 HORAS', 200)
    texto(b, (W/2, 400), 'Aquece', F('Thin', 170), (244, 240, 230))
    ouro_txt(b, (W/2, 560), 'o controle.', F('ExtraLight', 140), glow=0.3)
    rodape(b, 1650); salva(b, 'PS5-HOJE-3-18h-aquece-o-controle')
# 19h — 60 MINUTOS (número fino gigante atrás do console)
if quer('19h'):
    b = fundo(cy=H*0.5); brilho(b, (W/2-480, 380, W/2+480, 1300), (24, 90, 56), 200, 160); poeira(b, 40, 24)
    topo(b, 'O MARTELO BATE EM')
    ouro_txt(b, (W/2, 600), '60', F('Thin', 560), glow=0.45)
    c = console.resize((round(console.width*720/console.height), 720), Image.LANCZOS); poe(b, c, W/2+20, 1440, 0.2); linha_ouro(b, 160, W-160, 1442, 150)
    texto(b, (W/2, 1550), 'minutos.', F('ThinItalic', 90), (240, 236, 226))
    rodape(b, 1650); salva(b, 'PS5-HOJE-4-19h-60-minutos')
# 19h50 — ÚLTIMOS 10 MINUTOS (editorial, alinhado à esquerda, console grande cortado à direita)
if quer('19h50'):
    b = fundo(cx=W*0.75, cy=H*0.5); brilho(b, (W*0.45, 500, W*1.2, 1500), (24, 90, 56), 190, 150); poeira(b, 35, 25)
    c = console.resize((round(console.width*1080/console.height), 1080), Image.LANCZOS); poe(b, c, int(W*0.56) + c.width/2, 1500, 0.15)
    sh = Image.new('RGBA', (W, H)); ImageDraw.Draw(sh).rectangle((0, 0, int(W*0.62), H), fill=(3, 9, 6, 120)); b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(80)))
    texto(b, (90, 230), espac('SÁBADO · 19H50', 1), F('Light', 30), OCLARO, anchor='lm'); linha_ouro(b, 90, 210, 268, 220)
    texto(b, (80, 470), 'Últimos', F('Thin', 150), (244, 240, 230), anchor='lm')
    ouro_txt(b, (80, 760), '10', F('Thin', 520), anchor='lm', glow=0.45)
    texto(b, (90, 1060), 'minutos.', F('ThinItalic', 110), (240, 236, 226), anchor='lm')
    texto(b, (90, 1200), 'Lance no fim estende o tempo.', F('Light', 34), (210, 214, 206), anchor='lm')
    texto(b, (90, 1250), 'Quem tem coragem, leva.', F('Light', 34), (210, 214, 206), anchor='lm')
    rodape(b, 1650); salva(b, 'PS5-HOJE-5-19h50-ultimos-10')
# 20h — É AGORA. (a caixa + console + controle, linha do horizonte dourada)
if quer('20h'):
    b = fundo(c1=(12, 38, 25), cy=H*0.55); brilho(b, (W/2-520, 1050, W/2+520, 1500), OURO, 60, 120); poeira(b, 60, 26)
    topo(b, '20H · AO VIVO')
    texto(b, (W/2, 440), 'É agora.', F('Thin', 210), (244, 240, 230))
    ouro_txt(b, (W/2, 610), 'o martelo vai bater', F('ExtraLight', 72), glow=0.3)
    cx_ = caixa.resize((960, round(caixa.height*960/caixa.width)), Image.LANCZOS); poe(b, cx_, W/2, 1430, 0.18); linha_ouro(b, 60, W-60, 1432, 170)
    rodape(b, 1640); salva(b, 'PS5-HOJE-6-20h-e-agora')
