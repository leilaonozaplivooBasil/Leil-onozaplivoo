# Geladeira Brastemp Frost Free 385 L Duplex Inox — 3 banners (1920×1080)

Leilão termina quarta, 14/10 às 18h.

- v1 — "A cozinha dos sonhos vai a leilão" + selos Frost Free / 385 litros / Inox
- v2 — "Adeus, degelo. Olá, Frost Free." + balão da Leila
- v3 — "O martelo bate quarta 14/10 às 18h"

`geladeira.png` é provisória (desenho). Para trocar pela foto real do leilão:

```bash
# 1. salve a foto recortada (fundo transparente) como geladeira.png
python3 tela_celular.py "Termina 14/10" leila-geladeira.png
python3 -c "from PIL import Image; b=Image.open('leila-ombro.png').convert('RGB'); p=Image.open('leila-geladeira.png').convert('RGB'); b.paste(p.crop((30,330,310,790)),(30,330)); b.save('leila-ombro-geladeira.png')"
for v in v1 v2 v3; do node render.js $v geladeira-brastemp-$v-1920x1080.png; done
```
