"""
Email templates and sending utilities for Urban Oasis bookings
"""
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .invoice_generator import generate_invoice_pdf
import os

logger = logging.getLogger(__name__)


def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email with invoice PDF attachment (if available).
    Falls back to HTML-only email if PDF generation fails.
    
    Args:
        booking: Booking instance
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Try to generate invoice PDF, but don't fail if it errors
        invoice_bytes = None
        pdf_filename = None
        try:
            invoice_pdf = generate_invoice_pdf(booking)
            invoice_bytes = invoice_pdf.read()
            pdf_filename = f"invoice_URB{booking.id:06d}.pdf"
            logger.info("Invoice PDF generated successfully for booking id %s", booking.id)
        except Exception as e:
            logger.warning("Could not generate invoice PDF for booking id %s: %s", booking.id, str(e))
            # Continue without PDF—don't fail the entire email
        
        # Email content
        subject = f"Booking Confirmation - Reference #{booking.id:06d}"
        
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [booking.email]
        
        # Plain text version
        text_content = f"""
Dear {booking.first_name},

Thank you for your booking with Urban Oasis Apartment Rental!

BOOKING CONFIRMATION
Reference Number: URB{booking.id:06d}
Check-in: {booking.check_in.strftime('%B %d, %Y')}
Check-out: {booking.check_out.strftime('%B %d, %Y')}
Number of Guests: {booking.num_guests}
Total Price: ${booking.total_price:.2f}
Status: {booking.status.upper()}

Your invoice and booking details are attached to this email.

IMPORTANT INFORMATION:
- Please arrive between 3:00 PM - 9:00 PM on your check-in date
- Check-out time is 11:00 AM
- Your booking is confirmed and reserved under your name

If you have any questions or need to make changes to your reservation, 
please don't hesitate to contact us:

Email: {settings.BUSINESS_EMAIL}
Phone: {settings.BUSINESS_PHONE}

We look forward to hosting you at Urban Oasis!

Best regards,
Urban Oasis Apartment Rental Team
        """
        
        # HTML version
        html_content = f"""
<html>
<head></head>
<body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c3e50; margin: 0;">Urban Oasis</h1>
            <p style="color: #7f8c8d; margin: 5px 0;">Apartment Rental</p>
        </div>
        
        <p>Dear {booking.first_name},</p>
        
        <p>Thank you for your booking with <strong>Urban Oasis Apartment Rental</strong>!</p>
        
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h2 style="color: #2c3e50; margin-top: 0;">BOOKING CONFIRMATION</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; font-weight: bold; background-color: #fff;">Reference Number:</td>
                    <td style="padding: 8px; background-color: #fff;">URB{booking.id:06d}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Check-in:</td>
                    <td style="padding: 8px;">{booking.check_in.strftime('%B %d, %Y')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; background-color: #fff;">Check-out:</td>
                    <td style="padding: 8px; background-color: #fff;">{booking.check_out.strftime('%B %d, %Y')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Number of Guests:</td>
                    <td style="padding: 8px;">{booking.num_guests}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; background-color: #fff;">Total Price:</td>
                    <td style="padding: 8px; background-color: #fff;">${booking.total_price:.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                    <td style="padding: 8px; color: #27ae60;"><strong>{booking.status.upper()}</strong></td>
                </tr>
            </table>
        </div>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h3 style="color: #856404; margin-top: 0;">IMPORTANT INFORMATION:</h3>
            <ul style="color: #856404; margin: 10px 0;">
                <li>Please arrive between <strong>3:00 PM - 9:00 PM</strong> on your check-in date</li>
                <li>Check-out time is <strong>11:00 AM</strong></li>
                <li>Your booking is confirmed and reserved under your name</li>
            </ul>
        </div>
        
        <p>If you have any questions or need to make changes to your reservation, please don't hesitate to contact us:</p>
        
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p style="margin: 5px 0;"><strong>Email:</strong> <a href="mailto:{settings.BUSINESS_EMAIL}">{settings.BUSINESS_EMAIL}</a></p>
            <p style="margin: 5px 0;"><strong>Phone:</strong> {settings.BUSINESS_PHONE}</p>
        </div>
        
        <p>We look forward to hosting you at Urban Oasis!</p>
        
        <p>Best regards,<br/>
        <strong>Urban Oasis Apartment Rental Team</strong></p>
        
        <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 30px 0;">
        
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2c3e50; margin-top: 0; font-size: 14px;">INVOICE & ATTACHMENT</h3>
            <p style="margin: 10px 0; color: #555;">Your detailed invoice is attached to this email below:</p>
            <p style="margin: 5px 0; font-size: 12px; color: #7f8c8d;">📎 <strong>File:</strong> invoice_URB{booking.id:06d}.pdf</p>
        </div>
        
        <p style="font-size: 12px; color: #7f8c8d; text-align: center; margin-top: 30px;">
            This is an automated email. Please do not reply to this email address.
        </p>
    </div>
</body>
</html>
        """
        
        # Create email
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        
        # Attach PDF invoice if available
        if invoice_bytes and pdf_filename:
            msg.attach(pdf_filename, invoice_bytes, "application/pdf")
        
        # Send email
        msg.send(fail_silently=False)
        logger.info("Confirmation email sent to %s", booking.email)

        # Also notify admin/business email with booking details and copy of invoice
        try:
            admin_subject = f"New Booking Received - Reference URB{booking.id:06d}"
            admin_to = [settings.BUSINESS_EMAIL]

            admin_text = f"""
New booking received:

Reference: URB{booking.id:06d}
Name: {getattr(booking, 'first_name', '')} {getattr(booking, 'last_name', '')}
Email: {booking.email}
Phone: {getattr(booking, 'phone', '')}
Check-in: {booking.check_in.strftime('%Y-%m-%d')}
Check-out: {booking.check_out.strftime('%Y-%m-%d')}
Guests: {booking.num_guests}
Payment Method: {getattr(booking, 'payment_method', '')}
Total Price: ${booking.total_price:.2f}
Status: {booking.status}
Notes: {getattr(booking, 'notes', '')}

This message contains the full booking form information and invoice attachment.
"""

            admin_html = f"""
<html><body>
<h2>New booking received</h2>
<p><strong>Reference:</strong> URB{booking.id:06d}</p>
<p><strong>Name:</strong> {getattr(booking, 'first_name', '')} {getattr(booking, 'last_name', '')}</p>
<p><strong>Email:</strong> {booking.email}</p>
<p><strong>Phone:</strong> {getattr(booking, 'phone', '')}</p>
<p><strong>Check-in:</strong> {booking.check_in.strftime('%Y-%m-%d')}</p>
<p><strong>Check-out:</strong> {booking.check_out.strftime('%Y-%m-%d')}</p>
<p><strong>Guests:</strong> {booking.num_guests}</p>
<p><strong>Payment Method:</strong> {getattr(booking, 'payment_method', '')}</p>
<p><strong>Total Price:</strong> ${booking.total_price:.2f}</p>
<p><strong>Status:</strong> {booking.status}</p>
<p><strong>Notes:</strong> {getattr(booking, 'notes', '')}</p>
<p>This email includes the invoice attached as a PDF.</p>
</body></html>
"""

            admin_msg = EmailMultiAlternatives(admin_subject, admin_text, from_email, admin_to)
            admin_msg.attach_alternative(admin_html, 'text/html')
            if invoice_bytes and pdf_filename:
                admin_msg.attach(pdf_filename, invoice_bytes, 'application/pdf')
            admin_msg.send(fail_silently=False)
            logger.info("Admin notification sent to %s", settings.BUSINESS_EMAIL)
        except Exception as e:
            logger.exception("Error sending admin notification")

        return True

    except Exception as e:
        logger.exception("Error sending confirmation email")
        return False


def send_payment_receipt_email(booking, payment_details=None):
    """
    Send payment receipt email.
    
    Args:
        booking: Booking instance
        payment_details: Optional dict with payment info (payment_id, amount, timestamp)
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = f"Payment Receipt - Booking #{booking.id:06d}"
        
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [booking.email]
        
        payment_id = payment_details.get('payment_id', 'N/A') if payment_details else 'N/A'
        timestamp = payment_details.get('timestamp', '') if payment_details else ''
        
        # Plain text version
        text_content = f"""
Dear {booking.first_name},

Thank you for your payment! Here is your receipt:

PAYMENT RECEIPT
Receipt Number: {booking.id:06d}
Payment ID: {payment_id}
Amount Paid: ${booking.total_price:.2f}
Payment Method: Debit Card
Timestamp: {timestamp}
Status: COMPLETED

This payment is associated with:
Booking Reference: URB{booking.id:06d}
Check-in: {booking.check_in.strftime('%B %d, %Y')}
Check-out: {booking.check_out.strftime('%B %d, %Y')}

Your booking is now confirmed!

If you have any questions, please contact us:
Email: {settings.BUSINESS_EMAIL}
Phone: {settings.BUSINESS_PHONE}

Thank you for choosing Urban Oasis!

Best regards,
Urban Oasis Apartment Rental Team
        """
        
        # HTML version
        html_content = f"""
<html>
<head></head>
<body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #2c3e50; margin: 0;">Urban Oasis</h1>
            <p style="color: #7f8c8d; margin: 5px 0;">Payment Receipt</p>
        </div>
        
        <p>Dear {booking.first_name},</p>
        
        <p>Thank you for your payment! Here is your receipt:</p>
        
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #27ae60;">
            <h2 style="color: #27ae60; margin-top: 0;">PAYMENT RECEIPT</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Receipt Number:</td>
                    <td style="padding: 10px;">{booking.id:06d}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold; background-color: rgba(0,0,0,0.03);">Payment ID:</td>
                    <td style="padding: 10px; background-color: rgba(0,0,0,0.03);">{payment_id}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Amount Paid:</td>
                    <td style="padding: 10px; font-size: 18px; color: #27ae60; font-weight: bold;">${booking.total_price:.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold; background-color: rgba(0,0,0,0.03);">Payment Method:</td>
                    <td style="padding: 10px; background-color: rgba(0,0,0,0.03);">Debit Card</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Timestamp:</td>
                    <td style="padding: 10px;">{timestamp}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold; background-color: rgba(0,0,0,0.03);">Status:</td>
                    <td style="padding: 10px; background-color: rgba(0,0,0,0.03); color: #27ae60;"><strong>✓ COMPLETED</strong></td>
                </tr>
            </table>
        </div>
        
        <div style="background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0;">
            <h3 style="color: #2c3e50; margin-top: 0;">Booking Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Booking Reference:</td>
                    <td style="padding: 8px;">URB{booking.id:06d}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Check-in:</td>
                    <td style="padding: 8px;">{booking.check_in.strftime('%B %d, %Y')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Check-out:</td>
                    <td style="padding: 8px;">{booking.check_out.strftime('%B %d, %Y')}</td>
                </tr>
            </table>
        </div>
        
        <p><strong>Your booking is now confirmed!</strong></p>
        
        <p>If you have any questions, please contact us:</p>
        <p><strong>Email:</strong> <a href="mailto:{settings.BUSINESS_EMAIL}">{settings.BUSINESS_EMAIL}</a><br/>
        <strong>Phone:</strong> {settings.BUSINESS_PHONE}</p>
        
        <p>Thank you for choosing Urban Oasis!</p>
        
        <p>Best regards,<br/>
        <strong>Urban Oasis Apartment Rental Team</strong></p>
        
        <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 30px 0;">
        <p style="font-size: 12px; color: #7f8c8d; text-align: center;">
            This is an automated email. Please do not reply to this email address.
        </p>
    </div>
</body>
</html>
        """
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info("Receipt email sent to %s", booking.email)
        return True

    except Exception as e:
        logger.exception("Error sending receipt email")
        return False
