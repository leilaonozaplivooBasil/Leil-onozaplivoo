import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

// Cliente do Supabase para o lado do servidor (páginas, layouts e ações).
// Usa só a chave publicável: o que cada pessoa vê é decidido pelas políticas do banco (RLS).
export async function criarClienteServidor() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(paraGravar) {
          try {
            paraGravar.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options),
            );
          } catch {
            // Em componente de servidor não dá para gravar cookie; o proxy renova a sessão.
          }
        },
      },
    },
  );
}
