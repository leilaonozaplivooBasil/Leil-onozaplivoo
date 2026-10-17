import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { NDA_VERSAO } from "@/lib/nda";
import Image from "next/image";
import { MenuCelular, Navegacao } from "@/components/nav";

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
      <header className="sticky top-0 z-30 border-b border-white/10 bg-black/85 backdrop-blur-md">
        <div className="relative mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-5 py-3 sm:px-8">
          <a href="/app" className="flex items-center gap-3" aria-label="Leilão NoZap · início do portal">
            <Image src="/m/logo-horizontal.png" alt="Leilão NoZap" width={110} height={40} priority className="h-9 w-auto" />
            <span className="hidden border-l border-white/15 pl-3 text-xs uppercase tracking-[0.18em] text-muted sm:inline">Área do investidor</span>
          </a>
          <Navegacao />
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden text-xs text-muted xl:inline">
              {perfil.nome ?? perfil.email} · {PAPEL[perfil.papel] ?? perfil.papel}
            </span>
            <a href="/sair" className="text-white/80 underline underline-offset-4 hover:text-white">
              Sair
            </a>
            <MenuCelular />
          </div>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      <footer className="border-t border-white/10 px-5 py-8 text-center text-xs leading-relaxed text-muted">
        <p className="mx-auto max-w-3xl">
          Documento confidencial — uso restrito a convidados com termo de sigilo aceito. Não é oferta pública de valores
          mobiliários nem promessa de retorno. Cada número mostra a origem e a etiqueta de qualidade; o valuation independente
          só aparece depois da metodologia v1.0 travada e do primeiro fechamento oficial.
        </p>
      </footer>
    </div>
  );
}
