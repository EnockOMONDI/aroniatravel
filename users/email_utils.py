"""
Email utility functions for Aronia Travel using Mailtrap HTTP API
"""
import logging
from typing import List, Optional, Dict, Any
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

try:
    from mailtrap import Mail, Address, MailtrapClient
    MAILTRAP_AVAILABLE = True
except ImportError:
    MAILTRAP_AVAILABLE = False
    logger.warning("Mailtrap package not available. Falling back to Django's default email backend.")


def send_email_via_mailtrap(
    subject: str,
    html_message: str,
    from_email: str,
    recipient_list: List[str],
    text_message: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None
) -> bool:
    """
    Send email using Mailtrap HTTP API
    
    Args:
        subject: Email subject
        html_message: HTML content of the email
        from_email: Sender email address
        recipient_list: List of recipient email addresses
        text_message: Plain text version (optional, will be generated from HTML if not provided)
        attachments: List of attachment dictionaries (optional)
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not MAILTRAP_AVAILABLE or not getattr(settings, 'MAILTRAP_API_TOKEN', None):
        # Fallback to Django's default email backend
        logger.info("Using Django's default email backend as fallback")
        try:
            if not text_message:
                text_message = strip_tags(html_message)
            
            django_send_mail(
                subject=subject,
                message=text_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email via Django backend: {e}")
            return False
    
    try:
        client = MailtrapClient(token=settings.MAILTRAP_API_TOKEN)

        # Parse from_email to extract name and email
        if '<' in from_email and '>' in from_email:
            from_name = from_email.split('<')[0].strip()
            from_email_addr = from_email.split('<')[1].split('>')[0].strip()
        else:
            from_name = "Aronia Travel"
            from_email_addr = from_email

        # Create sender address
        sender = Address(email=from_email_addr, name=from_name)

        # Create recipient addresses
        recipients = [Address(email=email) for email in recipient_list]

        # Add text version if not provided
        if not text_message:
            text_message = strip_tags(html_message)

        # Create mail object
        mail = Mail(
            sender=sender,
            to=recipients,
            subject=subject,
            text=text_message,
            html=html_message
        )

        # Send email using Mailtrap API
        response = client.send(mail)
        logger.info(f"Email sent successfully via Mailtrap API. Response: {response}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email via Mailtrap API: {e}")
        return False


def send_inquiry_email(inquiry_type: str, inquiry_data: Dict[str, Any], template_name: str = None) -> bool:
    """
    Send inquiry email with proper routing based on inquiry type
    
    Args:
        inquiry_type: Type of inquiry (general, mice, careers, etc.)
        inquiry_data: Dictionary containing inquiry information
        template_name: Optional custom template name
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Get recipient email based on inquiry type
        recipient_email = settings.EMAIL_ROUTING.get(inquiry_type, settings.ADMIN_EMAIL)
        
        # Use default template if none provided
        if not template_name:
            template_name = f'emails/{inquiry_type}_inquiry.html'
        
        # Prepare email subject
        subject_map = {
            'general': 'New General Inquiry',
            'mice': 'New MICE Inquiry',
            'careers': 'New Career Inquiry',
            'booking': 'New Booking Inquiry',
            'support': 'New Support Request',
        }
        subject = subject_map.get(inquiry_type, 'New Inquiry')
        
        # Add company/name to subject if available
        if 'company_name' in inquiry_data:
            subject += f": {inquiry_data['company_name']}"
        elif 'full_name' in inquiry_data:
            subject += f" from {inquiry_data['full_name']}"
        
        # Render email template
        try:
            html_message = render_to_string(template_name, {
                'inquiry': inquiry_data,
                'inquiry_type': inquiry_type
            })
        except Exception as template_error:
            # Fallback to simple HTML if template not found
            logger.warning(f"Template {template_name} not found, using fallback: {template_error}")
            html_message = generate_fallback_email_html(inquiry_type, inquiry_data)
        
        # Send email
        return send_email_via_mailtrap(
            subject=subject,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email]
        )
        
    except Exception as e:
        logger.error(f"Failed to send inquiry email: {e}")
        return False


def generate_fallback_email_html(inquiry_type: str, inquiry_data: Dict[str, Any]) -> str:
    """
    Generate a simple HTML email when template is not available
    """
    html = f"""
    <html>
    <body>
        <h2>New {inquiry_type.title()} Inquiry - Aronia Travel</h2>
        <table style="border-collapse: collapse; width: 100%;">
    """
    
    for key, value in inquiry_data.items():
        if value:  # Only include non-empty values
            formatted_key = key.replace('_', ' ').title()
            html += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">{formatted_key}:</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{value}</td>
            </tr>
            """
    
    html += """
        </table>
        <br>
        <p>This inquiry was submitted through the Aronia Travel website.</p>
    </body>
    </html>
    """
    
    return html


def send_booking_confirmation_email(booking_data: Dict[str, Any], customer_email: str) -> bool:
    """
    Send booking confirmation email to customer
    
    Args:
        booking_data: Dictionary containing booking information
        customer_email: Customer's email address
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = f"Booking Confirmation - {booking_data.get('booking_reference', 'N/A')}"
        
        # Try to render template, fallback to simple HTML
        try:
            html_message = render_to_string('emails/booking_confirmation.html', {
                'booking': booking_data
            })
        except Exception:
            html_message = f"""
            <html>
            <body>
                <h2>Booking Confirmation - Aronia Travel</h2>
                <p>Dear {booking_data.get('full_name', 'Valued Customer')},</p>
                <p>Thank you for your booking with Aronia Travel!</p>
                <p><strong>Booking Reference:</strong> {booking_data.get('booking_reference', 'N/A')}</p>
                <p><strong>Tour:</strong> {booking_data.get('tour_name', 'N/A')}</p>
                <p><strong>Travel Date:</strong> {booking_data.get('travel_date', 'N/A')}</p>
                <p><strong>Number of People:</strong> {booking_data.get('number_of_people', 'N/A')}</p>
                <p><strong>Total Price:</strong> ${booking_data.get('total_price', 'N/A')}</p>
                <p>We will contact you soon with further details.</p>
                <p>Best regards,<br>Aronia Travel Team</p>
            </body>
            </html>
            """
        
        return send_email_via_mailtrap(
            subject=subject,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email]
        )
        
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {e}")
        return False


def test_email_configuration() -> bool:
    """
    Test email configuration by sending a test email
    
    Returns:
        bool: True if test email was sent successfully, False otherwise
    """
    test_subject = "Aronia Travel - Email Configuration Test"
    test_message = """
    <html>
    <body>
        <h2>Email Configuration Test</h2>
        <p>This is a test email to verify that the Aronia Travel email configuration is working correctly.</p>
        <p>If you receive this email, the configuration is successful!</p>
        <p>Best regards,<br>Aronia Travel System</p>
    </body>
    </html>
    """
    
    return send_email_via_mailtrap(
        subject=test_subject,
        html_message=test_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL]
    )
