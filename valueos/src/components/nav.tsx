"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

type Item = { href: string; rotulo: string };

const PRINCIPAIS: Item[] = [
  { href: "/app", rotulo: "Início" },
  { href: "/app/memorando", rotulo: "Memorando" },
  { href: "/app/valuation", rotulo: "Valuation" },
];
const NUMEROS: Item[] = [
  { href: "/app/numeros", rotulo: "Números com prova" },
  { href: "/app/dre", rotulo: "DRE" },
  { href: "/app/parceiros", rotulo: "Parceiros de compra" },
  { href: "/app/cargas", rotulo: "Cargas de dados" },
];
const DEPOIS: Item[] = [
  { href: "/app/riscos", rotulo: "Riscos" },
  { href: "/app/governanca", rotulo: "Governança" },
  { href: "/app/roadmap", rotulo: "Metas" },
  { href: "/app/dataroom", rotulo: "Data room" },
];
export const TODOS = [...PRINCIPAIS, ...NUMEROS, ...DEPOIS];

function useAtivo() {
  const caminho = usePathname();
  return (href: string) => (href === "/app" ? caminho === "/app" : caminho.startsWith(href));
}

// Fecha o menu aberto quando a página muda.
function useFechaAoNavegar() {
  const ref = useRef<HTMLDetailsElement>(null);
  const caminho = usePathname();
  useEffect(() => {
    if (ref.current) ref.current.open = false;
  }, [caminho]);
  return ref;
}

function Link1({ i, ativo }: { i: Item; ativo: boolean }) {
  return (
    <Link
      href={i.href}
      aria-current={ativo ? "page" : undefined}
      className={`whitespace-nowrap rounded-md px-3 py-2 text-sm transition ${ativo ? "text-pill" : "text-white/80 hover:text-white"}`}
    >
      {i.rotulo}
    </Link>
  );
}

export function Navegacao() {
  const ativo = useAtivo();
  const numeros = useFechaAoNavegar();
  const algumNumero = NUMEROS.some((i) => ativo(i.href));
  return (
    <nav aria-label="Seções" className="hidden items-center gap-0.5 xl:flex">
      {PRINCIPAIS.map((i) => (
        <Link1 key={i.href} i={i} ativo={ativo(i.href)} />
      ))}
      <details ref={numeros} className="relative">
        <summary className={`whitespace-nowrap rounded-md px-3 py-2 text-sm transition ${algumNumero ? "text-pill" : "text-white/80 hover:text-white"}`}>
          Números <span aria-hidden>▾</span>
        </summary>
        <div className="absolute left-0 top-full z-30 mt-2 w-56 rounded-lg border border-border bg-surface p-1 shadow-2xl">
          {NUMEROS.map((i) => (
            <Link
              key={i.href}
              href={i.href}
              aria-current={ativo(i.href) ? "page" : undefined}
              className={`block rounded-md px-3 py-2 text-sm ${ativo(i.href) ? "bg-accent/15 text-pill" : "text-white/85 hover:bg-white/5"}`}
            >
              {i.rotulo}
            </Link>
          ))}
        </div>
      </details>
      {DEPOIS.map((i) => (
        <Link1 key={i.href} i={i} ativo={ativo(i.href)} />
      ))}
    </nav>
  );
}

export function MenuCelular() {
  const ativo = useAtivo();
  const ref = useFechaAoNavegar();
  return (
    <details ref={ref} className="xl:hidden">
      <summary className="rounded-md border border-border px-3 py-2 text-sm text-white">Menu</summary>
      <div className="absolute inset-x-0 top-full z-30 border-b border-border bg-background/98 px-5 py-4 shadow-2xl">
        <ul className="grid grid-cols-2 gap-1">
          {TODOS.map((i) => (
            <li key={i.href}>
              <Link
                href={i.href}
                aria-current={ativo(i.href) ? "page" : undefined}
                className={`block rounded-md px-3 py-2.5 text-sm ${ativo(i.href) ? "bg-accent/15 text-pill" : "text-white/85"}`}
              >
                {i.rotulo}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </details>
  );
}
