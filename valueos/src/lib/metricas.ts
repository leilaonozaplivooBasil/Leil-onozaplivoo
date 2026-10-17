import { cache } from "react";
import { criarClienteServidor } from "@/lib/supabase/server";
import type { Etiqueta } from "@/lib/etiquetas";

export type ValorMetrica = {
  metric_id: string;
  periodo: string;
  valor: number | null;
  etiqueta: Etiqueta;
  fonte: string;
  nota: string | null;
};

// Todos os valores carregados, já organizados: o mais recente de cada métrica e a série completa.
export const valoresCarregados = cache(async () => {
  const supabase = await criarClienteServidor();
  const { data } = await supabase
    .from("vos_valores")
    .select("metric_id, periodo, valor, etiqueta, fonte, nota")
    .order("periodo", { ascending: false });
  const ultimo = new Map<string, ValorMetrica>();
  const serie = new Map<string, ValorMetrica[]>();
  for (const bruto of data ?? []) {
    const v: ValorMetrica = {
      ...bruto,
      valor: bruto.valor === null ? null : Number(bruto.valor),
      etiqueta: (bruto.etiqueta ?? "NAO_DISPONIVEL") as Etiqueta,
    };
    if (!ultimo.has(v.metric_id)) ultimo.set(v.metric_id, v);
    const lista = serie.get(v.metric_id) ?? [];
    lista.push(v);
    serie.set(v.metric_id, lista);
  }
  // Série em ordem cronológica.
  for (const lista of serie.values()) lista.reverse();
  return { ultimo, serie };
});

// Atalho: valor mais recente de uma métrica, ou null se não houver carga.
export function pega(ultimo: Map<string, ValorMetrica>, id: string) {
  return ultimo.get(id) ?? null;
}
