/**
 * Gallery API Integration
 * Fetches gallery images from Django API and dynamically populates the gallery
 */

const API_BASE_URL = '/api';

// Category mapping from API to filter classes
const categoryMap = {
  'living': 'rooms',
  'bedroom': 'rooms',
  'kitchen': 'amenities',
  'bathroom': 'amenities',
  'laundry': 'amenities',
  'dining': 'amenities',
  'exterior': 'exterior',
  'neighborhood': 'neighborhood'
};

async function loadGalleryImages() {
  try {
    const response = await fetch(`${API_BASE_URL}/gallery/`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const images = await response.json();
    const results = images.results || images;
    
    renderGalleryCards(results);
    renderCarouselItems(results);
    initializeGalleryFilters();
    
  } catch (error) {
    console.error('Error loading gallery images:', error);
    // Fallback: Keep static content if API fails
  }
}

function renderGalleryCards(images) {
  const galleryMasonry = document.getElementById('galleryMasonry');
  if (!galleryMasonry) return;
  
  // Clear existing cards
  galleryMasonry.innerHTML = '';
  
  // Add new cards from API
  images.forEach(image => {
    const filterClass = categoryMap[image.category] || 'rooms';
    const imageUrl = image.image_url || image.image;
    
    const card = document.createElement('div');
    card.className = `gallery-card ${filterClass}`;
    card.innerHTML = `
      <img src="${imageUrl}" alt="${image.alt_text || image.title}">
      <div class="gallery-overlay">
        <span>${image.title}</span>
      </div>
    `;
    
    galleryMasonry.appendChild(card);
  });
}

function renderCarouselItems(images) {
  const carouselTrack = document.getElementById('carouselTrack');
  if (!carouselTrack) return;
  
  // Clear existing items
  carouselTrack.innerHTML = '';
  
  // Add new items from API
  images.forEach(image => {
    const filterClass = categoryMap[image.category] || 'rooms';
    const imageUrl = image.image_url || image.image;
    
    const item = document.createElement('div');
    item.className = `carousel-item ${filterClass}`;
    item.innerHTML = `
      <img src="${imageUrl}" alt="${image.alt_text || image.title}">
      <div class="carousel-label">${image.title}</div>
    `;
    
    carouselTrack.appendChild(item);
  });
}

function initializeGalleryFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const galleryCards = document.querySelectorAll('.gallery-card');
  const carouselItems = document.querySelectorAll('.carousel-item');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      const filter = btn.getAttribute('data-filter');
      
      // Filter desktop gallery
      galleryCards.forEach(card => {
        if (filter === 'all' || card.classList.contains(filter)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
      
      // Filter mobile carousel
      carouselItems.forEach(item => {
        if (filter === 'all' || item.classList.contains(filter)) {
          item.style.display = 'flex';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}

// Initialize gallery when page loads
document.addEventListener('DOMContentLoaded', loadGalleryImages);
