// Shared app script: session guard, greeting, settings save, sign out.
(function () {
  var raw = localStorage.getItem('acme.session');
  if (!raw) { window.location.href = 'index.html'; return; }
  var session = JSON.parse(raw);

  var greeting = document.getElementById('greeting');
  if (greeting) greeting.textContent = 'Welcome back, ' + session.name + '.';

  var signOut = document.getElementById('sign-out');
  if (signOut) signOut.addEventListener('click', function () { localStorage.removeItem('acme.session'); });

  var settings = document.getElementById('settings-form');
  if (settings) {
    var nameInput = document.getElementById('display-name');
    nameInput.value = session.name;
    settings.addEventListener('submit', function (e) {
      e.preventDefault();
      session.name = nameInput.value.trim() || session.name;
      localStorage.setItem('acme.session', JSON.stringify(session));
      var toast = document.getElementById('toast');
      toast.classList.add('show');
      setTimeout(function () { toast.classList.remove('show'); }, 2500);
    });
  }

  // TODO: wire up CSV export
  var exportBtn = document.getElementById('export-csv');
  void exportBtn;
})();
