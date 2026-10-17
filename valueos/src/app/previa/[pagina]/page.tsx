import { notFound } from "next/navigation";
import Image from "next/image";
import { emPrevia } from "@/lib/metricas";
import Memorando from "@/app/app/(portal)/memorando/page";
import Inicio from "@/app/app/(portal)/page";
import Valuation from "@/app/app/(portal)/valuation/page";
import Parceiros from "@/app/app/(portal)/parceiros/page";
import Riscos from "@/app/app/(portal)/riscos/page";
import Governanca from "@/app/app/(portal)/governanca/page";
import Roadmap from "@/app/app/(portal)/roadmap/page";
import DataRoom from "@/app/app/(portal)/dataroom/page";
import Capital from "@/app/app/(portal)/capital/page";
import { MenuCelular, Navegacao } from "@/components/nav";

export const dynamic = "force-dynamic";

const PAGINAS: Record<string, () => Promise<React.ReactNode>> = {
  memorando: Memorando,
  inicio: Inicio,
  valuation: Valuation,
  parceiros: Parceiros,
  riscos: Riscos,
  governanca: Governanca,
  roadmap: Roadmap,
  dataroom: DataRoom,
  capital: Capital,
};

// Prévia visual com dados de arquivo, para conferir o desenho sem login. Não existe fora do modo de desenvolvimento.
export default async function Previa({ params }: { params: Promise<{ pagina: string }> }) {
  if (!emPrevia()) notFound();
  const { pagina } = await params;
  const Pagina = PAGINAS[pagina];
  if (!Pagina) notFound();
  return (
    <div className="flex min-h-full flex-1 flex-col">
      <header className="sticky top-0 z-30 border-b border-white/10 bg-black/85 backdrop-blur-md">
        <div className="relative mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-5 py-3 sm:px-8">
          <span className="flex items-center gap-3">
            <Image src="/m/logo-horizontal.png" alt="Leilão NoZap" width={110} height={40} priority className="h-9 w-auto" />
            <span className="hidden border-l border-white/15 pl-3 text-xs uppercase tracking-[0.18em] text-muted sm:inline">Área do investidor</span>
          </span>
          <Navegacao />
          <div className="flex items-center gap-3 text-sm">
            <span className="text-white/80 underline underline-offset-4">Sair</span>
            <MenuCelular />
          </div>
        </div>
      </header>
      <main className="flex-1">{await Pagina()}</main>
    </div>
  );
}
