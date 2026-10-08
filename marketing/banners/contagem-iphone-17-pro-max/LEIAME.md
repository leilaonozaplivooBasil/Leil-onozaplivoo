# Contagem regressiva — leilão do iPhone 17 Pro Max

Banners 1920×1080 (16:9) com a Leila. Para gerar outro dia da contagem:

```bash
python3 tela_celular.py "Termina 17/10" leila-faltam-2-dias.png
node render.js "n=2&falta=FALTAM&unit=DIAS&data=17/10&leila=leila-faltam-2-dias.png" faltam-2-dias-1920x1080.png
```

- `tela_celular.py`: troca o prazo ("Termina em ...") na tela do celular que a Leila segura.
- `banner.html`: arte do banner; `n`, `falta`, `unit` e `leila` vêm do endereço (depois do `#`).

## Versão com a data em destaque (sem contagem)

`banner-data.html` → `leilao-dia-17-10-1920x1080.png`

```bash
python3 tela_celular.py "Termina 17/10" leila-dia-17-10.png
PAGE=banner-data.html node render.js "" leilao-dia-17-10-1920x1080.png
```
