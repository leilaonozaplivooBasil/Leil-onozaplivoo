# Quinta 05/11: 6 artes de feed no molde do sábado (feed_foto) — 5 leilões do dia + o high ticket de sábado.
# Horários e preços vêm do sistema (auctions.end_time / market_price). Sem selo de % até 29/11.
import sys, pecas
from pecas import feed_foto
I = '/tmp/claude-0/-home-user/0ed67ded-c847-5a23-a4f2-d97436f79693/scratchpad/artes-0511/img'
pecas.foto = lambda n: n
OUT = '/home/user/Leil-onozaplivoo/marketing/semana-2026-11-05/quinta-05-11/feed'
H = sys.argv[1] if len(sys.argv) > 1 else '8H'
ARTES = [
  ('01-relogio-eyt', 'relogio4.jpg', 'Relógio EYT ouro rosa', 108.75),
  ('02-aparelho-de-pressao', 'pressao-c.jpg', 'Medidor de pressão', 56.21),
  ('03-camera-endoscopica', 'camera.png', 'Câmera endoscópica', 96.84),
  ('04-tapete-higienico-pet', 'tapete.webp', 'Tapete pet 60 un', 68.71),
  ('05-headset-gamer', 'headset.jpg', 'Headset gamer Flakes', 99.96),
]
for nome, ft, prod, loja in ARTES:
    feed_foto(f'{OUT}/{nome}.jpg', f'HOJE O MARTELO BATE ÀS *{H}*', f'{I}/{ft}', f'{prod} · na loja *{pecas.real(loja)}*', tam=76)
feed_foto(f'{OUT}/06-sabado-iphone-17-pro-max.jpg', 'SÁBADO O MARTELO BATE ÀS *20H*', f'{I}/iphone.webp',
          'iPhone 17 Pro Max · na loja *R$ 9.464,78*')
print('ok')
