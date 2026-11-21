document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    const card = document.querySelector('.auth-card');
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const togglePassBtn = document.getElementById('togglePassBtn');

    // If already logged in, show options rather than an aggressive silent redirect
    if (Auth.isLoggedIn()) {
      const user = Auth.user;
      if (card && form) {
        const notice = document.createElement('div');
        notice.style.cssText = 'background:#e8f4fd;color:#0c5460;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:14px;border:1px solid #bee5eb;line-height:1.5;';
        notice.innerHTML = `You are currently signed in as <strong>${escHtml(user ? (user.name || user.email) : 'User')}</strong>.<br/>
          <div style="margin-top:8px">
            <a href="index.html" class="btn btn-sm btn-outline" style="margin-right:8px;text-decoration:none">Back to Home</a>
            <button type="button" id="logoutToLoginBtn" class="btn btn-sm btn-primary" style="font-size:12px;padding:6px 12px">Log Out to Switch Account</button>
          </div>`;
        card.insertBefore(notice, form);
        document.getElementById('logoutToLoginBtn')?.addEventListener('click', function () {
          Auth.logout();
          window.location.reload();
        });
      }
    }

    // Prevent aggressive browser autofill of previous credentials
    if (form) form.reset();
    if (emailInput) emailInput.value = '';
    if (passwordInput) passwordInput.value = '';
    setTimeout(function () {
      if (emailInput && document.activeElement !== emailInput) emailInput.value = '';
      if (passwordInput && document.activeElement !== passwordInput) passwordInput.value = '';
    }, 150);

    // Toggle password visibility
    if (togglePassBtn && passwordInput) {
      togglePassBtn.addEventListener('click', function () {
        if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
          togglePassBtn.textContent = '🙈';
          togglePassBtn.setAttribute('aria-label', 'Hide password');
        } else {
          passwordInput.type = 'password';
          togglePassBtn.textContent = '👁️';
          togglePassBtn.setAttribute('aria-label', 'Show password');
        }
      });
    }

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const email = emailInput ? emailInput.value.trim() : '';
      const password = passwordInput ? passwordInput.value : '';
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