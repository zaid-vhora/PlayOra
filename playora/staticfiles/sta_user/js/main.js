// ============================
// TOYRENT - MAIN JS
// ============================

// Cart & Wishlist state
let cart = JSON.parse(localStorage.getItem('tr_cart') || '[]');
let wishlist = JSON.parse(localStorage.getItem('tr_wishlist') || '[]');

// Update badges
function updateBadges() {
  const serverCartCount = window.CART_COUNT;
  const serverWishlistCount = window.WISHLIST_COUNT;
  document.querySelectorAll('.cart-badge').forEach(el => {
    const count = serverCartCount !== undefined ? serverCartCount : cart.reduce((s, i) => s + i.qty, 0);
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });
  document.querySelectorAll('.wishlist-badge').forEach(el => {
    const count = serverWishlistCount !== undefined ? serverWishlistCount : wishlist.length;
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });
}

// Add to cart
function addToCart(id, name, price, img, period = '/week') {
  // We'll now use the Django backend for the cart
  fetch(`/cart/add/${id}/`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      showToast('🛒 Added to cart!', 'success');
      // Update badge if possible (here we might need to refresh or fetch count)
      // For now, let's just increment the badge locally for immediate feedback
      document.querySelectorAll('.cart-badge').forEach(el => {
        let current = parseInt(el.textContent) || 0;
        el.textContent = current + 1;
        el.style.display = 'flex';
      });
    } else {
      window.location.href = '/login/'; // Redirect to login if not authenticated
    }
  })
  .catch(error => {
    console.error('Error adding to cart:', error);
    // If not logged in, the redirect from @login_required might cause a CORS issue with fetch
    // So we handle it by redirecting to login
    window.location.href = '/login/';
  });
}

// Toggle wishlist
function toggleWishlist(id, name, price, img) {
  fetch(`/wishlist/add/${id}/`, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      showToast('❤️ Added to wishlist!', 'success');
      // Update badge locally
      document.querySelectorAll('.wishlist-badge').forEach(el => {
        let current = parseInt(el.textContent) || 0;
        el.textContent = current + 1;
        el.style.display = 'flex';
      });
    } else {
      window.location.href = '/login/';
    }
  })
  .catch(error => {
    console.error('Error toggling wishlist:', error);
    window.location.href = '/login/';
  });
}

// Toast
function showToast(message, type = 'success') {
  const existing = document.querySelector('.toast-container');
  if (!existing) {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = `
      position:fixed; bottom:24px; left:50%; transform:translateX(-50%);
      z-index:9999; display:flex; flex-direction:column; gap:8px; align-items:center;
    `;
    document.body.appendChild(container);
  }
  const container = document.querySelector('.toast-container');
  const colors = { success: '#4ECDC4', error: '#FF4757', info: '#667eea', warning: '#FF6B35' };
  const toast = document.createElement('div');
  toast.style.cssText = `
    background: ${colors[type] || colors.success};
    color: white; padding: 12px 24px; border-radius: 50px;
    font-weight: 700; font-size: 14px; font-family: 'Nunito', sans-serif;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    animation: slideUp 0.4s ease;
    white-space: nowrap;
  `;
  toast.textContent = message;

  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
  `;
  document.head.appendChild(style);
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; setTimeout(() => toast.remove(), 300); }, 2500);
}

// Header scroll
function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 20);
  });
}

// Mobile menu
function initMobileMenu() {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!hamburger || !mobileMenu) return;
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
  });
}

// Back to top
function initBackToTop() {
  const btn = document.querySelector('.back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// Fade in animations
function initFadeIn() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// Search overlay
function initSearch() {
  // Event delegation for opening
  document.addEventListener('click', e => {
    const trigger = e.target.closest('.search-trigger');
    if (trigger) {
      const overlay = document.querySelector('.search-overlay');
      if (overlay) {
        overlay.classList.add('active');
        overlay.querySelector('.search-input')?.focus();
      }
    }

    // Delegation for closing
    const closeBtn = e.target.closest('.search-close');
    const overlay = e.target.closest('.search-overlay');
    if (closeBtn || (overlay && e.target === overlay)) {
      document.querySelector('.search-overlay')?.classList.remove('active');
    }

    // Delegation for submit button
    const submitBtn = e.target.closest('.search-submit-btn');
    if (submitBtn) {
      const query = document.querySelector('.search-input')?.value.trim();
      if (query) window.location.href = `/shop_view/?q=${encodeURIComponent(query)}`;
    }
  });

  // Delegation for Enter key
  document.addEventListener('keypress', e => {
    if (e.key === 'Enter' && e.target.classList.contains('search-input')) {
      const query = e.target.value.trim();
      if (query) window.location.href = `/shop_view/?q=${encodeURIComponent(query)}`;
    }
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') document.querySelector('.search-overlay')?.classList.remove('active');
  });

  // Hero Search (Home Page)
  document.addEventListener('click', e => {
    const heroBtn = e.target.closest('.hero-search-btn');
    if (heroBtn) {
      const query = document.querySelector('.hero-search-input')?.value.trim();
      if (query) window.location.href = `/shop_view/?q=${encodeURIComponent(query)}`;
    }
  });

  document.addEventListener('keypress', e => {
    if (e.key === 'Enter' && e.target.classList.contains('hero-search-input')) {
      const query = e.target.value.trim();
      if (query) window.location.href = `/shop_view/?q=${encodeURIComponent(query)}`;
    }
  });
}

// Promo banner close
function initPromoBanner() {
  const btn = document.querySelector('.promo-close');
  const banner = document.querySelector('.promo-banner');
  if (!btn || !banner) return;
  btn.addEventListener('click', () => {
    banner.style.display = 'none';
    document.querySelector('.header')?.classList.remove('header-with-promo');
    document.querySelector('.header')?.style.setProperty('top', '0');
  });
}

// Qty controls
function initQtyControls() {
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const wrap = btn.closest('.qty-control');
      const numEl = wrap.querySelector('.qty-num');
      let val = parseInt(numEl.textContent);
      if (btn.dataset.action === 'minus') val = Math.max(1, val - 1);
      else val++;
      numEl.textContent = val;
    });
  });
}

// Star rating
function initStarRating() {
  document.querySelectorAll('.star-rating').forEach(wrap => {
    const stars = wrap.querySelectorAll('.star');
    stars.forEach((star, idx) => {
      star.addEventListener('mouseover', () => {
        stars.forEach((s, i) => s.classList.toggle('active', i <= idx));
      });
      star.addEventListener('click', () => {
        wrap.dataset.rating = idx + 1;
        stars.forEach((s, i) => s.classList.toggle('active', i <= idx));
      });
    });
    wrap.addEventListener('mouseleave', () => {
      const rating = parseInt(wrap.dataset.rating || 0);
      stars.forEach((s, i) => s.classList.toggle('active', i < rating));
    });
  });
}

// Filter toggle (mobile)
function initFilterToggle() {
  const toggleBtn = document.querySelector('.filter-toggle');
  const sidebar = document.querySelector('.filter-sidebar');
  if (!toggleBtn || !sidebar) return;
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
  });
}

// Tab system
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabGroup = btn.closest('.tab-group') || btn.closest('[data-tabs]')?.parentElement;
      const target = btn.dataset.tab;
      if (!target) return;
      document.querySelectorAll('.tab-btn').forEach(b => {
        if (b.dataset.tabGroup === btn.dataset.tabGroup || tabGroup?.contains(b)) b.classList.remove('active');
      });
      btn.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(content => {
        if (content.dataset.tabGroup === btn.dataset.tabGroup || tabGroup?.contains(content)) content.classList.remove('active');
        if (content.id === target) content.classList.add('active');
      });
    });
  });
}

// Wishlist button state
function initWishlistButtons() {
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    const id = btn.dataset.id;
    if (id && wishlist.some(i => i.id === id)) btn.classList.add('active');
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleWishlist(
        btn.dataset.id,
        btn.dataset.name,
        btn.dataset.price,
        btn.dataset.img
      );
    });
  });
}

// Add to cart button
function initCartButtons() {
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      addToCart(
        btn.dataset.id,
        btn.dataset.name,
        btn.dataset.price,
        btn.dataset.img
      );
    });
  });
}

// Password toggle
function initPasswordToggle() {
  document.querySelectorAll('.pw-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling || document.querySelector(btn.dataset.target);
      if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
        btn.textContent = input.type === 'password' ? '👁️' : '🙈';
      }
    });
  });
}

// Form validation helper
function validateForm(formEl) {
  let valid = true;
  formEl.querySelectorAll('[required]').forEach(input => {
    if (!input.value.trim()) {
      input.style.borderColor = '#FF4757';
      valid = false;
    } else {
      input.style.borderColor = '';
    }
  });
  return valid;
}

// Counter animation
function animateCounter(el) {
  const target = parseInt(el.dataset.count);
  const duration = 1500;
  const start = performance.now();
  function update(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target).toLocaleString() + (el.dataset.suffix || '');
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function initCounters() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { animateCounter(e.target); observer.unobserve(e.target); }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => observer.observe(el));
}

// Image gallery (toy detail)
function initGallery() {
  const mainImg = document.querySelector('.gallery-main img');
  document.querySelectorAll('.gallery-thumb').forEach(thumb => {
    thumb.addEventListener('click', () => {
      if (mainImg) mainImg.src = thumb.src;
      document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });
}

// Coupon code
function applyCoupon() {
  const input = document.querySelector('.coupon-input');
  if (!input) return;
  const codes = { 'PLAY20': 20, 'KIDS10': 10, 'FIRST15': 15 };
  const disc = codes[input.value.toUpperCase()];
  if (disc) {
    showToast(`🎉 Coupon applied! ${disc}% off`, 'success');
    const discRow = document.querySelector('.discount-row .value');
    if (discRow) discRow.textContent = `-${disc}%`;
  } else {
    showToast('❌ Invalid coupon code', 'error');
  }
}

// Init all
document.addEventListener('DOMContentLoaded', () => {
  updateBadges();
  initHeader();
  initMobileMenu();
  initBackToTop();
  initFadeIn();
  initSearch();
  initPromoBanner();
  initQtyControls();
  initStarRating();
  initTabs();
  initWishlistButtons();
  initCartButtons();
  initPasswordToggle();
  initCounters();
  initGallery();
  initFilterToggle();
});
