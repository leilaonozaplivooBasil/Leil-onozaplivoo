"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export const ITENS = [
  { href: "/app", rotulo: "Visão geral", tempo: "30 s" },
  { href: "/app/memorando", rotulo: "Memorando", tempo: "1 min" },
  { href: "/app/numeros", rotulo: "Números com prova", tempo: "5 min" },
  { href: "/app/dre", rotulo: "DRE", tempo: "5 min" },
  { href: "/app/parceiros", rotulo: "Parceiros de compra", tempo: "5 min" },
  { href: "/app/riscos", rotulo: "Riscos", tempo: "5 min" },
  { href: "/app/valuation", rotulo: "Valuation", tempo: "30 min" },
  { href: "/app/governanca", rotulo: "Governança e time", tempo: "30 min" },
  { href: "/app/roadmap", rotulo: "Metas e simulação", tempo: "30 min" },
  { href: "/app/dataroom", rotulo: "Data room", tempo: "30 min" },
  { href: "/app/cargas", rotulo: "Cargas", tempo: "30 min" },
];

// Navegação do portal: coluna na tela grande, faixa rolável no celular.
export function Navegacao({ horizontal }: { horizontal?: boolean }) {
  const caminho = usePathname();
  const ativo = (href: string) => (href === "/app" ? caminho === "/app" : caminho.startsWith(href));
  if (horizontal) {
    return (
      <nav aria-label="Seções" className="flex gap-1 overflow-x-auto px-4 py-2 text-sm">
        {ITENS.map((i) => (
          <Link
            key={i.href}
            href={i.href}
            className={`whitespace-nowrap rounded-full px-3 py-1.5 ${ativo(i.href) ? "bg-accent/15 font-semibold text-accent" : "text-muted hover:text-foreground"}`}
            aria-current={ativo(i.href) ? "page" : undefined}
          >
            {i.rotulo}
          </Link>
        ))}
      </nav>
    );
  }
  // Mostra o título do grupo ("30 s", "1 min"…) só no primeiro item de cada grupo.
  const comGrupo = ITENS.map((i, k) => ({ ...i, mostraTempo: k === 0 || ITENS[k - 1].tempo !== i.tempo }));
  return (
    <nav aria-label="Seções" className="space-y-1 text-sm">
      {comGrupo.map((i) => {
        const mostraTempo = i.mostraTempo;
        return (
          <div key={i.href}>
            {mostraTempo && (
              <p className="mb-1 mt-4 px-3 text-[11px] font-semibold uppercase tracking-widest text-muted first:mt-0">
                {i.tempo}
              </p>
            )}
            <Link
              href={i.href}
              className={`block rounded-lg px-3 py-2 ${ativo(i.href) ? "bg-accent/15 font-semibold text-accent" : "text-muted hover:bg-surface-2 hover:text-foreground"}`}
              aria-current={ativo(i.href) ? "page" : undefined}
            >
              {i.rotulo}
            </Link>
          </div>
        );
      })}
    </nav>
  );
}
