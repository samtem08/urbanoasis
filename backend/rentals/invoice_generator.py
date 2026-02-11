"""
Invoice generation utility for Urban Oasis bookings - Ultra-simple text-based approach
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def generate_invoice_pdf(booking):
    """
    Generate a PDF invoice for a booking - simplified text-only approach.
    
    Args:
        booking: Booking instance from models.py
        
    Returns:
        BytesIO object containing the PDF
    """
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            alignment=TA_LEFT
        )
        
        center_style = ParagraphStyle(
            'Center',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            spaceAfter=4
        )
        
        # Title
        elements.append(Paragraph(settings.BUSINESS_NAME, title_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Invoice header
        elements.append(Paragraph(f"<b>Invoice Date:</b> {datetime.now().strftime('%B %d, %Y')}", normal_style))
        elements.append(Paragraph(f"<b>Invoice #:</b> {booking.id:06d}", normal_style))
        elements.append(Paragraph(f"<b>Booking Reference:</b> URB{booking.id:06d}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Business info
        elements.append(Paragraph("<b>Bill From:</b>", heading_style))
        elements.append(Paragraph("Urban Oasis Apartment Rental", normal_style))
        elements.append(Paragraph(settings.BUSINESS_ADDRESS, normal_style))
        elements.append(Paragraph(settings.BUSINESS_EMAIL, normal_style))
        elements.append(Paragraph(settings.BUSINESS_PHONE, normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Guest info
        elements.append(Paragraph("<b>Bill To:</b>", heading_style))
        elements.append(Paragraph(f"{booking.first_name} {booking.last_name}", normal_style))
        elements.append(Paragraph(booking.email, normal_style))
        elements.append(Paragraph(booking.phone, normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Booking details
        elements.append(Paragraph("<b>Booking Details</b>", heading_style))
        elements.append(Paragraph(f"<b>Check-in:</b> {booking.check_in.strftime('%B %d, %Y')}", normal_style))
        elements.append(Paragraph(f"<b>Check-out:</b> {booking.check_out.strftime('%B %d, %Y')}", normal_style))
        
        num_nights = (booking.check_out - booking.check_in).days
        elements.append(Paragraph(f"<b>Number of Nights:</b> {num_nights}", normal_style))
        elements.append(Paragraph(f"<b>Number of Guests:</b> {booking.num_guests}", normal_style))
        elements.append(Paragraph(f"<b>Status:</b> {booking.status.upper()}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Price breakdown
        elements.append(Paragraph("<b>Price Summary</b>", heading_style))
        
        nightly_rate = 200.00
        subtotal = num_nights * nightly_rate
        total_amount = float(booking.total_price)
        
        # Create simple text-based price display
        elements.append(Paragraph(f"Nightly Rate: ${nightly_rate:.2f} x {num_nights} nights = ${subtotal:.2f}", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<b>Subtotal:</b> ${subtotal:.2f}", normal_style))
        elements.append(Paragraph("<b>Tax:</b> $0.00", normal_style))
        elements.append(Paragraph("<b>Discount:</b> $0.00", normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Total due
        total_style = ParagraphStyle(
            'Total',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#27ae60'),
            spaceAfter=6,
            alignment=TA_LEFT
        )
        elements.append(Paragraph(f"TOTAL DUE: ${total_amount:.2f}", total_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Payment info
        elements.append(Paragraph("<b>Payment Information</b>", heading_style))
        payment_method_text = {
            'debitcard': 'Debit Card',
            'zelle': 'Zelle Transfer',
            'cashapp': 'Cash App',
        }
        payment_method = payment_method_text.get(booking.payment_method, booking.payment_method or 'Not specified')
        elements.append(Paragraph(f"<b>Payment Method:</b> {payment_method}", normal_style))
        
        if booking.payment_method == 'debitcard':
            elements.append(Paragraph("<b>Payment Status:</b> Completed", normal_style))
        else:
            elements.append(Paragraph("<b>Payment Status:</b> Pending", normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Special requests
        if booking.special_requests:
            elements.append(Paragraph("<b>Special Requests</b>", heading_style))
            elements.append(Paragraph(booking.special_requests, normal_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            spaceAfter=4
        )
        footer_text = f"Thank you for choosing Urban Oasis! For questions, contact {settings.BUSINESS_EMAIL} or {settings.BUSINESS_PHONE}"
        elements.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        logger.info("Invoice PDF generated successfully for booking id %s", booking.id)
        return buffer
    
    except Exception as e:
        logger.exception("Error generating invoice PDF for booking id %s: %s", booking.id, str(e))
        raise
