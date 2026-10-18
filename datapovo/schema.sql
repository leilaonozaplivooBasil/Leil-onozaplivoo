-- DataPovo: esquema para o Supabase (cole no SQL Editor).
-- Não existe tabela de votos individuais: só um contador por opção, sem horário, sem ordem
-- e sem ligação com ninguém. O contato (opcional) fica em outra tabela, sem ligação com o voto.
-- O navegador só consegue chamar as 3 funções abaixo; não lê nem escreve nas tabelas.

create table if not exists placar (
  opcao text primary key check (opcao ~ '^([0-9]{1,3}|BRANCO|NULO)$'),
  votos bigint not null default 0
);

create table if not exists contatos (
  id bigint generated always as identity primary key,
  nome text check (char_length(nome) <= 80),
  whatsapp text not null unique check (whatsapp ~ '^55[0-9]{10,11}$'),
  consentimento text not null,          -- texto exato que a pessoa aceitou
  dia date not null default current_date -- só o dia, sem hora
);

alter table placar enable row level security;
alter table contatos enable row level security;
-- sem policies: acesso direto pelo navegador negado

create or replace function votar(p_opcao text) returns void
language plpgsql security definer set search_path = public as $$
begin
  insert into placar (opcao, votos) values (p_opcao, 1)
  on conflict (opcao) do update set votos = placar.votos + 1;
end $$;

create or replace function deixar_contato(p_nome text, p_whatsapp text, p_consentimento text) returns void
language plpgsql security definer set search_path = public as $$
begin
  insert into contatos (nome, whatsapp, consentimento)
  values (nullif(trim(p_nome), ''), p_whatsapp, p_consentimento)
  on conflict (whatsapp) do nothing;
end $$;

create or replace function resultado() returns table (opcao text, votos bigint)
language sql security definer set search_path = public as $$
  select p.opcao, p.votos from placar p;
$$;

revoke all on function votar(text), deixar_contato(text, text, text), resultado() from public;
grant execute on function votar(text), deixar_contato(text, text, text), resultado() to anon;
