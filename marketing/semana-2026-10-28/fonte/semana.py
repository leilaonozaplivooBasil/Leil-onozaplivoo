# Kits de quinta 29/10 a domingo 01/11/2026 (briefing Duda). Roda: python3 semana.py → artes + ROTEIRO de cada dia.
import os
import roteiro
from pecas import *

LINK_NOTE = 'leilaonozap.net/l/ea97c6608ca690bf3d76dfb4'
NOTE_LOJA = 3569.60


def pasta(p):
    return os.path.join(AQUI, '..', p)


def sem_figurinha():
    return 'Nenhuma. Só a FAIXA por cima do vídeo.'


# ---------------------------------------------------------------- QUINTA 29/10
Q = pasta('quinta-29-10')
personagem(f'{Q}/stories/01-05h00-leila-bom-dia.jpg', 'BOM DIA · 5H', 'leila', 'confiante',
           'Disciplina é *voltar* amanhã', 'Ontem o martelo bateu. Às 10h tem produto do dia aqui.', alt=700)
overlay(f'{Q}/stories/02-09h00-treino-FAIXA-cole-no-video.png', f'{Q}/previas/02-09h00-treino-como-fica.jpg',
        'Antes da primeira caixa, a gente *agradece*', 'Treino e oração da equipe, todo dia.', 'BASTIDOR NOZAP',
        '[ VÍDEO: EQUIPE TREINANDO OU EM ORAÇÃO ]')
enquete(f'{Q}/stories/03-10h00-produto-do-dia-enquete.jpg', f'{Q}/previas/03-10h00-enquete-onde-colar.jpg',
        'PRODUTO DO DIA', 'f-005.png', 'Quanto você *pagaria* nesse relógio?', 'Na loja: R$ 290,95. A resposta sai às 19h.')
overlay(f'{Q}/stories/04-14h00-quem-faz-FAIXA-cole-no-video.png', f'{Q}/previas/04-14h00-quem-faz-como-fica.jpg',
        'Quem faz o seu pedido *chegar*', 'Prazer, eu sou do time NoZap.', 'QUEM FAZ',
        '[ VÍDEO: ALGUÉM DA EQUIPE SE APRESENTANDO NO GALPÃO ]')
resposta(f'{Q}/stories/05-19h00-resposta-relogio.jpg', 'RESPOSTA DA ENQUETE', 'f-005.png',
         'Relógio *EYT*', 290.95, 20.20, 'Sábado às 20h tem Notebook Dell. Comenta SÁBADO.')
feed_foto(f'{Q}/feed/feed-12h-card1.jpg', 'CHUTA QUANTO O *MURILO* PAGOU NESSE IPHONE 17 PRO MAX', 'iphone.png',
          'Comenta seu chute *antes* de passar pro lado', tam=68)
feed_preco(f'{Q}/feed/feed-12h-card2.jpg', 'ELE PAGOU *ISSO* AQUI', 'iphone.png', 8404.23, 4640,
           'Sábado tem leilão às 20h · comenta *SÁBADO*')

# ---------------------------------------------------------------- SEXTA 30/10
S = pasta('sexta-30-10')
personagem(f'{S}/stories/01-05h00-leila-bom-dia.jpg', 'BOM DIA · 5H', 'leila', 'sorriso',
           'Sexta de *gratidão*', 'Agradece pela semana e vem com a gente: hoje tem entrega pra ver.', alt=700)
overlay(f'{S}/stories/02-09h00-treino-FAIXA-cole-no-video.png', f'{S}/previas/02-09h00-treino-como-fica.jpg',
        'Antes da primeira caixa, a gente *agradece*', 'Treino e oração da equipe, todo dia.', 'BASTIDOR NOZAP',
        '[ VÍDEO: EQUIPE TREINANDO OU EM ORAÇÃO ]')
enquete(f'{S}/stories/03-10h00-produto-do-dia-enquete.jpg', f'{S}/previas/03-10h00-enquete-onde-colar.jpg',
        'PRODUTO DO DIA', 'f-006.png', 'Quanto você *pagaria* nessa toalha de Natal?', 'Na loja: R$ 440,96. A resposta sai às 19h.')
overlay(f'{S}/stories/04-14h00-notebook-chegou-FAIXA-cole-no-video.png', f'{S}/previas/04-14h00-notebook-como-fica.jpg',
        'O notebook de *sábado* chegou', 'Conferido aqui no galpão. Martelo amanhã às 20h.', 'BASTIDOR NOZAP',
        '[ VÍDEO: ALGUÉM ABRINDO A CAIXA E LIGANDO O NOTEBOOK ]')
resposta(f'{S}/stories/05-19h00-resposta-toalha.jpg', 'RESPOSTA DA ENQUETE', 'f-006.png',
         'Toalha de *Natal*', 440.96, 8.00, 'Amanhã às 20h tem Notebook Dell. Comenta SÁBADO.')
feed_personagem(f'{S}/feed/feed-12h-card1.jpg', 'PRA ONDE VAI O QUE VOCÊ *DEVOLVE* NA INTERNET?',
                'Não volta pra prateleira. Vem pra cá.', 'leila', 'apresenta', 'Arrasta pro lado')
feed_passos(f'{S}/feed/feed-12h-card2.jpg', 'O CAMINHO DO *DEVOLVIDO*',
            ['Chega no nosso *galpão*', 'A equipe *confere* e testa', 'Vai pro *leilão* ou pra loja'], 'Comenta *GALPÃO*',
            quem='leila', pose='apontando')
feed_preco(f'{S}/feed/feed-12h-card3.jpg', 'ESSA ESTUFA SAIU *ASSIM*', 'estufa-a.jpg', 670.38, 28.47,
           'Comenta *GALPÃO* que eu mostro o próximo')

# ---------------------------------------------------------------- SÁBADO 31/10 (leilão, martelo 20h)
B = pasta('sabado-31-10')
T = 'SÁBADO · DIA DE LEILÃO'
overlay(f'{B}/stories/01-05h00-praia-FAIXA-cole-no-video.png', f'{B}/previas/01-05h00-praia-como-fica.jpg',
        'Sábado também é dia de *aquecer*', 'Hoje tem leilão. Às 10h o Leiloeiro revela o produto.', T,
        '[ VÍDEO DA EQUIPE CORRENDO NA PRAIA AO NASCER DO SOL ]')
personagem(f'{B}/stories/02-05h01-leiloeiro-bom-dia.jpg', T, 'leiloeiro', 'a-comemora',
           'Dou-lhe uma, dou-lhe duas… *bom dia*!', 'Hoje o martelo bate às 20h. Ativa o lembrete aqui embaixo.')
revela(f'{B}/stories/03-10h00-leiloeiro-revela.jpg', 'O MARTELO DE HOJE', 'f-004.png',
       'Notebook *Dell*', 'Core i3 · na loja R$ 3.569,60 · martelo hoje às 20h')
enquete(f'{B}/stories/04-10h01-enquete.jpg', f'{B}/previas/04-10h01-enquete-onde-colar.jpg', None, 'f-004.png',
        'Quanto você *daria* nele?', 'Responde a enquete. O valor real sai às 20h.')
overlay(f'{B}/stories/05-14h00-galpao-FAIXA-cole-no-video.png', f'{B}/previas/05-14h00-galpao-como-fica.jpg',
        'Conferido e *testado*', 'Antes de ir pra sua casa, passa pela nossa mão. Martelo às 20h.', T,
        '[ VÍDEO: ALGUÉM LIGANDO O NOTEBOOK NO GALPÃO ]')
personagem(f'{B}/stories/06-19h00-falta-1-hora.jpg', 'ÚLTIMA HORA', 'leiloeiro', 'a-relogio',
           'Falta *1 hora*', 'Martelo às 20h. O lance é no site: toca no link aqui embaixo.')
overlay(f'{B}/stories/06b-19h00-FAIXA-se-gravar-video.png', f'{B}/previas/06b-19h00-como-fica.jpg',
        'Falta *1 hora*', 'Martelo às 20h. O lance é no site: toca no link aqui embaixo.', 'ÚLTIMA HORA',
        '[ VÍDEO: LANCE ATUAL NA TELA DO SITE ]')
overlay(f'{B}/stories/07-20h-martelo-batido-FAIXA-cole-no-video.png', f'{B}/previas/07-20h-martelo-como-fica.jpg',
        'Martelo *batido*!', 'Na loja: R$ 3.569,60. Olha quanto saiu', 'LEILÃO DE SÁBADO',
        '[ VÍDEO: TELA DO LEILÃO NOS ÚLTIMOS SEGUNDOS ]')
feed_foto(f'{B}/feed/feed-12h-card1.jpg', 'HOJE O MARTELO BATE ÀS *20H*', 'f-004.png',
          'Notebook Dell · na loja *R$* *3.569,60*')
feed_passos(f'{B}/feed/feed-12h-card2.jpg', 'QUEM *DECIDE* O PREÇO É VOCÊ',
            ['Comenta *SÁBADO* aqui embaixo', 'Recebe o link no direct', 'Dá seu lance até as *20h*'], 'Comenta *SÁBADO*')

# ---------------------------------------------------------------- DOMINGO 01/11
D = pasta('domingo-01-11')
personagem(f'{D}/stories/01-05h00-leila-bom-dia.jpg', 'BOM DIA · 5H', 'leila', 'pensativa',
           'Domingo é dia de encher a *alma*', 'Quarta tem leilão. O que você quer ver no martelo?', alt=700)
overlay(f'{D}/stories/02-09h00-gratidao-FAIXA-cole-no-video.png', f'{D}/previas/02-09h00-gratidao-como-fica.jpg',
        'Gratidão pela *semana*', 'Cada entrega dessa semana foi uma família feliz.', 'GRATIDÃO DA SEMANA',
        '[ VÍDEO: EQUIPE REUNIDA AGRADECENDO ]')
enquete(f'{D}/stories/03-10h00-produto-do-dia-enquete.jpg', f'{D}/previas/03-10h00-enquete-onde-colar.jpg',
        'PRODUTO DO DIA', 'estufa-a.jpg', 'Quanto você *pagaria* nessa estufa?', 'Na loja: R$ 670,38. A resposta sai às 19h.')
overlay(f'{D}/stories/04-14h00-entregas-FAIXA-cole-no-video.png', f'{D}/previas/04-14h00-entregas-como-fica.jpg',
        'Entregue com *carinho*', 'As entregas da semana, uma por uma.', 'BASTIDOR NOZAP',
        '[ VÍDEO OU FOTOS DAS ENTREGAS DA SEMANA ]')
resposta(f'{D}/stories/05-19h00-resposta-estufa.jpg', 'RESPOSTA DA ENQUETE', 'estufa-a.jpg',
         'Estufa *5* *cubas*', 670.38, 28.47, 'Quarta tem leilão de novo. Comenta QUARTA.')
feed_personagem(f'{D}/feed/feed-12h-card1.jpg', 'O QUE SAIU NO *MARTELO*',
                'Preço da loja x preço que a pessoa pagou de verdade.', 'leiloeiro', 'a-trofeu', 'Arrasta pro lado')
feed_preco(f'{D}/feed/feed-12h-card2.jpg', 'IPHONE 17 *PRO* *MAX*', 'iphone.png', 8404.23, 4640, 'Arrematado em 24/10')
feed_preco(f'{D}/feed/feed-12h-card3.jpg', 'ESTUFA *5* *CUBAS*', 'estufa-a.jpg', 670.38, 28.47, 'Arrematada no leilão')
feed_preco(f'{D}/feed/feed-12h-card4.jpg', 'TOALHA DE *NATAL*', 'f-006.png', 440.96, 8.00, 'Arrematada no leilão')
feed_preco(f'{D}/feed/feed-12h-card5.jpg', 'RELÓGIO *EYT*', 'f-005.png', 290.95, 20.20, 'Salva pra ver no próximo leilão')

# ---------------------------------------------------------------- roteiros
COLAR = roteiro.COMO_COLAR
treino = dict(hora='09h00', quem='EQUIPE grava', arquivo='stories/02-09h00-treino-FAIXA-cole-no-video.png',
              previa='previas/02-09h00-treino-como-fica.jpg',
              gravar='10 segundos da equipe treinando, orando ou na reunião da manhã. Celular em pé.',
              falar='Ninguém precisa falar. Se quiser: "Bom dia! Começando o dia juntos."', figurinha=sem_figurinha())

roteiro.DIAS['quinta'] = dict(
    titulo='Quinta 29/10 — Chuta o Preço', pasta='quinta-29-10',
    resumo='Dia comum. Produto do dia: Relógio EYT (saiu por R$ 20,20; na loja R$ 290,95). Feed: o iPhone do Murilo.',
    itens=[
        dict(hora='05h00', quem='ARTE PRONTA', arquivo='stories/01-05h00-leila-bom-dia.jpg', falar='Nada.',
             figurinha='ENQUETE: "Acordou cedo hoje?" — Sim / Ainda não. Cole logo abaixo da faixa verde.'),
        treino,
        dict(hora='10h00', quem='ARTE PRONTA', arquivo='stories/03-10h00-produto-do-dia-enquete.jpg',
             previa='previas/03-10h00-enquete-onde-colar.jpg', falar='Nada.',
             figurinha='ENQUETE: "Quanto você pagaria?" — Até R$ 50 / R$ 50 a R$ 150 / Mais de R$ 150. No espaço entre a foto e a faixa.'),
        dict(hora='12h00', quem='FEED (carrossel)', arquivo='feed/feed-12h-card1.jpg', arquivo2='feed/feed-12h-card2.jpg',
             falar='Legenda pronta (copiar e colar):',
             legenda='Chuta quanto o Murilo pagou nesse iPhone 17 Pro Max 👀\n\nComenta seu chute ANTES de passar pro lado.\nNa loja ele custa R$ 8.404,23. No Leilão NoZap foi outra história.\n\nSábado às 20h tem leilão de novo: comenta SÁBADO que eu te mando o link 🔨\n\n#leilaonozap #iphone17promax #leilaoonline #consumointeligente',
             figurinha='Depois de publicar, compartilhe nos stories com a figurinha de LINK do notebook: ' + LINK_NOTE),
        dict(hora='14h00', quem='EQUIPE grava', arquivo='stories/04-14h00-quem-faz-FAIXA-cole-no-video.png',
             previa='previas/04-14h00-quem-faz-como-fica.jpg',
             gravar='10 a 15 segundos: uma pessoa da equipe olhando para a câmera, no galpão, fazendo o trabalho dela.',
             falar='"Eu sou [nome], e eu [separo / embalo / entrego] o seu pedido."', figurinha=sem_figurinha()),
        dict(hora='19h00', quem='ARTE PRONTA', arquivo='stories/05-19h00-resposta-relogio.jpg', falar='Nada.',
             figurinha='LINK do notebook (' + LINK_NOTE + ') — texto: VER O LEILÃO. Abaixo da faixa.'),
    ])

roteiro.DIAS['sexta'] = dict(
    titulo='Sexta 30/10 — Galpão', pasta='sexta-30-10',
    resumo='Dia comum. Produto do dia: Toalha de Natal (saiu por R$ 8; na loja R$ 440,96). Feed: pra onde vai o que você devolve.',
    itens=[
        dict(hora='05h00', quem='ARTE PRONTA', arquivo='stories/01-05h00-leila-bom-dia.jpg', falar='Nada.',
             figurinha='SLIDER (figurinha da barrinha) com emoji de coração: "Como foi sua semana?". Abaixo da faixa.'),
        treino,
        dict(hora='10h00', quem='ARTE PRONTA', arquivo='stories/03-10h00-produto-do-dia-enquete.jpg',
             previa='previas/03-10h00-enquete-onde-colar.jpg', falar='Nada.',
             figurinha='ENQUETE: "Quanto você pagaria?" — Até R$ 20 / R$ 20 a R$ 100 / Mais de R$ 100. No espaço entre a foto e a faixa.'),
        dict(hora='12h00', quem='FEED (carrossel)', arquivo='feed/feed-12h-card1.jpg', arquivo2='feed/feed-12h-card2.jpg',
             falar='3 cards (o card 3 é feed-12h-card3.jpg, a estufa). Legenda pronta:',
             legenda='Pra onde vai o que você devolve na internet? 📦\n\nNão volta pra prateleira. Vem pro nosso galpão, a equipe confere, testa e coloca no leilão.\nEssa estufa custa R$ 670,38 na loja. Aqui saiu por R$ 28,47.\n\nComenta GALPÃO que eu mostro o próximo.\n\n#leilaonozap #produtodevolvido #leilaoonline #consumointeligente',
             figurinha='Compartilhe nos stories com a figurinha de LINK do notebook.'),
        dict(hora='14h00', quem='EQUIPE grava', arquivo='stories/04-14h00-notebook-chegou-FAIXA-cole-no-video.png',
             previa='previas/04-14h00-notebook-como-fica.jpg',
             gravar='10 a 15 segundos: alguém abrindo a caixa do notebook e ligando ele no galpão.',
             falar='"Olha o notebook que vai pro martelo amanhã às 20h. Ligando, funcionando, conferido!"',
             figurinha='LINK do notebook (' + LINK_NOTE + '), abaixo da faixa.'),
        dict(hora='19h00', quem='ARTE PRONTA', arquivo='stories/05-19h00-resposta-toalha.jpg', falar='Nada.',
             figurinha='CONTAGEM REGRESSIVA: "Martelo do notebook" — sábado 31/10 às 20:00. Abaixo da faixa.'),
    ])

roteiro.DIAS['sabado'] = dict(
    titulo='Sábado 31/10 — Leilão do Notebook Dell', pasta='sabado-31-10',
    resumo='Dia de leilão. Martelo às 20h. Na loja: R$ 3.569,60. Os lances abrem quarta às 20h.',
    itens=[
        dict(hora='05h00', quem='EQUIPE grava', arquivo='stories/01-05h00-praia-FAIXA-cole-no-video.png',
             previa='previas/01-05h00-praia-como-fica.jpg',
             gravar='8 a 10 segundos, celular em pé, a equipe correndo na praia ao nascer do sol.',
             falar='"Bom dia, família NoZap! Sábado também é dia de aquecer: hoje tem leilão!"', figurinha=sem_figurinha()),
        dict(hora='05h01', quem='ARTE PRONTA', arquivo='stories/02-05h01-leiloeiro-bom-dia.jpg', falar='Nada.',
             figurinha='CONTAGEM REGRESSIVA (a mesma criada na sexta, "Martelo do notebook"). Abaixo da faixa.'),
        dict(hora='10h00', quem='ARTE PRONTA', arquivo='stories/03-10h00-leiloeiro-revela.jpg', falar='Nada.',
             figurinha='LINK: ' + LINK_NOTE + ' — texto: DAR MEU LANCE. Abaixo da faixa.'),
        dict(hora='10h01', quem='ARTE PRONTA', arquivo='stories/04-10h01-enquete.jpg',
             previa='previas/04-10h01-enquete-onde-colar.jpg', falar='Nada.',
             figurinha='ENQUETE: "Quanto você daria?" — Até R$ 800 / R$ 800 a 1.500 / R$ 1.500 a 2.500 / Mais de R$ 2.500.'),
        dict(hora='12h00', quem='FEED (carrossel)', arquivo='feed/feed-12h-card1.jpg', arquivo2='feed/feed-12h-card2.jpg',
             falar='Legenda pronta:',
             legenda='Hoje o martelo bate às 20h 🔨\n\nNotebook Dell Core i3, 8 GB, 512 GB, Windows 11. Na loja: R$ 3.569,60.\nAqui quem decide o preço é você.\n\nComenta SÁBADO que eu te mando o link do lance no direct.\n\n#leilaonozap #notebook #leilaoonline #consumointeligente',
             figurinha='Compartilhe nos stories com a figurinha de LINK do notebook.'),
        dict(hora='14h00', quem='EQUIPE grava', arquivo='stories/05-14h00-galpao-FAIXA-cole-no-video.png',
             previa='previas/05-14h00-galpao-como-fica.jpg',
             gravar='10 a 15 segundos: alguém ligando o notebook no galpão e mostrando a tela.',
             falar='"Eu sou [nome] e eu confiro o seu pedido. Olha o notebook de hoje: testado e funcionando. Às 20h o martelo bate!"',
             figurinha='LINK do notebook, abaixo da faixa.'),
        dict(hora='19h00', quem='ARTE PRONTA (ou equipe ao vivo)', arquivo='stories/06-19h00-falta-1-hora.jpg',
             gravar='Se der: filme o lance atual na tela do site e use a faixa 06b por cima.',
             falar='Se gravar: "Falta uma hora! O lance tá em R$ ___. Quem vai levar esse notebook?"',
             figurinha='CONTAGEM REGRESSIVA + LINK do notebook, abaixo da faixa.'),
        dict(hora='20h00', quem='EQUIPE ao vivo', arquivo='stories/07-20h-martelo-batido-FAIXA-cole-no-video.png',
             gravar='Filme a tela do leilão nos últimos 30 segundos e a reação de quem estiver junto.',
             falar='"Dou-lhe uma, dou-lhe duas… é NoZap! Saiu por R$ ___. Na loja custa R$ 3.569,60!"',
             figurinha=sem_figurinha()),
        dict(hora='20h15', quem='ARTE PRONTA (Duda manda)', arquivo=None,
             falar='A Duda confere no site quanto saiu e te manda aqui no chat a arte "Martelo Batido" com o valor real.',
             figurinha='Nenhuma.'),
    ])

roteiro.DIAS['domingo'] = dict(
    titulo='Domingo 01/11 — Gratidão da semana', pasta='domingo-01-11',
    resumo='Dia comum. Produto do dia: Estufa 5 cubas (saiu por R$ 28,47; na loja R$ 670,38). Feed: o que saiu no martelo.',
    itens=[
        dict(hora='05h00', quem='ARTE PRONTA', arquivo='stories/01-05h00-leila-bom-dia.jpg', falar='Nada.',
             figurinha='CAIXINHA DE PERGUNTA: "Qual produto você quer ver no leilão de quarta?". Abaixo da faixa. O mais pedido entra na quarta: "vocês pediram, a gente trouxe".'),
        dict(hora='09h00', quem='EQUIPE grava', arquivo='stories/02-09h00-gratidao-FAIXA-cole-no-video.png',
             previa='previas/02-09h00-gratidao-como-fica.jpg',
             gravar='10 segundos da equipe reunida, sorrindo, agradecendo a semana.',
             falar='"Obrigado, família NoZap! Foi uma semana de muita entrega."', figurinha=sem_figurinha()),
        dict(hora='10h00', quem='ARTE PRONTA', arquivo='stories/03-10h00-produto-do-dia-enquete.jpg',
             previa='previas/03-10h00-enquete-onde-colar.jpg', falar='Nada.',
             figurinha='ENQUETE: "Quanto você pagaria?" — Até R$ 50 / R$ 50 a R$ 200 / Mais de R$ 200.'),
        dict(hora='12h00', quem='FEED (carrossel)', arquivo='feed/feed-12h-card1.jpg', arquivo2='feed/feed-12h-card2.jpg',
             falar='5 cards (card1 a card5). Legenda pronta:',
             legenda='O que saiu no martelo 🔨\n\nPreço da loja x o que a pessoa pagou de verdade:\niPhone 17 Pro Max: R$ 8.404,23 → R$ 4.640\nEstufa 5 cubas: R$ 670,38 → R$ 28,47\nToalha de Natal: R$ 440,96 → R$ 8\nRelógio EYT: R$ 290,95 → R$ 20,20\n\nSalva pra lembrar: quarta tem leilão de novo.\n\n#leilaonozap #leilaoonline #consumointeligente #riodejaneiro',
             figurinha='Compartilhe nos stories.'),
        dict(hora='14h00', quem='EQUIPE grava', arquivo='stories/04-14h00-entregas-FAIXA-cole-no-video.png',
             previa='previas/04-14h00-entregas-como-fica.jpg',
             gravar='Junte 3 ou 4 vídeos ou fotos de entregas da semana (pode usar o que já tem no celular).',
             falar='Ninguém precisa falar.', figurinha=sem_figurinha()),
        dict(hora='19h00', quem='ARTE PRONTA', arquivo='stories/05-19h00-resposta-estufa.jpg', falar='Nada.',
             figurinha='Repostar também a arte do Martelo Batido do notebook (a Duda manda no sábado).'),
    ])

if __name__ == '__main__':
    for d in ('quinta', 'sexta', 'sabado', 'domingo'):
        print(roteiro.gerar(d))
