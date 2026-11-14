#!/bin/bash
# Acabamento final (pedido da Natália, 14/11): vinheta escura ~5%, contraste +2,5%, saturação -3,5%;
# som: corta clipagem, agudos um pouco mais baixos, compressor + limitador e volume no padrão do Instagram (-14 LUFS).
# Uso: acabamento.sh <entrada.mp4> <saida.mp4>
set -e
IN="$1"; OUT="$2"; T=$(mktemp -d)
ffmpeg -v error -y -i "$IN" -vn -af "adeclip,equalizer=f=4000:t=o:w=1.2:g=-2,highshelf=f=7000:g=-3,acompressor=threshold=-20dB:ratio=3:attack=5:release=150:knee=6,alimiter=limit=0.89:attack=2:release=50:level=false" -ar 48000 "$T/a.wav"
ffmpeg -v error -y -i "$T/a.wav" -af "loudnorm=I=-14:TP=-1.5:LRA=8" -ar 48000 "$T/b.wav"
ffmpeg -v error -y -i "$IN" -i "$T/b.wav" -map 0:v -map 1:a -vf "eq=contrast=1.025:saturation=0.965,vignette=angle=0.3" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
rm -rf "$T"
