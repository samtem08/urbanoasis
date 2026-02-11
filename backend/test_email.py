#!/usr/bin/env python
"""Test email sending with latest booking"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')
django.setup()

from rentals.models import Booking
from rentals.email_service import send_booking_confirmation_email
import traceback

try:
    b = Booking.objects.latest('id')
    print(f"Testing with booking: ID={b.id}, Email={b.email}")
    print(f"Check-in: {b.check_in}, Check-out: {b.check_out}")
    print(f"Name: {b.first_name} {b.last_name}")
    print(f"Total Price: ${b.total_price}")
    print()
    
    # Try sending
    print("Attempting to send confirmation email...")
    result = send_booking_confirmation_email(b)
    print(f"✓ Email send result: {result}")
    
except Booking.DoesNotExist:
    print("✗ No bookings found in database")
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
