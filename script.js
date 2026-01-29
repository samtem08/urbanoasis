// ========== HAMBURGER MENU ==========
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
const overlay = document.getElementById('menuOverlay');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('active');
        overlay.classList.toggle('active');
    });
}

// Close menu when clicking overlay
if (overlay) {
    overlay.addEventListener('click', () => {
        navLinks.classList.remove('open');
        hamburger.classList.remove('active');
        overlay.classList.remove('active');
    });
}

// Close menu on link click (mobile)
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if(navLinks && navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
            if (hamburger) hamburger.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
        }
    });
});

// ========== SMOOTH SCROLL ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }

        // Close mobile menu after click
        if(navLinks && navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
        }
    });
});

// ========== LANGUAGE SWITCHER ==========
const langBtns = document.querySelectorAll('.lang-btn');
langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active from all
        langBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const lang = btn.id.replace('lang','').toLowerCase();

        document.querySelectorAll('[data-en]').forEach(el => {
            const text = el.getAttribute(`data-${lang}`);
            if(text) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = text;
                } else {
                    el.textContent = text;
                }
            }
        });
    });
});

// ========== LIGHTBOX ==========
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.querySelector('.lightbox-img');
const closeBtn = document.querySelector('.lightbox-close');

if (lightbox && lightboxImg) {
    document.querySelectorAll('.gallery-card img').forEach(img => {
        img.addEventListener('click', () => {
            lightboxImg.src = img.src;
            lightbox.classList.add('active');
        });
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            lightbox.classList.remove('active');
        });
    }

    lightbox.addEventListener('click', e => {
        if (e.target !== lightboxImg && e.target !== closeBtn) {
            lightbox.classList.remove('active');
        }
    });
}

// ========== PRICING SECTION ==========
document.addEventListener('DOMContentLoaded', function() {
    const RATES = {
        nightly: 200,
        weekly: 1200,
        monthly: 4000
    };

    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');
    const calcButton = document.getElementById('calculate-price');
    const resultContainer = document.getElementById('price-result');
    const totalPriceEl = document.getElementById('total-price');
    const breakdownEl = document.getElementById('price-breakdown');

    if (calcButton) {
        calcButton.addEventListener('click', function() {
            if (!checkInInput.value || !checkOutInput.value) {
                alert('Please select both check-in and check-out dates.');
                return;
            }

            const checkIn = new Date(checkInInput.value);
            const checkOut = new Date(checkOutInput.value);

            if (checkOut <= checkIn) {
                alert('Check-out date must be after check-in date.');
                return;
            }

            const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
            let baseCost = nights * 200;
            let discount = 0;
            let discountText = '';

            if (nights >= 30) {
                baseCost = Math.floor(nights / 30) * RATES.monthly + (nights % 30) * RATES.nightly;
                discount = (nights * 200) - baseCost;
                discountText = ' (Monthly rate applied)';
            } else if (nights >= 7) {
                baseCost = Math.floor(nights / 7) * RATES.weekly + (nights % 7) * RATES.nightly;
                discount = (nights * 200) - baseCost;
                discountText = ' (Weekly rate applied)';
            }

            totalPriceEl.textContent = '$' + Math.round(baseCost).toLocaleString();
            breakdownEl.textContent = nights + ' night' + (nights === 1 ? '' : 's') + 
                                     (discount > 0 ? ' - Save $' + Math.round(discount) : '') + 
                                     discountText;
            resultContainer.style.display = 'block';
        });
    }

    // Animate price cards on scroll
    const animatePrices = document.querySelectorAll('.animate-price');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    animatePrices.forEach(el => observer.observe(el));

    // Price card selection
    const priceCards = document.querySelectorAll('.price-card');
    priceCards.forEach(card => {
        card.addEventListener('click', function() {
            priceCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });
});




// Terms Modal Logic
const termsLink      = document.getElementById('open-terms');
const termsModal     = document.getElementById('termsModal');
const closeTerms     = document.getElementById('closeTerms');
const closeTermsBtn  = document.getElementById('closeTermsBtn');
const termsCheckbox  = document.getElementById('terms');
const submitButton   = document.querySelector('.submit-btn');

// Open modal when clicking "terms and conditions"
termsLink.addEventListener('click', function(e) {
    e.preventDefault();
    termsModal.style.display = 'block';
});

// Close modal ways
closeTerms.addEventListener('click', () => {
    termsModal.style.display = 'none';
});

closeTermsBtn.addEventListener('click', () => {
    termsModal.style.display = 'none';
    // Optional: auto-check the box after reading (common pattern)
    // termsCheckbox.checked = true;
    // submitButton.disabled = false;
});

window.addEventListener('click', function(e) {
    if (e.target === termsModal) {
        termsModal.style.display = 'none';
    }
});

// Optional: Enable submit button only after checkbox is checked
// (you can remove this if you prefer to keep HTML5 required validation only)
termsCheckbox.addEventListener('change', function() {
    submitButton.disabled = !this.checked;
});

// If you want to force user to open terms at least once before checking:
let hasOpenedTerms = false;

termsLink.addEventListener('click', function() {
    hasOpenedTerms = true;
});

termsCheckbox.addEventListener('click', function(e) {
    if (!hasOpenedTerms) {
        e.preventDefault();
        alert('Please read the terms and conditions first.');
        termsModal.style.display = 'block';
    }
});



// Close when clicking outside
window.addEventListener('click', function(e) {
    if (e.target === termsModal) closeModal();
});

