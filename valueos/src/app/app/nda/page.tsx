import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { NDA_TEXTO, NDA_VERSAO } from "@/lib/nda";
import { aceitarNda } from "./actions";

export const dynamic = "force-dynamic";

export default async function Nda({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>;
}) {
  const supabase = await criarClienteServidor();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/entrar");

  const { data: aceite } = await supabase
    .from("vos_nda_aceites")
    .select("id")
    .eq("user_id", user.id)
    .eq("versao", NDA_VERSAO)
    .limit(1);
  if (aceite && aceite.length > 0) redirect("/app");

  const { erro } = await searchParams;

  return (
    <main className="mx-auto w-full max-w-2xl px-4 py-12">
      <p className="text-xs font-semibold uppercase tracking-widest text-accent">
        Antes de entrar
      </p>
      <h1 className="mt-2 text-2xl font-semibold">Termo de sigilo</h1>
      <p className="mt-2 text-sm text-muted">
        Versão {NDA_VERSAO}. O aceite fica registrado com data, hora e endereço
        de rede.
      </p>
      <pre className="mt-6 max-h-[50vh] overflow-auto whitespace-pre-wrap rounded-xl border border-border bg-surface p-5 text-sm leading-relaxed">
        {NDA_TEXTO}
      </pre>
      {erro && (
        <p role="alert" className="mt-4 text-sm text-danger">
          Não foi possível registrar o aceite. Tente de novo.
        </p>
      )}
      <form action={aceitarNda} className="mt-6 flex flex-wrap gap-3">
        <button
          type="submit"
          className="rounded-lg bg-accent px-5 py-2.5 font-semibold text-accent-ink"
        >
          Li e aceito
        </button>
        <a
          href="/sair"
          className="rounded-lg border border-border px-5 py-2.5 text-sm text-muted"
        >
          Não aceito — sair
        </a>
      </form>
    </main>
  );
}
