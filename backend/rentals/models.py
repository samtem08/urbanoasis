from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class PricingRule(models.Model):
    """
    Pricing rules for different seasons and durations
    """
    SEASON_CHOICES = [
        ('peak', 'Peak Season'),
        ('regular', 'Regular Season'),
        ('off', 'Off Season'),
    ]
    
    name = models.CharField(max_length=100, help_text="e.g., 'Summer Weekend' or 'Winter Weekday'")
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='regular')
    base_price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Base price per night in USD"
    )
    
    # Optional date range for seasonal pricing
    start_date = models.DateField(null=True, blank=True, help_text="Leave blank for year-round")
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank for year-round")
    
    # Pricing for different durations
    weekly_discount_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Discount for 7+ nights (percentage)"
    )
    monthly_discount_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Discount for 30+ nights (percentage)"
    )
    
    # Additional fees
    cleaning_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="One-time cleaning fee"
    )
    service_fee_percent = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Service fee percentage"
    )
    
    # Presentation fields for frontend pricing cards
    description = models.TextField(blank=True, help_text="Optional description shown on pricing cards")
    order = models.IntegerField(default=0, help_text="Controls ordering of pricing cards")
    is_featured = models.BooleanField(default=False, help_text="Highlight this pricing rule on the site")
    image = models.ImageField(upload_to='pricing/', null=True, blank=True, help_text="Optional image for the pricing card")
    
    # Display customization
    display_label = models.CharField(max_length=50, default='Per Night', help_text="e.g., 'Nightly Rate', 'Weekly Rate', 'Monthly Rate'")
    display_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price to display on the card (e.g., 150 for per night, 1200 for weekly)")
    display_price_unit = models.CharField(max_length=50, default='/night', help_text="e.g., '/night', '/7 nights', '/month'")
    features = models.TextField(blank=True, help_text="Features for this plan (one per line)")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pricing Rule'
        verbose_name_plural = 'Pricing Rules'
    
    def __str__(self):
        return f"{self.name} - ${self.base_price_per_night}/night"
    
    def calculate_total(self, num_nights, num_guests=1):
        """Calculate total price for a stay"""
        base_total = float(self.base_price_per_night) * num_nights
        
        # Apply discounts
        if num_nights >= 30:
            discount = base_total * (float(self.monthly_discount_percent) / 100)
            base_total -= discount
        elif num_nights >= 7:
            discount = base_total * (float(self.weekly_discount_percent) / 100)
            base_total -= discount
        
        # Add fees
        service_fee = base_total * (float(self.service_fee_percent) / 100)
        total = base_total + float(self.cleaning_fee) + service_fee
        
        return round(total, 2)


class GalleryImage(models.Model):
    """
    Gallery images for the property
    """
    CATEGORY_CHOICES = [
        ('living', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('dining', 'Dining Area'),
        ('exterior', 'Exterior'),
        ('amenities', 'Amenities'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/%Y/%m/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, help_text="Alt text for accessibility")
    
    # Display order
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    is_featured = models.BooleanField(default=False, help_text="Show on home page")
    is_active = models.BooleanField(default=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return f"{self.title} ({self.category})"


class Amenity(models.Model):
    """
    Amenities and features of the property
    """
    AMENITY_TYPE_CHOICES = [
        ('popular', 'Most Popular'),
        ('apartment', 'Apartment Features'),
        ('service', 'Services & Safety'),
        ('facility', 'Facilities'),
        ('inroom', 'In-room Amenities'),
    ]
    
    name = models.CharField(max_length=100)
    amenity_type = models.CharField(max_length=20, choices=AMENITY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon name (e.g., 'fa-wifi')")
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
    
    def __str__(self):
        return f"{self.name} ({self.get_amenity_type_display()})"


class Booking(models.Model):
    """
    Guest bookings
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('zelle', 'Zelle'),
        ('cashapp', 'Cash App'),
        ('debitcard', 'Debit Card'),
    ]
    
    # Guest information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Booking details
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Pricing
    pricing_rule = models.ForeignKey(PricingRule, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status & Payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    special_requests = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.check_in} to {self.check_out}"
    
    @property
    def num_nights(self):
        """Calculate number of nights"""
        # Guard against empty dates when viewing/adding in admin
        if not self.check_in or not self.check_out:
            return None

        # If dates are provided but check_out is before check_in, return 0
        try:
            delta = (self.check_out - self.check_in).days
        except Exception:
            return None

        return delta if delta >= 0 else 0
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    """
    Guest reviews
    """
    guest_name = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField()
    
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_approved = models.BooleanField(default=False, help_text="Show on website")
    is_featured = models.BooleanField(default=False, help_text="Feature on home page")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f"{self.guest_name} - {self.rating} stars"


class SiteSettings(models.Model):
    """
    General site settings that can be edited from admin
    """
    site_name = models.CharField(max_length=100, default="Urban Oasis")
    tagline = models.CharField(max_length=200, default="Your home away from home")
    
    # Contact information
    address = models.CharField(max_length=200, default="5110 Daybreak Dr, Killeen, TX 76542")
    phone = models.CharField(max_length=20, default="+1 (407) 900-6046")
    email = models.EmailField(default="hello@urbanoasis.com")
    
    # Check-in/out times
    check_in_time = models.TimeField(default="15:00")
    check_out_time = models.TimeField(default="11:00")
    
    # Social media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Property details
    max_guests = models.IntegerField(default=6)
    num_bedrooms = models.IntegerField(default=3)
    num_bathrooms = models.IntegerField(default=2)
    square_feet = models.IntegerField(default=1172)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
