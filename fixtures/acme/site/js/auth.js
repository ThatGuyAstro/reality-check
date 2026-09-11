// Demo-only auth: one seeded user, session flag in localStorage.
(function () {
  var form = document.getElementById('login-form');
  var err = document.getElementById('login-error');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var email = document.getElementById('email').value.trim();
    var pw = document.getElementById('password').value;
    if (email === 'demo@example.com' && pw === 'demo1234') {
      localStorage.setItem('acme.session', JSON.stringify({ name: 'Demo User', email: email }));
      window.location.href = 'dashboard.html';
    } else {
      err.classList.add('show');
    }
  });
})();
