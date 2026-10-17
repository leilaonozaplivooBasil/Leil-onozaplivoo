import { valoresCarregados } from "@/lib/metricas";
import { papelAtual, eConselho } from "@/lib/papel";
import { mesCurto } from "@/lib/etiquetas";
import { Aviso, Barras, Cartao, Etiqueta, NotaRevisao, Pagina, Secao, Tabela, brl, brlMil } from "@/components/ui";
import { Simulador } from "./Simulador";

export const dynamic = "force-dynamic";

// Metas declaradas pela administração × o que o sistema mede hoje, e uma simulação por alavancas.
export default async function Roadmap() {
  const [{ ultimo, serie }, papel] = await Promise.all([valoresCarregados(), papelAtual()]);
  const conselho = eConselho(papel);
  const v = (id: string) => ultimo.get(id);
  const entradas = serie.get("CASH_IN_GROSS") ?? [];
  const gmv = serie.get("GMV_GOODS") ?? [];
  const licCargo = v("LICENSEES_TOTAL");
  const licAtivo = v("LICENSEES_ACTIVE_30D");
  const despesas = v("EXPENSES_PAID");
  const ultimoMes = entradas.at(-1);

  const plano = [
    ["Faturamento mensal (dez/2026)", "R$ 1.000.000", ultimoMes?.valor != null ? `${brl(ultimoMes.valor)} de entradas brutas em ${mesCurto(ultimoMes.periodo)} (com depósitos); ${gmv.at(-1)?.valor != null ? brl(gmv.at(-1)!.valor!) : "—"} de mercadoria` : "—", ultimoMes?.valor != null ? `${Math.round((100 * ultimoMes.valor) / 1_000_000)}%` : "—"],
    ["Licenciados ativos (dez/2026)", "300", `${licCargo?.valor ?? "—"} por cargo · ${licAtivo?.valor ?? "—"} com acesso em 30 dias`, licAtivo?.valor != null ? `${Math.round((100 * licAtivo.valor) / 300)}%` : "—"],
    ["Lojas físicas (dez/2026)", "8", "0 registradas no sistema; 1 conta com nível \"loja física\"", "0%"],
    ["Centro de distribuição (Recreio)", "1", "planejado", "—"],
    ["Licenciados (2027)", "1.000", "—", "—"],
    ["Vendedores ativos (2027)", "10.000", "—", "—"],
  ];

  return (
    <Pagina
      sobretitulo="30 minutos"
      titulo="Metas e simulação"
      descricao="O plano da administração ao lado do realizado medido no sistema, e um simulador por alavancas para ver o que precisa ser verdade. Nada aqui é valuation."
    >
      <Secao sobretitulo="Plano × realizado" titulo="Metas declaradas e onde o sistema está hoje">
        <Tabela
          cabecalho={["Meta", "Plano", "Realizado (sistema)", "Avanço"]}
          linhas={plano.map((p) => [
            p[0],
            <span key="p"><span className="num font-semibold">{p[1]}</span> <Etiqueta tipo="FORECAST" pequena /></span>,
            <span key="r" className="text-muted">{p[2]} {p[2] !== "—" && p[2] !== "planejado" && <Etiqueta tipo="VERIFIED" pequena />}</span>,
            <span key="a" className="num">{p[3]}</span>,
          ])}
        />
        <Aviso tipo="info">
          “Avanço” compara o realizado medido com a meta declarada. Entradas brutas incluem depósitos de carteira (que não são receita); por
          isso a linha mostra também a mercadoria vendida. O plano é versionado: toda mudança de meta fica registrada com data.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Série oficial" titulo="O que já aconteceu, mês a mês">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Cartao titulo="Entradas brutas no app (com depósitos)">
            <Barras dados={entradas.map((s) => ({ rotulo: mesCurto(s.periodo), valor: s.valor, etiqueta: s.etiqueta }))} formato={brlMil} />
          </Cartao>
          <Cartao titulo="Mercadoria vendida e paga (sem depósitos)">
            <Barras dados={gmv.map((s) => ({ rotulo: mesCurto(s.periodo), valor: s.valor, etiqueta: s.etiqueta }))} formato={brlMil} />
          </Cartao>
        </div>
        <p className="text-xs text-muted">Outubro vai até o dia 16. A projeção por tendência exige mais meses; por isso o sistema simula por alavancas em vez de extrapolar.</p>
      </Secao>

      <Secao sobretitulo="Simulador" titulo="O que precisa ser verdade">
        <Simulador
          inicial={{
            licenciados: licAtivo?.valor ?? 8,
            vendasPorLicenciado: 5,
            ticket: 350,
            margem: 15,
            comissao: 10,
            despesas: despesas?.valor != null ? Math.round(despesas.valor / 1000) * 1000 : 53_000,
            parceiros: 10_500,
          }}
        />
      </Secao>

      <NotaRevisao
        conselho={conselho}
        itens={[
          "A projeção R$ 12 mi (2026) · R$ 36 mi (2027) · R$ 96 mi (2028) do memorando não fecha com a meta de dez/26 (item 13); aqui aparece só no memorando, com etiqueta de projeção.",
          "Fase 2 (modelo por alavancas completo, cenários salvos, Plan × Actual automático e exportação XLSX) substitui este simulador quando houver custo por venda e 12 meses de série.",
        ]}
      />
    </Pagina>
  );
}
