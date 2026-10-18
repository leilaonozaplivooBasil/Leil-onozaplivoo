"use client";

import { useState } from "react";

// Simulação por alavancas. Não é projeção oficial nem valuation: serve para ver o que precisa ser verdade.
type Entradas = {
  licenciados: number;
  vendasPorLicenciado: number;
  ticket: number;
  margem: number;
  comissao: number;
  despesas: number;
  parceiros: number;
};

const brl = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });

export function Simulador({ inicial }: { inicial: Entradas }) {
  const [e, setE] = useState<Entradas>(inicial);
  const gmv = e.licenciados * e.vendasPorLicenciado * e.ticket;
  const lucroBruto = gmv * (e.margem / 100);
  const comissoes = gmv * (e.comissao / 100);
  const resultado = lucroBruto - comissoes - e.despesas - e.parceiros;
  const precisaLicenciados = e.vendasPorLicenciado * e.ticket > 0 ? Math.ceil(1_000_000 / (e.vendasPorLicenciado * e.ticket)) : 0;

  const campo = (
    chave: keyof Entradas,
    rotulo: string,
    min: number,
    max: number,
    passo: number,
    formato: (v: number) => string,
    nota: string,
  ) => (
    <label className="block text-sm">
      <span className="flex items-baseline justify-between gap-2">
        <span>{rotulo}</span>
        <span className="num font-semibold">{formato(e[chave])}</span>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={passo}
        value={e[chave]}
        onChange={(ev) => setE({ ...e, [chave]: Number(ev.target.value) })}
        className="mt-1 w-full accent-[var(--accent)]"
        aria-label={rotulo}
      />
      <span className="text-xs text-muted">{nota}</span>
    </label>
  );

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="space-y-5 rounded-2xl border border-border bg-surface p-5">
        {campo("licenciados", "Licenciados ativos", 0, 1000, 1, (v) => v.toString(), "hoje: 8 com acesso em 30 dias · meta dez/26: 300")}
        {campo("vendasPorLicenciado", "Vendas pagas por licenciado, por mês", 0, 60, 1, (v) => v.toString(), "premissa — o app ainda não liga venda a licenciado de forma auditável")}
        {campo("ticket", "Ticket médio (R$)", 50, 2000, 10, brl, "premissa — mercadoria vendida em out/26: R$ 14,3 mil até o dia 16")}
        {campo("margem", "Margem bruta sobre a venda (%)", 0, 60, 1, (v) => `${v}%`, "premissa — aproximação medida na loja: +6% a +15%; custo por venda não é gravado")}
        {campo("comissao", "Comissão paga à rede (%)", 0, 40, 1, (v) => `${v}%`, "código do app: licenciado 3–6%, vendedor 10%, loja ~11%, distribuidor até 20%")}
        {campo("despesas", "Despesas fixas por mês (R$)", 0, 300_000, 1000, brl, "despesas pagas em out/26 (lançamento manual): R$ 53,3 mil")}
        {campo("parceiros", "Remuneração dos parceiros de compra (R$/mês)", 0, 50_000, 500, brl, "capital de terceiros hoje: R$ 14.600 (parceiros A e B R$ 10.500 + investidores R$ 4.100)")}
      </div>
      <div className="space-y-4">
        <div className="rounded-2xl border border-danger/40 bg-danger/5 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-danger">
          Simulação com premissas · não é projeção oficial nem valuation
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <Saida rotulo="Mercadoria vendida por mês" valor={brl(gmv)} />
          <Saida rotulo="Lucro bruto" valor={brl(lucroBruto)} />
          <Saida rotulo="Comissões da rede" valor={`− ${brl(comissoes)}`} />
          <Saida rotulo="Despesas + parceiros" valor={`− ${brl(e.despesas + e.parceiros)}`} />
          <Saida rotulo="Resultado antes de impostos" valor={brl(resultado)} destaque negativo={resultado < 0} />
          <Saida rotulo="Licenciados para R$ 1 mi/mês com estas premissas" valor={precisaLicenciados ? precisaLicenciados.toLocaleString("pt-BR") : "—"} />
        </div>
        <p className="text-xs text-muted">
          A conta é simples de propósito: licenciados × vendas × ticket = mercadoria vendida; margem e comissão são percentuais sobre ela;
          despesas e parceiros são fixos. Impostos ficam de fora (PGDAS/DAS de 2026 não disponíveis). Mexa nas alavancas e veja o que precisa
          ser verdade — o valuation não entra aqui.
        </p>
      </div>
    </div>
  );
}

function Saida({ rotulo, valor, destaque, negativo }: { rotulo: string; valor: string; destaque?: boolean; negativo?: boolean }) {
  return (
    <div className={`rounded-2xl border p-4 ${destaque ? (negativo ? "border-danger/40 bg-danger/5" : "border-accent/40 bg-accent/5") : "border-border bg-surface"}`}>
      <p className="text-xs uppercase tracking-widest text-muted">{rotulo}</p>
      <p className={`num mt-1 text-xl font-semibold ${negativo ? "text-danger" : ""}`}>{valor}</p>
    </div>
  );
}
