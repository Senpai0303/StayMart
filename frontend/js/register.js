document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    const card = document.querySelector('.auth-card');
    const form = document.getElementById('registerForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const cityInput = document.getElementById('city');
    const stateInput = document.getElementById('state');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const togglePassBtn = document.getElementById('togglePassBtn');
    const toggleConfirmPassBtn = document.getElementById('toggleConfirmPassBtn');

    // If already logged in, show options rather than an aggressive silent redirect
    if (Auth.isLoggedIn()) {
      const user = Auth.user;
      if (card && form) {
        const notice = document.createElement('div');
        notice.style.cssText = 'background:#e8f4fd;color:#0c5460;padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:14px;border:1px solid #bee5eb;line-height:1.5;';
        notice.innerHTML = `You are currently signed in as <strong>${escHtml(user ? (user.name || user.email) : 'User')}</strong>.<br/>
          <div style="margin-top:8px">
            <a href="index.html" class="btn btn-sm btn-outline" style="margin-right:8px;text-decoration:none">Back to Home</a>
            <button type="button" id="logoutToRegisterBtn" class="btn btn-sm btn-primary" style="font-size:12px;padding:6px 12px">Log Out to Create New Account</button>
          </div>`;
        card.insertBefore(notice, form);
        document.getElementById('logoutToRegisterBtn')?.addEventListener('click', function () {
          Auth.logout();
          window.location.reload();
        });
      }
    }

    // Toggle password visibility
    function setupToggle(btn, input) {
      if (!btn || !input) return;
      btn.addEventListener('click', function () {
        if (input.type === 'password') {
          input.type = 'text';
          btn.textContent = '🙈';
          btn.setAttribute('aria-label', 'Hide password');
        } else {
          input.type = 'password';
          btn.textContent = '👁️';
          btn.setAttribute('aria-label', 'Show password');
        }
      });
    }
    setupToggle(togglePassBtn, passwordInput);
    setupToggle(toggleConfirmPassBtn, confirmPasswordInput);

    // Clean initial inputs
    if (form) form.reset();

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const name = nameInput ? nameInput.value.trim() : '';
      const email = emailInput ? emailInput.value.trim().toLowerCase() : '';
      const phone = phoneInput ? phoneInput.value.trim() : '';
      const city = cityInput ? cityInput.value : '';
      const state = stateInput ? stateInput.value.trim() : 'Uttarakhand';
      const password = passwordInput ? passwordInput.value : '';
      const confirmPassword = confirmPasswordInput ? confirmPasswordInput.value : '';

      if (!name) {
        showToast('Please enter your full name.', 'error');
        if (nameInput) nameInput.focus();
        return;
      }
      if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
        showToast('Please enter a valid email address.', 'error');
        if (emailInput) emailInput.focus();
        return;
      }
      if (!phone || !/^[0-9]{10}$/.test(phone)) {
        showToast('Please enter a valid 10-digit mobile number.', 'error');
        if (phoneInput) phoneInput.focus();
        return;
      }
      if (!password || password.length < 6) {
        showToast('Password must be at least 6 characters long.', 'error');
        if (passwordInput) passwordInput.focus();
        return;
      }
      if (password !== confirmPassword) {
        showToast('Passwords do not match. Please check and retry.', 'error');
        if (confirmPasswordInput) confirmPasswordInput.focus();
        return;
      }

      const submitBtn = document.getElementById('submitBtn');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating account…';
      }

      try {
        await Auth.register({ name, email, password, phone, city, state });
        showToast('Account created successfully! Welcome to StayMart 🎉', 'success');
        setTimeout(function () {
          window.location.href = 'index.html';
        }, 800);
      } catch (error) {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Create Account';
        }
        showToast(error.message || 'Registration failed. Please try again.', 'error');
      }
    });
  });
});