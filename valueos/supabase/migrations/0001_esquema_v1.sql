-- LNZ VALUE OS — esquema v1 (aplicado em 17/10/2026 no projeto hmldusqewfckxgzldqga; tabelas com prefixo vos_)
-- Cópia fiel do que foi aplicado pela conexão do Supabase. Nada aqui toca o banco do app.
create extension if not exists pgcrypto with schema extensions;

create table if not exists public.vos_profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  email text not null unique,
  nome text,
  papel text not null default 'PUBLIC' check (papel in ('PUBLIC','INVESTOR','BOARD','ADMIN')),
  ativo boolean not null default true,
  expira_em timestamptz,
  criado_em timestamptz not null default now()
);
create table if not exists public.vos_convites (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  papel text not null default 'INVESTOR' check (papel in ('INVESTOR','BOARD','ADMIN')),
  convidado_por text,
  criado_em timestamptz not null default now(),
  expira_em timestamptz not null default now() + interval '30 days',
  usado_em timestamptz,
  revogado_em timestamptz
);
create index if not exists vos_convites_email_idx on public.vos_convites (lower(email));
create table if not exists public.vos_nda_aceites (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  versao text not null,
  hash_texto text not null,
  aceito_em timestamptz not null default now(),
  ip text,
  user_agent text
);
create table if not exists public.vos_acessos (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete set null,
  rota text not null,
  quando timestamptz not null default now(),
  ip text,
  user_agent text
);
create table if not exists public.vos_metricas (
  metric_id text primary key,
  nome text not null,
  familia text not null,
  definicao text not null,
  unidade text not null default 'BRL',
  fonte_primaria text not null,
  escopo_entidade text not null default 'Compras Full Comércio Ltda',
  exclusoes text,
  regra_conflito text,
  series_start date not null default '2026-08-01',
  versao text not null default 'v1.0',
  ativo boolean not null default true,
  criado_em timestamptz not null default now()
);
create table if not exists public.vos_cargas (
  id uuid primary key default gen_random_uuid(),
  tipo text not null check (tipo in ('app_query','upload','manual')),
  descricao text not null,
  origem text not null,
  arquivo_nome text,
  hash_sha256 text not null,
  linhas integer,
  periodo_ini date,
  periodo_fim date,
  carregado_por text not null,
  carregado_em timestamptz not null default now(),
  consulta text
);
create table if not exists public.vos_evidencias (
  id bigint generated always as identity primary key,
  carga_id uuid not null references public.vos_cargas(id),
  metric_id text not null references public.vos_metricas(metric_id),
  periodo date not null,
  consulta text,
  resultado jsonb not null,
  hash_anterior text,
  hash text not null,
  criado_em timestamptz not null default now()
);
create or replace function public.vos_evidencia_hash() returns trigger
language plpgsql security definer set search_path = public, extensions as $$
declare anterior text;
begin
  select hash into anterior from public.vos_evidencias order by id desc limit 1;
  new.hash_anterior := anterior;
  new.hash := encode(extensions.digest(coalesce(anterior,'') || new.metric_id || new.periodo::text || new.resultado::text || new.carga_id::text, 'sha256'), 'hex');
  return new;
end $$;
create trigger vos_evidencias_hash before insert on public.vos_evidencias for each row execute function public.vos_evidencia_hash();
create or replace function public.vos_bloqueia_alteracao() returns trigger language plpgsql as $$
begin raise exception 'tabela só-acrescenta: % não permitido em %', tg_op, tg_table_name; end $$;
create trigger vos_evidencias_imutavel before update or delete on public.vos_evidencias for each row execute function public.vos_bloqueia_alteracao();
create trigger vos_nda_imutavel before update or delete on public.vos_nda_aceites for each row execute function public.vos_bloqueia_alteracao();
create trigger vos_acessos_imutavel before update or delete on public.vos_acessos for each row execute function public.vos_bloqueia_alteracao();
create table if not exists public.vos_snapshots (
  id uuid primary key default gen_random_uuid(),
  tipo text not null check (tipo in ('live','shadow','official')),
  periodo date not null,
  fechado_em timestamptz not null default now(),
  metodologia_versao text not null default 'v1.0',
  hash text,
  aprovado_por text,
  observacao text
);
create or replace function public.vos_snapshot_oficial_imutavel() returns trigger language plpgsql as $$
begin
  if old.tipo = 'official' then raise exception 'snapshot oficial é imutável'; end if;
  if tg_op = 'DELETE' then return old; end if;
  return new;
end $$;
create trigger vos_snapshots_imutavel before update or delete on public.vos_snapshots for each row execute function public.vos_snapshot_oficial_imutavel();
create table if not exists public.vos_valores (
  id bigint generated always as identity primary key,
  metric_id text not null references public.vos_metricas(metric_id),
  periodo date not null,
  valor numeric,
  etiqueta text not null check (etiqueta in ('VERIFIED','MANAGEMENT_DATA','FORECAST','AI_ASSUMPTION','NAO_DISPONIVEL')),
  fonte text not null,
  carga_id uuid references public.vos_cargas(id),
  evidencia_id bigint references public.vos_evidencias(id),
  snapshot_id uuid references public.vos_snapshots(id),
  nota text,
  criado_em timestamptz not null default now()
);
create index if not exists vos_valores_metric_periodo_idx on public.vos_valores (metric_id, periodo);
create or replace function public.vos_papel() returns text language sql stable security definer set search_path = public as $$
  select papel from public.vos_profiles where user_id = auth.uid() and ativo and (expira_em is null or expira_em > now())
$$;
grant execute on function public.vos_papel() to authenticated;
alter table public.vos_profiles enable row level security;
alter table public.vos_convites enable row level security;
alter table public.vos_nda_aceites enable row level security;
alter table public.vos_acessos enable row level security;
alter table public.vos_metricas enable row level security;
alter table public.vos_cargas enable row level security;
alter table public.vos_evidencias enable row level security;
alter table public.vos_snapshots enable row level security;
alter table public.vos_valores enable row level security;
create policy vos_profiles_proprio on public.vos_profiles for select to authenticated using (user_id = auth.uid());
create policy vos_nda_proprio_sel on public.vos_nda_aceites for select to authenticated using (user_id = auth.uid());
create policy vos_nda_proprio_ins on public.vos_nda_aceites for insert to authenticated with check (user_id = auth.uid());
create policy vos_acessos_proprio_ins on public.vos_acessos for insert to authenticated with check (user_id = auth.uid());
create policy vos_metricas_leitura on public.vos_metricas for select to authenticated using (public.vos_papel() in ('INVESTOR','BOARD','ADMIN'));
create policy vos_valores_leitura on public.vos_valores for select to authenticated using (public.vos_papel() in ('INVESTOR','BOARD','ADMIN'));
create policy vos_snapshots_leitura on public.vos_snapshots for select to authenticated using (public.vos_papel() in ('INVESTOR','BOARD','ADMIN'));
create policy vos_cargas_leitura on public.vos_cargas for select to authenticated using (public.vos_papel() in ('INVESTOR','BOARD','ADMIN'));
create policy vos_evidencias_leitura on public.vos_evidencias for select to authenticated using (public.vos_papel() in ('BOARD','ADMIN'));
