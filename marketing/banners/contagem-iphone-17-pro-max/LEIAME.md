# Contagem regressiva — leilão do iPhone 17 Pro Max

Banners 1920×1080 (16:9) com a Leila. Para gerar outro dia da contagem:

```bash
python3 tela_celular.py "Começa em 2 dias" leila-faltam-2-dias.png
node render.js "n=2&falta=FALTAM&unit=DIAS&leila=leila-faltam-2-dias.png" faltam-2-dias-1920x1080.png
```

- `tela_celular.py`: troca o texto de status na tela do celular que a Leila segura.
- `banner.html`: arte do banner; `n`, `falta`, `unit` e `leila` vêm do endereço (depois do `#`).
