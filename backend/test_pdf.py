#!/usr/bin/env python
"""
Test PDF generation directly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')
django.setup()

from rentals.models import Booking
from rentals.invoice_generator import generate_invoice_pdf

# Get latest booking
booking = Booking.objects.latest('id')

print(f"Testing PDF generation for Booking #{booking.id}")
print(f"Guest: {booking.first_name} {booking.last_name}")
print(f"Email: {booking.email}")
print(f"Total: ${booking.total_price}")

try:
    # Generate PDF
    pdf_buffer = generate_invoice_pdf(booking)
    pdf_size = len(pdf_buffer.getvalue())
    
    print(f"\n✓ PDF Generated Successfully!")
    print(f"  Size: {pdf_size} bytes")
    print(f"  Type: {type(pdf_buffer)}")
    
    # Save to file for manual inspection
    with open(f'invoice_{booking.id}.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    print(f"  Saved to: invoice_{booking.id}.pdf")
    
except Exception as e:
    print(f"\n✗ PDF Generation Failed!")
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()
