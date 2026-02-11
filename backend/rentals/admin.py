from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PricingRule, GalleryImage, Amenity, 
    Booking, Review, SiteSettings
)


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'season', 'base_price_per_night', 
        'weekly_discount', 'monthly_discount', 
        'is_featured', 'order', 'is_active', 'date_range'
    ]
    list_filter = ['season', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'season', 'is_active')
        }),
        ('Pricing', {
            'fields': (
                'base_price_per_night',
                'weekly_discount_percent',
                'monthly_discount_percent',
            )
        }),
        ('Presentation', {
            'fields': ('description', 'image', 'image_preview', 'order', 'is_featured'),
            'description': 'Optional fields to control how pricing cards appear on the frontend'
        }),
        ('Display Customization', {
            'fields': ('display_label', 'display_price', 'display_price_unit', 'features'),
            'description': 'Customize how this pricing plan displays on the frontend card'
        }),
        ('Additional Fees', {
            'fields': ('cleaning_fee', 'service_fee_percent')
        }),
        ('Date Range (Optional)', {
            'fields': ('start_date', 'end_date'),
            'description': 'Leave blank for year-round pricing'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def weekly_discount(self, obj):
        return f"{obj.weekly_discount_percent}%"
    weekly_discount.short_description = 'Weekly Discount'
    
    def monthly_discount(self, obj):
        return f"{obj.monthly_discount_percent}%"
    monthly_discount.short_description = 'Monthly Discount'
    
    def date_range(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date} to {obj.end_date}"
        return "Year-round"
    date_range.short_description = 'Active Period'

    def image_preview(self, obj):
        if getattr(obj, 'image', None):
            return format_html(
                '<img src="{}" style="max-height:100px; max-width:150px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Image Preview'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 'title', 'category', 
        'order', 'is_featured', 'is_active', 'uploaded_at'
    ]
    list_filter = ['category', 'is_featured', 'is_active', 'uploaded_at']
    search_fields = ['title', 'description', 'alt_text']
    readonly_fields = ['image_preview', 'uploaded_at', 'updated_at']
    list_editable = ['order', 'is_featured', 'is_active']
    
    fieldsets = (
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Details', {
            'fields': ('title', 'category', 'description', 'alt_text')
        }),
        ('Display Options', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'amenity_type', 'order', 'is_active']
    list_filter = ['amenity_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'amenity_type', 'description')
        }),
        ('Display', {
            'fields': ('icon_name', 'order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'full_name', 'email', 'check_in', 
        'check_out', 'num_nights_display', 'num_guests', 
        'total_price', 'status', 'created_at'
    ]
    list_filter = ['status', 'check_in', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['num_nights_display', 'created_at', 'updated_at']
    date_hierarchy = 'check_in'
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': (
                'check_in', 'check_out', 'num_nights_display',
                'num_guests', 'special_requests'
            )
        }),
        ('Pricing', {
            'fields': ('pricing_rule', 'total_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def num_nights_display(self, obj):
        return obj.num_nights
    num_nights_display.short_description = 'Nights'
    
    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed']
    
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = 'Mark selected as Confirmed'
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = 'Mark selected as Cancelled'
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Mark selected as Completed'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'guest_name', 'rating_display', 'comment_preview', 
        'is_approved', 'is_featured', 'created_at'
    ]
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['guest_name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved', 'is_featured']
    
    fieldsets = (
        ('Review Details', {
            'fields': ('guest_name', 'rating', 'comment', 'booking')
        }),
        ('Display Options', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_display.short_description = 'Rating'
    
    def comment_preview(self, obj):
        return obj.comment[:75] + '...' if len(obj.comment) > 75 else obj.comment
    comment_preview.short_description = 'Comment'
    
    actions = ['approve_reviews', 'unapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'
    
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_reviews.short_description = 'Unapprove selected reviews'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'tagline')
        }),
        ('Contact Details', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Check-in/out Times', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url')
        }),
        ('Property Details', {
            'fields': ('max_guests', 'num_bedrooms', 'num_bathrooms', 'square_feet')
        }),
    )


# Customize admin site header
admin.site.site_header = "Urban Oasis Administration"
admin.site.site_title = "Urban Oasis Admin"
admin.site.index_title = "Welcome to Urban Oasis Admin Panel"
