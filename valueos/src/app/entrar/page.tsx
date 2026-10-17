"use client";

import { useActionState } from "react";
import { pedirCodigo, type EstadoLogin } from "./actions";

const inicial: EstadoLogin = {};

export default function Entrar() {
  const [estado, acao, pendente] = useActionState(pedirCodigo, inicial);

  return (
    <main className="flex flex-1 items-center justify-center px-4 py-12">
      <div className="w-full max-w-md rounded-2xl border border-border bg-surface p-8">
        <p className="text-xs font-semibold uppercase tracking-widest text-accent">
          LNZ Value OS
        </p>
        <h1 className="mt-2 text-2xl font-semibold">Área do investidor</h1>
        <p className="mt-2 text-sm text-muted">
          Acesso só por convite. Digite seu e-mail e enviamos um código de
          entrada.
        </p>

        <form action={acao} className="mt-6 space-y-4">
          <label className="block text-sm">
            <span className="text-muted">E-mail</span>
            <input
              name="email"
              type="email"
              autoComplete="email"
              required
              className="mt-1 w-full rounded-lg border border-border bg-background px-3 py-2 text-base outline-none focus:border-accent"
            />
          </label>
          {estado.erro && (
            <p role="alert" className="text-sm text-danger">
              {estado.erro}
            </p>
          )}
          <button
            type="submit"
            disabled={pendente}
            className="w-full rounded-lg bg-accent px-4 py-2.5 font-semibold text-accent-ink disabled:opacity-60"
          >
            {pendente ? "Enviando…" : "Receber código"}
          </button>
        </form>

        <p className="mt-6 text-xs text-muted">
          Cada acesso fica registrado. Material confidencial, protegido por
          termo de sigilo.
        </p>
      </div>
    </main>
  );
}
