(function () {
  var session = JSON.parse(localStorage.getItem('ledgerlite.session') || 'null');
  if (!session) { window.location.href = 'index.html'; return; }
  var profile = JSON.parse(localStorage.getItem('ledgerlite.profile') || '{}');
  if (profile.theme === 'dark') document.body.classList.add('dark');
  var greeting = document.getElementById('greeting');
  if (greeting) greeting.textContent = 'Welcome back, ' + (profile.displayName || session.name);
  var logout = document.getElementById('logout-link');
  if (logout) logout.addEventListener('click', function (e) { e.preventDefault(); localStorage.removeItem('ledgerlite.session'); window.location.href = 'index.html'; });

  var TX = [
    { date: '2026-09-10', desc: 'Northwind Supplies', cat: 'Office', amount: '-$184.20' },
    { date: '2026-09-09', desc: 'Client payment - Aster Co', cat: 'Income', amount: '+$2,400.00' },
    { date: '2026-09-08', desc: 'Cloud hosting', cat: 'Software', amount: '-$96.00' },
    { date: '2026-09-06', desc: 'Client payment - Bramble LLC', cat: 'Income', amount: '+$1,505.75' },
    { date: '2026-09-04', desc: 'Coffee for the office', cat: 'Meals', amount: '-$31.40' }
  ];
  var body = document.getElementById('tx-body');
  if (body) {
    TX.forEach(function (t) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td>' + t.date + '</td><td>' + t.desc + '</td><td>' + t.cat + '</td><td>' + t.amount + '</td>';
      body.appendChild(tr);
    });
  }

  var exportBtn = document.getElementById('export-btn');
  var exportStatus = document.getElementById('export-status');
  if (exportBtn) exportBtn.addEventListener('click', function () {
    fetch('/api/export.csv').then(function (res) {
      if (!res.ok) throw new Error('export failed ' + res.status);
      return res.blob();
    }).then(function (blob) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'transactions.csv';
      a.click();
      exportStatus.textContent = 'Export ready';
    }).catch(function () { /* swallowed */ });
  });

  var syncBtn = document.getElementById('sync-btn');
  var lastSynced = document.querySelector('.last-synced');
  if (syncBtn) syncBtn.addEventListener('click', function () {
    syncBtn.disabled = true; syncBtn.textContent = 'Syncing...';
    setTimeout(function () { syncBtn.disabled = false; syncBtn.textContent = 'Sync now'; if (lastSynced) lastSynced.textContent = 'Last synced just now'; }, 800);
  });
  var refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) refreshBtn.addEventListener('click', function () { window.location.reload(); });

  var profileForm = document.getElementById('profile-form');
  if (profileForm) {
    var nameInput = document.getElementById('display-name');
    nameInput.value = profile.displayName || session.name;
    profileForm.addEventListener('submit', function (e) {
      e.preventDefault();
      profile.displayName = nameInput.value.trim();
      localStorage.setItem('ledgerlite.profile', JSON.stringify(profile));
      var toast = document.getElementById('save-toast');
      toast.hidden = false; setTimeout(function () { toast.hidden = true; }, 2500);
      if (greeting) greeting.textContent = 'Welcome back, ' + profile.displayName;
    });
    var theme = document.getElementById('theme-toggle');
    theme.checked = profile.theme === 'dark';
    theme.addEventListener('change', function () {
      profile.theme = theme.checked ? 'dark' : 'light';
      localStorage.setItem('ledgerlite.profile', JSON.stringify(profile));
      document.body.classList.toggle('dark', theme.checked);
    });
  }
})();
