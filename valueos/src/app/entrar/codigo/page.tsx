"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { criarClienteNavegador } from "@/lib/supabase/client";

function FormularioCodigo() {
  const params = useSearchParams();
  const router = useRouter();
  const email = (params.get("email") ?? "").toLowerCase();
  const [codigo, setCodigo] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [pendente, setPendente] = useState(false);

  async function confirmar(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setPendente(true);
    const supabase = criarClienteNavegador();
    const { error } = await supabase.auth.verifyOtp({
      email,
      token: codigo.trim(),
      type: "email",
    });
    setPendente(false);
    if (error) {
      setErro("Código inválido ou vencido. Peça um novo código.");
      return;
    }
    router.replace("/app");
    router.refresh();
  }

  return (
    <main className="flex flex-1 items-center justify-center px-4 py-12">
      <div className="w-full max-w-md rounded-2xl border border-border bg-surface p-8">
        <p className="text-xs font-semibold uppercase tracking-widest text-accent">
          LNZ Value OS
        </p>
        <h1 className="mt-2 text-2xl font-semibold">Digite o código</h1>
        <p className="mt-2 text-sm text-muted">
          Enviamos um código para <strong className="text-foreground">{email}</strong>.
          Se o e-mail trouxer um link, pode clicar nele também.
        </p>

        <form onSubmit={confirmar} className="mt-6 space-y-4">
          <input
            inputMode="numeric"
            autoComplete="one-time-code"
            pattern="[0-9]{6,8}"
            required
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            placeholder="000000"
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-center font-mono text-2xl tracking-[0.4em] outline-none focus:border-accent"
          />
          {erro && (
            <p role="alert" className="text-sm text-danger">
              {erro}
            </p>
          )}
          <button
            type="submit"
            disabled={pendente || !email}
            className="w-full rounded-lg bg-accent px-4 py-2.5 font-semibold text-accent-ink disabled:opacity-60"
          >
            {pendente ? "Conferindo…" : "Entrar"}
          </button>
        </form>

        <a href="/entrar" className="mt-6 block text-sm text-muted underline">
          Usar outro e-mail
        </a>
      </div>
    </main>
  );
}

export default function Codigo() {
  return (
    <Suspense>
      <FormularioCodigo />
    </Suspense>
  );
}
