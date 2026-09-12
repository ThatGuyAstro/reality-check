// Shared shell: session guard, theme, sidebar collapse, sign out.
(function () {
  var raw = localStorage.getItem('orbit.session');
  if (!raw) { window.location.href = 'index.html'; return; }
  var session = JSON.parse(raw);
  var prefs = JSON.parse(localStorage.getItem('orbit.prefs') || '{}');
  if (prefs.theme === 'dark') document.body.classList.add('dark');
  var who = document.getElementById('who'); if (who) who.textContent = session.name;
  var out = document.getElementById('sign-out');
  if (out) out.addEventListener('click', function () { localStorage.removeItem('orbit.session'); window.location.href = 'index.html'; });
  var toggle = document.getElementById('nav-toggle');
  var sidebar = document.getElementById('sidebar');
  if (toggle && sidebar) {
    var collapsed = !!prefs.collapsed;
    function apply() { sidebar.classList.toggle('collapsed', collapsed); toggle.setAttribute('aria-expanded', String(!collapsed)); toggle.textContent = collapsed ? '»' : '«'; }
    apply();
    toggle.addEventListener('click', function () { collapsed = !collapsed; prefs.collapsed = collapsed; localStorage.setItem('orbit.prefs', JSON.stringify(prefs)); apply(); });
  }
  window.orbitToast = function (text, ms) {
    var t = document.getElementById('toast'); if (!t) return;
    t.textContent = text; t.classList.add('open');
    setTimeout(function () { t.classList.remove('open'); }, ms);
  };
})();
