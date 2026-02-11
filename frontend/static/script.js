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




// Terms Modal Logic (guarded)
const termsLink      = document.getElementById('open-terms');
const termsModal     = document.getElementById('termsModal');
const closeTerms     = document.getElementById('closeTerms');
const closeTermsBtn  = document.getElementById('closeTermsBtn');
const termsCheckbox  = document.getElementById('terms');
const submitButton   = document.querySelector('.submit-btn');

// Only attach handlers if the elements exist
if (termsLink && termsModal) {
    termsLink.addEventListener('click', function(e) {
        e.preventDefault();
        termsModal.style.display = 'block';
    });

    // Track that user opened the terms
    let hasOpenedTerms = false;
    termsLink.addEventListener('click', function() {
        hasOpenedTerms = true;
    });

    // Close handlers (if elements exist)
    if (closeTerms) {
        closeTerms.addEventListener('click', () => {
            termsModal.style.display = 'none';
        });
    }

    if (closeTermsBtn) {
        closeTermsBtn.addEventListener('click', () => {
            termsModal.style.display = 'none';
        });
    }

    // Click outside to close
    window.addEventListener('click', function(e) {
        if (e.target === termsModal) {
            termsModal.style.display = 'none';
        }
    });

    // Terms checkbox / submit button behavior
    if (termsCheckbox && submitButton) {
        termsCheckbox.addEventListener('change', function() {
            submitButton.disabled = !this.checked;
        });

        termsCheckbox.addEventListener('click', function(e) {
            if (!hasOpenedTerms) {
                e.preventDefault();
                alert('Please read the terms and conditions first.');
                termsModal.style.display = 'block';
            }
        });
    }
}


// ========== AVAILABILITY CHECK MODAL ==========
function checkAvailability() {
    const modal = document.getElementById('availabilityModal');
    if (modal) {
        modal.classList.add('active');
        console.log('Modal opened');
    }
}

// Initialize availability modal after DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing availability modal...');
    
    const availabilityModal = document.getElementById('availabilityModal');
    const closeAvailabilityBtn = document.getElementById('closeAvailabilityModal');
    const checkAvailabilityBtn = document.getElementById('checkAvailabilityBtn');
    const proceedBookingBtn = document.querySelector('.proceed-booking-btn');
    
    console.log('Modal found:', !!availabilityModal);
    console.log('Close btn found:', !!closeAvailabilityBtn);
    console.log('Check btn found:', !!checkAvailabilityBtn);
    console.log('Proceed btn found:', !!proceedBookingBtn);

    // Close button click handler
    if (closeAvailabilityBtn) {
        closeAvailabilityBtn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Close button clicked');
            if (availabilityModal) {
                availabilityModal.classList.remove('active');
                document.getElementById('availabilityCheckIn').value = '';
                document.getElementById('availabilityCheckOut').value = '';
                document.getElementById('availabilityResult').style.display = 'none';
            }
        };
    }

    // Close modal when clicking outside
    if (availabilityModal) {
        availabilityModal.onclick = function(e) {
            if (e.target === availabilityModal) {
                console.log('Outside click detected');
                availabilityModal.classList.remove('active');
                document.getElementById('availabilityCheckIn').value = '';
                document.getElementById('availabilityCheckOut').value = '';
                document.getElementById('availabilityResult').style.display = 'none';
            }
        };
    }

    // Check availability button
    if (checkAvailabilityBtn) {
        checkAvailabilityBtn.onclick = function() {
            console.log('Check availability clicked');
            const checkInInput = document.getElementById('availabilityCheckIn');
            const checkOutInput = document.getElementById('availabilityCheckOut');
            const resultContainer = document.getElementById('availabilityResult');
            const messageEl = document.getElementById('availabilityMessage');

            if (!checkInInput.value || !checkOutInput.value) {
                alert('Please select both check-in and check-out dates.');
                return;
            }

            const checkInDate = new Date(checkInInput.value);
            const checkOutDate = new Date(checkOutInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (checkInDate < today) {
                messageEl.textContent = 'Check-in date must be today or later.';
                resultContainer.classList.remove('success');
                resultContainer.classList.add('unavailable');
                resultContainer.style.display = 'block';
                return;
            }

            if (checkOutDate <= checkInDate) {
                messageEl.textContent = 'Check-out date must be after check-in date.';
                resultContainer.classList.remove('success');
                resultContainer.classList.add('unavailable');
                resultContainer.style.display = 'block';
                return;
            }

            const nights = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));
            const checkInFormatted = checkInDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const checkOutFormatted = checkOutDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

            // Pricing rules (match those used on pricing section)
            const RATES = { nightly: 200, weekly: 1200, monthly: 4000 };
            let baseCost = nights * RATES.nightly;
            if (nights >= 30) {
                baseCost = Math.floor(nights / 30) * RATES.monthly + (nights % 30) * RATES.nightly;
            } else if (nights >= 7) {
                baseCost = Math.floor(nights / 7) * RATES.weekly + (nights % 7) * RATES.nightly;
            }

            const taxRate = 0.04;
            const taxAmount = Math.round(baseCost * taxRate * 100) / 100; // 2 decimals
            const totalWithTax = Math.round((baseCost + taxAmount) * 100) / 100;

            messageEl.innerHTML = `✓ <strong>Available!</strong><br><br>
                                  Check-in: ${checkInFormatted}<br>
                                  Check-out: ${checkOutFormatted}<br>
                                  Total Nights: ${nights}<br><br>
                                  Estimated Cost: $${baseCost.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}<br>
                                  Tax (4%): $${taxAmount.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}<br>
                                  <strong>Total (incl. tax): $${totalWithTax.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</strong><br><br>
                                  Ready to complete your booking?`;
            resultContainer.classList.remove('unavailable');
            resultContainer.classList.add('success');
            resultContainer.style.display = 'block';

            // Persist estimate so booking page can use it
            try {
                localStorage.setItem('availableNights', String(nights));
                localStorage.setItem('estimateBase', String(baseCost));
                localStorage.setItem('estimateTax', String(taxAmount));
                localStorage.setItem('estimateTotal', String(totalWithTax));
                console.log('Stored estimate in localStorage');
            } catch (e) {
                console.warn('Could not store estimate in localStorage', e);
            }

            console.log('Availability check completed, result shown');
        };
    }

    // Proceed to booking button
    if (proceedBookingBtn) {
        proceedBookingBtn.onclick = function(e) {
            e.preventDefault();
            console.log('Proceed to booking clicked');
            const checkInInput = document.getElementById('availabilityCheckIn');
            const checkOutInput = document.getElementById('availabilityCheckOut');
            
            if (checkInInput.value && checkOutInput.value) {
                localStorage.setItem('selectedCheckIn', checkInInput.value);
                localStorage.setItem('selectedCheckOut', checkOutInput.value);
                console.log('Dates stored:', checkInInput.value, checkOutInput.value);
            }
            
            window.location.href = "/checkout/"; 
            
        };
    }
});
