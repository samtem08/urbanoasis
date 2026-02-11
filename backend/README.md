# Urban Oasis Backend - Django API

This is the Django backend for the Urban Oasis apartment rental website. It provides a REST API and admin panel for managing pricing, images, amenities, bookings, and reviews.

## Features

### Admin Panel Features
- **Pricing Management**: Set different pricing rules for peak/off seasons with weekly/monthly discounts
- **Image Gallery Management**: Upload and organize property images with categories
- **Amenities Management**: Add and organize property amenities and features
- **Booking Management**: View and manage guest bookings
- **Reviews Management**: Approve and feature guest reviews
- **Site Settings**: Update contact information, check-in times, and property details

### Booking & Payment Features
- **Stripe Payment Integration**: Secure debit card payments with Stripe tokenization
- **Automatic Invoice Generation**: Professional PDF invoices generated for each booking
- **Email Confirmations**: Automatic booking confirmation emails with invoice attachments
- **Payment Receipts**: Separate receipt emails for debit card payments

### API Endpoints
- `/api/pricing/` - Get pricing rules and calculate totals
- `/api/gallery/` - Get gallery images (filterable by category)
- `/api/amenities/` - Get property amenities
- `/api/bookings/` - Create and manage bookings, check availability
- `/api/reviews/` - Get approved reviews
- `/api/settings/` - Get site settings
- `/api/stripe-config/` - Get Stripe publishable key
- `/api/create-payment-intent/` - Create Stripe PaymentIntent
- `/api/stripe-webhook/` - Webhook for Stripe payment events

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Set Up Virtual Environment

```bash
# Navigate to the backend directory
cd urban_oasis_backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 4: Create Admin User

```bash
# Create a superuser account
python manage.py createsuperuser

# Follow the prompts to set:
# - Username
# - Email
# - Password
```

### Step 5: Load Sample Data (Optional)

```bash
# Load initial data
python manage.py loaddata initial_data.json
```

### Step 6: Run Development Server

```bash
# Start the server
python manage.py runserver

# The server will be available at:
# - API: http://127.0.0.1:8000/api/
# - Admin: http://127.0.0.1:8000/admin/
```

## Configuration

### Environment Variables

Create a `.env` file in the `urban_oasis_backend` directory with the following variables:

```env
# Email Configuration (for invoices and confirmations)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@urbanoasis.com

# Business Information (for invoices)
BUSINESS_NAME=Urban Oasis Apartment Rental
BUSINESS_EMAIL=info@urbanoasis.com
BUSINESS_PHONE=+1 (555) 123-4567
BUSINESS_ADDRESS=123 Main Street, Austin, TX 78701

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed email configuration instructions.

### Email Setup

Urban Oasis includes automatic invoice generation and email confirmation features:

1. **Booking Confirmation Email**: Sent automatically when a booking is created, includes PDF invoice
2. **Payment Receipt Email**: Sent for debit card payments with payment confirmation details

For setup instructions, see [EMAIL_SETUP.md](EMAIL_SETUP.md).

To test without sending emails, set in `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Admin Panel Usage

### Accessing the Admin Panel

1. Start the server: `python manage.py runserver`
2. Navigate to: http://127.0.0.1:8000/admin/
3. Log in with your superuser credentials

### Managing Pricing


1. Go to **Pricing Rules** in the admin panel
2. Click **Add Pricing Rule**
3. Set:
   - Name (e.g., "Summer Peak Season")
   - Season (Peak/Regular/Off)
   - Base price per night
   - Weekly/monthly discount percentages
   - Cleaning fee and service fee
   - Optional date range for seasonal pricing
4. Click **Save**

**Pricing Calculation:**
- Base Total = Base Price × Number of Nights
- Discounts applied automatically:
  - 7+ nights: Weekly discount
  - 30+ nights: Monthly discount
- Final Total = Base Total + Cleaning Fee + Service Fee

### Managing Gallery Images

1. Go to **Gallery Images**
2. Click **Add Gallery Image**
3. Upload image and set:
   - Title and category
   - Description and alt text (for accessibility)
   - Display order (lower numbers appear first)
   - Mark as featured to show on homepage
4. Click **Save**

**Image Categories:**
- Living Room
- Bedroom
- Kitchen
- Bathroom
- Dining Area
- Exterior
- Amenities
- Other

### Managing Amenities

1. Go to **Amenities**
2. Click **Add Amenity**
3. Set:
   - Name (e.g., "Free WiFi")
   - Type (Popular/Apartment/Service/Facility/In-room)
   - Description
   - Icon name (Font Awesome class)
   - Display order
4. Click **Save**

### Managing Bookings

1. Go to **Bookings** to view all reservations
2. Filter by status, date, or search by guest name
3. Click a booking to view/edit details
4. Change status: Pending → Confirmed → Completed
5. View calculated nights and total price

**Bulk Actions:**
- Select multiple bookings
- Use dropdown to mark as Confirmed/Cancelled/Completed

### Managing Reviews

1. Go to **Reviews**
2. View submitted reviews (pending approval)
3. Click a review to:
   - Approve for public display
   - Mark as featured for homepage
4. Reviews show star rating and comment preview

## API Usage

### Base URL
```
http://127.0.0.1:8000/api/
```

### Example API Calls

#### Get All Pricing Rules
```bash
GET /api/pricing/
```

#### Calculate Price for Stay
```bash
POST /api/pricing/calculate/
Content-Type: application/json

{
  "pricing_rule_id": 1,
  "num_nights": 7,
  "num_guests": 2
}
```

#### Get Gallery Images
```bash
# All images
GET /api/gallery/

# Featured images only
GET /api/gallery/?featured=true

# By category
GET /api/gallery/?category=bedroom
```

#### Create Booking
```bash
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
  "special_requests": "Early check-in if possible"
}
```

#### Check Availability
```bash
GET /api/bookings/availability/?check_in=2026-03-15&check_out=2026-03-22
```

#### Get Approved Reviews
```bash
# All approved reviews
GET /api/reviews/

# Featured reviews only
GET /api/reviews/?featured=true
```

#### Get Site Settings
```bash
GET /api/settings/
```

## Frontend Integration

### Update Your Frontend

To connect your existing frontend to this backend:

1. **Update API Base URL:**
   ```javascript
   const API_BASE_URL = 'http://127.0.0.1:8000/api';
   ```

2. **Fetch Pricing:**
   ```javascript
   async function getPricing() {
     const response = await fetch(`${API_BASE_URL}/pricing/`);
     const data = await response.json();
     return data;
   }
   ```

3. **Load Gallery Images:**
   ```javascript
   async function getGalleryImages() {
     const response = await fetch(`${API_BASE_URL}/gallery/`);
     const images = await response.json();
     return images;
   }
   ```

4. **Submit Booking:**
   ```javascript
   async function createBooking(bookingData) {
     const response = await fetch(`${API_BASE_URL}/bookings/`, {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify(bookingData)
     });
     return await response.json();
   }
   ```

## Directory Structure

```
urban_oasis_backend/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (created after migration)
├── urban_oasis/          # Main project settings
│   ├── __init__.py
│   ├── settings.py       # Project settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── rentals/              # Main app
│   ├── __init__.py
│   ├── models.py        # Database models
│   ├── admin.py         # Admin panel configuration
│   ├── views.py         # API views
│   ├── serializers.py   # API serializers
│   ├── urls.py          # App URL routing
│   ├── apps.py          # App configuration
│   └── migrations/      # Database migrations
└── media/               # Uploaded images (created automatically)
    └── gallery/
```

## Production Deployment

### Security Checklist

1. **Change SECRET_KEY:**
   ```python
   # In settings.py
   SECRET_KEY = 'your-production-secret-key'
   ```

2. **Disable DEBUG:**
   ```python
   DEBUG = False
   ```

3. **Set ALLOWED_HOSTS:**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Configure CORS properly:**
   ```python
   CORS_ALLOW_ALL_ORIGINS = False
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
   ]
   ```

5. **Use PostgreSQL instead of SQLite:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. **Set up static files:**
   ```bash
   python manage.py collectstatic
   ```

### Recommended Hosting Options
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Elastic Beanstalk or EC2
- **PythonAnywhere**: Simple Python hosting

## Common Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell
```

## Troubleshooting

### Images not showing up
- Check that `MEDIA_URL` and `MEDIA_ROOT` are configured in settings.py
- Ensure the development server is serving media files
- Check file permissions on the media directory

### CORS errors from frontend
- Verify CORS settings in settings.py
- Ensure `corsheaders` is in INSTALLED_APPS and MIDDLEWARE
- Check that your frontend URL is in CORS_ALLOWED_ORIGINS (or CORS_ALLOW_ALL_ORIGINS is True)

### Database errors
- Run `python manage.py migrate` to ensure database is up to date
- Check that migrations folder exists and contains migration files
- Delete db.sqlite3 and run migrations again if needed

### Admin panel CSS not loading
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings

## Support

For questions or issues:
- Email: hello@urbanoasis.com
- Phone: +1 (407) 900-6046

## License

© 2026 Urban Oasis. All rights reserved.
