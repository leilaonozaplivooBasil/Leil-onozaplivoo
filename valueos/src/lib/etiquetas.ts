// Etiquetas de qualidade do dado, iguais em todas as telas.
export const ETIQUETA = {
  VERIFIED: { texto: "VERIFICADO", classe: "border border-accent/60 bg-accent/10 text-pill" },
  MANAGEMENT_DATA: { texto: "DADO DA ADMINISTRAÇÃO", classe: "border border-warn/60 bg-warn/10 text-warn" },
  FORECAST: { texto: "PROJEÇÃO", classe: "border border-info/60 bg-info/10 text-info" },
  AI_ASSUMPTION: { texto: "PREMISSA", classe: "border border-danger/60 bg-danger/10 text-danger" },
  NAO_DISPONIVEL: { texto: "NÃO DISPONÍVEL", classe: "border border-muted/50 bg-muted/10 text-muted" },
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
