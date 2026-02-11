# Invoice & Email Configuration Guide

## Overview
The Urban Oasis application now includes automatic invoice generation and email receipt confirmation for all bookings. This guide explains how to set up and configure the email system.

## Features

1. **Automatic Invoice Generation**
   - PDF invoices generated automatically for every booking
   - Professional formatting with business details
   - Includes booking details, pricing breakdown, and payment information

2. **Email Receipt Confirmation**
   - Sends confirmation emails immediately after booking
   - Includes PDF invoice as attachment
   - Both HTML and plain text versions for compatibility

3. **Payment Receipt Emails**
   - Additional receipt email sent for debit card payments
   - Contains payment confirmation details
   - Links booking reference with payment ID

## Setup Instructions

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

Required packages:
- `reportlab==4.0.9` - PDF generation
- `Jinja2==3.1.2` - Template rendering

### 2. Configure Email Backend

#### Option A: Gmail SMTP (Recommended for Testing)
1. Create a Gmail account or use an existing one
2. Enable 2-Factor Authentication
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Create a `.env` file in the `urban_oasis_backend` directory:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-16chars
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Business Information
BUSINESS_EMAIL=info@urbanoasis.com
BUSINESS_PHONE=+1 (555) 123-4567
BUSINESS_ADDRESS=123 Main Street, Austin, TX 78701

# Stripe Keys (if not already set)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Option B: Console Backend (Development Only)
For testing without sending actual emails:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This will print emails to the console instead of sending them.

#### Option C: SendGrid / Other SMTP Services
Replace EMAIL_HOST and EMAIL_PORT with your service's SMTP details.

### 3. Create .env File
Create `.env` file in `urban_oasis_backend/`:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=False  # Set to False in production

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@urbanoasis.com

# Business Information
BUSINESS_NAME=Urban Oasis Apartment Rental
BUSINESS_EMAIL=info@urbanoasis.com
BUSINESS_PHONE=+1 (555) 123-4567
BUSINESS_ADDRESS=123 Main Street, Austin, TX 78701

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Verify Configuration
Test the email setup:

```python
python manage.py shell
from django.core.mail import send_mail

# Send test email
send_mail(
    'Test Email',
    'This is a test email from Urban Oasis.',
    'noreply@urbanoasis.com',
    ['test@example.com'],
    fail_silently=False,
)
```

## How It Works

### Booking Submission Flow

1. **User submits booking form** (checkout.html or booking.html)
2. **Stripe processes payment** (if debit card selected)
3. **Booking record created** in database with status='confirmed'
4. **Email service triggered automatically**:
   - Generates PDF invoice
   - Sends booking confirmation email with PDF attachment
   - If debit card payment: sends payment receipt email

### Email Templates

#### 1. Booking Confirmation Email
- **Recipient:** Guest's email address
- **Content:** Welcome message, booking details, check-in/check-out info
- **Attachment:** Invoice PDF
- **Trigger:** On booking creation

#### 2. Payment Receipt Email
- **Recipient:** Guest's email address
- **Content:** Payment confirmation, receipt details, booking reference
- **Trigger:** On booking creation with debit card payment method

### Invoice PDF Contents

The generated invoice includes:
- Invoice number (same as booking ID)
- Invoice date
- Guest information (name, email, phone)
- Business information
- Booking details (check-in, check-out, guests)
- Price breakdown:
  - Nightly rate per night
  - Subtotal
  - Tax (if applicable)
  - Discounts (if applicable)
  - **Total amount due**
- Payment method information
- Special requests (if any)
- Footer with business contact info

## Troubleshooting

### Email Not Sending

1. **Check Django logs:**
   ```bash
   python manage.py runserver
   ```
   Look for email errors in console output

2. **Verify SMTP credentials:**
   - Ensure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct
   - For Gmail: use app-specific password, not your regular password

3. **Firewall/Network issues:**
   - Check if port 587 is open
   - SMTP may be blocked on your network

4. **Console Backend troubleshooting:**
   If using console backend for testing:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```
   Emails will print to console instead of sending

### PDF Generation Issues

1. **ReportLab import error:**
   ```bash
   pip install reportlab==4.0.9
   ```

2. **Missing invoice details:**
   Ensure booking has all required fields (name, email, phone, dates, price)

3. **Special character issues:**
   ReportLab handles UTF-8 correctly; if you see garbled text, check your database encoding

## Email Configuration by Provider

### Gmail
- **Host:** smtp.gmail.com
- **Port:** 587
- **TLS:** True
- **Auth:** 2FA + App Password required

### Microsoft Outlook/Office 365
- **Host:** smtp-mail.outlook.com
- **Port:** 587
- **TLS:** True
- **Auth:** Your Outlook email and password

### SendGrid
- **Host:** smtp.sendgrid.net
- **Port:** 587
- **TLS:** True
- **Auth:** apikey (username) + SENDGRID_API_KEY (password)

### Amazon SES
- **Host:** email-smtp.region.amazonaws.com
- **Port:** 587
- **TLS:** True
- **Auth:** SMTP credentials from AWS console

## Security Best Practices

1. **Never commit .env file**
   - Add `.env` to `.gitignore`
   - Use environment variables in production

2. **Use app-specific passwords**
   - Don't use your main email password
   - Gmail, Outlook, etc. offer app-specific passwords

3. **Secure SMTP connection**
   - Always use TLS (EMAIL_USE_TLS=True)
   - Never use unencrypted SMTP on port 25

4. **Rate limiting**
   - Consider implementing rate limiting for email sends
   - Prevent spam/abuse

## Production Deployment

For production:

1. Use a professional email service (SendGrid, AWS SES, etc.)
2. Set DEBUG=False in settings
3. Update ALLOWED_HOSTS with your domain
4. Use environment variables for all sensitive data
5. Test email delivery before going live
6. Set up error logging and monitoring
7. Consider email templates in database for easy updates

## API Integration

The email system integrates automatically with:

1. **Booking API Endpoint** (`POST /api/bookings/`)
   - Automatically sends emails when booking is created
   - No additional API call needed

2. **Stripe Payment Processing**
   - Payment receipt email sent for debit card bookings
   - References payment ID and timestamp

## Testing

### Test with Console Backend
```bash
# In settings.py or .env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Manual Email Test
```python
from rentals.email_service import send_booking_confirmation_email
from rentals.models import Booking

booking = Booking.objects.last()
send_booking_confirmation_email(booking)
```

### Test Invoice Generation
```python
from rentals.invoice_generator import generate_invoice_pdf
from rentals.models import Booking

booking = Booking.objects.last()
pdf = generate_invoice_pdf(booking)

# Save to file for inspection
with open('test_invoice.pdf', 'wb') as f:
    f.write(pdf.getvalue())
```

## API Response Example

When a booking is created, the response includes the booking data:

```json
{
  "id": 123,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1 (555) 123-4567",
  "check_in": "2024-02-15",
  "check_out": "2024-02-20",
  "num_guests": 2,
  "total_price": "1200.00",
  "status": "confirmed",
  "payment_method": "debitcard",
  "special_requests": "Early check-in if possible",
  "created_at": "2024-02-08T10:30:00Z"
}
```

The email is automatically sent in the background immediately after this response is generated.

## Support & Issues

For issues with:

1. **Email sending:** Check EMAIL_HOST_USER credentials and SMTP settings
2. **PDF generation:** Verify ReportLab is installed and working
3. **Attachments:** Check disk space and file permissions
4. **HTML formatting:** Test in different email clients (Gmail, Outlook, Apple Mail)

---

Last Updated: February 8, 2024
Version: 1.0
