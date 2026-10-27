# Peças prontas reaproveitadas na semana (stories 9:16 e feed 4:5), todas no molde do kit.py.
from PIL import ImageDraw
from kit import *

FW, FH = 1080, 1350


def real(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def foto(nome):
    return f'{AQUI}/{nome}'


def personagem(out, topo, quem, pose, titulo, sub, alt=860):
    b = fundo(brilho=(540, 820))
    logo(b)
    selo(b, topo, 330)
    p = (leila if quem == 'leila' else leiloeiro)(pose, alt)
    sombra(p, b, ((W - p.width) // 2, 1250 - p.height + 20))
    faixa(b, titulo, sub)
    salvar(b, out)


def overlay(out, previa, titulo, sub, topo, legenda):
    sob = sobreposicao(titulo, sub, topo=topo)
    salvar(sob, out)
    base = fundo()
    texto_rico(ImageDraw.Draw(base), (540, 760), legenda, fonte('Bold', 44), 760, cor=(150, 190, 165))
    base.alpha_composite(sob)
    salvar(base, previa)


def revela(out, topo, ft, titulo, sub):
    b = fundo(brilho=(420, 760))
    logo(b)
    selo(b, topo, 330)
    cartao_foto(b, foto(ft), (480, 430, 1010, 1190))
    p = leiloeiro('a-apresenta', 820)  # nunca espelhar: o colete tem o nome escrito
    sombra(p, b, (-70, 1240 - p.height))
    faixa(b, titulo, sub)
    salvar(b, out)


def enquete(out, guia, topo, ft, titulo, sub, texto_guia='COLE A ENQUETE AQUI'):
    def base():
        b = fundo(brilho=(540, 640))
        logo(b)
        if topo:
            selo(b, topo, 315, tam=30)
        cartao_foto(b, foto(ft), (190, 390, 890, 1000))
        faixa(b, titulo, sub)
        return b
    salvar(base(), out)
    g = base()
    d = ImageDraw.Draw(g)
    d.rounded_rectangle((150, 1030, 930, 1210), radius=30, outline=DOURADO, width=3)
    d.text((540, 1120), texto_guia, font=fonte('Black', 36), fill=DOURADO, anchor='mm')
    salvar(g, guia)


def resposta(out, topo, ft, produto, loja, pago, sub, pose='a-comemora'):
    b = fundo(brilho=(540, 700))
    logo(b)
    selo(b, topo, 330)
    cartao_foto(b, foto(ft), (70, 430, 600, 930))
    p = leiloeiro(pose, 720)
    sombra(p, b, (W - p.width + 40, 1240 - p.height))
    preco(b, (90, 955), 'Na loja', real(loja), cor_valor=(235, 235, 235), riscado=True, tam=60)
    preco(b, (90, 1075), 'Saiu por', real(pago), cor_valor=DOURADO, tam=86)
    faixa(b, produto, sub)
    salvar(b, out)


def _rodape(b, texto, caixa=(60, 1170, 1020, 1300), tam=44):
    d = ImageDraw.Draw(b)
    d.rounded_rectangle(caixa, radius=34, fill=VERDE_ESCURO, outline=DOURADO, width=3)
    texto_rico(d, ((caixa[0] + caixa[2]) / 2, (caixa[1] + caixa[3]) / 2), texto, fonte('Black', tam), caixa[2] - caixa[0] - 60)


def feed_foto(out, titulo, ft, rodape, tam=76):
    b = fundo(FW, FH, brilho=(540, 600))
    logo(b, y=60, largura=300)
    texto_rico(ImageDraw.Draw(b), (540, 300), titulo, fonte('Black', tam), 960)
    cartao_foto(b, foto(ft), (250, 450, 830, 1130))
    _rodape(b, rodape)
    salvar(b, out)


def feed_preco(out, titulo, ft, loja, pago, rodape):
    b = fundo(FW, FH, brilho=(300, 700))
    logo(b, y=60, largura=300)
    texto_rico(ImageDraw.Draw(b), (540, 260), titulo, fonte('Black', 70), 960)
    cartao_foto(b, foto(ft), (60, 400, 560, 1120))
    preco(b, (600, 520), 'Na loja', real(loja), cor_valor=(235, 235, 235), riscado=True, tam=58 if loja < 1000 else 52)
    preco(b, (600, 680), 'Saiu por', real(pago), cor_valor=DOURADO, tam=80 if pago < 1000 else 66)
    d = ImageDraw.Draw(b)
    off = round(100 * (1 - pago / loja))
    d.rounded_rectangle((610, 860, 1010, 960), radius=26, fill=DOURADO)
    d.text((810, 910), f'{off}% ABAIXO', font=fonte('Black', 50), fill=VERDE_ESCURO, anchor='mm')
    _rodape(b, rodape)
    salvar(b, out)


def feed_passos(out, titulo, passos, cta, quem='leiloeiro', pose='a-apresenta'):
    b = fundo(FW, FH, brilho=(780, 760))
    logo(b, y=60, largura=300)
    d = ImageDraw.Draw(b)
    texto_rico(d, (540, 270), titulo, fonte('Black', 72), 960)
    p = (leila if quem == 'leila' else leiloeiro)(pose, 760)
    sombra(p, b, (FW - p.width + 120, FH - p.height - 40))
    f = fonte('Black', 44)
    y = 450
    for n, t in enumerate(passos, 1):
        d.ellipse((70, y, 160, y + 90), fill=DOURADO)
        d.text((115, y + 45), str(n), font=fonte('Black', 54), fill=VERDE_ESCURO, anchor='mm')
        x = 190
        for w_ in t.split(' '):
            s = w_.replace('*', '') + ' '
            if x + d.textlength(s, font=f) > 600:
                x, y = 190, y + 54
            d.text((x, y + 18), s, font=f, fill=DOURADO if '*' in w_ else BRANCO)
            x += d.textlength(s, font=f)
        y += 190
    _rodape(b, cta, caixa=(60, 1170, 640, 1300), tam=50)
    salvar(b, out)


def feed_personagem(out, titulo, sub, quem, pose, rodape):
    b = fundo(FW, FH, brilho=(540, 760))
    logo(b, y=60, largura=300)
    d = ImageDraw.Draw(b)
    fim = texto_rico(d, (540, 290), titulo, fonte('Black', 78), 960)
    texto_rico(d, (540, fim + 40), sub, fonte('Bold', 40), 900, cor=VERDE_CLARO)
    p = (leila if quem == 'leila' else leiloeiro)(pose, 1140 - int(fim + 90))
    sombra(p, b, ((FW - p.width) // 2, 1160 - p.height))
    _rodape(b, rodape)
    salvar(b, out)
