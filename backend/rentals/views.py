from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import (
    PricingRule, GalleryImage, Amenity, 
    Booking, Review, SiteSettings
)
from .serializers import (
    PricingRuleSerializer, GalleryImageSerializer, AmenitySerializer,
    BookingSerializer, ReviewSerializer, SiteSettingsSerializer
)
from .email_service import send_booking_confirmation_email, send_payment_receipt_email
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
import stripe
import json
from datetime import datetime
import logging


class PricingRuleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for pricing rules
    """
    queryset = PricingRule.objects.filter(is_active=True)
    serializer_class = PricingRuleSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Calculate total price for a stay
        Expected payload: {
            "pricing_rule_id": 1,
            "num_nights": 7,
            "num_guests": 2
        }
        """
        pricing_rule_id = request.data.get('pricing_rule_id')
        num_nights = request.data.get('num_nights')
        num_guests = request.data.get('num_guests', 1)
        
        try:
            pricing_rule = PricingRule.objects.get(id=pricing_rule_id, is_active=True)
            total = pricing_rule.calculate_total(num_nights, num_guests)
            
            return Response({
                'pricing_rule': PricingRuleSerializer(pricing_rule).data,
                'num_nights': num_nights,
                'num_guests': num_guests,
                'base_total': float(pricing_rule.base_price_per_night) * num_nights,
                'cleaning_fee': float(pricing_rule.cleaning_fee),
                'service_fee': float(pricing_rule.service_fee_percent),
                'total_price': total
            })
        except PricingRule.DoesNotExist:
            return Response(
                {'error': 'Pricing rule not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for gallery images
    """
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        featured = self.request.query_params.get('featured', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for amenities
    """
    queryset = Amenity.objects.filter(is_active=True)
    serializer_class = AmenitySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        amenity_type = self.request.query_params.get('type', None)
        
        if amenity_type:
            queryset = queryset.filter(amenity_type=amenity_type)
        
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to exempt from CSRF for booking API"""
        # Apply csrf_exempt to this viewset
        return csrf_exempt(super().dispatch)(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Calculate total price if pricing rule is provided
        pricing_rule_id = request.data.get('pricing_rule_id')
        if pricing_rule_id:
            try:
                pricing_rule = PricingRule.objects.get(id=pricing_rule_id, is_active=True)
                num_nights = (serializer.validated_data['check_out'] - 
                            serializer.validated_data['check_in']).days
                total_price = pricing_rule.calculate_total(
                    num_nights, 
                    serializer.validated_data['num_guests']
                )
                serializer.validated_data['total_price'] = total_price
                serializer.validated_data['pricing_rule'] = pricing_rule
            except PricingRule.DoesNotExist:
                pass
        
        self.perform_create(serializer)
        booking = serializer.instance
        
        # Send confirmation email with invoice
        logger = logging.getLogger(__name__)
        try:
            email_sent = send_booking_confirmation_email(booking)
            if not email_sent:
                logger.warning("send_booking_confirmation_email returned False for booking id %s", booking.id)
        except Exception as e:
            logger.exception("Failed to send booking confirmation email for booking id %s", booking.id)
            email_sent = False
        
        # Send payment receipt email if payment method is debit card
        if booking.payment_method == 'debitcard' and booking.status == 'confirmed':
            try:
                payment_details = {
                    'payment_id': f"ch_{booking.id:06d}",
                    'timestamp': datetime.now().strftime('%B %d, %Y at %I:%M %p')
                }
                send_payment_receipt_email(booking, payment_details)
            except Exception as e:
                print(f"Failed to send payment receipt email: {str(e)}")
        
        headers = self.get_success_headers(serializer.data)
        response_data = dict(serializer.data)
        # Include email send status for debugging/clients
        response_data['email_sent'] = bool(email_sent)

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=False, methods=['get'])
    def availability(self, request):
        """
        Check availability for given date range
        Query params: check_in, check_out
        """
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        
        if not check_in or not check_out:
            return Response(
                {'error': 'Both check_in and check_out dates are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            status__in=['pending', 'confirmed'],
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        
        return Response({
            'available': not overlapping.exists(),
            'overlapping_bookings': overlapping.count()
        })


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews
    """
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        featured = self.request.query_params.get('featured', None)
        
        if featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for site settings
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        """Return the single site settings instance"""
        settings = SiteSettings.load()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)


class StripeConfigView(APIView):
    """Return Stripe publishable key to the frontend"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY})


class CreatePaymentIntentView(APIView):
    """Create a Stripe PaymentIntent and return client_secret"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            data = request.data
            amount = int(data.get('amount_cents', 0))
            currency = data.get('currency', 'usd')
            metadata = data.get('metadata', {})

            if amount <= 0:
                return Response({'error': 'Invalid amount'}, status=400)

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata,
            )

            return Response({'client_secret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        # You can use metadata to link to a booking and mark it paid
        booking_id = intent.get('metadata', {}).get('booking_id')
        if booking_id:
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.status = 'confirmed'
                booking.save()
            except Booking.DoesNotExist:
                pass

    return HttpResponse(status=200)
