from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import PricingRule, GalleryImage, Amenity, Booking, Review, SiteSettings


class PricingRuleTestCase(TestCase):
    def setUp(self):
        self.pricing = PricingRule.objects.create(
            name="Test Pricing",
            season="regular",
            base_price_per_night=Decimal("100.00"),
            weekly_discount_percent=Decimal("10.00"),
            monthly_discount_percent=Decimal("20.00"),
            cleaning_fee=Decimal("50.00"),
            service_fee_percent=Decimal("5.00"),
            is_active=True
        )
    
    def test_pricing_creation(self):
        """Test that pricing rule is created correctly"""
        self.assertEqual(self.pricing.name, "Test Pricing")
        self.assertEqual(self.pricing.base_price_per_night, Decimal("100.00"))
    
    def test_price_calculation_basic(self):
        """Test basic price calculation for 3 nights"""
        total = self.pricing.calculate_total(3, 2)
        # Base: 3 * 100 = 300
        # Service fee: 300 * 0.05 = 15
        # Cleaning: 50
        # Total: 300 + 15 + 50 = 365
        self.assertEqual(total, 365.00)
    
    def test_price_calculation_weekly_discount(self):
        """Test price calculation with weekly discount"""
        total = self.pricing.calculate_total(7, 2)
        # Base: 7 * 100 = 700
        # Discount: 700 * 0.10 = 70
        # After discount: 630
        # Service fee: 630 * 0.05 = 31.5
        # Cleaning: 50
        # Total: 630 + 31.5 + 50 = 711.5
        self.assertEqual(total, 711.50)
    
    def test_price_calculation_monthly_discount(self):
        """Test price calculation with monthly discount"""
        total = self.pricing.calculate_total(30, 2)
        # Base: 30 * 100 = 3000
        # Discount: 3000 * 0.20 = 600
        # After discount: 2400
        # Service fee: 2400 * 0.05 = 120
        # Cleaning: 50
        # Total: 2400 + 120 + 50 = 2570
        self.assertEqual(total, 2570.00)


class BookingTestCase(TestCase):
    def setUp(self):
        from datetime import date
        self.booking = Booking.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1234567890",
            check_in=date(2026, 3, 15),
            check_out=date(2026, 3, 22),
            num_guests=2,
            total_price=Decimal("800.00"),
            status="pending"
        )
    
    def test_booking_creation(self):
        """Test that booking is created correctly"""
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(self.booking.email, "john@example.com")
    
    def test_num_nights_calculation(self):
        """Test that number of nights is calculated correctly"""
        self.assertEqual(self.booking.num_nights, 7)
    
    def test_full_name_property(self):
        """Test full name property"""
        self.assertEqual(self.booking.full_name, "John Doe")


class ReviewTestCase(TestCase):
    def setUp(self):
        self.review = Review.objects.create(
            guest_name="Jane Smith",
            rating=5,
            comment="Great place!",
            is_approved=True,
            is_featured=False
        )
    
    def test_review_creation(self):
        """Test that review is created correctly"""
        self.assertEqual(self.review.guest_name, "Jane Smith")
        self.assertEqual(self.review.rating, 5)
        self.assertTrue(self.review.is_approved)


class SiteSettingsTestCase(TestCase):
    def test_singleton_pattern(self):
        """Test that only one SiteSettings instance can exist"""
        settings1 = SiteSettings.load()
        settings2 = SiteSettings.load()
        
        self.assertEqual(settings1.pk, settings2.pk)
        self.assertEqual(SiteSettings.objects.count(), 1)
