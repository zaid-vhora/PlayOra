// ============================
// SHARED COMPONENTS
// ============================

function getHeader(activePage = '') {
  const pages = [
    { label: 'Home', href: '/', key: 'home' },
    { label: 'Shop', href: '/shop_view/', key: 'shop' },
    {
      label: 'Toys', href: '/toy_view/', key: 'toys', children: [
        { label: 'All Toys', href: '/toy_view/' },
        { label: 'New Arrivals', href: '/toy_view/' },
        { label: 'Best Sellers', href: '/toy_view/' },
        { label: 'Deals', href: '/toy_view/' },
      ]
    },
    { label: 'Services', href: '/services_view/', key: 'services' },
    // { label: 'Blog', href: '/blog_view/', key: 'blog' },
    { label: 'About', href: '/about_view/', key: 'about' },
    { label: 'Contact', href: '/contact_view/', key: 'contact' },
  ];

  const menuItems = pages.map(p => {
    if (p.children) {
      const children = p.children.map(c => `<a href="${c.href}" class="dropdown-link">${c.label}</a>`).join('');
      return `<li class="nav-item dropdown">
        <a href="${p.href}" class="nav-link ${activePage === p.key ? 'active' : ''}">${p.label} <span class="arrow">▾</span></a>
        <div class="dropdown-menu">${children}</div>
      </li>`;
    }
    return `<li class="nav-item"><a href="${p.href}" class="nav-link ${activePage === p.key ? 'active' : ''}">${p.label}</a></li>`;
  }).join('');

  const mobileLinks = pages.map(p =>
    `<a href="${p.href}" class="mobile-nav-link">${p.label} <span>→</span></a>`
  ).join('');

  const isAuthenticated = window.USER_AUTH === 'true';
  const username = window.USER_NAME || 'User';

  const authSection = isAuthenticated ?
    `<div class="nav-user-dropdown dropdown">
        <a href="/profile_view/" class="btn btn-outline btn-sm">👋 ${username}</a>
        <div class="dropdown-menu" style="min-width: 150px;">
          <a href="/profile_view/" class="dropdown-link">👤 My Profile</a>
          <a href="/logout/" class="dropdown-link" style="color: #E53E3E;">🚪 Logout</a>
        </div>
     </div>` :
    `<div class="nav-auth-buttons" style="display:flex;gap:5px;">
        <a href="/login/" class="btn btn-primary btn-sm">Sign In</a>
        <div class="dropdown">
           <button class="btn btn-outline btn-sm dropdown-trigger">Register ▾</button>
           <div class="dropdown-menu">
              <a href="/user-register/" class="dropdown-link">User Register</a>
              <a href="/rental-register/" class="dropdown-link">Rental Partner</a>
           </div>
        </div>
     </div>`;

  const mobileAuth = isAuthenticated ?
    `<div style="margin-top:24px;display:flex;flex-direction:column;gap:10px">
      <a href="/profile_view/" class="btn btn-primary" style="justify-content:center">👤 Go to Profile</a>
      <a href="/logout/" class="btn btn-outline" style="justify-content:center; color:#E53E3E; border-color:#E53E3E;">🚪 Logout</a>
    </div>` :
    `<div style="margin-top:24px;display:flex;gap:10px">
      <a href="/login/" class="btn btn-primary" style="flex:1;justify-content:center">Sign In</a>
      <a href="/user-register/" class="btn btn-outline" style="flex:1;justify-content:center">Register</a>
    </div>`;

  return `
  <div class="promo-banner">
    🎉 FREE delivery on your first rental! Use code <strong>PLAY20</strong> for 20% off
    <button class="promo-close">✕</button>
  </div>
  <header class="header header-with-promo">
    <div class="container">
      <nav class="nav">
        <a href="/" class="nav-logo">
          <div class="nav-logo-icon">🧸</div>
          <span class="nav-logo-text">Play<span>Ora</span></span>
        </a>
        <ul class="nav-menu">${menuItems}</ul>
        <div class="nav-actions">
          <button class="nav-icon-btn search-trigger" data-tooltip="Search" aria-label="Search">🔍</button>
          <a href="/wishlist_view/" class="nav-icon-btn" data-tooltip="Wishlist" aria-label="Wishlist" style="position:relative;">
            ❤️ <span class="badge wishlist-badge" style="display:none">0</span>
          </a>
          <a href="/cart_view/" class="nav-icon-btn" data-tooltip="Cart" aria-label="Cart" style="position:relative;">
            🛒 <span class="badge cart-badge" style="display:none">0</span>
          </a>
          ${authSection}
        </div>
        <button class="hamburger" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </nav>
    </div>
  </header>
  <div class="mobile-menu">
    ${mobileLinks}
    ${mobileAuth}
  </div>
  <!-- Search Overlay -->
  <div class="search-overlay">
    <div class="search-box">
      <div class="search-input-wrap">
        <button class="search-submit-btn" style="background:none;border:none;font-size:20px;cursor:pointer">🔍</button>
        <input type="text" class="search-input" placeholder="Search for toys, brands, categories...">
        <button class="search-close" style="background:none;border:none;font-size:20px;cursor:pointer;color:#999">✕</button>
      </div>
      <div class="search-suggestions">
        <div class="search-sug-title">POPULAR SEARCHES</div>
        <a href="/shop_view/?q=lego" class="search-sug-item">🧱 LEGO Sets</a>
        <a href="/shop_view/?q=board+games" class="search-sug-item">🎲 Board Games</a>
        <a href="/shop_view/?q=outdoor" class="search-sug-item">🌳 Outdoor Toys</a>
        <a href="/shop_view/?q=educational" class="search-sug-item">📚 Educational Toys</a>
      </div>
    </div>
  </div>
  `;
}

function getFooter() {
  return `
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="footer-logo">
            <div class="footer-logo-icon">🧸</div>
            <span class="footer-logo-text">Play<span>Ora</span></span>
          </a>
          <p class="footer-desc">India's premier toy rental platform. Giving every child access to the best toys without the burden of ownership. Sustainable, affordable, and magical.</p>
          <div class="footer-socials">
            // <a href="#" class="social-btn" aria-label="Facebook">📘</a>
            // <a href="#" class="social-btn" aria-label="Instagram">📸</a>
            // <a href="#" class="social-btn" aria-label="Twitter">🐦</a>
            // <a href="#" class="social-btn" aria-label="YouTube">▶️</a>
            // <a href="https://wa.me/919316685580" class="social-btn" aria-label="WhatsApp">💬</a>
          </div>
        </div>
        <div>
          <h4 class="footer-heading">Quick Links</h4>
          <ul class="footer-links">
            <li><a href="/" class="footer-link">Home</a></li>
            <li><a href="/about_view/" class="footer-link">About Us</a></li>
            <li><a href="/shop_view/" class="footer-link">Shop</a></li>
            <li><a href="/services_view/" class="footer-link">Services</a></li>
            <li><a href="/contact_view/" class="footer-link">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 class="footer-heading">My Account</h4>
          <ul class="footer-links">
            <li><a href="/profile_view/" class="footer-link">My Profile</a></li>
            <li><a href="/ordersuccess_view/" class="footer-link">My Orders</a></li>
            <li><a href="/wishlist_view/" class="footer-link">Wishlist</a></li>
            <li><a href="/cart_view/" class="footer-link">My Cart</a></li>
            <li><a href="/login/" class="footer-link">Login</a></li>
            <li><a href="/user-register/" class="footer-link">Register</a></li>
          </ul>
        </div>
        <div>
          <h4 class="footer-heading">Contact Us</h4>
          <div class="footer-contact-item">
            <div class="footer-contact-icon">📍</div>
            <span>52,<br>Modasa, Arvalli 383315</span>
          </div>
          <div class="footer-contact-item">
            <div class="footer-contact-icon">📞</div>
            <span>+91 93166 85580</span>
          </div>
          <div class="footer-contact-item">
            <div class="footer-contact-icon">✉️</div>
            <span>mozaidv@gmail.com</span>
          </div>
          <h4 class="footer-heading" style="margin-top:20px;margin-bottom:12px">Newsletter</h4>
          <p style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:10px">Get deals & toy tips weekly!</p>
          <div class="newsletter-form">
            <input type="email" class="newsletter-input" placeholder="Your email">
            <button class="btn btn-primary btn-sm" onclick="showToast('🎉 Subscribed!','success')">Go</button>
          </div>
        </div>
      </div>
    </div>
    <div style="background:rgba(0,0,0,0.2)">
      <div class="container">
        <div class="footer-bottom">
          <p class="footer-copy">© 2025 <span>PLAYORA</span>. Made with ❤️ for little ones everywhere.</p>
          <div class="footer-bottom-links">
            <a href="#" class="footer-bottom-link">Privacy Policy</a>
            <a href="#" class="footer-bottom-link">Terms of Service</a>
            <a href="/faq_view/" class="footer-bottom-link">FAQ</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
  <button class="back-to-top" aria-label="Back to top">↑</button>
  `;
}

// Inject on load
document.addEventListener('DOMContentLoaded', () => {
  const headerEl = document.querySelector('#header-inject');
  const footerEl = document.querySelector('#footer-inject');
  const activePage = document.body.dataset.page || '';
  if (headerEl) headerEl.innerHTML = getHeader(activePage);
  if (footerEl) footerEl.innerHTML = getFooter();
});
