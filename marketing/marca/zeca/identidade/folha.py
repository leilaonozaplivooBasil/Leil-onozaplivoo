from PIL import Image, ImageDraw, ImageFont
foto=Image.open('foto-crua.png').convert('RGB')
hexa=lambda c:'#%02X%02X%02X'%c
polo=(111,191,166); luz=(253,206,107)
foto.resize((1080,1080),Image.LANCZOS).save('zeca-foto-oficial-1080.jpg',quality=95)
B='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; XB='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; SB='/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'; R='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
f=lambda p,s: ImageFont.truetype(p,s)
W,H=1800,2400
NOITE=(10,20,16); VERDE=(27,122,72); NEON=(63,208,126); OURO=(245,196,81); BR=(255,255,255); CINZA=(170,190,180); CARTAO=(18,34,27)
im=Image.new('RGB',(W,H),NOITE); d=ImageDraw.Draw(im)
d.text((90,80),'IDENTIDADE DO PERSONAGEM',font=f(XB,30),fill=NEON)
d.text((90,120),'ZECA',font=f(B,150),fill=BR)
d.text((90,290),'Executivo de vendas do Leilão NoZap · atende pelo WhatsApp, 24h',font=f(SB,38),fill=CINZA)
logo=Image.open('/home/user/leilonozap/public/brand/logo-horizontal-dark.png').convert('RGBA'); logo.thumbnail((380,140))
im.paste(logo,(W-90-logo.width,95),logo)
fg=foto.resize((820,820),Image.LANCZOS)
m=Image.new('L',fg.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,820,820],radius=40,fill=255)
im.paste(fg,(90,400),m)
d.text((90,1240),'Foto oficial (a do perfil do WhatsApp). O rosto nunca é alterado por IA.',font=f(R,26),fill=CINZA)
x0=980
def circulo(tam):
    c=foto.resize((tam,tam),Image.LANCZOS); mm=Image.new('L',(tam,tam),0); ImageDraw.Draw(mm).ellipse([0,0,tam,tam],fill=255); return c,mm
c,mm=circulo(330); im.paste(c,(x0,400),mm); d.text((x0+165,750),'perfil',font=f(R,24),fill=CINZA,anchor='mt')
c,mm=circulo(140); im.paste(c,(x0+400,420),mm); d.text((x0+470,575),'lista de conversas',font=f(R,22),fill=CINZA,anchor='mt')
c,mm=circulo(64); im.paste(c,(x0+438,640),mm); d.text((x0+470,715),'notificação',font=f(R,22),fill=CINZA,anchor='mt')
d.rounded_rectangle([x0,800,W-90,960],radius=24,fill=CARTAO)
c,mm=circulo(96); im.paste(c,(x0+30,832),mm)
d.text((x0+150,850),'Zeca • Leilão NoZap',font=f(XB,34),fill=BR)
d.text((x0+150,898),'Opa! Esse leilão fecha às 14h. Te mando o link?',font=f(R,27),fill=CINZA)
d.text((x0,1000),'CORES DELE',font=f(XB,28),fill=NEON)
cores=[(polo,'Polo verde-menta',hexa(polo)),(VERDE,'Verde da marca','#1B7A48'),(luz,'Luz quente','#FDCE6B'),(NOITE,'Noite (fundo)','#0A1410')]
for i,(cor,nome,hx) in enumerate(cores):
    x=x0+(i%2)*370; y=1050+(i//2)*100
    d.rounded_rectangle([x,y,x+76,y+76],radius=16,fill=cor,outline=(60,80,70),width=2)
    d.text((x+96,y+8),nome,font=f(SB,27),fill=BR); d.text((x+96,y+44),hx,font=f(R,24),fill=CINZA)
def bloco(x,y,w,titulo,linhas,cor=NEON):
    d.text((x,y),titulo,font=f(XB,30),fill=cor); y+=50
    for l in linhas:
        fonte=f(R,27); palavras=l.split(); atual=''; prim=True
        for p in palavras:
            t=(atual+' '+p).strip()
            if d.textlength(('• ' if prim else '   ')+t,font=fonte)>w and atual:
                d.text((x,y),('• ' if prim else '   ')+atual,font=fonte,fill=BR); y+=38; atual=p; prim=False
            else: atual=t
        d.text((x,y),('• ' if prim else '   ')+atual,font=fonte,fill=BR); y+=48
    return y
col=(W-180-60)//2; Y=1330
y1=bloco(90,Y,col,'O ROSTO (para nunca errar)',['Homem brasileiro, uns 32 a 38 anos, pele morena.','Cabelo preto, curto e crespo, mais baixo nas laterais.','Barba curta e rente, desenhando o queixo, com bigode.','Sorriso largo e aberto, mostrando os dentes; olhos castanhos.','Selfie de celular, de frente, rosto no centro, olhando para a câmera.'])
y2=bloco(90+col+60,Y,col,'A ROUPA E O CENÁRIO',['Sempre camisa polo verde-menta, gola aberta, sem logo.','Escritório aconchegante: estante preta com livros coloridos, planta, quadro "Sonhe, Planeje, Conquiste".','Luminária de chão acesa atrás: luz quente, cor dourada.','Nunca terno, nunca boné, nunca fundo de estúdio branco.'])
y=max(y1,y2)+30
y3=bloco(90,y,col,'COMO ELE FALA',['Consultivo, brasileiro, direto e confiante: o melhor vendedor da casa, 24h.','2 a 4 linhas por mensagem, uma ideia e no máximo uma pergunta.','Sem formalidade, sem lista, sem "espero ter ajudado".','Responde com dado real: leilão, preço, prazo, saldo.'])
y4=bloco(90+col+60,y,col,'O QUE ELE NUNCA FAZ',['Nunca promete ganho; não usa "sorte", "aposta", "garantido".','Nunca pede senha ou código de acesso.','Não inventa preço nem prazo: consulta antes.','Quando precisa de gente, chama o time (João, Beatriz ou Luiz).'],cor=OURO)
y=max(y3,y4)+20
d.line([(90,y),(W-90,y)],fill=(40,60,50),width=2); y+=30
d.text((90,y),'ONDE ELE APARECE',font=f(XB,30),fill=NEON); y+=50
d.text((90,y),'Foto de perfil do WhatsApp · painel "Conversas do Zeca" no CRM · chamadas "Chama o Zeca no WhatsApp" em posts e no site',font=f(R,27),fill=BR)
d.text((90,H-70),'Leilão NoZap · identidade do Zeca · outubro de 2026',font=f(R,22),fill=(110,130,120))
im.save('zeca-identidade.png',optimize=True); im.convert('RGB').save('zeca-identidade.pdf',resolution=150)
