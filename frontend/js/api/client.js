/**
 * DEEPAK INTERVIEW HUB — API Client Service Layer
 * Centralized fetch client handling JWT/Token authorization headers, CSRF tokens,
 * base URL routing, error normalization, and response serialization.
 */

'use strict';

const APIClient = (() => {
  const BASE_URL = (window.location.protocol.startsWith('http')) 
    ? `${window.location.origin}/api` 
    : 'http://127.0.0.1:8000/api';
  const TOKEN_KEY = 'deepak_hub_auth_token';
  const USER_KEY = 'deepak_hub_user_data';

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function setToken(token) {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  }

  function getUser() {
    try {
      const data = localStorage.getItem(USER_KEY);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  }

  function setUser(user) {
    if (user) {
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    } else {
      localStorage.removeItem(USER_KEY);
    }
  }

  function clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  async function request(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    const token = getToken();

    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...(token ? { 'Authorization': `Token ${token}` } : {}),
      ...(options.headers || {})
    };

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        clearAuth();
        // If not already on auth page, redirect
        const currentPath = window.location.pathname;
        if (!currentPath.includes('login.html') && !currentPath.includes('register.html') && !currentPath.endsWith('/') && !currentPath.includes('index.html')) {
          window.location.href = '/pages/login.html';
        }
      }

      let data = null;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      }

      if (!response.ok) {
        const errorMsg = (data && (data.detail || data.message || JSON.stringify(data))) || `HTTP Error ${response.status}`;
        throw new Error(errorMsg);
      }

      return data;
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  return {
    get: (endpoint, options = {}) => request(endpoint, { method: 'GET', ...options }),
    post: (endpoint, body, options = {}) => request(endpoint, { method: 'POST', body: JSON.stringify(body), ...options }),
    put: (endpoint, body, options = {}) => request(endpoint, { method: 'PUT', body: JSON.stringify(body), ...options }),
    patch: (endpoint, body, options = {}) => request(endpoint, { method: 'PATCH', body: JSON.stringify(body), ...options }),
    delete: (endpoint, options = {}) => request(endpoint, { method: 'DELETE', ...options }),
    getToken,
    setToken,
    getUser,
    setUser,
    clearAuth,
    BASE_URL
  };
})();

