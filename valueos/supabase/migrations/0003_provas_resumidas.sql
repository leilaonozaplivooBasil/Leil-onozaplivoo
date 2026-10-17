-- Prova resumida para o investidor: vê que a evidência existe (período, carga, hash), sem a consulta nem o resultado bruto. (aplicado em 17/10/2026)
create or replace view public.vos_provas as
  select e.id, e.metric_id, e.periodo, e.carga_id, e.hash, e.hash_anterior, e.criado_em
  from public.vos_evidencias e
  where public.vos_papel() in ('INVESTOR','BOARD','ADMIN');
grant select on public.vos_provas to authenticated;
