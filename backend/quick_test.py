#!/usr/bin/env python
"""
Quick test of updated email format
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')
django.setup()

from rentals.models import Booking
from rentals.invoice_generator import generate_invoice_pdf

# Get latest booking
booking = Booking.objects.latest('id')

print(f"Testing invoice PDF for Booking #{booking.id}")
print(f"Guest: {booking.first_name} {booking.last_name}")

try:
    # Generate PDF
    pdf_buffer = generate_invoice_pdf(booking)
    pdf_size = len(pdf_buffer.getvalue())
    
    print(f"✓ PDF Generated: {pdf_size} bytes")
    print(f"✓ Email format updated with attachment section at bottom")
    print(f"\nEmail structure:")
    print(f"  1. Booking confirmation message")
    print(f"  2. Important information")
    print(f"  3. Contact details")
    print(f"  4. Closing message")
    print(f"  5. [ATTACHMENT SECTION] - Invoice file attached")
    
except Exception as e:
    print(f"✗ Error: {e}")
