import Image from "next/image";

// Moldura da entrada: a mesma capa do memorando, com a logo, antes de qualquer número.
export default function LayoutEntrar({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative isolate flex min-h-screen flex-1 flex-col">
      <Image src="/m/capa.jpg" alt="" fill priority sizes="100vw" className="-z-10 object-cover" />
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-black/70 via-black/80 to-black" aria-hidden />
      <header className="px-5 py-6 sm:px-8">
        <Image src="/m/logo-horizontal.png" alt="Leilão NoZap" width={132} height={48} priority className="h-11 w-auto" />
      </header>
      {children}
      <footer className="px-5 py-6 text-center text-xs text-muted">
        Leilão NoZap · área do investidor · acesso por convite, com termo de sigilo e registro de cada acesso
      </footer>
    </div>
  );
}
