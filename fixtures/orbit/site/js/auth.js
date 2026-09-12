// Demo-only auth: one seeded user, session flag in localStorage.
(function () {
  var ACCOUNT = { email: 'demo@orbit.test', password: 'orbit-pass', name: 'Demo User' };
  if (localStorage.getItem('orbit.session')) { window.location.href = 'board.html'; return; }
  var form = document.getElementById('login-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value;
    var err = document.getElementById('login-error');
    if (email === ACCOUNT.email && password === ACCOUNT.password) {
      localStorage.setItem('orbit.session', JSON.stringify({ email: email, name: ACCOUNT.name }));
      window.location.href = 'board.html';
    } else {
      err.textContent = 'That email and password do not match.';
      err.style.display = 'block';
      document.getElementById('password').setAttribute('aria-invalid', 'true');
    }
  });
})();
