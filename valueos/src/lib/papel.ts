import { cache } from "react";
import { criarClienteServidor } from "@/lib/supabase/server";

// Papel de quem está logado (INVESTOR, BOARD, ADMIN). Uma consulta por requisição.
export const papelAtual = cache(async (): Promise<string | null> => {
  if (process.env.NODE_ENV === "development" && process.env.VALUEOS_PREVIA === "1") return process.env.VALUEOS_PREVIA_PAPEL ?? "INVESTOR";
  const supabase = await criarClienteServidor();
  const { data } = await supabase.from("vos_profiles").select("papel").maybeSingle();
  return data?.papel ?? null;
});

// Conselho e administração veem a camada de revisão (auditoria, divergências, consultas).
export function eConselho(papel: string | null) {
  return papel === "BOARD" || papel === "ADMIN";
}
