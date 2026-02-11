#!/usr/bin/env python
"""
End-to-end test of the booking workflow
"""
import os
import django
import json
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')
django.setup()

from django.test import Client
from rentals.models import Booking
from rentals.email_service import send_booking_confirmation_email

# Create test client
client = Client()

# Prepare booking data
check_in = datetime(2026, 2, 15).date()
check_out = datetime(2026, 2, 20).date()
num_nights = (check_out - check_in).days
nightly_rate = 200.00
subtotal = num_nights * nightly_rate

booking_data = {
    'first_name': 'Test',
    'last_name': 'Guest',
    'email': 'test@example.com',
    'phone': '555-0100',
    'check_in': str(check_in),
    'check_out': str(check_out),
    'num_guests': 2,
    'payment_method': 'cashapp',
    'total_price': str(subtotal),
    'special_requests': 'High floor preferred'
}

print("=" * 60)
print("END-TO-END BOOKING WORKFLOW TEST")
print("=" * 60)
print(f"\n1. Submitting booking via API...")
print(f"   Check-in: {check_in}")
print(f"   Check-out: {check_out}")
print(f"   Nights: {num_nights}")
print(f"   Total: ${subtotal:.2f}")
print(f"   Guest: {booking_data['first_name']} {booking_data['last_name']}")

# Submit booking via API
response = client.post(
    '/api/bookings/',
    data=json.dumps(booking_data),
    content_type='application/json'
)

print(f"\n2. API Response Status: {response.status_code}")
if response.status_code in [200, 201, 202]:
    try:
        response_data = json.loads(response.content)
        print(f"   ✓ Response: {json.dumps(response_data, indent=2)}")
        
        # Check if email was sent
        if 'email_sent' in response_data:
            print(f"\n3. Email Sent Status: {response_data.get('email_sent')}")
        if 'id' in response_data:
            booking_id = response_data['id']
            print(f"   Booking ID: {booking_id}")
            
            # Verify booking in database
            print(f"\n4. Verifying booking in database...")
            booking = Booking.objects.get(id=booking_id)
            print(f"   ✓ Booking found")
            print(f"     - Name: {booking.first_name} {booking.last_name}")
            print(f"     - Email: {booking.email}")
            print(f"     - Total: ${booking.total_price}")
            print(f"     - Payment Method: {booking.payment_method or 'Not set'}")
            print(f"     - Status: {booking.status}")
            
    except Exception as e:
        print(f"   Error parsing response: {e}")
        print(f"   Raw response: {response.content}")
else:
    print(f"   ✗ Error: {response.status_code}")
    print(f"   {response.content}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
