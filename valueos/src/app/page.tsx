import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";

export const dynamic = "force-dynamic";

// Raiz: quem está logado vai para o portal; quem não está, para o login.
export default async function Raiz() {
  const supabase = await criarClienteServidor();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  redirect(user ? "/app" : "/entrar");
}
