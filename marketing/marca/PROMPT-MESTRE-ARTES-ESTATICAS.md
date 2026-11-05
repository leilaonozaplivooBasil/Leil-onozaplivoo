# Prompt mestre — artes estáticas "vitrine limpa" (Natália, 05/11/2026)
Referência: posts do Mercado Livre (fundo de uma cor, produto grande, quase nenhum texto). Exemplos prontos em
`marca/estilo-vitrine/exemplos/`. Vale para feed, carrossel e kit dos vendedores.

## As 10 regras
1. **Fundo de UMA cor só, chapado.** Ouro da marca `#F5C451` (o nosso "amarelo") ou areia `#F6EFE2`. Nada de cenário, neon, chamas, moedas ou fumaça.
2. **Texto sempre verde-escuro `#0A3D26`** (no areia, o destaque pode ser `#1B7A48`). Uma família de letra só (Inter Display): Black para a palavra forte, Medium para o resto.
3. **Um produto (ou no máximo 3), foto ORIGINAL recortada**, grande — ocupa de 40% a 60% da arte. Nunca produto desenhado por IA.
4. **Sombra curta embaixo do produto**, para ele "pousar" no fundo. Pode ter bloco/pódio liso da MESMA cor, um tom mais escuro.
5. **No máximo 2 frases curtas**, de até 4 palavras cada linha. Tom de conversa: "O que eu queria ganhar de Natal:", "Cuidar de quem você ama custa pouco."
6. **O número é o herói**: o lance aparece gigante (o maior elemento depois do produto), com "R$" menor ao lado.
7. **Só 1 linha pequena de informação** no rodapé: produto · dia/hora do martelo.
8. **Logo pequeno** (no máximo 170 px de largura), num canto. Mascote não entra em arte de produto.
9. **Respiro**: pelo menos 1/3 da arte vazio. Se está cheio, tira coisa.
10. **Verdade sempre**: preço e horário do sistema; "lance desde/lance inicial" nunca vira "paguei"; sem % e sem link até 29/11; sem nome de cliente.

## Moldes que funcionam (escolha 1 por post e varie ao longo da semana)
- **Metade/metade (carrossel)**: em cima "O que eu queria…" + produto; embaixo "Onde o lance começa:" + preço gigante.
- **Número herói**: título curto em cima, 3 produtos em blocos lisos, preço gigante embaixo, palavra-tema bem clara ao fundo (marca d'água a 9%).
- **Um produto, uma frase**: fundo areia, frase de 3 linhas à esquerda, produto à direita, preço embaixo.
- **Selo redondo** (opcional, 1 por arte): menta `#D6ECDD` com 2 palavras ("É HOJE", "12H-20H").

## Prompt para a IA (copiar e colar)
> Crie uma arte de post de Instagram 1080x1350 no estilo vitrine limpa de grande varejista brasileiro.
> Fundo chapado de uma cor só: #F5C451 (ou #F6EFE2). Sem cenário, sem degradê, sem neon, sem moedas, sem chamas.
> Use a FOTO ORIGINAL do produto que eu enviar, recortada e sem alterar o produto, grande, ocupando 40–60% da arte, com uma sombra curta e suave embaixo.
> NÃO escreva nenhum texto na imagem: deixe espaço vazio à esquerda/em cima para o título e embaixo para o preço (o texto é colocado depois, à parte).
> Visual calmo, sofisticado, com muito espaço vazio. Nada de pessoas geradas por IA.

Depois da IA: o texto, o preço e o logo são colocados por cima com o molde (`fonte/estilo_vitrine.py`), nunca escritos pela IA
(ela erra letra e inventa logo).

## Checklist antes de entregar
- [ ] Fundo de uma cor? [ ] Produto é a foto original? [ ] Até 2 frases? [ ] Preço é o maior texto?
- [ ] Preço e horário batem com o sistema? [ ] Sem %, sem link, sem nome de cliente? [ ] 1/3 vazio?
