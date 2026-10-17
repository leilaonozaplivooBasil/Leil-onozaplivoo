-- Quem já tinha conta neste projeto antes do portal não passa pelo gatilho de usuário novo.
-- Esta função cria o perfil a partir do convite para o usuário logado, se o convite for válido. (aplicado em 17/10/2026)
create or replace function public.vos_ativar_convite() returns text
language plpgsql security definer set search_path = public as $$
declare
  c record;
  em text;
begin
  if auth.uid() is null then return null; end if;
  select email into em from auth.users where id = auth.uid();
  if exists (select 1 from public.vos_profiles where user_id = auth.uid()) then
    return (select papel from public.vos_profiles where user_id = auth.uid());
  end if;
  select * into c from public.vos_convites
  where lower(email) = lower(em) and revogado_em is null and expira_em > now()
  order by criado_em desc limit 1;
  if c.id is null then return null; end if;
  insert into public.vos_profiles (user_id, email, papel) values (auth.uid(), em, c.papel)
  on conflict (user_id) do nothing;
  update public.vos_convites set usado_em = now() where id = c.id;
  return c.papel;
end $$;
grant execute on function public.vos_ativar_convite() to authenticated;

-- Perfis para contas já existentes que têm convite
insert into public.vos_profiles (user_id, email, papel)
select u.id, u.email, c.papel
from auth.users u
join public.vos_convites c on lower(c.email) = lower(u.email) and c.revogado_em is null and c.expira_em > now()
on conflict (user_id) do nothing;
