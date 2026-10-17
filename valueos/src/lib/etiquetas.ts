// Etiquetas de qualidade do dado, iguais em todas as telas.
export const ETIQUETA = {
  VERIFIED: { texto: "VERIFICADO", classe: "bg-accent/15 text-accent" },
  MANAGEMENT_DATA: { texto: "DADO DA ADMINISTRAÇÃO", classe: "bg-warn/15 text-warn" },
  FORECAST: { texto: "PROJEÇÃO", classe: "bg-sky-400/15 text-sky-300" },
  AI_ASSUMPTION: { texto: "PREMISSA", classe: "bg-danger/15 text-danger" },
  NAO_DISPONIVEL: { texto: "NÃO DISPONÍVEL", classe: "bg-muted/15 text-muted" },
} as const;

export type Etiqueta = keyof typeof ETIQUETA;

export function formata(valor: number | null | undefined, unidade: string) {
  if (valor === null || valor === undefined) return "—";
  if (unidade === "BRL")
    return valor.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0,
    });
  if (unidade === "%")
    return `${valor.toLocaleString("pt-BR", { maximumFractionDigits: 1 })}%`;
  return valor.toLocaleString("pt-BR");
}

export function mesCurto(iso: string) {
  return new Date(iso + "T12:00:00").toLocaleDateString("pt-BR", {
    month: "short",
    year: "numeric",
  });
}
