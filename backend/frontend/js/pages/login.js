/**
 * DEEPAK INTERVIEW HUB — Login Controller
 * Handles client-side validation, authentication API request, and token storage.
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
  // If already logged in, redirect to dashboard
  if (APIClient.getToken()) {
    window.location.href = '/pages/dashboard.html';
    return;
  }

  const form = document.getElementById('login-form');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const loginBtn = document.getElementById('login-btn');
  const alertEl = document.getElementById('auth-alert');
  const alertMsg = document.getElementById('auth-alert-msg');

  function clearErrors() {
    alertEl.style.display = 'none';
    document.querySelectorAll('.form-error').forEach((el) => {
      el.style.display = 'none';
      el.textContent = '';
    });
    document.querySelectorAll('.form-input').forEach((el) => {
      el.classList.remove('is-invalid');
    });
  }

  function showError(inputEl, errorEl, message) {
    inputEl.classList.add('is-invalid');
    errorEl.textContent = message;
    errorEl.style.display = 'block';
  }

  function validate() {
    clearErrors();
    let isValid = true;

    if (!usernameInput.value.trim()) {
      showError(usernameInput, document.getElementById('username-error'), 'Username or email is required');
      isValid = false;
    }

    if (!passwordInput.value) {
      showError(passwordInput, document.getElementById('password-error'), 'Password is required');
      isValid = false;
    }

    return isValid;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validate()) return;

    // Loading state
    loginBtn.disabled = true;
    const originalText = loginBtn.innerHTML;
    loginBtn.innerHTML = '<span class="btn-spinner"></span> Signing in...';

    try {
      const response = await APIClient.post('/auth/login/', {
        username: usernameInput.value.trim(),
        password: passwordInput.value
      });

      if (response && response.token) {
        APIClient.setToken(response.token);
        APIClient.setUser(response.user);
        Toast.success('Login successful! Redirecting to dashboard...');
        setTimeout(() => {
          window.location.href = '/pages/dashboard.html';
        }, 500);
      } else {
        throw new Error('Authentication failed: No token received.');
      }
    } catch (err) {
      alertEl.style.display = 'flex';
      alertMsg.textContent = err.message || 'Invalid username or password. Please try again.';
      Toast.error(alertMsg.textContent);
    } finally {
      loginBtn.disabled = false;
      loginBtn.innerHTML = originalText;
    }
  });
});

