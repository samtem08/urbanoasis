/**
 * Booking API Integration
 * Fetches pricing rules and manages bookings through Django API
 */

const API_BASE_URL = '/api';

// Store available pricing rules
let pricingRules = [];

async function loadPricingRules() {
  try {
    const response = await fetch(`${API_BASE_URL}/pricing/`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    pricingRules = data.results || data;
    
    return pricingRules;
  } catch (error) {
    console.error('Error loading pricing rules:', error);
    return [];
  }
}

async function calculatePrice(pricingRuleId, checkInDate, checkOutDate, numGuests) {
  try {
    const checkIn = new Date(checkInDate);
    const checkOut = new Date(checkOutDate);
    const numNights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
    
    const response = await fetch(`${API_BASE_URL}/pricing/calculate/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pricing_rule_id: pricingRuleId,
        num_nights: numNights,
        num_guests: numGuests
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
    
  } catch (error) {
    console.error('Error calculating price:', error);
    return null;
  }
}

async function checkAvailability(checkInDate, checkOutDate) {
  try {
    const params = new URLSearchParams({
      check_in: checkInDate,
      check_out: checkOutDate
    });
    
    const response = await fetch(`${API_BASE_URL}/bookings/availability/?${params}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.available;
    
  } catch (error) {
    console.error('Error checking availability:', error);
    return true; // Assume available on error
  }
}

async function submitBooking(bookingData) {
  try {
    const response = await fetch(`${API_BASE_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData)
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
    
  } catch (error) {
    console.error('Error submitting booking:', error);
    throw error;
  }
}

// Initialize booking on page load
document.addEventListener('DOMContentLoaded', async () => {
  await loadPricingRules();
  
  // You can now use pricingRules throughout your booking form
  console.log('Pricing rules loaded:', pricingRules);
});
