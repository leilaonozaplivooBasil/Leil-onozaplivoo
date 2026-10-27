# Monta o roteiro de execução do dia (HTML → PDF), com miniatura de cada arte.
# Uso: python3 roteiro.py quarta   (lê o dicionário DIAS abaixo)
import base64, io, os, sys, json, subprocess
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
LINK_MAQUINA = 'leilaonozap.net/l/ec5e411ecba76f35dcea347b'

COMO_COLAR = ('Como pôr a FAIXA por cima do vídeo: grave o vídeo pelo Instagram, toque no ícone de figurinha, '
              'escolha a figurinha de FOTO (o quadradinho da galeria) e pegue o arquivo da faixa. Estique com dois dedos '
              'até cobrir a tela toda: a faixa cai sozinha no lugar certo. No iPhone dá também para copiar a imagem na '
              'galeria e colar direto no stories.')

DIAS = {
    'quarta': {
        'titulo': 'Quarta 28/10 — Leilão da máquina de lavar',
        'pasta': 'quarta-28-10',
        'resumo': 'Martelo às 18h. Lance atual na terça à noite: R$ 500 (subindo de R$ 50 em R$ 50). Na loja: R$ 904,62.',
        'itens': [
            dict(hora='05h00', quem='EQUIPE grava', arquivo='stories/01-05h00-praia-FAIXA-cole-no-video.png',
                 previa='previas/01-05h00-praia-NATALIA-como-fica.jpg',
                 gravar='10 a 12 segundos, celular em pé (selfie), a Natália correndo na areia com o sol nascendo atrás. Rosto já no primeiro segundo.',
                 falar='"Bom dia, família NoZap! Eu sou a Natália, da equipe do Leilão NoZap, e já tô aquecendo pro leilão de hoje. Às 10h o Leiloeiro revela o produto. Vamos com tudo!"',
                 figurinha='LEGENDAS (a figurinha que escreve sozinha o que você fala), no alto da tela. A FAIXA vai por cima do vídeo.'),
            dict(hora='05h01', quem='ARTE PRONTA', arquivo='stories/02-05h01-leiloeiro-bom-dia.jpg',
                 falar='Nada. A arte já fala sozinha.',
                 figurinha='CONTAGEM REGRESSIVA. Nome: "Martelo da máquina de lavar". Termina: quarta 28/10 às 18:00. Cole logo abaixo da faixa verde.'),
            dict(hora='10h00', quem='ARTE PRONTA', arquivo='stories/03-10h00-leiloeiro-revela.jpg',
                 falar='Nada.',
                 figurinha=f'LINK: {LINK_MAQUINA} — texto do link: DAR MEU LANCE. Cole logo abaixo da faixa verde.'),
            dict(hora='10h01', quem='ARTE PRONTA', arquivo='stories/04-10h01-enquete.jpg',
                 previa='previas/04-10h01-enquete-onde-colar.jpg',
                 falar='Nada.',
                 figurinha='ENQUETE: "Quanto você daria?" — opções: Até R$ 600 / R$ 600 a 700 / R$ 700 a 800 / Mais de R$ 800. Cole no espaço vazio entre a foto e a faixa (veja a prévia).'),
            dict(hora='12h00', quem='FEED (carrossel)', arquivo='feed/feed-12h-card1.jpg', arquivo2='feed/feed-12h-card2.jpg',
                 falar='Legenda pronta (copiar e colar):',
                 legenda='Quanto você daria nessa máquina de lavar? 🤔\n\nPanasonic 15 kg, novinha de fábrica. Na loja: R$ 904,62.\nAqui quem decide o preço é você: o martelo bate HOJE às 18h.\n\nComenta QUARTA que eu te mando o link do lance no direct 🔨\n\n#leilaonozap #leilaoonline #maquinadelavar #consumointeligente #riodejaneiro',
                 figurinha='Depois de publicar, compartilhe o post nos stories com a figurinha de LINK do leilão.'),
            dict(hora='14h00', quem='EQUIPE grava', arquivo='stories/05-14h00-galpao-FAIXA-cole-no-video.png',
                 previa='previas/05-14h00-galpao-como-fica.jpg',
                 gravar='10 a 15 segundos no galpão: alguém liga a máquina, abre a tampa e mostra o painel acendendo.',
                 falar='"Eu sou [nome] e eu confiro o seu pedido. Olha a máquina de hoje: testada e funcionando. Às 18h o martelo bate!"',
                 figurinha='LINK do leilão (o mesmo das 10h), abaixo da faixa.'),
            dict(hora='17h00', quem='ARTE PRONTA (ou equipe ao vivo)', arquivo='stories/06-17h00-falta-1-hora.jpg',
                 gravar='Se der para gravar: alguém do time mostrando o lance atual na tela do site e use a faixa 06b por cima. Se não der, poste a arte pronta.',
                 falar='Se gravar: "Falta uma hora! O lance tá em R$ ___. Quem vai levar essa máquina?"',
                 figurinha='CONTAGEM REGRESSIVA (escolha a mesma que você criou às 5h) + LINK do leilão, abaixo da faixa.'),
            dict(hora='18h00', quem='EQUIPE ao vivo', arquivo='stories/07-18h-martelo-batido-FAIXA-cole-no-video.png',
                 gravar='Filme a tela do leilão nos últimos 30 segundos e a reação de quem estiver junto quando o martelo bater.',
                 falar='"Dou-lhe uma, dou-lhe duas… é NoZap! Saiu por R$ ___. Na loja custa R$ 904,62!"',
                 figurinha='Nenhuma. Só a FAIXA por cima.'),
            dict(hora='18h15', quem='ARTE PRONTA (Duda manda)', arquivo=None,
                 falar='A Duda confere no site quanto saiu e te manda aqui no chat a arte "Martelo Batido" com o valor real, logo depois do martelo.',
                 figurinha='Nenhuma. Se quiser, LINK do leilão de sábado (Notebook Dell).'),
        ],
    },
}


def mini(caminho, alt=520):
    im = Image.open(caminho).convert('RGBA')
    if caminho.endswith('.png'):
        fundo = Image.new('RGBA', im.size, (40, 60, 50, 255))
        fundo.alpha_composite(im)
        im = fundo
    im = im.convert('RGB')
    im.thumbnail((alt, alt))
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def html(dia):
    D = DIAS[dia]
    base = os.path.join(AQUI, '..', D['pasta'])
    blocos = []
    for it in D['itens']:
        imgs = ''
        for k in ('previa', 'arquivo', 'arquivo2'):
            if it.get(k) and (k != 'arquivo' or not it.get('previa')):
                imgs += f'<img src="{mini(os.path.join(base, it[k]))}">'
        nome = f'<div class="arq">Arquivo: <b>{os.path.basename(it["arquivo"])}</b>' + (f' + <b>{os.path.basename(it["arquivo2"])}</b>' if it.get('arquivo2') else '') + '</div>' if it.get('arquivo') else ''
        leg = f'<pre>{it["legenda"]}</pre>' if it.get('legenda') else ''
        grav = f'<p><span class="r">GRAVAR</span>{it["gravar"]}</p>' if it.get('gravar') else ''
        blocos.append(f'''<section><div class="topo"><span class="hora">{it["hora"]}</span><span class="quem">{it["quem"]}</span></div>
<div class="corpo"><div class="imgs">{imgs}</div><div class="txt">{nome}{grav}<p><span class="r">FALAR</span>{it["falar"]}</p>{leg}
<p><span class="r">FIGURINHA</span>{it["figurinha"]}</p></div></div></section>''')
    return f'''<!doctype html><meta charset="utf-8"><style>
@page {{ size: A4; margin: 14mm 12mm; }}
body {{ font-family: Inter, Arial, sans-serif; color:#0b2619; font-size:12.5pt; }}
h1 {{ background:#082619; color:#fff; padding:14px 18px; border-radius:14px; margin:0 0 8px; font-size:20pt; }}
h1 b {{ color:#e8ba4a; }}
.res {{ background:#fdf6e3; border:2px solid #e8ba4a; border-radius:12px; padding:10px 14px; margin-bottom:10px; }}
section {{ border:2px solid #cfe7d6; border-radius:14px; padding:10px 12px; margin:10px 0; page-break-inside:avoid; }}
.topo {{ display:flex; gap:10px; align-items:center; margin-bottom:8px; }}
.hora {{ background:#e8ba4a; color:#082619; font-weight:900; padding:4px 12px; border-radius:20px; font-size:15pt; }}
.quem {{ font-weight:800; color:#228b4c; }}
.corpo {{ display:flex; gap:12px; }}
.imgs img {{ height:250px; border-radius:10px; margin-right:6px; }}
.txt p {{ margin:4px 0 8px; }}
.r {{ display:inline-block; background:#082619; color:#fff; font-size:9pt; font-weight:800; padding:2px 8px; border-radius:6px; margin-right:6px; }}
.arq {{ font-size:10pt; color:#555; margin-bottom:6px; }}
pre {{ white-space:pre-wrap; font-family:inherit; background:#f2f8f4; padding:8px; border-radius:8px; font-size:11pt; }}
.dica {{ font-size:10.5pt; background:#f2f8f4; border-radius:10px; padding:8px 12px; }}
</style><h1>Roteiro Duda · <b>{D["titulo"]}</b></h1>
<div class="res">{D["resumo"]}<br>Tudo já está no tamanho do stories (9:16). Arte pronta = é só postar e colar a figurinha indicada.</div>
<div class="dica">{COMO_COLAR}</div>
{"".join(blocos)}'''


def gerar(dia):
    destino = os.path.join(AQUI, '..', DIAS[dia]['pasta'], f'ROTEIRO-{DIAS[dia]["pasta"]}.pdf')
    h = os.path.join(AQUI, '..', DIAS[dia]['pasta'], '.roteiro.html')
    open(h, 'w').write(html(dia))
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{os.path.abspath(h)}');await p.pdf({{path:'{os.path.abspath(destino)}',format:'A4',printBackground:true}});await b.close();}})()"
    subprocess.run(['node', '-e', js], check=True)
    os.remove(h)
    return destino


if __name__ == '__main__':
    print(gerar(sys.argv[1]))
