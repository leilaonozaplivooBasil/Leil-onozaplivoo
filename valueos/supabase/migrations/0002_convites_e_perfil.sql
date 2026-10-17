-- Só quem tem convite entra; o perfil nasce do convite quando a conta é criada. (aplicado em 17/10/2026)
create or replace function public.vos_convite_valido(p_email text) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.vos_convites where lower(email) = lower(p_email) and revogado_em is null and expira_em > now())
      or exists (select 1 from public.vos_profiles where lower(email) = lower(p_email) and ativo);
$$;
grant execute on function public.vos_convite_valido(text) to anon, authenticated;
create or replace function public.vos_novo_usuario() returns trigger
language plpgsql security definer set search_path = public as $$
declare c record;
begin
  select * into c from public.vos_convites where lower(email) = lower(new.email) and revogado_em is null and expira_em > now() order by criado_em desc limit 1;
  insert into public.vos_profiles (user_id, email, papel) values (new.id, new.email, coalesce(c.papel, 'PUBLIC')) on conflict (user_id) do nothing;
  if c.id is not null then update public.vos_convites set usado_em = now() where id = c.id; end if;
  return new;
end $$;
create trigger vos_on_auth_user_created after insert on auth.users for each row execute function public.vos_novo_usuario();
