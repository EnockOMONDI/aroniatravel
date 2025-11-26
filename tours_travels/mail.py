import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def verification_mail(link, user):
    """Send verification email using Mailtrap API"""
    from users.email_utils import send_email_via_mailtrap
    from django.conf import settings


    # Create the email message
    message = f'Hi {user.username}, welcome to Aronia Travel.<br>To activate your account, click the link below:<br>{link}<br><br>'

    # Add a new paragraph about the advantages of your travel agency in HTML
    directors_message = """
    <p><strong>Directors message</strong></p>
    """

    advantages_message = """
    <p>We are delighted to have you as part of the Aronia Travel community. Our goal is simple: We want every trip you take with us to be <strong>affordable</strong> and wonderfully <strong>memorable</strong>. That's where we come in, we take care of all the little things to ensure your journey is smooth and effortless, creating moments you'll treasure forever.</p>
    """

    # Combine all message parts
    html_message = f"""
    <html>
    <body>
        {message}
        {directors_message}
        {advantages_message}
    </body>
    </html>
    """

    # Send email using Mailtrap
    try:
        success = send_email_via_mailtrap(
            subject="Welcome to Aronia Travel",
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
    except Exception as e:
        print(f"Exception sending verification email to {user.email}: {e}")
        return False
    if success:
        print(f"Verification email sent successfully to {user.email}")
    else:
        print(f"Failed to send verification email to {user.email}")

    return success

    

