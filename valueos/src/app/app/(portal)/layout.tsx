import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { NDA_VERSAO } from "@/lib/nda";

export const dynamic = "force-dynamic";

const PAPEIS_COM_ACESSO = ["INVESTOR", "BOARD", "ADMIN"];

// Tudo que está dentro do portal passa por aqui: sessão, papel, termo de sigilo e registro do acesso.
export default async function LayoutPortal({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = await criarClienteServidor();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/entrar");

  const { data: perfil } = await supabase
    .from("vos_profiles")
    .select("papel, nome, email")
    .eq("user_id", user.id)
    .maybeSingle();

  if (!perfil || !PAPEIS_COM_ACESSO.includes(perfil.papel)) {
    return (
      <main className="flex flex-1 items-center justify-center px-4 py-12">
        <div className="max-w-md rounded-2xl border border-border bg-surface p-8 text-center">
          <h1 className="text-xl font-semibold">Acesso ainda não liberado</h1>
          <p className="mt-2 text-sm text-muted">
            Sua conta existe, mas o convite ainda não foi confirmado pelo
            Leilão NoZap. Avise quem te convidou.
          </p>
          <a href="/sair" className="mt-6 inline-block text-sm underline">
            Sair
          </a>
        </div>
      </main>
    );
  }

  const { data: aceite } = await supabase
    .from("vos_nda_aceites")
    .select("id")
    .eq("user_id", user.id)
    .eq("versao", NDA_VERSAO)
    .limit(1);
  if (!aceite || aceite.length === 0) redirect("/app/nda");

  const h = await headers();
  await supabase.from("vos_acessos").insert({
    user_id: user.id,
    rota: h.get("x-invoke-path") ?? "/app",
    ip: h.get("x-forwarded-for")?.split(",")[0]?.trim() ?? null,
    user_agent: h.get("user-agent") ?? null,
  });

  return (
    <div className="flex min-h-full flex-1 flex-col">
      <header className="border-b border-border bg-surface">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-accent">
              LNZ Value OS
            </p>
            <p className="text-xs text-muted">Leilão NoZap · área do investidor</p>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <a href="/app" className="hover:underline">Visão geral</a>
            <a href="/app/dre" className="hover:underline">DRE</a>
            <a href="/app/cargas" className="hover:underline">Cargas</a>
            <span className="hidden text-muted sm:inline">
              {perfil.nome ?? perfil.email} · {perfil.papel}
            </span>
            <a href="/sair" className="underline">
              Sair
            </a>
          </nav>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">{children}</main>
      <footer className="border-t border-border px-4 py-4 text-center text-xs text-muted">
        Material confidencial. Não é oferta pública nem promessa de retorno. Cada
        número mostra a origem e a etiqueta de qualidade.
      </footer>
    </div>
  );
}
