/**
 * DEEPAK INTERVIEW HUB — Student Registration Controller
 * Validates inputs, handles registration API dispatch, and logs the user in upon success.
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
  if (APIClient.getToken()) {
    window.location.href = '/pages/dashboard.html';
    return;
  }

  const form = document.getElementById('register-form');
  const firstNameInput = document.getElementById('first_name');
  const lastNameInput = document.getElementById('last_name');
  const usernameInput = document.getElementById('username');
  const emailInput = document.getElementById('email');
  const branchSelect = document.getElementById('branch');
  const collegeInput = document.getElementById('college_name');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm_password');
  const registerBtn = document.getElementById('register-btn');
  const alertEl = document.getElementById('auth-alert');
  const alertMsg = document.getElementById('auth-alert-msg');

  function clearErrors() {
    alertEl.style.display = 'none';
    document.querySelectorAll('.form-error').forEach((el) => {
      el.style.display = 'none';
      el.textContent = '';
    });
    document.querySelectorAll('.form-input, .form-select').forEach((el) => {
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

    if (!firstNameInput.value.trim()) {
      showError(firstNameInput, document.getElementById('first_name-error'), 'First name is required');
      isValid = false;
    }

    if (!usernameInput.value.trim()) {
      showError(usernameInput, document.getElementById('username-error'), 'Username is required');
      isValid = false;
    } else if (usernameInput.value.trim().length < 3) {
      showError(usernameInput, document.getElementById('username-error'), 'Username must be at least 3 characters');
      isValid = false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailInput.value.trim()) {
      showError(emailInput, document.getElementById('email-error'), 'Email is required');
      isValid = false;
    } else if (!emailRegex.test(emailInput.value.trim())) {
      showError(emailInput, document.getElementById('email-error'), 'Please enter a valid email address');
      isValid = false;
    }

    if (!branchSelect.value) {
      showError(branchSelect, document.getElementById('branch-error'), 'Please select your branch');
      isValid = false;
    }

    if (!passwordInput.value) {
      showError(passwordInput, document.getElementById('password-error'), 'Password is required');
      isValid = false;
    } else if (passwordInput.value.length < 8) {
      showError(passwordInput, document.getElementById('password-error'), 'Password must be at least 8 characters');
      isValid = false;
    }

    if (passwordInput.value !== confirmPasswordInput.value) {
      showError(confirmPasswordInput, document.getElementById('confirm_password-error'), 'Passwords do not match');
      isValid = false;
    }

    return isValid;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validate()) return;

    registerBtn.disabled = true;
    const originalText = registerBtn.innerHTML;
    registerBtn.innerHTML = '<span class="btn-spinner"></span> Creating Account...';

    try {
      const payload = {
        username: usernameInput.value.trim(),
        email: emailInput.value.trim(),
        first_name: firstNameInput.value.trim(),
        last_name: lastNameInput.value.trim(),
        branch: branchSelect.value,
        college_name: collegeInput.value.trim(),
        password: passwordInput.value
      };

      const response = await APIClient.post('/auth/register/', payload);

      if (response && response.token) {
        APIClient.setToken(response.token);
        APIClient.setUser(response.user);
        Toast.success('Account created successfully! Welcome to Deepak Interview Hub.');
        setTimeout(() => {
          window.location.href = '/pages/dashboard.html';
        }, 600);
      } else {
        Toast.success('Account created! Please log in.');
        setTimeout(() => {
          window.location.href = '/pages/login.html';
        }, 600);
      }
    } catch (err) {
      alertEl.style.display = 'flex';
      alertMsg.textContent = err.message || 'Registration failed. Please check your details.';
      Toast.error(alertMsg.textContent);
    } finally {
      registerBtn.disabled = false;
      registerBtn.innerHTML = originalText;
    }
  });
});

