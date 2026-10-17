"use server";

import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/server";

export type EstadoLogin = { erro?: string };

// Passo 1 do login: confere o convite no banco e manda o código por e-mail.
export async function pedirCodigo(
  _anterior: EstadoLogin,
  formData: FormData,
): Promise<EstadoLogin> {
  const email = String(formData.get("email") ?? "")
    .trim()
    .toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { erro: "Digite um e-mail válido." };
  }

  const supabase = await criarClienteServidor();
  const { data: temConvite, error: erroConvite } = await supabase.rpc(
    "vos_convite_valido",
    { p_email: email },
  );
  if (erroConvite) {
    return { erro: "Não foi possível conferir o convite. Tente de novo." };
  }
  if (!temConvite) {
    return {
      erro: "Este e-mail não tem convite. Peça acesso ao Leilão NoZap.",
    };
  }

  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: { shouldCreateUser: true },
  });
  if (error) {
    return {
      erro: "Não foi possível enviar o código agora. Espere alguns minutos e tente de novo.",
    };
  }

  redirect(`/entrar/codigo?email=${encodeURIComponent(email)}`);
}
