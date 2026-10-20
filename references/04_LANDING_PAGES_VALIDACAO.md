# 04 · Landing Pages Single-File & Validação Inteligente de Leads

## 1. Arquitetura Single-File & Blindagem GreatPages / CMS

Todo o código é compilado em um **arquivo único autônomo** (`index.html`) contendo `<head>`, `<style>`, `<body>` e `<script>`.

### Blindagem de Reset Universal:
```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Oculta contêineres fantasmas e resets de construtores de página */
.centralizar:empty,
[id^="b_3641"],
[id^="b_"] {
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

#site {
  min-width: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  overflow: visible !important;
  display: block !important;
  margin: 0 !important;
  padding: 0 !important;
}

[hidden],
.global-status[hidden], .result-card[hidden], .form-step[hidden],
.global-status:empty, .result-card:empty, .form-feedback:empty {
  display: none !important;
}
```

---

## 2. Validação Inteligente de Leads (B2B vs B2C)

A biblioteca `validacao-forms.js` classifica a proposta da página para blindar a qualidade do lead sem custos de APIs pagas:

| Campo | Matriz B2B (PJ / Revenda / Distribuidor) | Matriz B2C (Consumidor / PF / Criador) |
| :--- | :--- | :--- |
| **Email** | **Bloqueia webmails grátis** (gmail, hotmail, yahoo, etc.) exigindo domínio corporativo | **Aceita** webmails pessoais (gmail, hotmail, etc.) |
| **Telefone** | DDD válido + formato BR `(XX) XXXXX-XXXX` | DDD válido + formato BR `(XX) XXXXX-XXXX` |
| **Documento** | Validação módulo 11 de **CNPJ** | Validação módulo 11 de **CPF** |
| **Estado / Cidade** | Cascata dinâmica oficial da API do IBGE | Cascata dinâmica oficial da API do IBGE |
| **Submit Gate** | Botão permanece travado até que todos os campos sejam válidos | Botão permanece travado até que todos os campos sejam válidos |

### Atributos HTML dos Campos:
* `data-validate="email"`
* `data-validate="telefone"`
* `data-validate="cnpj"` ou `data-validate="cpf"`
* `data-validate="estado"` e `data-validate="cidade"` (com `data-uf="id_estado"`)

---

## 3. Prevenção de Mojibake (Acentuação Corrompida)
Textos em português são codificados utilizando entidades HTML seguras:
* `&ccedil;` (ç) | `&Ccedil;` (Ç)
* `&atilde;` (ã) | `&otilde;` (õ)
* `&eacute;` (é) | `&aacute;` (á) | `&iacute;` (í) | `&oacute;` (ó) | `&uacute;` (ú)
* `&ecirc;` (ê) | `&acirc;` (â) | `&ocirc;` (ô)
