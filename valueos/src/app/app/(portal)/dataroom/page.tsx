import Link from "next/link";
import { papelAtual, eConselho } from "@/lib/papel";
import { Aviso, Cartao, Grade, NotaRevisao, Pagina, Secao, Tabela } from "@/components/ui";

export const dynamic = "force-dynamic";

type Estado = "disponível" | "parcial" | "não disponível";
const COR: Record<Estado, string> = {
  disponível: "bg-accent/15 text-accent",
  parcial: "bg-warn/15 text-warn",
  "não disponível": "bg-muted/15 text-muted",
};

const PASTAS: { pasta: string; itens: [string, Estado, string][] }[] = [
  { pasta: "01 Corporativo", itens: [["Contrato social", "parcial", "versão de 12/08/2025; falta o quadro atual"], ["Cartão CNPJ", "disponível", "porte ME"], ["Atas, organograma", "não disponível", ""]] },
  { pasta: "02 Financeiro", itens: [["Balanço e DRE 2025 (ECD/ECF)", "disponível", "caixa de R$ 705,9 mil não reconciliado"], ["Extratos Mercado Pago jul–out/2026", "disponível", "fecham ao centavo"], ["Extratos Itaú, Santander e Mercado Pago 2026", "disponível", "conciliados de jan a 16/out — R$ 2,7 mi movimentados; 2025 não"], ["Histórico de lotes", "disponível", "6 lotes comprados (7.306 peças) e 33 analisados no app, abr–out/2026"], ["Balancete 2026", "não disponível", ""]] },
  { pasta: "03 Jurídico", itens: [["Contratos de parceiro de compra (A e B)", "disponível", "sem o certificado de conclusão DocuSign"], ["Contrato da venda de 1%", "não disponível", "será assinado após o último R$ 50 mil"], ["Consórcios: relatório de 30/06 e 21 boletos", "parcial", "sem contratos e sem saldo devedor"], ["Litígios", "não disponível", ""]] },
  { pasta: "04 Fiscal", itens: [["PGDAS-D do PA 05/2026", "disponível", "R$ 714 mil declarados de jan a mai/2026; 2025 zerado"], ["Opção pelo Simples 2026", "não disponível", ""], ["DAS pagos 2026, certidões", "não disponível", ""]] },
  { pasta: "05 Tecnologia", itens: [["Arquitetura e medição do código", "disponível", "331 mil linhas, 3.272 arquivos (18/10)"], ["Titularidade do código, contratos de desenvolvimento", "não disponível", ""], ["Licenças de terceiros (Supabase, Vercel, gateway)", "parcial", "lista no estudo"]] },
  { pasta: "06 Contratos", itens: [["Fornecedores, leiloeiros, licenciados, gateway", "não disponível", ""]] },
  { pasta: "07 Propriedade intelectual", itens: [["Marca (INPI), domínios, software", "não disponível", "domínios: leilaonozap.net e os dois .com dos sites"]] },
  { pasta: "08 Governança", itens: [["Política de comissões", "parcial", "lida no código do app"], ["Regimento, acordo de sócios", "não disponível", ""]] },
  { pasta: "09 Materiais", itens: [["Memorando e página de valuation (Gamma)", "disponível", "versão revisada neste portal"], ["Estudo LNZ Value OS (12 partes + anexos)", "disponível", "só conselho"], ["FAQ de investidores", "não disponível", "nasce das perguntas respondidas"]] },
];

const REGRAS = [
  ["Convite por e-mail + código", "obrigatório — é o login deste portal"],
  ["Termo de sigilo com aceite registrado (versão, hash, IP, data)", "obrigatório antes de qualquer número"],
  ["Registro de cada abertura (quem, quando, o quê)", "ativo — tabela só-acrescenta"],
  ["Permissão por pasta e por arquivo, marca d'água, prazo de acesso", "próxima fase (cofre de arquivos)"],
  ["Ligação documento ↔ métrica", "cada número aponta para a carga e o hash que o sustentam"],
];

export default async function DataRoom() {
  const conselho = eConselho(await papelAtual());
  return (
    <Pagina
      sobretitulo="30 minutos"
      titulo="Data room"
      descricao="O que existe, o que está parcial e o que ainda falta — pasta por pasta. Os arquivos em si entram no cofre na próxima fase; hoje a lista é o mapa honesto."
    >
      <Grade colunas={3}>
        {PASTAS.map((p) => (
          <Cartao key={p.pasta} titulo={p.pasta}>
            <ul className="space-y-2">
              {p.itens.map((i) => (
                <li key={i[0]} className="flex flex-col gap-1">
                  <span className="flex items-start justify-between gap-2">
                    <span>{i[0]}</span>
                    <span className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold ${COR[i[1]]}`}>{i[1]}</span>
                  </span>
                  {i[2] && <span className="text-xs text-muted">{i[2]}</span>}
                </li>
              ))}
            </ul>
          </Cartao>
        ))}
      </Grade>

      <Secao sobretitulo="Regras do cofre" titulo="Como o acesso funciona">
        <Tabela cabecalho={["Recurso", "Estado"]} linhas={REGRAS.map((r) => [r[0], <span key="e" className="text-muted">{r[1]}</span>])} />
        <Aviso tipo="regra" titulo="O que não entra no data room">
          Documentos pessoais de sócios (RG, comprovante de residência, informe de rendimentos). Não são necessários e aumentam o risco com a
          LGPD. O portal recebe só agregados; nome, CPF e conta de qualquer pessoa ficam fora.
        </Aviso>
      </Secao>

      <Secao sobretitulo="Antes de abrir a um investidor externo" titulo="Checklist">
        <ol className="list-decimal space-y-1 pl-5 text-sm text-muted">
          <li>Contador independente explica as receitas diferentes (memorando, declaração ao banco, livros, PGDAS).</li>
          <li>Extratos de 2025 e de todas as contas.</li>
          <li>Contrato social atual e titularidade dos ativos.</li>
          <li>Aportes, consórcios e contratos em pasta própria.</li>
          <li>Situação tributária de 2025 e do Simples 2026.</li>
          <li>Dados pessoais fora de qualquer pasta compartilhada.</li>
        </ol>
      </Secao>

      <NotaRevisao
        conselho={conselho}
        itens={[
          "O dossiê do Drive foi compartilhado em caráter confidencial; as pastas 08, 12 e 14 (documentos pessoais) não foram abertas e devem sair do compartilhamento (DEC-20).",
          "A conta DocuSign está em período de avaliação expirado: baixar PDF e certificado de conclusão de cada contrato antes de perder o acesso.",
        ]}
      />

      <p className="text-xs text-muted">
        As cargas de dados (consultas e arquivos com impressão digital) estão em <Link href="/app/cargas" className="underline">Cargas</Link>.
      </p>
    </Pagina>
  );
}
