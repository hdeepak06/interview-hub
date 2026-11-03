/**
 * DEEPAK INTERVIEW HUB — Toast Notification Utility
 * Provides lightweight, accessible, non-blocking alert toasts.
 */

'use strict';

const Toast = (() => {
  let container = null;

  function ensureContainer() {
    if (!container) {
      container = document.querySelector('.toast-container');
      if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        container.setAttribute('aria-live', 'polite');
        document.body.appendChild(container);
      }
    }
    return container;
  }

  function show({ title = '', message = '', type = 'info', duration = 4000 }) {
    const parent = ensureContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');

    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ'
    };

    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || 'ℹ'}</div>
      <div class="toast-content">
        ${title ? `<div class="toast-title">${title}</div>` : ''}
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" aria-label="Close notification">&times;</button>
      <div class="toast-progress"></div>
    `;

    const closeBtn = toast.querySelector('.toast-close');
    const progressBar = toast.querySelector('.toast-progress');

    function dismiss() {
      toast.classList.add('is-closing');
      setTimeout(() => {
        if (toast.parentElement) {
          toast.remove();
        }
      }, 250);
    }

    closeBtn.addEventListener('click', dismiss);

    if (duration > 0) {
      progressBar.style.transition = `transform ${duration}ms linear`;
      requestAnimationFrame(() => {
        progressBar.style.transform = 'scaleX(0)';
      });
      setTimeout(dismiss, duration);
    }

    parent.appendChild(toast);
  }

  return {
    success: (msg, title = 'Success') => show({ title, message: msg, type: 'success' }),
    error: (msg, title = 'Error') => show({ title, message: msg, type: 'error' }),
    warning: (msg, title = 'Warning') => show({ title, message: msg, type: 'warning' }),
    info: (msg, title = 'Notice') => show({ title, message: msg, type: 'info' })
  };
})();

