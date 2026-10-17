import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { NDA_VERSAO } from "@/lib/nda";
import { Navegacao } from "@/components/nav";

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

  let { data: perfil } = await supabase
    .from("vos_profiles")
    .select("papel, nome, email")
    .eq("user_id", user.id)
    .maybeSingle();

  // Conta antiga sem perfil? Se houver convite válido, ativa agora.
  if (!perfil) {
    await supabase.rpc("vos_ativar_convite");
    ({ data: perfil } = await supabase
      .from("vos_profiles")
      .select("papel, nome, email")
      .eq("user_id", user.id)
      .maybeSingle());
  }

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

  const PAPEL: Record<string, string> = { INVESTOR: "investidor", BOARD: "conselho", ADMIN: "administração" };

  return (
    <div className="flex min-h-full flex-1 flex-col">
      <header className="sticky top-0 z-20 border-b border-border bg-background/90 backdrop-blur">
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3">
          <a href="/app" className="block">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-accent">LNZ Value OS</p>
            <p className="text-xs text-muted">Leilão NoZap · área do investidor</p>
          </a>
          <div className="flex items-center gap-4 text-sm">
            <span className="hidden text-muted sm:inline">
              {perfil.nome ?? perfil.email} · {PAPEL[perfil.papel] ?? perfil.papel}
            </span>
            <a href="/sair" className="underline">
              Sair
            </a>
          </div>
        </div>
        <div className="border-t border-border lg:hidden">
          <Navegacao horizontal />
        </div>
      </header>
      <div className="mx-auto flex w-full max-w-7xl flex-1 gap-8 px-4 py-8">
        <aside className="hidden w-56 shrink-0 lg:block">
          <div className="sticky top-24">
            <Navegacao />
          </div>
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>
      <footer className="border-t border-border px-4 py-5 text-center text-xs text-muted">
        Material confidencial, de uso restrito a convidados. Não é oferta pública de valores mobiliários nem promessa
        de retorno. Cada número mostra a origem e a etiqueta de qualidade; o valuation independente só aparece depois
        da metodologia v1.0 travada e do primeiro fechamento oficial.
      </footer>
    </div>
  );
}
