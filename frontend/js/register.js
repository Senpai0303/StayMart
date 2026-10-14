document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    if (Auth.isLoggedIn()) {
      Auth.redirectByRole();
      return;
    }
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const city = document.getElementById('city').value;
      const state = document.getElementById('state').value.trim() || 'Uttarakhand';
      const password = document.getElementById('password').value;

      if (!name || !email || !phone || !password) {
        showToast('Please fill in all required fields.', 'error');
        return;
      }
      if (!/^[0-9]{10}$/.test(phone)) {
        showToast('Please enter a valid 10-digit phone number.', 'error');
        return;
      }
      if (!/^\S+@\S+\.\S+$/.test(email)) {
        showToast('Please enter a valid email address.', 'error');
        return;
      }
      if (password.length < 6) {
        showToast('Password must be at least 6 characters.', 'error');
        return;
      }
      if (password !== document.getElementById('confirmPassword').value) {
        showToast('Passwords do not match.', 'error');
        return;
      }

      const submitBtn = document.getElementById('submitBtn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Creating account…';
      try {
        await Auth.register({ name, email, password, phone, city, state });
        showToast('Account created! Welcome to StayMart 🎉', 'success');
        setTimeout(function () { window.location.href = 'index.html'; }, 1000);
      } catch (error) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Create Account';
        showToast(error.message || 'Registration failed. Please try again.', 'error');
      }
    });
  });
});