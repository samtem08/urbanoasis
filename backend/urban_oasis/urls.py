"""
URL configuration for urban_oasis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('amenities/', TemplateView.as_view(template_name='amenities.html'), name='amenities'),
    path('gallery/', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('booking/', TemplateView.as_view(template_name='booking.html'), name='booking'),
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='checkout'),
    path('location/', TemplateView.as_view(template_name='location.html'), name='location'),
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('admin/', admin.site.urls),
    path('api/', include('rentals.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
