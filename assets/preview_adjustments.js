/* Tweaks for the PREVIEW (workbench). Live adjustment of CSS variables, no framework.
   Source of the idea: huashu-design (MIT), rewritten in plain JS. The FINAL file does not carry this script.
   Usage: define window.TWEAKS before including this file, and use var(--name) in the CSS.
     window.TWEAKS = {
       key: 'cliente-lp',                       // localStorage namespace
       items: [
         { id: 'cor',   label: 'Cor principal', type: 'color',  cssVar: '--primary', value: '#F26B1D' },
         { id: 'tipo',  label: 'Corpo (px)',    type: 'range',  cssVar: '--body',    value: 18, min: 14, max: 22, unit: 'px' },
         { id: 'dens',  label: 'Densidade',     type: 'select', cssVar: '--gap',     value: '24px',
           options: [['16px', 'Compacta'], ['24px', 'Normal'], ['40px', 'Ampla']] }
       ]
     };
   Best practices: at most 5 to 6 items, discrete and thoughtful options (not a slider from 0 to 50), and the
   default value is already the complete piece. */
(function () {
  var cfg = window.TWEAKS;
  if (!cfg || !cfg.items || !cfg.items.length) return;
  var NS = 'tweaks:' + (cfg.key || 'default');
  var state = {};
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(NS) || '{}') || {}; } catch (e) { saved = {}; }

  function apply(item, v) {
    state[item.id] = v;
    document.documentElement.style.setProperty(item.cssVar, v + (item.unit && item.type === 'range' ? item.unit : ''));
  }
  function persist() { try { localStorage.setItem(NS, JSON.stringify(state)); } catch (e) {} }

  cfg.items.forEach(function (it) { apply(it, saved[it.id] != null ? saved[it.id] : it.value); });

  var box = document.createElement('div');
  box.setAttribute('data-tweaks', '');
  box.style.cssText = 'position:fixed;right:16px;bottom:16px;z-index:2147483647;font:13px/1.4 system-ui,sans-serif;color:#111';
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.textContent = 'Tweaks';
  btn.style.cssText = 'padding:8px 14px;border:0;border-radius:999px;background:#111;color:#fff;cursor:pointer;font:inherit';
  var panel = document.createElement('div');
  panel.style.cssText = 'display:none;width:260px;margin-bottom:8px;padding:14px;background:#fff;border:1px solid #ddd;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.14)';
  btn.addEventListener('click', function () { panel.style.display = panel.style.display === 'none' ? 'block' : 'none'; });

  cfg.items.forEach(function (it) {
    var row = document.createElement('label');
    row.style.cssText = 'display:block;margin-bottom:10px';
    var cap = document.createElement('div');
    cap.style.cssText = 'margin-bottom:4px;color:#555';
    cap.textContent = it.label;
    var input;
    if (it.type === 'select') {
      input = document.createElement('select');
      it.options.forEach(function (o) {
        var op = document.createElement('option');
        op.value = o[0]; op.textContent = o[1];
        input.appendChild(op);
      });
      input.style.width = '100%';
    } else {
      input = document.createElement('input');
      input.type = it.type === 'range' ? 'range' : 'color';
      if (it.type === 'range') { input.min = it.min; input.max = it.max; input.step = it.step || 1; }
      input.style.width = '100%';
    }
    input.value = state[it.id];
    input.addEventListener('input', function () { apply(it, input.value); persist(); });
    row.appendChild(cap); row.appendChild(input); panel.appendChild(row);
  });

  var reset = document.createElement('button');
  reset.type = 'button';
  reset.textContent = 'Reset to default';
  reset.style.cssText = 'width:100%;padding:7px;border:0;border-radius:6px;background:#f2f2f2;cursor:pointer;font:inherit';
  reset.addEventListener('click', function () {
    try { localStorage.removeItem(NS); } catch (e) {}
    cfg.items.forEach(function (it, i) { apply(it, it.value); panel.querySelectorAll('input,select')[i].value = it.value; });
  });
  panel.appendChild(reset);

  box.appendChild(panel); box.appendChild(btn);
  function mount() { document.body.appendChild(box); }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
