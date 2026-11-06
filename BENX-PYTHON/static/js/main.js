// ============================================================
// BENX XITERS — Main JavaScript
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

  // ---- PRELOADER ----
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => {
      preloader?.classList.add('hidden');
    }, 1200);
  });

  // ---- NAVBAR SCROLL ----
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 50);
  });

  // ---- HAMBURGER MENU ----
  const hamburger = document.getElementById('hamburger');
  let mobileMenu = document.getElementById('mobileMenu');

  if (hamburger && !mobileMenu) {
    mobileMenu = document.createElement('div');
    mobileMenu.id = 'mobileMenu';
    mobileMenu.className = 'mobile-menu';
    const links = [
      { href: 'index.html', text: 'Home' },
      { href: 'products.html', text: 'Products' },
      { href: 'pricing.html', text: 'Pricing' },
      { href: 'features.html', text: 'Features' },
      { href: 'contact.html', text: 'Contact' },
      { href: 'login.html', text: 'Login' },
      { href: 'register.html', text: 'Get Started' },
    ];
    links.forEach(l => {
      const a = document.createElement('a');
      a.href = l.href; a.textContent = l.text;
      mobileMenu.appendChild(a);
    });
    document.body.appendChild(mobileMenu);
  }

  hamburger?.addEventListener('click', () => {
    mobileMenu?.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    if (mobileMenu?.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });

  // ---- SCROLL TO TOP ----
  const scrollTopBtn = document.createElement('div');
  scrollTopBtn.className = 'scroll-top';
  scrollTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
  document.body.appendChild(scrollTopBtn);

  window.addEventListener('scroll', () => {
    scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
  });
  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ---- COUNTER ANIMATION ----
  const counters = document.querySelectorAll('[data-count]');
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-count'));
        let current = 0;
        const step = target / 60;
        const timer = setInterval(() => {
          current += step;
          if (current >= target) { current = target; clearInterval(timer); }
          el.textContent = Math.floor(current).toLocaleString();
        }, 25);
        countObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => countObserver.observe(c));

  // ---- PARTICLES BG ----
  const particlesBg = document.getElementById('particles-bg');
  if (particlesBg) {
    for (let i = 0; i < 40; i++) {
      const dot = document.createElement('div');
      dot.style.cssText = `
        position:absolute;
        width:${Math.random()*3+1}px;
        height:${Math.random()*3+1}px;
        border-radius:50%;
        background:rgba(${Math.random()>0.5?'124,58,237':'6,182,212'},${Math.random()*0.4+0.1});
        left:${Math.random()*100}%;
        top:${Math.random()*100}%;
        animation: particleFloat ${Math.random()*15+8}s linear ${Math.random()*8}s infinite;
      `;
      particlesBg.appendChild(dot);
    }
    if (!document.getElementById('particleStyle')) {
      const st = document.createElement('style');
      st.id = 'particleStyle';
      st.textContent = `
        @keyframes particleFloat {
          0%   { transform: translateY(0) translateX(0); opacity:0; }
          10%  { opacity:1; }
          90%  { opacity:1; }
          100% { transform: translateY(-100vh) translateX(${Math.random()>0.5?'+':'-'}50px); opacity:0; }
        }
      `;
      document.head.appendChild(st);
    }
  }

  // ---- PRICING TOGGLE ----
  const pricingToggle = document.getElementById('pricingToggle');
  if (pricingToggle) {
    pricingToggle.addEventListener('change', () => {
      const dailyPrices  = document.querySelectorAll('.plan-price.daily');
      const monthlyPrices= document.querySelectorAll('.plan-price.monthly');
      if (pricingToggle.checked) {
        dailyPrices.forEach(p => p.style.display = 'none');
        monthlyPrices.forEach(p => p.style.display = 'block');
      } else {
        dailyPrices.forEach(p => p.style.display = 'block');
        monthlyPrices.forEach(p => p.style.display = 'none');
      }
    });
  }

  // ---- AOS FADE ANIMATION (simple) ----
  const aosEls = document.querySelectorAll('[data-aos]');
  const aosObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.getAttribute('data-delay') || 0;
        setTimeout(() => entry.target.classList.add('aos-visible'), parseInt(delay));
        aosObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  aosEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    aosObserver.observe(el);
  });

  document.head.insertAdjacentHTML('beforeend', `
    <style>
      .aos-visible { opacity:1 !important; transform:translateY(0) !important; }
    </style>
  `);

  // ---- TOAST NOTIFICATION ----
  window.showToast = (msg, type = 'success') => {
    const toast = document.createElement('div');
    toast.style.cssText = `
      position:fixed; bottom:90px; right:30px; z-index:9999;
      background:${type==='success'?'rgba(16,185,129,.95)':'rgba(239,68,68,.95)'};
      color:#fff; padding:14px 20px; border-radius:12px;
      font-family:'Rajdhani',sans-serif; font-weight:600; font-size:15px;
      box-shadow:0 8px 30px rgba(0,0,0,.3);
      animation: toastIn .3s ease;
    `;
    toast.textContent = msg;
    document.body.appendChild(toast);
    if (!document.getElementById('toastStyle')) {
      const s = document.createElement('style');
      s.id = 'toastStyle';
      s.textContent = `@keyframes toastIn{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:translateX(0)}}`;
      document.head.appendChild(s);
    }
    setTimeout(() => toast.remove(), 3000);
  };

  // ---- ACTIVE NAV LINK ----
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === currentPage) a.classList.add('active');
    else a.classList.remove('active');
  });

  // ---- SMOOTH HOVER GLOW ON CARDS ----
  document.querySelectorAll('.feature-card, .product-card, .pricing-card, .testimonial-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty('--mouse-x', x + '%');
      card.style.setProperty('--mouse-y', y + '%');
    });
  });

});

