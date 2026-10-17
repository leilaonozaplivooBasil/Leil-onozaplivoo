# E-mail de código do portal

`magic-link.html` é o corpo do modelo **Magic link or OTP** do Supabase Auth (projeto `hmldusqewfckxgzldqga`),
colado à mão no painel (Authentication → Emails → Modelos). Segue o mesmo desenho dos e-mails do app
(`api/_lib/modeloDeEmail.js`: logo `brand/logo-email.png`, marinho `#0B2D4F`, verde `#1B7F4B`, quadro de código).

- Assunto: `Seu código de acesso · Leilão NoZap`
- Variáveis do Supabase usadas: `{{ .Token }}` (código de 6–8 dígitos) e `{{ .ConfirmationURL }}` (link de entrada).
- Quem muda o arquivo aqui precisa colar de novo no painel — o Supabase não lê o repositório.
