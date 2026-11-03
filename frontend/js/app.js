/**
 * DEEPAK INTERVIEW HUB — Main Application Orchestrator
 * Learn. Practise. Test. Get Interview Ready.
 */

'use strict';

const DeepakHub = (() => {
  function init() {
    // Check user authentication and update header UI
    syncAuthUI();

    // Setup global logout listeners
    document.querySelectorAll('[data-action="logout"]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        handleLogout();
      });
    });
  }

  function syncAuthUI() {
    const user = APIClient.getUser();
    const token = APIClient.getToken();
    const isAuthenticated = Boolean(token && user);

    const guestElements = document.querySelectorAll('.auth-guest-only');
    const userElements = document.querySelectorAll('.auth-user-only');
    const userNameElements = document.querySelectorAll('.auth-user-name');
    const userAvatarElements = document.querySelectorAll('.auth-user-avatar');

    guestElements.forEach((el) => {
      el.style.display = isAuthenticated ? 'none' : '';
    });

    userElements.forEach((el) => {
      el.style.display = isAuthenticated ? '' : 'none';
    });

    if (isAuthenticated && user) {
      userNameElements.forEach((el) => {
        el.textContent = user.first_name || user.username || 'Student';
      });
      userAvatarElements.forEach((el) => {
        const initial = (user.username || 'S').charAt(0).toUpperCase();
        el.textContent = initial;
      });
    }
  }

  async function handleLogout() {
    try {
      if (typeof APIClient !== 'undefined' && APIClient.getToken()) {
        try {
          await APIClient.post('/auth/logout/', {});
        } catch (e) {
          // Ignore network errors on logout
        }
        APIClient.clearAuth();
      }
      if (typeof Toast !== 'undefined') {
        Toast.success('Logged out successfully');
      }
      setTimeout(() => {
        window.location.href = '/pages/login.html';
      }, 500);
    } catch (err) {
      console.error('Logout error:', err);
      window.location.href = '/pages/login.html';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  return {
    syncAuthUI,
    handleLogout
  };
})();

