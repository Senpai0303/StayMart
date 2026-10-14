document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    if (Auth.isLoggedIn()) {
      Auth.redirectByRole();
      return;
    }
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      if (!email || !password) {
        showToast('Please enter email and password.', 'error');
        return;
      }
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Logging in…';
      try {
        await Auth.login(email, password);
        showToast('Welcome back! 🎉', 'success');
        setTimeout(function () { Auth.redirectByRole(); }, 800);
      } catch (error) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
        showToast(error.message || 'Login failed. Check your credentials.', 'error');
      }
    });
  });
});