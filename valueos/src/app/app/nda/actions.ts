"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";
import { NDA_TEXTO, NDA_VERSAO, hashDoTexto } from "@/lib/nda";

// Grava o aceite do termo: versão, impressão digital do texto, IP e navegador. Só-acrescenta.
export async function aceitarNda(): Promise<void> {
  const supabase = await criarClienteServidor();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/entrar");

  const h = await headers();
  const ip = h.get("x-forwarded-for")?.split(",")[0]?.trim() ?? null;
  const userAgent = h.get("user-agent") ?? null;

  const { error } = await supabase.from("vos_nda_aceites").insert({
    user_id: user.id,
    versao: NDA_VERSAO,
    hash_texto: await hashDoTexto(NDA_TEXTO),
    ip,
    user_agent: userAgent,
  });
  if (error) redirect("/app/nda?erro=1");
  redirect("/app");
}
