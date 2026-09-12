(function () {
  var state = { tasks: [], view: 'board', filter: 'all' };
  var columns = { todo: 'To do', in_progress: 'In progress', done: 'Done' };
  function load() {
    fetch('data/tasks.json').then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) { state.tasks = data; render(); })
      .catch(function (e) { document.getElementById('view').innerHTML = '<pre class="err">' + String(e.stack || e) + '</pre>'; });
  }
  function card(t) {
    return '<article class="card" tabindex="0" data-id="' + t.id + '">' +
      '<p class="title">' + t.title + '</p>' +
      '<div class="meta"><span class="chip">' + t.status.toUpperCase() + '</span><span>' + t.assignee + '</span><span>' + t.due + '</span></div>' +
      '<div class="sample">Sample data · <a href="#">Learn more</a></div>' +
      '<div class="actions"><button class="icon-btn" aria-label="Archive ' + t.title + '" data-act="archive" data-id="' + t.id + '">⌫</button><button class="icon-btn" aria-label="Edit ' + t.title + '" data-act="edit" data-id="' + t.id + '">✎</button></div>' +
      '</article>';
  }
  function visible() { return state.tasks.filter(function (t) { return state.filter === 'all' || t.status === state.filter; }); }
  function render() {
    var view = document.getElementById('view');
    var tasks = visible();
    if (state.view === 'board') {
      view.innerHTML = '<div class="columns">' + Object.keys(columns).map(function (k) {
        var items = tasks.filter(function (t) { return t.status === k; });
        var body = items.length ? items.map(card).join('') :
          (k === 'done' ? '<div class="empty good">Nothing is done yet.<br>Move a card here when you finish it.<a href="#" data-act="new">Add a task</a></div>' : '<div class="empty">No results</div>');
        return '<section class="column" id="' + k + '"><h2>' + columns[k] + ' · ' + items.length + '</h2>' + body + '</section>';
      }).join('') + '</div>';
    } else if (state.view === 'list') {
      view.innerHTML = tasks.length ? '<table><thead><tr><th>Title</th><th>Status</th><th>Assignee</th><th>Due</th></tr></thead><tbody>' +
        tasks.map(function (t) { return '<tr><td>' + t.title + '</td><td>' + columns[t.status] + '</td><td>' + t.assignee + '</td><td>' + t.due + '</td></tr>'; }).join('') + '</tbody></table>'
        : '<div class="empty good">No tasks match this filter.<a href="#" data-act="clear-filter">Clear the filter</a></div>';
    } else {
      // P4: bare empty state
      view.innerHTML = '<div class="empty">No results</div>';
    }
    document.getElementById('count').textContent = tasks.length + ' tasks';
  }
  document.querySelectorAll('.tab').forEach(function (tab, i, all) {
    tab.addEventListener('click', function () { select(tab); });
    tab.addEventListener('keydown', function (e) {
      var idx = Array.prototype.indexOf.call(all, tab);
      if (e.key === 'ArrowRight') { select(all[(idx + 1) % all.length]); all[(idx + 1) % all.length].focus(); }
      if (e.key === 'ArrowLeft') { select(all[(idx - 1 + all.length) % all.length]); all[(idx - 1 + all.length) % all.length].focus(); }
    });
  });
  function select(tab) {
    document.querySelectorAll('.tab').forEach(function (t) { t.setAttribute('aria-selected', String(t === tab)); t.tabIndex = t === tab ? 0 : -1; });
    state.view = tab.dataset.view; render();
  }
  // filter menu: P3 never closes on outside click or Escape
  var menuBtn = document.getElementById('filter-btn'); var menu = document.getElementById('filter-menu');
  menuBtn.addEventListener('click', function () { var open = menu.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', String(open)); });
  menu.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; state.filter = b.dataset.filter; menuBtn.textContent = 'Filter: ' + b.textContent; render(); });
  // search
  var search = document.getElementById('search');
  search.addEventListener('input', function () {
    var q = search.value.trim().toLowerCase();
    document.querySelectorAll('.card').forEach(function (c) { c.style.display = !q || c.querySelector('.title').textContent.toLowerCase().indexOf(q) >= 0 ? '' : 'none'; });
  });
  // dialog: P2 no focus in, no trap, no Escape; scrim click closes
  var dlg = document.getElementById('new-dialog'); var scrim = document.getElementById('scrim');
  function openDlg() { dlg.classList.add('open'); scrim.classList.add('open'); }
  function closeDlg() { dlg.classList.remove('open'); scrim.classList.remove('open'); }
  document.getElementById('new-btn').addEventListener('click', openDlg);
  document.getElementById('view').addEventListener('click', function (e) { var a = e.target.closest('[data-act]'); if (!a) return; e.preventDefault();
    if (a.dataset.act === 'new') openDlg();
    if (a.dataset.act === 'clear-filter') { state.filter = 'all'; menuBtn.textContent = 'Filter: All'; render(); }
    if (a.dataset.act === 'archive') { state.tasks = state.tasks.filter(function (t) { return t.id !== a.dataset.id; }); render(); }
  });
  scrim.addEventListener('click', closeDlg);
  document.getElementById('dlg-cancel').addEventListener('click', closeDlg);
  document.getElementById('dlg-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var title = document.getElementById('dlg-title').value.trim();
    if (!title) { document.getElementById('dlg-title').setAttribute('aria-invalid', 'true'); document.getElementById('dlg-err').textContent = 'Title is required.'; return; }
    state.tasks.unshift({ id: 'tsk_' + Date.now(), title: title, status: 'todo', assignee: 'usr_8f3a', due: 'No date' });
    document.getElementById('dlg-title').value = ''; closeDlg(); render();
  });
  document.getElementById('archived-list').innerHTML = ['Old onboarding doc','Q2 retro notes','Vendor comparison','Logo refresh','Support macros','Hiring plan v1','Offsite agenda','Budget draft'].map(function (t) { return '<div class="activity-row"><span>' + t + '</span><span class="who">archived</span></div>'; }).join('');
  load();
})();
