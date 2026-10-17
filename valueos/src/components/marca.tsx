import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";
import { Etiqueta } from "@/components/ui";
import type { Etiqueta as TipoEtiqueta } from "@/lib/etiquetas";

// Peças visuais do memorando (mesma linguagem dos sites originais), sem estado: rodam no servidor.

export function Conteiner({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`mx-auto w-full max-w-6xl px-5 sm:px-8 ${className}`}>{children}</div>;
}

export function Faixa({ id, children, className = "" }: { id?: string; children: ReactNode; className?: string }) {
  return (
    <section id={id} className={`scroll-mt-20 py-16 sm:py-24 ${className}`}>
      <Conteiner>{children}</Conteiner>
    </section>
  );
}

// A etiqueta verde-menta dos capítulos ("CARTA DO FUNDADOR", "CAPÍTULO 1").
export function Tag({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-md bg-pill px-2.5 py-1 text-xs font-normal uppercase tracking-wide text-black">
      {children}
    </span>
  );
}

export function Titulo({
  tag,
  children,
  sub,
  verde,
  className = "",
}: {
  tag?: ReactNode;
  children: ReactNode;
  sub?: ReactNode;
  verde?: boolean;
  className?: string;
}) {
  return (
    <div className={`max-w-4xl ${className}`}>
      {tag && <Tag>{tag}</Tag>}
      <h2 className={`mt-3 font-display text-3xl font-light leading-tight sm:text-[2.6rem] ${verde ? "text-accent" : "text-white"}`}>{children}</h2>
      {sub && <p className="mt-2 font-display text-xl font-light text-white/90 sm:text-2xl">{sub}</p>}
    </div>
  );
}

export function Texto({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`prosa max-w-4xl text-base ${className}`}>{children}</div>;
}

// Abertura de capítulo com imagem: ao fundo (escurecida) ou dividida (imagem de um lado, texto do outro).
export function Capitulo({
  id,
  numero,
  titulo,
  sub,
  imagem,
  lado = "fundo",
  verde,
  children,
}: {
  id?: string;
  numero: string;
  titulo: ReactNode;
  sub?: ReactNode;
  imagem: string;
  lado?: "fundo" | "esquerda" | "direita";
  verde?: boolean;
  children?: ReactNode;
}) {
  const cabeca = (
    <>
      <Tag>{numero}</Tag>
      <h2 className={`mt-4 font-display text-4xl font-light leading-[1.1] sm:text-6xl ${verde ? "text-accent" : "text-white"}`}>{titulo}</h2>
      {sub && <p className="mt-3 font-display text-2xl font-light leading-snug text-white sm:text-3xl">{sub}</p>}
      {children && <div className="prosa mt-6 max-w-2xl text-base">{children}</div>}
    </>
  );
  if (lado === "fundo") {
    return (
      <section id={id} className="relative isolate flex min-h-[78vh] scroll-mt-20 items-center overflow-hidden">
        <Image src={imagem} alt="" fill sizes="100vw" className="-z-10 object-cover" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-black/95 via-black/80 to-black/55" aria-hidden />
        <Conteiner className="py-24">{cabeca}</Conteiner>
      </section>
    );
  }
  return (
    <section
      id={id}
      className={`grid min-h-[78vh] scroll-mt-20 ${lado === "direita" ? "lg:grid-cols-[minmax(0,62%)_minmax(0,38%)]" : "lg:grid-cols-[minmax(0,38%)_minmax(0,62%)]"}`}
    >
      <div className={`relative min-h-[46vh] ${lado === "direita" ? "lg:order-2" : ""}`}>
        <Image src={imagem} alt="" fill sizes="(min-width:1024px) 38vw, 100vw" className="object-cover" />
      </div>
      <div className={`flex items-center bg-[#070707] px-5 py-16 sm:px-12 lg:px-16 ${lado === "direita" ? "lg:order-1" : ""}`}>
        <div className="max-w-2xl">{cabeca}</div>
      </div>
    </section>
  );
}

type Tom = "verde" | "lateral" | "cinza" | "escuro" | "azul" | "cheio";

export function Cartao({
  titulo,
  tom = "verde",
  icone,
  children,
  rodape,
  className = "",
}: {
  titulo?: ReactNode;
  tom?: Tom;
  icone?: ReactNode;
  children?: ReactNode;
  rodape?: ReactNode;
  className?: string;
}) {
  const estilo: Record<Tom, string> = {
    verde: "border-2 border-accent bg-black",
    lateral: "border-2 border-l-[7px] border-accent bg-black",
    cinza: "bg-cinza/85",
    escuro: "bg-surface",
    azul: "border-2 border-info bg-black",
    cheio: "bg-accent text-accent-ink",
  };
  const corTitulo = tom === "cheio" ? "text-accent-ink font-normal" : tom === "azul" ? "text-info" : tom === "cinza" ? "text-accent" : "text-accent";
  return (
    <div className={`flex flex-col rounded-lg p-6 ${estilo[tom]} ${className}`}>
      {icone && (
        <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-full ${tom === "cinza" ? "bg-black text-white" : "text-accent"}`}>{icone}</div>
      )}
      {titulo && <h3 className={`font-display text-xl font-light leading-snug ${corTitulo}`}>{titulo}</h3>}
      {children && (
        <div className={`mt-2 flex-1 text-[15px] font-light leading-relaxed ${tom === "cheio" ? "text-accent-ink" : "text-texto"}`}>{children}</div>
      )}
      {rodape && <div className="mt-4 border-t border-white/10 pt-3 text-sm">{rodape}</div>}
    </div>
  );
}

// Cartão com o número no círculo verde sobre a borda (as "12 barreiras").
export function CartaoNumerado({ n, titulo, children }: { n: number; titulo: ReactNode; children: ReactNode }) {
  return (
    <div className="relative mt-6 rounded-lg border-2 border-t-[6px] border-accent bg-black p-6 pt-9">
      <span className="absolute -top-6 left-1/2 flex h-11 w-11 -translate-x-1/2 items-center justify-center rounded-full bg-accent font-display text-lg font-light text-white">
        {n}
      </span>
      <h3 className="font-display text-xl font-light text-accent">{titulo}</h3>
      <div className="mt-2 text-[15px] font-light leading-relaxed text-texto">{children}</div>
    </div>
  );
}

export function Grade({ colunas = 2, children, className = "" }: { colunas?: 2 | 3 | 4; children: ReactNode; className?: string }) {
  const c = { 2: "md:grid-cols-2", 3: "md:grid-cols-2 lg:grid-cols-3", 4: "sm:grid-cols-2 lg:grid-cols-4" }[colunas];
  return <div className={`grid grid-cols-1 gap-5 ${c} ${className}`}>{children}</div>;
}

export function Citacao({ children, verde, className = "" }: { children: ReactNode; verde?: boolean; className?: string }) {
  return (
    <blockquote
      className={`border-l-2 border-white/80 py-3 pl-6 text-base leading-relaxed ${verde ? "font-medium text-accent" : "font-medium text-white"} ${className}`}
    >
      {children}
    </blockquote>
  );
}

export function Nota({ children }: { children: ReactNode }) {
  return <div className="rounded-lg bg-cinza/85 px-5 py-4 text-[15px] font-light leading-relaxed text-white">{children}</div>;
}

export function NumeroGrande({
  valor,
  rotulo,
  sub,
  etiqueta,
  href,
  cor = "branco",
}: {
  valor: ReactNode;
  rotulo: ReactNode;
  sub?: ReactNode;
  etiqueta?: TipoEtiqueta | string;
  href?: string;
  cor?: "branco" | "verde";
}) {
  const corpo = (
    <div className="text-center">
      <p className={`num font-display text-5xl font-light tracking-tight sm:text-6xl ${cor === "verde" ? "text-accent" : "text-white"}`}>{valor}</p>
      <p className="mt-3 font-display text-xl font-light text-accent">{rotulo}</p>
      {sub && <p className="mt-1 text-sm font-light text-muted">{sub}</p>}
      {etiqueta && (
        <div className="mt-3">
          <Etiqueta tipo={etiqueta} pequena />
        </div>
      )}
    </div>
  );
  return href ? (
    <Link href={href} className="block rounded-xl p-2 transition hover:bg-white/[0.03]">
      {corpo}
    </Link>
  ) : (
    corpo
  );
}

// Linha "hoje, no sistema" embaixo de um cartão: o dado atualizado com etiqueta e link para a prova.
export function Hoje({ children, etiqueta = "VERIFIED", href }: { children: ReactNode; etiqueta?: TipoEtiqueta | string; href?: string }) {
  return (
    <div className="flex flex-wrap items-center gap-2 text-sm text-white/90">
      <span className="text-xs font-semibold uppercase tracking-widest text-muted">Hoje</span>
      <span className="font-light">{children}</span>
      <Etiqueta tipo={etiqueta} pequena />
      {href && (
        <Link href={href} className="text-xs text-pill underline underline-offset-2">
          ver prova
        </Link>
      )}
    </div>
  );
}

export function LinhaDoTempo({ itens }: { itens: { quando: string; texto: ReactNode; etiqueta?: TipoEtiqueta | string; novo?: boolean }[] }) {
  return (
    <ol className="relative mt-10 space-y-8 before:absolute before:bottom-0 before:left-[11px] before:top-0 before:w-0.5 before:bg-accent md:before:left-1/2 md:before:-translate-x-1/2">
      {itens.map((item, i) => {
        const direita = i % 2 === 1;
        return (
          <li key={item.quando} className="relative md:grid md:grid-cols-2 md:gap-16">
            <span className="absolute left-[5px] top-7 h-3.5 w-3.5 rounded-full bg-accent md:left-1/2 md:-translate-x-1/2" aria-hidden />
            <div className={`ml-10 md:ml-0 ${direita ? "md:col-start-2" : "md:text-right"}`}>
              <div className={`rounded-lg border p-5 ${item.novo ? "border-pill/70 bg-accent/10" : "border-accent/50 bg-cinza/85"}`}>
                <p className="font-display text-xl font-light text-accent">{item.quando}</p>
                <div className="mt-2 text-[15px] font-light leading-relaxed text-white">{item.texto}</div>
                {(item.etiqueta || item.novo) && (
                  <div className={`mt-3 flex flex-wrap items-center gap-2 ${direita ? "" : "md:justify-end"}`}>
                    {item.novo && <span className="text-xs font-semibold uppercase tracking-widest text-pill">atualização 17/10</span>}
                    {item.etiqueta && <Etiqueta tipo={item.etiqueta} pequena />}
                  </div>
                )}
              </div>
            </div>
          </li>
        );
      })}
    </ol>
  );
}

// Trajetória: linha horizontal com marcos acima e abaixo (vira lista no celular).
export function Trajetoria({ itens }: { itens: { titulo: string; texto: string }[] }) {
  return (
    <div className="mt-10">
      <ol className="space-y-6 md:hidden">
        {itens.map((i) => (
          <li key={i.titulo} className="border-l-2 border-accent pl-5">
            <p className="font-display text-xl font-light text-accent">{i.titulo}</p>
            <p className="mt-1 text-[15px] font-light text-texto">{i.texto}</p>
          </li>
        ))}
      </ol>
      <div className="relative hidden md:block">
        <div className="grid grid-cols-4 gap-6">
          {itens.map((i, k) => (
            <div key={i.titulo} className={`flex flex-col items-center text-center ${k % 2 === 0 ? "" : "invisible"}`}>
              <p className="font-display text-xl font-light text-accent">{i.titulo}</p>
              <p className="mt-2 text-[15px] font-light text-texto">{i.texto}</p>
              <span className="mt-4 h-8 w-0.5 bg-accent" />
            </div>
          ))}
        </div>
        <div className="relative h-4">
          <div className="absolute inset-x-0 top-1/2 h-0.5 -translate-y-1/2 bg-accent" />
          <div className="relative grid h-full grid-cols-4 gap-6">
            {itens.map((i) => (
              <span key={i.titulo} className="mx-auto h-3.5 w-3.5 self-center rounded-full bg-accent" />
            ))}
          </div>
        </div>
        <div className="grid grid-cols-4 gap-6">
          {itens.map((i, k) => (
            <div key={i.titulo} className={`flex flex-col items-center text-center ${k % 2 === 1 ? "" : "invisible"}`}>
              <span className="mb-4 h-8 w-0.5 bg-accent" />
              <p className="font-display text-xl font-light text-accent">{i.titulo}</p>
              <p className="mt-2 text-[15px] font-light text-texto">{i.texto}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// "A infraestrutura que faltava": faixas em forma de seta, cada uma um pouco maior.
export function Setas({ itens }: { itens: string[] }) {
  return (
    <div className="mt-10 space-y-4">
      {itens.map((t, i) => (
        <div
          key={t}
          className="seta-faixa flex min-h-[4.5rem] items-center bg-[#f2f2f2] py-4 pl-8 pr-16 font-display text-lg font-normal text-black sm:text-2xl"
          style={{ width: `${Math.min(100, 70 + i * (30 / Math.max(1, itens.length - 1)))}%` }}
        >
          {t}
        </div>
      ))}
    </div>
  );
}

// Gráfico de barras com escala honesta (começa no zero), linhas de grade e valor em cada barra.
export function GraficoBarras({
  dados,
  formato,
  titulo,
  altura = 320,
  className = "",
}: {
  dados: { rotulo: string; valor: number | null; tom: "gestao" | "verificado" | "projecao" }[];
  formato: (v: number) => string;
  titulo?: string;
  altura?: number;
  className?: string;
}) {
  // Régua com passos redondos (1, 2, 2,5 ou 5 × potência de 10), começando sempre no zero.
  const max = Math.max(1, ...dados.map((d) => d.valor ?? 0));
  const bruto = (max * 1.08) / 4;
  const mag = Math.pow(10, Math.floor(Math.log10(bruto)));
  const norm = bruto / mag;
  const passo = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10) * mag;
  const topo = passo * Math.ceil((max * 1.08) / passo);
  const linhas = Array.from({ length: Math.round(topo / passo) + 1 }, (_, i) => i * passo);
  // Largura lógica proporcional ao número de barras; abaixo de 70% dela o gráfico rola sozinho (texto nunca menor que 12px).
  const W = Math.max(520, dados.length * 120);
  const H = altura;
  const esq = 64;
  const base = H - 40;
  const larg = (W - esq - 20) / dados.length;
  const cor = { gestao: "#a1a1aa", verificado: "#00b86b", projecao: "#22a6f2" };
  return (
    <figure className={`mt-6 min-w-0 ${className}`}>
      {titulo && <figcaption className="mb-2 text-sm font-medium text-white">{titulo}</figcaption>}
      <div className="overflow-x-auto">
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ minWidth: Math.round(W * 0.7) }} role="img" aria-label={titulo ?? "gráfico"}>
        <rect x={esq} y={10} width={W - esq - 10} height={base - 10} fill="none" stroke="#3f3f46" strokeDasharray="5 5" rx="8" />
        {linhas.map((v) => {
          const y = base - (v / topo) * (base - 20);
          return (
            <g key={v}>
              <line x1={esq} x2={W - 10} y1={y} y2={y} stroke="#3f3f46" strokeDasharray="5 5" />
              <text x={esq - 10} y={y + 5} textAnchor="end" fontSize="17" fill="#d4d4d8">
                {formato(v)}
              </text>
            </g>
          );
        })}
        {dados.map((d, i) => {
          const h = d.valor === null ? 0 : (d.valor / topo) * (base - 20);
          const x = esq + i * larg + larg * 0.15;
          const w = larg * 0.7;
          return (
            <g key={d.rotulo}>
              {d.valor === null ? (
                <rect x={x} y={base - 40} width={w} height={40} fill="none" stroke="#52525b" strokeDasharray="4 4" rx="6" />
              ) : (
                <rect x={x} y={base - h} width={w} height={Math.max(2, h)} fill={cor[d.tom]} opacity={d.tom === "gestao" ? 0.55 + (0.4 * i) / dados.length : 1} rx="6" />
              )}
              <text x={x + w / 2} y={d.valor === null ? base - 15 : base - h - 10} textAnchor="middle" fontSize="18" fontWeight="600" fill="#f4f4f5">
                {d.valor === null ? "—" : formato(d.valor)}
              </text>
              <text x={x + w / 2} y={H - 12} textAnchor="middle" fontSize="18" fill="#f4f4f5">
                {d.rotulo}
              </text>
            </g>
          );
        })}
      </svg>
      </div>
    </figure>
  );
}

// Ciclo virtuoso: anel em seis partes, verde e azul, com os nomes ao redor.
export function Ciclo({ itens }: { itens: { titulo: string; texto: string; icone: ReactNode }[] }) {
  const n = itens.length;
  const R = 150;
  const r = 80;
  const cx = 200;
  const cy = 200;
  const arco = (i: number) => {
    const g = 3;
    const a0 = ((i * 360) / n - 90 + g) * (Math.PI / 180);
    const a1 = (((i + 1) * 360) / n - 90 - g) * (Math.PI / 180);
    const p = (rad: number, a: number) => `${cx + rad * Math.cos(a)} ${cy + rad * Math.sin(a)}`;
    return `M ${p(R, a0)} A ${R} ${R} 0 0 1 ${p(R, a1)} L ${p(r, a1)} A ${r} ${r} 0 0 0 ${p(r, a0)} Z`;
  };
  return (
    <div className="mt-10 grid items-center gap-8 lg:grid-cols-[1fr_auto_1fr]">
      <ul className="order-2 space-y-8 lg:order-1 lg:text-right">
        {itens.filter((_, i) => i >= n / 2).reverse().map((i) => (
          <li key={i.titulo}>
            <p className="font-display text-xl font-light text-white">{i.titulo}</p>
            <p className="text-[15px] font-light text-texto">{i.texto}</p>
          </li>
        ))}
      </ul>
      <div className="relative order-1 mx-auto h-[300px] w-[300px] sm:h-[400px] sm:w-[400px] lg:order-2">
        <svg viewBox="0 0 400 400" className="h-full w-full" aria-hidden>
          {itens.map((_, i) => (
            <path key={i} d={arco(i)} fill={i % 2 === 0 ? "#00b86b" : "#22a6f2"} />
          ))}
        </svg>
        {itens.map((it, i) => {
          const a = (((i + 0.5) * 360) / n - 90) * (Math.PI / 180);
          const rad = (R + r) / 2;
          return (
            <span
              key={it.titulo}
              className="absolute -translate-x-1/2 -translate-y-1/2 text-white"
              style={{ left: `${((cx + rad * Math.cos(a)) / 400) * 100}%`, top: `${((cy + rad * Math.sin(a)) / 400) * 100}%` }}
            >
              {it.icone}
            </span>
          );
        })}
      </div>
      <ul className="order-3 space-y-8">
        {itens.filter((_, i) => i < n / 2).map((i) => (
          <li key={i.titulo}>
            <p className="font-display text-xl font-light text-white">{i.titulo}</p>
            <p className="text-[15px] font-light text-texto">{i.texto}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function Imagem({ src, alt, className = "", prioridade }: { src: string; alt: string; className?: string; prioridade?: boolean }) {
  return (
    <div className={`relative overflow-hidden rounded-lg ${className}`}>
      <Image src={src} alt={alt} fill sizes="(min-width:1024px) 1100px, 100vw" className="object-cover" priority={prioridade} />
    </div>
  );
}
