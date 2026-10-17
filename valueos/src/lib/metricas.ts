import { readFile } from "node:fs/promises";
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
// Prévia visual local (só em desenvolvimento): lê os valores de um arquivo em vez do banco.
export const emPrevia = () => process.env.NODE_ENV === "development" && process.env.VALUEOS_PREVIA === "1";

type Linha = { metric_id: string; periodo: string; valor: number | string | null; etiqueta: string | null; fonte: string; nota: string | null };

async function linhas(): Promise<Linha[]> {
  if (emPrevia() && process.env.VALUEOS_PREVIA_DADOS) {
    const todas = JSON.parse(await readFile(process.env.VALUEOS_PREVIA_DADOS, "utf8")) as Linha[];
    return todas.sort((a, b) => b.periodo.localeCompare(a.periodo));
  }
  const supabase = await criarClienteServidor();
  const { data } = await supabase
    .from("vos_valores")
    .select("metric_id, periodo, valor, etiqueta, fonte, nota")
    .order("periodo", { ascending: false })
    .order("criado_em", { ascending: false });
  return (data ?? []) as Linha[];
}

export const valoresCarregados = cache(async () => {
  const data = await linhas();
  const ultimo = new Map<string, ValorMetrica>();
  const serie = new Map<string, ValorMetrica[]>();
  for (const bruto of data) {
    const v: ValorMetrica = {
      ...bruto,
      valor: bruto.valor === null ? null : Number(bruto.valor),
      etiqueta: (bruto.etiqueta ?? "NAO_DISPONIVEL") as Etiqueta,
    };
    if (!ultimo.has(v.metric_id)) ultimo.set(v.metric_id, v);
    const lista = serie.get(v.metric_id) ?? [];
    // Correção entra como linha nova no mesmo período (o banco só acrescenta): vale a mais recente.
    if (lista.some((x) => x.periodo === v.periodo)) continue;
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
