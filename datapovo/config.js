// Única coisa que você precisa editar para mudar a pesquisa.
window.DATAPOVO = {
  TITULO: 'DataPovo',
  PERGUNTA: 'Qual assunto é mais urgente para você?',

  // Todos os números com a mesma quantidade de dígitos (1, 2, 3 ou 01, 02, 03...).
  OPCOES: [
    { n: '1', nome: 'Saúde' },
    { n: '2', nome: 'Educação' },
    { n: '3', nome: 'Segurança' },
    { n: '4', nome: 'Emprego e renda' },
    { n: '5', nome: 'Custo de vida' },
  ],

  // Quem responde pelos dados e como pedir exclusão. Aparece no aviso de consentimento.
  // Vazio = a urna só conta votos e NÃO pede WhatsApp de ninguém.
  // Exemplo: 'DataPovo — contato@seudominio.com.br'
  RESPONSAVEL: '',

  // Deixe vazio para testar só neste aparelho. Preencha para juntar votos de todo mundo
  // (veja o README e o arquivo schema.sql).
  SUPABASE_URL: '',
  SUPABASE_KEY: '',
};
