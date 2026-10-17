// Termo de sigilo do portal. Mudou o texto? Sobe a versão: o aceite antigo deixa de valer.
export const NDA_VERSAO = "v1.0-2026-10";

export const NDA_TEXTO = `TERMO DE CONFIDENCIALIDADE — LNZ VALUE OS

1. As informações deste portal (números, documentos, projeções, contratos e qualquer material aqui disponível) são confidenciais e pertencem à Compras Full Comércio Ltda ("Leilão NoZap").

2. Você se compromete a usar essas informações apenas para avaliar uma possível relação de investimento ou parceria com a empresa, e a não copiar, repassar, publicar ou divulgar nada a terceiros, por qualquer meio, sem autorização por escrito.

3. Cada número do portal traz a sua origem e uma etiqueta de qualidade (VERIFICADO, DADO DA ADMINISTRAÇÃO, PROJEÇÃO ou PREMISSA). Projeções e premissas não são promessa de resultado. Nada aqui é oferta pública de valores mobiliários nem promessa de rentabilidade.

4. O acesso é pessoal e intransferível. Cada entrada e cada tela aberta ficam registradas com data, hora e endereço de rede.

5. Este compromisso vale por 5 (cinco) anos a partir do aceite, mesmo que você deixe de usar o portal.

6. Foro: Comarca do Rio de Janeiro/RJ.`;

export async function hashDoTexto(texto: string): Promise<string> {
  const dados = new TextEncoder().encode(texto);
  const digest = await crypto.subtle.digest("SHA-256", dados);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
