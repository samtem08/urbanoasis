# Urban Oasis API Documentation

Base URL: `http://127.0.0.1:8000/api/`

## Authentication

Currently, all endpoints are publicly accessible (AllowAny). For production, you should implement authentication.

## Endpoints

### Pricing Rules

#### List All Pricing Rules
```http
GET /api/pricing/
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Regular Season",
      "season": "regular",
      "base_price_per_night": "125.00",
      "weekly_discount_percent": "10.00",
      "monthly_discount_percent": "20.00",
      "cleaning_fee": "75.00",
      "service_fee_percent": "5.00",
      "start_date": null,
      "end_date": null,
      "is_active": true
    }
  ]
}
```

#### Get Single Pricing Rule
```http
GET /api/pricing/{id}/
```

#### Calculate Total Price
```http
POST /api/pricing/calculate/
Content-Type: application/json

{
  "pricing_rule_id": 1,
  "num_nights": 7,
  "num_guests": 2
}
```

**Response:**
```json
{
  "pricing_rule": {
    "id": 1,
    "name": "Regular Season",
    "base_price_per_night": "125.00",
    ...
  },
  "num_nights": 7,
  "num_guests": 2,
  "base_total": 875.00,
  "cleaning_fee": 75.00,
  "service_fee": 5.00,
  "total_price": 831.25
}
```

---

### Gallery Images

#### List All Images
```http
GET /api/gallery/
```

**Query Parameters:**
- `category` - Filter by category (living, bedroom, kitchen, bathroom, dining, exterior, amenities, other)
- `featured` - Show only featured images (true/false)

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Living Room",
      "image": "/media/gallery/2026/02/living.jpg",
      "image_url": "http://127.0.0.1:8000/media/gallery/2026/02/living.jpg",
      "category": "living",
      "description": "Spacious living area with modern furniture",
      "alt_text": "Modern living room with couch and TV",
      "order": 1,
      "is_featured": true
    }
  ]
}
```

#### Get Single Image
```http
GET /api/gallery/{id}/
```

---

### Amenities

#### List All Amenities
```http
GET /api/amenities/
```

**Query Parameters:**
- `type` - Filter by type (popular, apartment, service, facility, inroom)

**Response:**
```json
{
  "count": 6,
  "results": [
    {
      "id": 1,
      "name": "Free WiFi",
      "amenity_type": "popular",
      "description": "High-speed internet throughout the property",
      "icon_name": "fa-wifi",
      "order": 1
    }
  ]
}
```

#### Get Single Amenity
```http
GET /api/amenities/{id}/
```

---

### Bookings

#### List All Bookings
```http
GET /api/bookings/
```

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "check_in": "2026-03-15",
      "check_out": "2026-03-22",
      "num_nights": 7,
      "num_guests": 2,
      "total_price": "831.25",
      "status": "pending",
      "special_requests": "Early check-in if possible",
      "created_at": "2026-02-07T10:30:00Z"
    }
  ]
}
```

#### Create Booking
```http
POST /api/bookings/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "check_in": "2026-03-15",
  "check_out": "2026-03-22",
  "num_guests": 2,
  "pricing_rule_id": 1,
  "special_requests": "Early check-in if possible",
  "total_price": "831.25"
}
```

**Response:** 201 Created with booking details

#### Get Single Booking
```http
GET /api/bookings/{id}/
```

#### Check Availability
```http
GET /api/bookings/availability/?check_in=2026-03-15&check_out=2026-03-22
```

**Response:**
```json
{
  "available": true,
  "overlapping_bookings": 0
}
```

---

### Reviews

#### List All Approved Reviews
```http
GET /api/reviews/
```

**Query Parameters:**
- `featured` - Show only featured reviews (true/false)

**Response:**
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "guest_name": "Kellyann",
      "rating": 4,
      "comment": "The host was very communicative, friendly and very helpful...",
      "is_approved": true,
      "is_featured": true,
      "created_at": "2026-01-15T14:20:00Z"
    }
  ]
}
```

#### Create Review
```http
POST /api/reviews/
Content-Type: application/json

{
  "guest_name": "Jane Smith",
  "rating": 5,
  "comment": "Amazing place! Would definitely stay again.",
  "booking": 1
}
```

**Note:** Reviews created via API are not approved by default. Admin must approve them.

#### Get Single Review
```http
GET /api/reviews/{id}/
```

---

### Site Settings

#### Get Site Settings
```http
GET /api/settings/
```

**Response:**
```json
{
  "site_name": "Urban Oasis",
  "tagline": "Your home away from home in Killeen",
  "address": "5110 Daybreak Dr, Killeen, TX 76542",
  "phone": "+1 (407) 900-6046",
  "email": "hello@urbanoasis.com",
  "check_in_time": "15:00:00",
  "check_out_time": "11:00:00",
  "facebook_url": "",
  "twitter_url": "",
  "instagram_url": "",
  "max_guests": 6,
  "num_bedrooms": 3,
  "num_bathrooms": 2,
  "square_feet": 1172
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data provided",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## CORS

CORS is enabled for all origins in development. For production, update `CORS_ALLOWED_ORIGINS` in settings.py:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

## Pagination

List endpoints are paginated with 20 items per page by default.

**Query Parameters:**
- `page` - Page number (default: 1)

**Response includes:**
- `count` - Total number of items
- `next` - URL to next page (null if last page)
- `previous` - URL to previous page (null if first page)
- `results` - Array of items for current page

Example:
```http
GET /api/gallery/?page=2
```

---

## Complete Frontend Integration Example

```javascript
// config.js
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// pricing.js
async function loadPricing() {
  try {
    const response = await fetch(`${API_BASE_URL}/pricing/`);
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Error loading pricing:', error);
    return [];
  }
}

async function calculatePrice(pricingRuleId, numNights, numGuests) {
  try {
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
    return await response.json();
  } catch (error) {
    console.error('Error calculating price:', error);
    return null;
  }
}

// gallery.js
async function loadGallery(category = null) {
  try {
    let url = `${API_BASE_URL}/gallery/`;
    if (category) {
      url += `?category=${category}`;
    }
    const response = await fetch(url);
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Error loading gallery:', error);
    return [];
  }
}

// booking.js
async function createBooking(formData) {
  try {
    const response = await fetch(`${API_BASE_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(JSON.stringify(error));
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error creating booking:', error);
    throw error;
  }
}

async function checkAvailability(checkIn, checkOut) {
  try {
    const url = `${API_BASE_URL}/bookings/availability/?check_in=${checkIn}&check_out=${checkOut}`;
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error('Error checking availability:', error);
    return { available: false };
  }
}

// reviews.js
async function loadReviews(featured = false) {
  try {
    let url = `${API_BASE_URL}/reviews/`;
    if (featured) {
      url += '?featured=true';
    }
    const response = await fetch(url);
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Error loading reviews:', error);
    return [];
  }
}

// settings.js
async function loadSiteSettings() {
  try {
    const response = await fetch(`${API_BASE_URL}/settings/`);
    return await response.json();
  } catch (error) {
    console.error('Error loading settings:', error);
    return null;
  }
}
```
