from rest_framework import serializers
from .models import (
    PricingRule, GalleryImage, Amenity, 
    Booking, Review, SiteSettings
)


class PricingRuleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    features_list = serializers.SerializerMethodField()
    
    class Meta:
        model = PricingRule
        fields = [
            'id', 'name', 'season', 'base_price_per_night',
            'weekly_discount_percent', 'monthly_discount_percent',
            'cleaning_fee', 'service_fee_percent',
            'start_date', 'end_date', 'is_active',
            'description', 'order', 'is_featured', 'image', 'image_url',
            'display_label', 'display_price', 'display_price_unit', 'features', 'features_list'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_features_list(self, obj):
        """Convert features text to list"""
        if obj.features:
            return [f.strip() for f in obj.features.split('\n') if f.strip()]
        return []


class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'image', 'image_url', 'category',
            'description', 'alt_text', 'order', 'is_featured'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            'id', 'name', 'amenity_type', 'description',
            'icon_name', 'order'
        ]


class BookingSerializer(serializers.ModelSerializer):
    num_nights = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'check_in', 'check_out',
            'num_nights', 'num_guests', 'total_price',
            'status', 'payment_method', 'special_requests', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']
    
    def validate(self, data):
        # Ensure check-out is after check-in
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date"
            )
        
        # Ensure at least one night
        nights = (data['check_out'] - data['check_in']).days
        if nights < 1:
            raise serializers.ValidationError(
                "Booking must be for at least one night"
            )
        
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'guest_name', 'rating', 'comment',
            'is_approved', 'is_featured', 'created_at'
        ]
        read_only_fields = ['is_approved', 'is_featured', 'created_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'tagline', 'address', 'phone', 'email',
            'check_in_time', 'check_out_time',
            'facebook_url', 'twitter_url', 'instagram_url',
            'max_guests', 'num_bedrooms', 'num_bathrooms', 'square_feet'
        ]
