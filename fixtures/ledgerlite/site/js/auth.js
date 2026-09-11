(function () {
  var ACCOUNT = { email: 'demo@planted.test', password: 'planted-pass', name: 'Demo User' };
  var form = document.getElementById('login-form');
  var error = document.getElementById('login-error');
  if (localStorage.getItem('ledgerlite.session')) { window.location.href = 'dashboard.html'; return; }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value;
    if (email === ACCOUNT.email && password === ACCOUNT.password) {
      localStorage.setItem('ledgerlite.session', JSON.stringify({ email: email, name: ACCOUNT.name, at: Date.now() }));
      window.location.href = 'dashboard.html';
    } else {
      error.hidden = false;
    }
  });
})();
