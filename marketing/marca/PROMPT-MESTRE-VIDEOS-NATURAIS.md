# Prompt mestre — vídeos naturais (Natália, 04/11/2026)
Regra oficial para TODOS os vídeos de leilão a partir de 04/11/2026.

1. Gente real primeiro: pessoa ou mão real nos 2 primeiros segundos; 70% ou mais de gravação real; o momento mais emocionante no começo.
2. Evitar o que denuncia IA: produto 3D flutuando, degradê liso, câmera parada, pessoas geradas por IA, voz de locutor, card parado por mais de 2 s, transições chamativas.
3. Natural: câmera na mão (balanço de 2% a 4%), luz real, produto na mão ou na caixa, texto estilo Instagram (frases curtas, minúsculas), cores da marca só em detalhe; voz real; música de 5% a 10% na fala e subindo na revelação.
4. Estrutura (15 a 30 s): gancho 0-2 s → história 2-10 s → revelação com preço FINAL → convite falado + no máximo 2 s de card com dia e hora.
5. Preço e verdade: sempre o preço FINAL pago ao lado do preço de loja, comprovável; nada de carteira, depósito, rendimento, aposta ou sorteio.
Formatos: Encontrou dono · Unboxing no escritório · Embalando pedidos · Vem comigo · 5h da manhã · Chuta o preço · Últimos segundos · É golpe?
Checklist antes de entregar e entregáveis (vídeo, capa, legenda, linha de formato/teste): ver o texto completo enviado pela Natália em 04/11.

## Conferência de áudio OBRIGATÓRIA antes de entregar ou agendar (lição de 04/11, ep. 01)
O ep. 01 subiu com a música alta demais: fala da Natália a -16 LUFS e música sozinha a -18,6 LUFS (só 2 dB de diferença).
Regra, medida com `ffmpeg -af ebur128` em cada trecho do arquivo FINAL (o mesmo que vai para o Instagram):
- Fala: -16 LUFS.
- Música por baixo da fala: pelo menos 20 dB abaixo da fala (é o "5% a 10%").
- Trechos só com música (sem ninguém falando): no máximo -24 LUFS, ou seja, 8 dB abaixo da fala.
- Se não passar, não entrega e não agenda. Ajusta e mede de novo.
- Junto com o vídeo, mandar para a Natália os números medidos e pedir que ela ouça COM FONE antes do ok.
- (07/11) Nunca usar `loudnorm` no mesmo filtro com `amix duration=first`/sidechain: o atraso de ~3 s dele corta o fim do áudio. Tratar a voz num arquivo à parte, misturar depois, e conferir que a duração do áudio = duração do vídeo (ffprobe) antes de entregar.

## Capa de Reels: área que aparece na grade do perfil (OBRIGATÓRIO, lição de 23/11)
A capa é 1080x1920, mas a grade do perfil mostra só o miolo 3:4: **de y=240 a y=1680**. Em 23/11 as capas do
"Arrematado de sábado EP. 01" e da "Novelinha EP. 01" subiram com o título em y≈190 e ficaram cortadas no perfil.
- Todo texto e todo elemento importante da capa fica **entre y=260 e y=1660** (folga de 20 px).
- Selo da série logo abaixo de y=260; título logo abaixo do selo; **nunca em cima do rosto**.
- Foto de pessoa: **olho aberto e sorrindo** (escolher o quadro; conferir ampliado).
- Antes de subir: gerar a prévia do corte (`img.crop((0,240,1080,1680))`) e olhar a capa inteira E o corte.
- A capa é separada do vídeo: o título dentro do vídeo pode ficar no alto; a capa segue esta regra.
