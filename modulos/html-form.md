# Submódulo HTML — Formulário

- Não precisa ser nativo do construtor: implementar em HTML/JS no próprio arquivo.
- **Telefone BR:**
  - máscara `(00) 00000-0000` ou `(00) 0000-0000`, aplicada no evento `input` e preservando o cursor;
  - proibido `maxlength` sobre o texto formatado e `preventDefault` em teclas;
  - Backspace, colar e autocompletar livres;
  - valida 10–11 dígitos com DDD.
- **UTMs:** `utm_source`, `utm_medium`, `utm_campaign`, `utm_term` e `utm_content` em campos ocultos, persistidos em `sessionStorage`, mais `page_url`, `referrer` e data/hora.
- **E-mail:**
  - B2B (conforme `design_system.md` (seção Inteligência)) bloqueia webmail e valida CNPJ, se houver o campo;
  - B2C aceita webmail e valida CPF, se houver o campo.
- **Webhook (Make/Celonis):**
  - `POST` `application/x-www-form-urlencoded` para a URL registrada em `design_system.md` (seção Inteligência);
  - sem URL, deixar o placeholder e avisar. Nunca inventar URL.
- **Comportamento:** botão travado no envio, mensagem de sucesso ou erro, honeypot, `autocomplete` correto e erro por campo.
- **Campos:** só os necessários. Cada campo a mais reduz a conversão.
