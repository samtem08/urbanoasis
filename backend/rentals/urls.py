from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PricingRuleViewSet, GalleryImageViewSet, AmenityViewSet,
    BookingViewSet, ReviewViewSet, SiteSettingsViewSet
)
from .views import StripeConfigView, CreatePaymentIntentView, stripe_webhook

router = DefaultRouter()
router.register(r'pricing', PricingRuleViewSet, basename='pricing')
router.register(r'gallery', GalleryImageViewSet, basename='gallery')
router.register(r'amenities', AmenityViewSet, basename='amenities')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'settings', SiteSettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
    path('stripe-config/', StripeConfigView.as_view(), name='stripe-config'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]
