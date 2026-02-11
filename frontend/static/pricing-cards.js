/**
 * Pricing Cards Component
 * Fetches and displays pricing plans from Django API
 */

const API_BASE_URL = '/api';

/**
 * Load and render pricing cards from API
 * @param {string} containerId - ID of container element to render cards into
 * @param {object} options - Configuration options
 */
async function loadPricingCards(containerId = 'pricingCards', options = {}) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.warn(`Pricing cards container with id "${containerId}" not found`);
    return;
  }

  try {
    // Show loading state
    container.innerHTML = '<div class="pricing-loading">Loading pricing plans...</div>';

    const response = await fetch(`${API_BASE_URL}/pricing/`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    const pricingRules = (data.results || data).filter(rule => rule.is_active);

    if (pricingRules.length === 0) {
      container.innerHTML = '<p style="text-align: center; color: #999;">No pricing plans available.</p>';
      return;
    }

    // Sort by order and featured status
    pricingRules.sort((a, b) => {
      // Featured items first
      if (a.is_featured !== b.is_featured) {
        return b.is_featured ? 1 : -1;
      }
      // Then by order
      return a.order - b.order;
    });

    // Render cards
    container.innerHTML = '';
    pricingRules.forEach((rule, index) => {
      const card = createPricingCard(rule);
      container.appendChild(card);
    });

  } catch (error) {
    console.error('Error loading pricing cards:', error);
    container.innerHTML = '<div style="color: red; padding: 20px;">Error loading pricing plans. Please try again later.</div>';
  }
}

/**
 * Create a pricing card element
 * @param {object} rule - Pricing rule object from API
 * @returns {HTMLElement} Card element
 */
function createPricingCard(rule) {
  const card = document.createElement('div');
  card.className = `pricing-card ${rule.is_featured ? 'featured' : ''}`;
  
  const imageHtml = rule.image_url ? `<div class="pricing-card-image"><img src="${rule.image_url}" alt="${rule.name}"></div>` : '';
  
  const descriptionHtml = rule.description ? `<p class="pricing-description">${escapeHtml(rule.description)}</p>` : '';
  
  const seasonBadge = `<span class="season-badge season-${rule.season}">${capitalizeFirst(rule.season)} Season</span>`;
  
  const dateRangeHtml = rule.start_date && rule.end_date 
    ? `<p class="date-range">${formatDate(rule.start_date)} - ${formatDate(rule.end_date)}</p>`
    : '';
  
  const weeklyDiscount = rule.weekly_discount_percent > 0 
    ? `<li><strong>Weekly (7+ nights):</strong> ${rule.weekly_discount_percent}% off</li>`
    : '';
  
  const monthlyDiscount = rule.monthly_discount_percent > 0
    ? `<li><strong>Monthly (30+ nights):</strong> ${rule.monthly_discount_percent}% off</li>`
    : '';

  const feesHtml = (rule.cleaning_fee > 0 || rule.service_fee_percent > 0)
    ? `
      <div class="fees-section">
        <h4>Additional Fees</h4>
        <ul>
          ${rule.cleaning_fee > 0 ? `<li>Cleaning Fee: $${parseFloat(rule.cleaning_fee).toFixed(2)}</li>` : ''}
          ${rule.service_fee_percent > 0 ? `<li>Service Fee: ${rule.service_fee_percent}%</li>` : ''}
        </ul>
      </div>
    `
    : '';

  // Features list from admin
  const featuresHtml = rule.features_list && rule.features_list.length > 0
    ? `
      <div class="features-section">
        <h4>Features</h4>
        <ul>
          ${rule.features_list.map(f => `<li>${escapeHtml(f)}</li>`).join('')}
        </ul>
      </div>
    `
    : '';

  card.innerHTML = `
    ${imageHtml}
    <div class="pricing-card-content">
      <div class="pricing-card-header">
        <h3 class="pricing-name">${escapeHtml(rule.name)}</h3>
        ${seasonBadge}
      </div>
      
      ${descriptionHtml}
      ${dateRangeHtml}
      
      <div class="pricing-main">
        <h3 class="pricing-display-label">${escapeHtml(rule.display_label)}</h3>
        <div class="base-price">
          <span class="price-amount">$${parseFloat(rule.display_price).toFixed(2)}</span>
          <span class="price-unit">${escapeHtml(rule.display_price_unit)}</span>
        </div>
      </div>
      
      ${featuresHtml}
      
      ${weeklyDiscount || monthlyDiscount ? `
        <div class="discounts-section">
          <h4>Duration Discounts</h4>
          <ul>
            ${weeklyDiscount}
            ${monthlyDiscount}
          </ul>
        </div>
      ` : ''}
      
      ${feesHtml}
      
      <button class="pricing-select-btn" data-pricing-id="${rule.id}" onclick="selectPricingRule(${rule.id})">
        Select This Plan
      </button>
    </div>
  `;

  return card;
}

/**
 * Handle pricing plan selection
 * @param {number} pricingId - Pricing rule ID
 */
function selectPricingRule(pricingId) {
  console.log('Selected pricing rule:', pricingId);
  
  // Store selected pricing rule ID
  localStorage.setItem('selectedPricingRuleId', pricingId);
  
  // Optional: Scroll to booking form or perform other action
  const bookingForm = document.getElementById('bookingForm');
  if (bookingForm) {
    bookingForm.scrollIntoView({ behavior: 'smooth' });
  }
  
  // Dispatch custom event
  window.dispatchEvent(new CustomEvent('pricingRuleSelected', { detail: { pricingId } }));
}

/**
 * Get selected pricing rule ID from storage
 * @returns {number|null} Pricing rule ID or null
 */
function getSelectedPricingRuleId() {
  const id = localStorage.getItem('selectedPricingRuleId');
  return id ? parseInt(id, 10) : null;
}

/**
 * Utility: Format date string
 * @param {string} dateStr - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateStr).toLocaleDateString('en-US', options);
}

/**
 * Utility: Capitalize first letter
 * @param {string} str - String to capitalize
 * @returns {string} Capitalized string
 */
function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Utility: Escape HTML characters
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  // Auto-load if container exists
  if (document.getElementById('pricingCards')) {
    loadPricingCards();
  }
});
