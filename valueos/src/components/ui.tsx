import Link from "next/link";
import type { ReactNode } from "react";
import { ETIQUETA, type Etiqueta as TipoEtiqueta } from "@/lib/etiquetas";

// Peças que se repetem em todas as telas do portal. Sem estado: funcionam no servidor.

export function Etiqueta({ tipo, pequena }: { tipo: TipoEtiqueta | string; pequena?: boolean }) {
  const et = ETIQUETA[(tipo as TipoEtiqueta) in ETIQUETA ? (tipo as TipoEtiqueta) : "NAO_DISPONIVEL"];
  return (
    <span
      className={`inline-block whitespace-nowrap rounded-full font-semibold ${pequena ? "px-1.5 py-0.5 text-xs" : "px-2 py-0.5 text-xs"} ${et.classe}`}
    >
      {et.texto}
    </span>
  );
}

// Selo especial: o único número que não entra como dado, mas como referência declarada.
export function SeloReferencia() {
  return (
    <span className="inline-block whitespace-nowrap rounded-full bg-warn/15 px-2 py-0.5 text-xs font-semibold text-warn">
      REFERÊNCIA DO FUNDADOR
    </span>
  );
}

export function Numero({
  rotulo,
  valor,
  etiqueta,
  origem,
  href,
  grande,
}: {
  rotulo: string;
  valor: string;
  etiqueta?: TipoEtiqueta | string;
  origem?: string;
  href?: string;
  grande?: boolean;
}) {
  const conteudo = (
    <>
      <p className="text-xs uppercase tracking-widest text-muted">{rotulo}</p>
      <p className={`num mt-2 font-display font-light ${grande ? "text-4xl sm:text-5xl" : "text-3xl"}`}>{valor}</p>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        {etiqueta && <Etiqueta tipo={etiqueta} pequena />}
        {origem && <span className="text-xs text-muted">{origem}</span>}
      </div>
    </>
  );
  const classe = "block rounded-2xl border border-border bg-surface p-5";
  return href ? (
    <Link href={href} className={`${classe} transition hover:border-accent/60`}>
      {conteudo}
    </Link>
  ) : (
    <div className={classe}>{conteudo}</div>
  );
}

export function Pagina({
  sobretitulo,
  titulo,
  descricao,
  children,
}: {
  sobretitulo?: string;
  titulo: string;
  descricao?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <div className="mx-auto w-full max-w-6xl space-y-10 px-5 py-12 sm:px-8 sm:py-16">
      <header className="max-w-3xl">
        {sobretitulo && (
          <span className="inline-block rounded-md bg-pill px-2.5 py-1 text-xs uppercase tracking-wide text-black">{sobretitulo}</span>
        )}
        <h1 className="mt-3 font-display text-4xl font-light leading-tight sm:text-5xl">{titulo}</h1>
        {descricao && <div className="mt-3 text-base text-muted">{descricao}</div>}
      </header>
      {children}
    </div>
  );
}

export function Secao({
  id,
  sobretitulo,
  titulo,
  descricao,
  children,
}: {
  id?: string;
  sobretitulo?: string;
  titulo: string;
  descricao?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-24 space-y-5">
      <div className="max-w-3xl">
        {sobretitulo && <p className="text-xs font-semibold uppercase tracking-widest text-muted">{sobretitulo}</p>}
        <h2 className="mt-1 font-display text-2xl font-light leading-snug sm:text-3xl">{titulo}</h2>
        {descricao && <div className="mt-2 text-sm text-muted">{descricao}</div>}
      </div>
      {children}
    </section>
  );
}

export function Cartao({
  titulo,
  children,
  destaque,
  className = "",
}: {
  titulo?: ReactNode;
  children: ReactNode;
  destaque?: boolean;
  className?: string;
}) {
  return (
    <div className={`min-w-0 rounded-2xl border p-5 ${destaque ? "border-accent/40 bg-accent/5" : "border-border bg-surface"} ${className}`}>
      {titulo && <p className="mb-2 font-display text-lg font-light text-accent">{titulo}</p>}
      <div className="text-sm">{children}</div>
    </div>
  );
}

export function Grade({ colunas = 3, children }: { colunas?: 2 | 3 | 4; children: ReactNode }) {
  const c = { 2: "sm:grid-cols-2", 3: "sm:grid-cols-2 lg:grid-cols-3", 4: "sm:grid-cols-2 lg:grid-cols-4" }[colunas];
  return <div className={`grid grid-cols-1 gap-4 ${c}`}>{children}</div>;
}

export function Aviso({
  tipo = "info",
  titulo,
  children,
}: {
  tipo?: "info" | "atencao" | "regra";
  titulo?: string;
  children: ReactNode;
}) {
  const estilo = {
    info: "border-info/40 bg-info/5",
    atencao: "border-warn/40 bg-warn/5",
    regra: "border-accent/40 bg-accent/5",
  }[tipo];
  return (
    <div className={`rounded-xl border px-4 py-3 text-sm ${estilo}`}>
      {titulo && <p className="font-semibold">{titulo}</p>}
      <div className={titulo ? "mt-1 text-muted" : ""}>{children}</div>
    </div>
  );
}

// Gráfico de barras simples, em CSS, com zero de verdade. Cada barra pode ter etiqueta própria.
export function Barras({
  dados,
  formato,
  altura = 160,
}: {
  dados: { rotulo: string; valor: number | null; etiqueta?: TipoEtiqueta | string }[];
  formato: (v: number) => string;
  altura?: number;
}) {
  const max = Math.max(1, ...dados.map((d) => d.valor ?? 0));
  return (
    <div className="overflow-x-auto">
      <div className="flex min-w-[420px] items-end gap-2" style={{ height: altura }}>
        {dados.map((d) => {
          const h = d.valor === null ? 0 : Math.max(2, Math.round(((d.valor ?? 0) / max) * (altura - 48)));
          const cor =
            d.etiqueta === "VERIFIED" ? "bg-accent" : d.etiqueta === "FORECAST" ? "bg-info/70" : d.etiqueta === "AI_ASSUMPTION" ? "bg-danger/60" : "bg-warn/70";
          return (
            <div key={d.rotulo} className="flex flex-1 flex-col items-center justify-end gap-1">
              <span className="num text-xs text-muted">{d.valor === null ? "—" : formato(d.valor)}</span>
              <div
                className={`w-full rounded-t ${d.valor === null ? "border border-dashed border-border" : cor}`}
                style={{ height: d.valor === null ? 24 : h }}
                aria-label={`${d.rotulo}: ${d.valor === null ? "não disponível" : formato(d.valor)}`}
              />
              <span className="text-xs text-muted">{d.rotulo}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function LinhaDoTempo({
  itens,
}: {
  itens: { quando: string; titulo: string; texto: ReactNode; etiqueta?: TipoEtiqueta | string }[];
}) {
  return (
    <ol className="relative space-y-6 border-l border-border pl-6">
      {itens.map((i) => (
        <li key={i.quando + i.titulo} className="relative">
          <span className="absolute -left-[31px] top-1.5 h-2.5 w-2.5 rounded-full bg-accent" aria-hidden />
          <p className="text-xs font-semibold uppercase tracking-widest text-muted">{i.quando}</p>
          <p className="mt-1 font-semibold">{i.titulo}</p>
          <div className="mt-1 text-sm text-muted">{i.texto}</div>
          {i.etiqueta && (
            <div className="mt-2">
              <Etiqueta tipo={i.etiqueta} pequena />
            </div>
          )}
        </li>
      ))}
    </ol>
  );
}

// Tabela genérica: cabeçalho e linhas já prontas.
export function Tabela({ cabecalho, linhas }: { cabecalho: ReactNode[]; linhas: ReactNode[][] }) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-border bg-surface">
      <table className="w-full text-sm">
        <thead className="text-left text-xs uppercase text-muted">
          <tr>
            {cabecalho.map((c, i) => (
              <th key={i} className="px-4 py-3 font-semibold">
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {linhas.map((l, i) => (
            <tr key={i} className="border-t border-border align-top">
              {l.map((c, j) => (
                <td key={j} className="px-4 py-3">
                  {c}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Nota de revisão: só o conselho e a administração veem o que foi mudado em relação ao site público.
export function NotaRevisao({ conselho, itens }: { conselho: boolean; itens: ReactNode[] }) {
  if (!conselho || itens.length === 0) return null;
  return (
    <details className="rounded-xl border border-warn/30 bg-warn/5 px-4 py-3 text-sm">
      <summary className="flex items-center gap-2 font-semibold text-warn">
        <span className="seta inline-block transition" aria-hidden>
          ▸
        </span>
        Nota de revisão (visível só para conselho e administração)
      </summary>
      <ul className="mt-3 list-disc space-y-1 pl-5 text-muted">
        {itens.map((i, k) => (
          <li key={k}>{i}</li>
        ))}
      </ul>
    </details>
  );
}

export function Legenda() {
  return (
    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-muted">
      <span className="font-semibold uppercase tracking-widest">Como ler as etiquetas</span>
      <span className="flex items-center gap-1.5"><Etiqueta tipo="VERIFIED" pequena /> recalculado do banco do app ou conferido em extrato</span>
      <span className="flex items-center gap-1.5"><Etiqueta tipo="MANAGEMENT_DATA" pequena /> informado pela administração, sem rastro no sistema</span>
      <span className="flex items-center gap-1.5"><Etiqueta tipo="FORECAST" pequena /> meta ou projeção declarada</span>
      <span className="flex items-center gap-1.5"><Etiqueta tipo="AI_ASSUMPTION" pequena /> estimativa do sistema</span>
      <span className="flex items-center gap-1.5"><Etiqueta tipo="NAO_DISPONIVEL" pequena /> o dado não existe ainda — e dizemos por quê</span>
    </div>
  );
}

export const brl = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
export const brlMil = (v: number) => `R$ ${(v / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} mil`;
export const inteiro = (v: number) => v.toLocaleString("pt-BR");
