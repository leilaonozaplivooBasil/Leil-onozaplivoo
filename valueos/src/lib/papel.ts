import { cache } from "react";
import { criarClienteServidor } from "@/lib/supabase/server";

// Papel de quem está logado (INVESTOR, BOARD, ADMIN). Uma consulta por requisição.
export const papelAtual = cache(async (): Promise<string | null> => {
  const supabase = await criarClienteServidor();
  const { data } = await supabase.from("vos_profiles").select("papel").maybeSingle();
  return data?.papel ?? null;
});

// Conselho e administração veem a camada de revisão (auditoria, divergências, consultas).
export function eConselho(papel: string | null) {
  return papel === "BOARD" || papel === "ADMIN";
}
