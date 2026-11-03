/**
 * DEEPAK INTERVIEW HUB — Responsive Navbar & Drawer Controller
 * Handles desktop navigation, mobile drawer toggle, active route highlighting,
 * and sticky navbar scroll elevation.
 */

'use strict';

function initNavbar() {
  const mobileToggle = document.querySelector('.navbar-mobile-toggle');
  const drawer = document.querySelector('.mobile-drawer');
  const backdrop = document.querySelector('.mobile-drawer-backdrop');
  const drawerClose = document.querySelector('.mobile-drawer-close');
  const navbar = document.querySelector('.navbar');

  function openDrawer() {
    if (drawer && backdrop) {
      drawer.classList.add('is-open');
      backdrop.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'true');
    }
  }

  function closeDrawer() {
    if (drawer && backdrop) {
      drawer.classList.remove('is-open');
      backdrop.classList.remove('is-open');
      document.body.style.overflow = '';
      if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
    }
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (drawer && drawer.classList.contains('is-open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeDrawer);
  }

  if (drawerClose) {
    drawerClose.addEventListener('click', closeDrawer);
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) {
      closeDrawer();
    }
  });

  // Sticky Navbar background blur & shadow on scroll
  function handleScroll() {
    if (!navbar) return;
    if (window.scrollY > 40) {
      navbar.classList.add('is-scrolled');
    } else {
      navbar.classList.remove('is-scrolled');
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // initialize on load

  // Active route highlighting
  highlightActiveLinks();

  // Handle dropdown clicks for touch devices
  const dropdowns = document.querySelectorAll('.navbar-dropdown');
  dropdowns.forEach((dd) => {
    const trigger = dd.querySelector('.navbar-link');
    if (trigger) {
      trigger.addEventListener('click', (e) => {
        if (window.innerWidth < 1024) {
          e.preventDefault();
          dd.classList.toggle('is-open');
        }
      });
    }
  });
}

function highlightActiveLinks() {
  const currentPath = window.location.pathname.toLowerCase();
  const allLinks = document.querySelectorAll('.navbar-link, .mobile-drawer-link, .sidebar-link');

  allLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;
    const cleanHref = href.toLowerCase().split('?')[0].split('#')[0];

    // Check exact or relative match
    if (
      currentPath.endsWith(cleanHref) ||
      (cleanHref !== '/' && cleanHref !== 'index.html' && currentPath.includes(cleanHref))
    ) {
      link.classList.add('is-active');
    } else {
      link.classList.remove('is-active');
    }
  });
}

// Global initialization
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initNavbar);
} else {
  initNavbar();
}

