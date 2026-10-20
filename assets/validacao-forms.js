/* ============================================================
   V4 Forms — validação de leads (email, telefone, CPF, CNPJ)
   ------------------------------------------------------------
   Uso:
     1. Marque cada input com data-validate:
        <input data-validate="email">
        <input data-validate="telefone">
        <input data-validate="cpf">
        <input data-validate="cnpj">
        <input data-validate="documento">  (alterna CPF/CNPJ pelo nº de dígitos)
     2. Defina o modo no <form> ou no <body>:
        <form data-mode="b2b"> ... </form>   (bloqueia webmail no email)
        <form data-mode="b2c"> ... </form>   (email aceita gmail; só sintaxe+MX)
     3. Inclua este script no fim da página.

   Comportamento:
     - aplica máscara enquanto digita (telefone/cpf/cnpj)
     - valida no blur; mostra mensagem inline abaixo do campo
     - bloqueia o submit enquanto houver campo inválido
     - email faz MX check via dns.google (assíncrono, com fallback offline)
   ============================================================ */
(function () {
  'use strict';

  /* ---------- EMAIL ---------- */
  var FREE_PROVIDERS = new Set([
    'gmail.com','googlemail.com',
    'yahoo.com','yahoo.com.br','ymail.com',
    'hotmail.com','hotmail.com.br','outlook.com','outlook.com.br','live.com','live.com.br','msn.com',
    'icloud.com','me.com','mac.com',
    'aol.com','aim.com',
    'proton.me','protonmail.com','pm.me',
    'gmx.com','gmx.net','mail.com',
    'yandex.com','yandex.ru','zoho.com',
    'uol.com.br','bol.com.br','terra.com.br','ig.com.br','globo.com','globomail.com','r7.com',
    'oi.com.br','pop.com.br','itelefonica.com.br'
  ]);
  var DISPOSABLE = new Set([
    'mailinator.com','10minutemail.com','guerrillamail.com','guerrillamail.net','yopmail.com',
    'tempmail.com','temp-mail.org','throwawaymail.com','trashmail.com','sharklasers.com',
    'getairmail.com','maildrop.cc','mintemail.com','mohmal.com','dispostable.com',
    'fakeinbox.com','tempinbox.com','spamgourmet.com','tempr.email','mailcatch.com'
  ]);
  var EMAIL_SYNTAX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  function mxCheck(domain) {
    return fetch('https://dns.google/resolve?name=' + encodeURIComponent(domain) + '&type=MX')
      .then(function (r) { return r.json(); })
      .then(function (j) { return Array.isArray(j.Answer) && j.Answer.some(function (a) { return a.type === 15; }); })
      .catch(function () { return null; }); // null = DNS indisponível → não trava
  }

  // Retorna Promise<{ok, msg}>
  function validateEmail(value, mode) {
    var email = (value || '').trim().toLowerCase();
    if (!EMAIL_SYNTAX.test(email)) return Promise.resolve({ ok: false, msg: 'Email inválido.' });
    var parts = email.split('@');
    var domain = parts[1];
    if (mode === 'b2b' && FREE_PROVIDERS.has(domain)) {
      return Promise.resolve({ ok: false, msg: 'Use o email da sua empresa (não use gmail, hotmail, etc).' });
    }
    if (DISPOSABLE.has(domain)) return Promise.resolve({ ok: false, msg: 'Email temporário não é aceito. Use um email real.' });
    return mxCheck(domain).then(function (hasMx) {
      if (hasMx === false) return { ok: false, msg: 'Esse domínio não recebe email. Confira se digitou certo.' };
      return { ok: true, msg: '' }; // hasMx true ou null (fallback)
    });
  }

  /* ---------- TELEFONE (BR) ---------- */
  var DDD = new Set([
    11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,
    41,42,43,44,45,46,47,48,49,51,53,54,55,61,62,63,64,65,66,67,68,69,
    71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99
  ]);
  function maskPhone(v) {
    var d = v.replace(/\D/g, '').slice(0, 11);
    if (d.length <= 2) return d.replace(/^(\d{0,2})/, '($1');
    if (d.length <= 6) return d.replace(/^(\d{2})(\d{0,4})/, '($1) $2');
    if (d.length <= 10) return d.replace(/^(\d{2})(\d{0,4})(\d{0,4})/, '($1) $2-$3').replace(/-$/, '');
    return d.replace(/^(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
  }
  function validatePhone(value) {
    var d = (value || '').replace(/\D/g, '');
    if (d.length < 10 || d.length > 11) return { ok: false, msg: 'Telefone incompleto. Use DDD + número.' };
    if (!DDD.has(parseInt(d.slice(0, 2), 10))) return { ok: false, msg: 'DDD inválido.' };
    if (d.length === 11 && d[2] !== '9') return { ok: false, msg: 'Celular deve começar com 9 após o DDD.' };
    return { ok: true, msg: '' };
  }

  /* ---------- CPF ---------- */
  function maskCPF(v) {
    var d = v.replace(/\D/g, '').slice(0, 11);
    return d.replace(/^(\d{3})(\d)/, '$1.$2').replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1-$2');
  }
  function validateCPF(value) {
    var c = (value || '').replace(/\D/g, '');
    if (c.length !== 11 || /^(\d)\1{10}$/.test(c)) return { ok: false, msg: 'CPF inválido.' };
    var calc = function (slice) {
      var sum = 0, len = slice.length + 1;
      for (var i = 0; i < slice.length; i++) sum += parseInt(slice[i], 10) * (len - i);
      var r = (sum * 10) % 11;
      return r === 10 ? 0 : r;
    };
    if (calc(c.slice(0, 9)) !== parseInt(c[9], 10)) return { ok: false, msg: 'CPF inválido.' };
    if (calc(c.slice(0, 10)) !== parseInt(c[10], 10)) return { ok: false, msg: 'CPF inválido.' };
    return { ok: true, msg: '' };
  }

  /* ---------- CNPJ ---------- */
  function maskCNPJ(v) {
    var d = v.replace(/\D/g, '').slice(0, 14);
    return d.replace(/^(\d{2})(\d)/, '$1.$2').replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
            .replace(/\.(\d{3})(\d)/, '.$1/$2').replace(/(\d{4})(\d)/, '$1-$2');
  }
  function validateCNPJ(value) {
    var c = (value || '').replace(/\D/g, '');
    if (c.length !== 14 || /^(\d)\1{13}$/.test(c)) return { ok: false, msg: 'CNPJ inválido.' };
    var calc = function (len) {
      var nums = c.slice(0, len), pos = len - 7, sum = 0;
      for (var i = len; i >= 1; i--) {
        sum += nums[len - i] * pos--;
        if (pos < 2) pos = 9;
      }
      var r = sum % 11;
      return r < 2 ? 0 : 11 - r;
    };
    if (calc(12) !== parseInt(c[12], 10)) return { ok: false, msg: 'CNPJ inválido.' };
    if (calc(13) !== parseInt(c[13], 10)) return { ok: false, msg: 'CNPJ inválido.' };
    return { ok: true, msg: '' };
  }

  /* ---------- ESTADO -> CIDADE (cascata via IBGE) ----------
     Marque o <select> de cidade com data-validate="cidade" e data-uf="ID_DO_SELECT_ESTADO".
     Ao trocar a UF, busca a lista oficial de municípios daquele estado (API gratuita do IBGE)
     e popula só essas cidades. Se o IBGE falhar, vira campo de texto livre (não trava o lead). */
  function loadCidades(ufSel, citySel) {
    var uf = (ufSel.value || '').trim();
    if (!uf) return;
    citySel.innerHTML = '<option value="" disabled selected>Carregando cidades…</option>';
    citySel.disabled = true;
    refreshSubmit(citySel.closest('form'));
    fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados/' + encodeURIComponent(uf) + '/municipios?orderBy=nome')
      .then(function (r) { if (!r.ok) throw new Error('IBGE ' + r.status); return r.json(); })
      .then(function (list) {
        citySel.innerHTML = '<option value="" disabled selected>Selecione a cidade</option>' +
          list.map(function (c) { return '<option>' + c.nome + '</option>'; }).join('');
        citySel.disabled = false;
        refreshSubmit(citySel.closest('form'));
      })
      .catch(function () {
        var inp = document.createElement('input');
        inp.type = 'text'; inp.id = citySel.id; inp.name = citySel.name;
        inp.placeholder = 'Sua cidade';
        inp.setAttribute('autocomplete', 'address-level2');
        inp.setAttribute('data-validate', 'cidade');
        if (citySel.required) inp.required = true;
        inp.addEventListener('input', function () { setState(inp, !!inp.value.trim(), ''); });
        citySel.replaceWith(inp);
        ensureMsgEl(inp);
        refreshSubmit(inp.closest('form'));
      });
  }

  /* ---------- WIRING ---------- */
  function getMode(input) {
    var form = input.closest('form');
    var holder = (form && form.dataset.mode) ? form : document.body;
    return (holder.dataset.mode || 'b2c').toLowerCase();
  }

  function ensureMsgEl(input) {
    var next = input.nextElementSibling;
    if (next && next.classList.contains('v4-msg')) return next;
    var el = document.createElement('div');
    el.className = 'v4-msg';
    el.style.cssText = 'font-size:12px;margin-top:4px;min-height:14px;line-height:1.3;';
    input.insertAdjacentElement('afterend', el);
    return el;
  }

  function setState(input, ok, msg) {
    var el = ensureMsgEl(input);
    input.dataset.valid = ok ? 'true' : 'false';
    if (msg) { el.textContent = msg; el.style.color = ok ? '#16a34a' : '#dc2626'; }
    else { el.textContent = ''; }
    refreshSubmit(input.closest('form'));
  }

  function refreshSubmit(form) {
    if (!form) return;
    var inputs = form.querySelectorAll('[data-validate]');
    var allOk = true;
    inputs.forEach(function (i) {
      if (i.value.trim() && i.dataset.valid === 'false') allOk = false;
      if (i.required && !i.value.trim()) allOk = false;
    });
    var btn = form.querySelector('[type="submit"], button:not([type="button"])');
    if (btn) btn.disabled = !allOk;
  }

  function bind(input) {
    var kind = input.dataset.validate;

    if (kind === 'telefone') input.addEventListener('input', function () { input.value = maskPhone(input.value); });
    if (kind === 'cpf') input.addEventListener('input', function () { input.value = maskCPF(input.value); });
    if (kind === 'cnpj') input.addEventListener('input', function () { input.value = maskCNPJ(input.value); });
    if (kind === 'documento') input.addEventListener('input', function () {
      var d = input.value.replace(/\D/g, '');
      input.value = d.length > 11 ? maskCNPJ(input.value) : maskCPF(input.value);
    });

    // selects (estado/cidade): atualiza o gate do submit ao escolher
    if (input.tagName === 'SELECT') input.addEventListener('change', function () { setState(input, !!input.value.trim(), ''); });
    // cidade depende do estado: liga a cascata do IBGE
    if (kind === 'cidade' && input.dataset.uf) {
      var ufEl = document.getElementById(input.dataset.uf);
      if (ufEl) ufEl.addEventListener('change', function () { loadCidades(ufEl, input); });
    }

    input.addEventListener('blur', function () {
      var v = input.value.trim();
      if (!v) { setState(input, true, ''); return; }
      var res;
      if (kind === 'email') {
        validateEmail(v, getMode(input)).then(function (r) { setState(input, r.ok, r.msg); });
        return;
      }
      if (kind === 'telefone') res = validatePhone(v);
      else if (kind === 'cpf') res = validateCPF(v);
      else if (kind === 'cnpj') res = validateCNPJ(v);
      else if (kind === 'documento') res = (v.replace(/\D/g, '').length > 11) ? validateCNPJ(v) : validateCPF(v);
      else return;
      setState(input, res.ok, res.msg);
    });
  }

  function init() {
    document.querySelectorAll('[data-validate]').forEach(function (i) {
      bind(i);
      ensureMsgEl(i); // reserva o espaço da mensagem na carga -> layout não "pula" ao validar
    });
    document.querySelectorAll('form').forEach(refreshSubmit);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // expõe pra uso programático / testes
  window.V4Forms = {
    validateEmail: validateEmail, validatePhone: validatePhone,
    validateCPF: validateCPF, validateCNPJ: validateCNPJ,
    maskPhone: maskPhone, maskCPF: maskCPF, maskCNPJ: maskCNPJ
  };
})();
