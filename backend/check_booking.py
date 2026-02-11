#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')
django.setup()

from rentals.models import Booking

# Get latest booking
latest = Booking.objects.latest('id')
print(f'Latest Booking: ID={latest.id}, {latest.first_name} {latest.last_name}')
print(f'Email: {latest.email}')
print(f'Total: ${latest.total_price}')
print(f'Check-in: {latest.check_in}')
print(f'Check-out: {latest.check_out}')
print(f'Payment Method: {latest.payment_method}')
