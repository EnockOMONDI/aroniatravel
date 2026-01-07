from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Avg
from .models import Destination, Tour, Review, OptionalActivity
from adminside.models import Accomodation
from django.views.generic.edit import CreateView
from .models import Tour, Booking, DayTrip, DayTripBooking, QuoteInquiry
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from events.models import EventCategory
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q  # Add this import at the top with other imports
from users.email_utils import send_email_via_mailtrap


# Add this view function



class HomeView(ListView):
    model = Tour
    template_name = 'users/aronia/index.html'
    context_object_name = 'tours'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # First get all featured day trips
        featured_daytrips = DayTrip.objects.filter(is_featured=True)
        
        # Then filter based on dates and recurrence
        featured_daytrips = featured_daytrips.filter(
            Q(recurrence='none', start_date__gte=today) |  # Future one-time trips
            Q(recurrence__in=['weekend', 'saturday', 'sunday'])  # All recurring trips
        )
        
        context.update({
            'featured_tours': Tour.objects.filter(is_featured=True)[:6],
            'top_tours': Tour.objects.filter(rating__gte=4.5)[:6],
            'popular_destinations': Destination.objects.all()[:6],
            'event_categories': EventCategory.objects.all(),
            'featured_daytrips': featured_daytrips[:4],
            'today': today,
        })
        return context




class DayTripListView(ListView):
    model = DayTrip
    template_name = 'users/aronia/daytrip_list.html'
    context_object_name = 'daytrips'
    paginate_by = 9

    def get_queryset(self):
        today = timezone.now().date()
        # Show both one-time and recurring trips
        return DayTrip.objects.filter(
            Q(recurrence='none', start_date__gte=today) |  # One-time trips in future
            Q(recurrence__in=['weekend', 'saturday', 'sunday'], start_date__lte=today)  # Active recurring trips
        ).order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['featured_daytrips'] = DayTrip.objects.filter(
            is_featured=True
        ).filter(
            Q(recurrence='none', start_date__gte=today) |
            Q(recurrence__in=['weekend', 'saturday', 'sunday'], start_date__lte=today)
        )[:6]
        context['today'] = today
        return context
    

class DayTripDetailView(DetailView):
    model = DayTrip
    template_name = 'users/aronia/daytrip_detail.html'
    context_object_name = 'daytrip'
    slug_url_kwarg = 'daytrip_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        daytrip = self.object
        
        # Get available dates for the next 8 weeks
        available_dates = daytrip.get_available_dates(num_weeks=8)
        
        # Format dates for the template
        formatted_dates = [
            {
                'date': date,
                'remaining_slots': daytrip.get_remaining_slots(date)
            }
            for date in available_dates
        ]
        
        context['available_dates'] = formatted_dates
        context['upcoming_daytrips'] = DayTrip.objects.filter(
            start_date__gte=timezone.now().date()
        ).exclude(
            id=self.object.id
        )[:3]
        return context

def send_daytrip_confirmation_email(booking):
    """Send day trip booking confirmation email using Mailtrap API"""
    from users.email_utils import send_email_via_mailtrap
    from django.conf import settings

    try:
        # Create activities list for email if any were selected
        activities_html = ""
        if booking.optional_activities.exists():
            activities_html = """
            <div class="booking-details" style="margin-top: 20px;">
                <h3>Optional Activities Booked:</h3>
                <ul>
            """
            for activity in booking.optional_activities.all():
                activities_html += f"<li>{activity.name} - USD {activity.price} per person</li>"
            activities_html += "</ul></div>"

        # Customer email message
        customer_email = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Day Trip Booking Confirmation</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    padding: 20px 0;
                    background-color: #f8f9fa;
                }}
                .logo {{
                    max-width: 200px;
                    height: auto;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .booking-details {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <img src="https://www.aroniatravel.com/static/assets4/" alt="ARONIA" class="logo">
                </div>
                
                <div class="content">
                    <h2>Day Trip Booking Confirmation</h2>
                    <p>Dear {booking.full_name},</p>
                    
                    <p>Thank you for booking your day trip with ARONIA! We're excited to have you join us for {booking.daytrip.name}.</p>
                    
                    <div class="booking-details">
                        <h3>Booking Details:</h3>
                        <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                        <p><strong>Day Trip:</strong> {booking.daytrip.name}</p>
                        <p><strong>Date:</strong> {booking.daytrip.date}</p>
                        <p><strong>Pickup Time:</strong> {booking.daytrip.pickup_time}</p>
                        <p><strong>Pickup Location:</strong> {booking.daytrip.pickup_location}</p>
                        <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                        <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                    </div>
                    
                    {activities_html}
                    
                    <p>Your booking status is currently <strong>pending</strong>. Our team will contact you shortly regarding payment and final confirmation.</p>
                    
                    <p>If you have any questions, please contact us with your booking reference: {booking.booking_reference}</p>
                </div>
                
                <div class="footer">
                    <p>Best regards,<br>The ARONIA TRAVEL Team</p>
                    <p>© 2024 ARONIA. All rights reserved.</p>
                    <p>
                        <a href="tel:+254116784345</a> 
                        <a href="mailto:info@aroniatravel.com">info@aroniatravel.com</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        # Admin email message
        admin_email = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Day Trip Booking</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    padding: 20px 0;
                    background-color: #f8f9fa;
                }}
                .logo {{
                    max-width: 200px;
                    height: auto;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .booking-details {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <img src="https://www.aroniatravel.com/static/assets4/" alt="ARONIA" class="logo">
                </div>
                
                <div class="content">
                    <h2>New Day Trip Booking</h2>
                    <p>A booking has been made for a day trip. Here are the details:</p>
                    
                    <div class="booking-details">
                        <h3>Customer Information:</h3>
                        <p><strong>Customer Name:</strong> {booking.full_name}</p>
                        <p><strong>Email:</strong> {booking.email}</p>
                        <p><strong>Phone:</strong> {booking.phone}</p>
                        
                        <h3>Booking Details:</h3>
                        <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                        <p><strong>Day Trip:</strong> {booking.daytrip.name}</p>
                        <p><strong>Date:</strong> {booking.daytrip.date}</p>
                        <p><strong>Pickup Time:</strong> {booking.daytrip.pickup_time}</p>
                        <p><strong>Pickup Location:</strong> {booking.daytrip.pickup_location}</p>
                        <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                        <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                        
                        <h3>Special Requirements:</h3>
                        <p>{booking.special_requirements if booking.special_requirements else 'None specified'}</p>
                    </div>
                    
                    {activities_html}
                    
                    <p>Please review and process this booking as soon as possible.</p>
                </div>
                
                <div class="footer">
                    <p>© 2024 ARONIA. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Send customer confirmation email
        customer_success = send_email_via_mailtrap(
            subject=f"Day Trip Booking Confirmation - {booking.booking_reference}",
            html_message=customer_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email]
        )

        # Send admin notification email
        admin_success = send_email_via_mailtrap(
            subject=f"New Day Trip Booking - {booking.booking_reference}",
            html_message=admin_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["travel@aroniatravel.com"]
        )

        if customer_success and admin_success:
            print(f"SUCCESSFULLY SENT EMAIL to {booking.email} and travel@aroniatravel.com for booking {booking.booking_reference}")
        else:
            print(f"Email sending partially failed for booking {booking.booking_reference}")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        raise e

def daytrip_booking(request, daytrip_slug):
    daytrip = get_object_or_404(DayTrip, slug=daytrip_slug)
    today = timezone.now().date()
    
    if request.method == 'POST':
        try:
            # Get and validate selected date
            travel_date = datetime.datetime.strptime(request.POST.get('travel_date'), '%Y-%m-%d').date()
            
            if travel_date < today:
                raise ValidationError("Travel date cannot be in the past")
                
            # Validate date is available
            if not daytrip.is_available_on_date(travel_date):
                raise ValidationError("Selected date is not available for this trip")

            # Validate number of people
            try:
                number_of_people = int(request.POST.get('number_of_people', 1))
                if number_of_people < 1:
                    raise ValidationError("Number of people must be at least 1")
                
                # Check remaining slots for the selected date
                remaining_slots = daytrip.get_remaining_slots(travel_date)
                if number_of_people > remaining_slots:
                    raise ValidationError(f"Only {remaining_slots} slots available for this date")
            except ValueError:
                raise ValidationError("Please enter a valid number of people")

            # Calculate base price
            base_price = daytrip.price * number_of_people
            
            # Handle optional activities
            total_price = base_price
            selected_activities = []
            optional_activities = request.POST.getlist('optional_activities')
            
            if optional_activities:
                for activity_id in optional_activities:
                    try:
                        activity = OptionalActivity.objects.get(id=activity_id, daytrip=daytrip)
                        if activity.price:
                            total_price += activity.price * number_of_people
                        selected_activities.append(activity)
                    except OptionalActivity.DoesNotExist:
                        continue

            # Create new booking
            booking = DayTripBooking(
                daytrip=daytrip,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                travel_date=travel_date,
                number_of_people=number_of_people,
                special_requirements=request.POST.get('special_requirements'),
                total_price=total_price,
                booking_status='pending',
                payment_status='pending'
            )
            
            # Validate the model
            booking.full_clean()
            
            # Save the booking
            booking.save()

            # Add optional activities after saving
            if selected_activities:
                booking.optional_activities.set(selected_activities)

            # Send confirmation emails
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
                s.starttls()
                s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                # Create two separate messages - one for each recipient
                # First message (for customer)
                msg1 = MIMEMultipart('alternative')
                msg1['From'] = "ARONIA TRAVEL <aroniatravelke@gmail.com>"
                msg1['To'] = booking.email
                msg1['Subject'] = f"Day Trip Booking Confirmation - {booking.booking_reference}"

                # Second message (for info@aroniatravel.com)
                msg2 = MIMEMultipart('alternative')
                msg2['From'] = "ARONIA TRAVEL <aroniatravelke@gmail.com>"
                msg2['To'] = "travel@aroniatravel.com"
                msg2['Subject'] = f"New Day Trip Booking - {booking.booking_reference}"

                # Create activities list for email if any were selected
                activities_html = ""
                if booking.optional_activities.exists():
                    activities_html = """
                    <div class="booking-details" style="margin-top: 20px;">
                        <h3>Optional Activities Booked:</h3>
                        <ul>
                    """
                    for activity in booking.optional_activities.all():
                        activities_html += f"<li>{activity.name} - USD {activity.price} per person</li>"
                    activities_html += "</ul></div>"

                # Customer email message
                customer_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Day Trip Booking Confirmation</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .booking-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="ARONIA" class="logo">
                        </div>
                        
                        <div class="content">
                            <h2>Day Trip Booking Confirmation</h2>
                            <p>Dear {booking.full_name},</p>
                            
                            <p>Thank you for booking your day trip with ARONIA TRAVEL! We're excited to have you join us for {booking.daytrip.name}.</p>
                            
                            <div class="booking-details">
                                <h3>Booking Details:</h3>
                                <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                                <p><strong>Day Trip:</strong> {booking.daytrip.name}</p>
                                <p><strong>Date:</strong> {booking.travel_date}</p>
                                <p><strong>Pickup Time:</strong> {booking.daytrip.pickup_time}</p>
                                <p><strong>Pickup Location:</strong> {booking.daytrip.pickup_location}</p>
                                <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                                <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                            </div>
                            
                            {activities_html}
                            
                            <p>Your booking status is currently <strong>pending</strong>. Our team will contact you shortly regarding payment and final confirmation.</p>
                            
                            <p>If you have any questions, please contact us with your booking reference: {booking.booking_reference}</p>
                        </div>
                        
                        <div class="footer">
                            <p>Best regards,<br>The ARONIA TRAVEL Team</p>
                            <p>© 2024 ARONIA. All rights reserved.</p>
                            <p>
                                <a href="tel:+254116784345</a> |
                                <a href="mailto:info@aroniatravel.com">info@aroniatravel.com</a>
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Admin email message
                admin_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>New Day Trip Booking</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .booking-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="ARONIA" class="logo">
                        </div>
                        
                        <div class="content">
                            <h2>New Day Trip Booking</h2>
                            <p>A booking has been made for a day trip. Here are the details:</p>
                            
                            <div class="booking-details">
                                <h3>Customer Information:</h3>
                                <p><strong>Customer Name:</strong> {booking.full_name}</p>
                                <p><strong>Email:</strong> {booking.email}</p>
                                <p><strong>Phone:</strong> {booking.phone}</p>
                                
                                <h3>Booking Details:</h3>
                                <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                                <p><strong>Day Trip:</strong> {booking.daytrip.name}</p>
                                <p><strong>Date:</strong> {booking.travel_date}</p>
                                <p><strong>Pickup Time:</strong> {booking.daytrip.pickup_time}</p>
                                <p><strong>Pickup Location:</strong> {booking.daytrip.pickup_location}</p>
                                <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                                <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                                
                                <h3>Special Requirements:</h3>
                                <p>{booking.special_requirements if booking.special_requirements else 'None specified'}</p>
                            </div>
                            
                            {activities_html}
                            
                            <p>Please review and process this booking as soon as possible.</p>
                        </div>
                        
                        <div class="footer">
                            <p>© 2024 ARONIA. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Attach the HTML content to respective messages
                msg1.attach(MIMEText(customer_email, 'html'))
                msg2.attach(MIMEText(admin_email, 'html'))

                # Send both messages
                s.send_message(msg1)
                s.send_message(msg2)
                
                s.quit()
                print(f"SUCCESSFULLY SENT EMAIL to {booking.email} and travel@aroniatravel.com for booking {booking.booking_reference}")
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                # Continue with the booking process even if email fails

            messages.success(request, 'Day Trip booking successful! Check your email for confirmation.')
            return redirect('aronia:daytrip_booking_confirmation', booking_reference=booking.booking_reference)
            
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, str(e))
            print(f"Validation error: {str(e)}")  # For debugging
        except Exception as e:
            messages.error(request, 'There was an error processing your booking. Please try again.')
            print(f"Booking error: {str(e)}")  # For debugging
        
        # If there's an error, re-render the form with the submitted data
        return render(request, 'users/aronia/daytrip-booking-form.html', {
            'daytrip': daytrip,
            'form_data': request.POST,
            'today': today,
            'available_dates': daytrip.get_available_dates()
        })
    
    # For GET requests, render empty form
    return render(request, 'users/aronia/daytrip-booking-form.html', {
        'daytrip': daytrip,
        'today': today,
        'form_data': None,
        'available_dates': daytrip.get_available_dates()
    })

def daytrip_booking_confirmation(request, booking_reference):
    booking = get_object_or_404(DayTripBooking, booking_reference=booking_reference)
    return render(request, 'users/aronia/daytrip-booking-confirmation.html', {'booking': booking})
    
class AboutView(TemplateView):
    template_name = 'users/aronia/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data you want to display on the about page
        return context
    


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    return render(request, 'users/aronia/destination_detail.html', {'destination': destination})

# class ShopView(ListView):
#     model = Product
#     template_name = 'users/aronia/shop.html'
#     context_object_name = 'products'
#     paginate_by = 9  # Number of products per page

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Add any filtering logic here if needed
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add any additional context data for the shop page
#         return context

class ContactView(TemplateView):
    template_name = 'users/aronia/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data for the contact page
        return context
    

    def post(self, request, *args, **kwargs):
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Add your contact form processing logic here
        # For example, sending an email or saving to database

        # Redirect or render response
        return render(request, self.template_name, {
            'success_message': 'Thank you for your message. We will get back to you soon!'
        })


class TutorialsView(TemplateView):
    template_name = 'users/aronia/tutorials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guide_sections'] = [
            {
                'title': 'Sign In & Dashboard Orientation',
                'icon': 'fa-lock',
                'summary': 'Use the Django admin to manage every section of the site.',
                'steps': [
                    'Visit /admin/ and sign in with your staff account.',
                    'Use the left sidebar to open the section you want to manage (BLOG, ARONIA, EVENTS, USERS).',
                    'The search bar at the top of the admin lists helps you quickly find tours, day trips, or bookings.'
                ]
            },
            {
                'title': 'Publish Blog Stories',
                'icon': 'fa-pen-nib',
                'summary': 'Keep the blog fresh with new posts and highlights.',
                'steps': [
                    'Open BLOG ▸ Posts and click “Add Post”.',
                    'Fill in the title, summary/excerpt, body content, thumbnail, and select the destination or category.',
                    'Set the status to “Published” and hit Save; use “Draft” when you need editorial review.'
                ]
            },
            {
                'title': 'Add Tour Packages',
                'icon': 'fa-suitcase-rolling',
                'summary': 'Packages appear on the public Tours page.',
                'steps': [
                    'Go to ARONIA ▸ Tours and click “Add tour”.',
                    'Choose the destination, upload hero and gallery images via UploadCare, and fill in pricing, duration, and highlights.',
                    'Add itinerary days, inclusions, and highlights at the bottom of the form, then Save.'
                ]
            },
            {
                'title': 'Create Day Trips',
                'icon': 'fa-map-marked-alt',
                'summary': 'One-day experiences with optional activities.',
                'steps': [
                    'Open ARONIA ▸ Day trips ▸ Add day trip.',
                    'Set the recurrence (one-time, weekend, Saturday, or Sunday) and include pickup details plus included items.',
                    'Use the optional activities inline form to upsell add-ons guests can pick on checkout.'
                ]
            },
            {
                'title': 'Review Bookings & Quotes',
                'icon': 'fa-receipt',
                'summary': 'Every request is stored in the admin.',
                'steps': [
                    'Tours: ARONIA ▸ Bookings shows pending, confirmed, or completed reservations.',
                    'Day trips: ARONIA ▸ Day trip bookings lists attendees and remaining slots.',
                    'Quotes: ARONIA ▸ Quote inquiries tracks travelers waiting for a price proposal.'
                ]
            },
            {
                'title': 'Manage Events',
                'icon': 'fa-calendar-check',
                'summary': 'Events keep your community informed.',
                'steps': [
                    'Visit EVENTS ▸ Events to add or update experiences, tickets, and galleries.',
                    'Ticket types let you control prices, quotas, and sale dates.',
                    'Use “Launch notifications” to see who subscribed for updates.'
                ]
            }
        ]

        context['quick_actions'] = [
            {
                'title': 'Check New Bookings',
                'detail': 'ARONIA ▸ Bookings ▸ filter by “Pending” to contact travelers who just booked.'
            },
            {
                'title': 'Update Hero Images',
                'detail': 'Blog posts, tours, and day trips all use UploadCare. Replace images directly inside each record.'
            },
            {
                'title': 'Coordinate Quotes',
                'detail': 'ARONIA ▸ Quote inquiries ▸ open each entry, add your price and validity date, then update the status.'
            },
        ]

        context['booking_flow'] = [
            'Visitors browse Tours or Day Trips and submit a booking or quote form.',
            'The request appears immediately inside the ARONIA ▸ Bookings or Quote inquiries tables.',
            'Automatic confirmation emails go to the traveler; admins receive the same details.',
            'Staff reviews the request, updates the status (Pending → Confirmed/Completed), and adds notes as needed.',
            'Finance or reservations reaches out to collect payment and final travel documents.'
        ]

        context['support_cards'] = [
            {
                'title': 'Need a New Admin User?',
                'body': 'Create staff accounts under USERS ▸ Users, check “Staff status”, and assign only the groups they need.'
            },
            {
                'title': 'Content Ready to Publish?',
                'body': 'Use the Preview button in the admin to double-check formatting before publishing blog stories or tour updates.'
            },
            {
                'title': 'Keep the Inbox in Sync',
                'body': 'When a booking is handled offline, update its status inside the admin so the dashboard reflects reality.'
            }
        ]
        return context

class TourListView(ListView):
    model = Tour
    template_name = 'users/aronia/tour-grid-1.html'
    context_object_name = 'tours'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        context['featured_tours'] = Tour.objects.filter(is_featured=True)
        return context

    def get_queryset(self):
        queryset = Tour.objects.all()
        destination = self.request.GET.get('destination')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        duration = self.request.GET.get('duration')
        featured = self.request.GET.get('featured')  # Add this line

        if destination:
            queryset = queryset.filter(destination__slug=destination)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if duration:
            queryset = queryset.filter(duration=duration)
        if featured:  # Add this block
            queryset = queryset.filter(is_featured=True)

        return queryset.select_related('destination')  # Optimize database queries

class HotelListView(ListView):
    model = Accomodation
    template_name = 'users/aronia/hotel-grid-1.html'
    context_object_name = 'hotels'
    paginate_by = 9

    CATEGORY_FILTERS = {
        'luxury': {'min_price': 400},
        'comfort': {'min_price': 200, 'max_price': 399},
        'budget': {'max_price': 199},
        'longstay': {'min_price': 150},
        'airport': {}
    }

    def get_queryset(self):
        queryset = super().get_queryset().order_by('hotel_name')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if search:
            queryset = queryset.filter(hotel_name__icontains=search.strip())

        if category in self.CATEGORY_FILTERS:
            filters = self.CATEGORY_FILTERS[category]
            min_price = filters.get('min_price')
            max_price = filters.get('max_price')
            if min_price is not None:
                queryset = queryset.filter(price_per_room__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price_per_room__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['categories'] = [
            {'key': 'luxury', 'label': 'Luxury Hotels'},
            {'key': 'comfort', 'label': 'Comfort Stays'},
            {'key': 'budget', 'label': 'Affordable Lodging'},
            {'key': 'longstay', 'label': 'Extended Stays'},
            {'key': 'airport', 'label': 'Airport Convenience'},
        ]
        return context

class HotelDetailView(DetailView):
    model = Accomodation
    template_name = 'users/aronia/hotel-detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_hotels'] = Accomodation.objects.exclude(pk=self.object.pk)[:3]
        return context

class TourDetailView(DetailView):
    model = Tour
    template_name = 'users/aronia/tourdetailsmain.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'  # Add this line to match the URL pattern

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()
        
        # Get reviews with aggregated ratings
        reviews = tour.reviews.all()
        avg_ratings = reviews.aggregate(
            avg_location=Avg('location_rating'),
            avg_price=Avg('price_rating'),
            avg_amenities=Avg('amenities_rating'),
            avg_services=Avg('services_rating'),
            avg_rooms=Avg('rooms_rating')
        )
        
        context.update({
            'reviews': reviews,
            'avg_ratings': avg_ratings,
            'highlights': tour.highlights.all(),
            'inclusions': tour.inclusions.filter(is_included=True),
            'exclusions': tour.inclusions.filter(is_included=False),
            'tour_days': tour.tour_days.all(),
            'related_tours': Tour.objects.filter(destination=tour.destination).exclude(id=tour.id)[:3]
        })
        
        return context

def submit_review(request, tour_slug):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, slug=tour_slug)
        
        review = Review(
            tour=tour,
            user_name=request.POST.get('name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('message'),
            location_rating=request.POST.get('location_rating'),
            price_rating=request.POST.get('price_rating'),
            amenities_rating=request.POST.get('amenities_rating'),
            services_rating=request.POST.get('services_rating'),
            rooms_rating=request.POST.get('rooms_rating')
        )
        review.save()
        
        # Update tour rating and review count
        tour.reviews_count = tour.reviews.count()
        tour.rating = tour.reviews.aggregate(Avg('rating'))['rating__avg']
        tour.save()
        
        messages.success(request, 'Your review has been submitted successfully!')
        # Update the redirect to use tour_slug instead of slug
        return redirect('aronia:tour_detail', tour_slug=tour_slug)
    
    return redirect('aronia:tour_detail', tour_slug=tour_slug)


def tour_booking(request, tour_slug):
    tour = get_object_or_404(Tour, slug=tour_slug)
    today = timezone.now().date()
    
    if request.method == 'POST':
        try:
            # Validate travel date
            travel_date = datetime.datetime.strptime(request.POST.get('travel_date'), '%Y-%m-%d').date()
            if travel_date < today:
                raise ValidationError("Travel date cannot be in the past")

            # Validate number of people
            try:
                number_of_people = int(request.POST.get('number_of_people', 1))
                if number_of_people < 1:
                    raise ValidationError("Number of people must be at least 1")
                if number_of_people > tour.group_size:
                    raise ValidationError(f"Number of people cannot exceed tour's maximum group size of {tour.group_size}")
            except ValueError:
                raise ValidationError("Please enter a valid number of people")

            # Calculate total price
            total_price = tour.price * number_of_people

            # Create new booking
            booking = Booking(
                tour=tour,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                travel_date=travel_date,
                number_of_people=number_of_people,
                special_requirements=request.POST.get('special_requirements'),
                total_price=total_price,
                booking_status='pending',
                payment_status='pending',
                deposit_paid=0
            )
            
            # Validate the model
            booking.full_clean()
            
            # Save the booking
            booking.save()

            # Send confirmation email
            try:
                from users.email_utils import send_email_via_mailtrap

                # Customer email message
                customer_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Tour Booking Confirmation</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .booking-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="ARONIA" class="logo">
                        </div>
                        
                        <div class="content">
                            <h2>Tour Booking Confirmation</h2>
                            <p>Dear {booking.full_name},</p>
                            
                            <p>Thank you for booking your tour with ARONIA! We're excited to help you explore {tour.name}.</p>
                            
                            <div class="booking-details">
                                <h3>Booking Details:</h3>
                                <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                                <p><strong>Tour:</strong> {tour.name}</p>
                                <p><strong>Travel Date:</strong> {booking.travel_date}</p>
                                <p><strong>Duration:</strong> {tour.duration} days</p>
                                <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                                <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                            </div>
                            
                            <p>Your booking status is currently <strong>pending</strong>. Our team will contact you shortly regarding payment and final confirmation.</p>
                            
                            <p>If you have any questions, please contact us with your booking reference: {booking.booking_reference}</p>
                        </div>
                        
                        <div class="footer">
                                    <p>Best regards,<br>The ARONIA TRAVEL Team</p>
                            <p>© 2024 ARONIA. All rights reserved.</p>
                            <p>
                                <a href="tel:+254758355325">+254758355325</a> |
                                <a href="mailto:info@aroniatravel.com">info@aroniatravel.com</a>
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Admin email message
                admin_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>New Tour Booking</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .booking-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="ARONIA" class="logo">
                        </div>
                        
                        <div class="content">
                            <h2>New Tour Booking</h2>
                            <p>A booking has been made for a tour. Here are the details:</p>
                            
                            <div class="booking-details">
                                <h3>Customer Information:</h3>
                                <p><strong>Customer Name:</strong> {booking.full_name}</p>
                                <p><strong>Email:</strong> {booking.email}</p>
                                <p><strong>Phone:</strong> {booking.phone}</p>
                                
                                <h3>Booking Details:</h3>
                                <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                                <p><strong>Tour:</strong> {tour.name}</p>
                                <p><strong>Travel Date:</strong> {booking.travel_date}</p>
                                <p><strong>Duration:</strong> {tour.duration} days</p>
                                <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                                <p><strong>Total Price:</strong> USD {booking.total_price}</p>
                                
                                <h3>Special Requirements:</h3>
                                <p>{booking.special_requirements if booking.special_requirements else 'None specified'}</p>
                            </div>
                            
                            <p>Please review and process this booking as soon as possible.</p>
                        </div>
                        
                        <div class="footer">
                            <p>© 2024 ARONIA. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Send customer confirmation email
                customer_success = send_email_via_mailtrap(
                    subject=f"Tour Booking Confirmation - {booking.booking_reference}",
                    html_message=customer_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email]
                )

                # Send admin notification email
                admin_success = send_email_via_mailtrap(
                    subject=f"New Tour Booking - {booking.booking_reference}",
                    html_message=admin_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["travel@aroniatravel.com"]
                )

                if customer_success and admin_success:
                    print(f"SUCCESSFULLY SENT EMAIL to {booking.email} and travel@aroniatravel.com for booking {booking.booking_reference}")
                else:
                    print(f"Email sending partially failed for booking {booking.booking_reference}")
            except Exception as e:
                # Log the error but don't stop the booking process
                print(f"Email sending failed: {str(e)}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {str(e)}")

            messages.success(request, 'Booking successful! Check your email for confirmation.')
            return redirect('aronia:booking_confirmation', booking_reference=booking.booking_reference)
            
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'There was an error processing your booking. Please try again.')
            print(f"Booking error: {str(e)}")  # For debugging
        
        # If there's an error, re-render the form with the submitted data
        return render(request, 'users/aronia/booking-form.html', {
            'tour': tour,
            'form_data': request.POST,
            'today': today,
        })
    
    # For GET requests, render empty form
    return render(request, 'users/aronia/booking-form.html', {
        'tour': tour,
        'today': today,
        'form_data': None,
    })

def tour_quote_inquiry(request, tour_slug):
    """Handle quote inquiry form submissions"""
    tour = get_object_or_404(Tour, slug=tour_slug)
    today = timezone.now().date()

    if request.method == 'POST':
        try:
            # Validate preferred date
            preferred_date_str = request.POST.get('preferred_date')
            if preferred_date_str:
                preferred_date = datetime.datetime.strptime(preferred_date_str, '%Y-%m-%d').date()
                if preferred_date < today:
                    raise ValidationError("Preferred date cannot be in the past")
            else:
                raise ValidationError("Please select a preferred date")

            # Validate number of people
            try:
                number_of_people = int(request.POST.get('number_of_people', 1))
                if number_of_people < 1:
                    raise ValidationError("Number of people must be at least 1")
                if number_of_people > 1000:
                    raise ValidationError("Number of people cannot exceed 1000")
            except ValueError:
                raise ValidationError("Please enter a valid number of people")

            # Get form data
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            nationality = request.POST.get('nationality', '').strip()
            special_requirements = request.POST.get('special_requirements', '').strip()

            # Validate required fields
            if not full_name:
                raise ValidationError("Full name is required")
            if not email:
                raise ValidationError("Email is required")
            if not phone:
                raise ValidationError("Phone number is required")
            if not nationality:
                raise ValidationError("Nationality is required")

            # Create new quote inquiry
            quote_inquiry = QuoteInquiry(
                tour=tour,
                full_name=full_name,
                email=email,
                phone=phone,
                nationality=nationality,
                preferred_date=preferred_date,
                number_of_people=number_of_people,
                special_requirements=special_requirements,
                status='pending'
            )

            # Validate the model
            quote_inquiry.full_clean()

            # Save the quote inquiry
            quote_inquiry.save()

            # Send confirmation emails
            try:
                # Customer email message
                customer_email = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Quote Request Received - Aronia Travel</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .quote-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="ARONIA" class="logo">
                        </div>

                        <div class="content">
                            <h2>Quote Request Received</h2>
                            <p>Dear {quote_inquiry.full_name},</p>

                            <p>Thank you for your interest in <strong>{tour.name}</strong>! We have received your quote request and our team will respond within 2-24 hours with a personalized quote.</p>

                            <div class="quote-details">
                                <h3>Your Quote Request Details:</h3>
                                <p><strong>Reference:</strong> {quote_inquiry.inquiry_reference}</p>
                                <p><strong>Tour:</strong> {tour.name}</p>
                                <p><strong>Preferred Date:</strong> {quote_inquiry.preferred_date}</p>
                                <p><strong>Duration:</strong> {tour.duration} days</p>
                                <p><strong>Number of People:</strong> {quote_inquiry.number_of_people}</p>
                                <p><strong>Nationality:</strong> {quote_inquiry.nationality}</p>
                                {f'<p><strong>Special Requirements:</strong> {quote_inquiry.special_requirements}</p>' if quote_inquiry.special_requirements else ''}
                            </div>

                            <p>Our travel experts will review your requirements and provide you with a detailed quote including:</p>
                            <ul>
                                <li>Competitive pricing based on your group size</li>
                                <li>Accommodation options</li>
                                <li>Transportation details</li>
                                <li>Meal arrangements</li>
                                <li>Activity inclusions</li>
                            </ul>

                            <p>If you have any urgent questions, please contact us with your reference number: <strong>{quote_inquiry.inquiry_reference}</strong></p>
                        </div>

                        <div class="footer">
                            <p>Best regards,<br>The ARONIA TRAVEL Team</p>
                            <p>© 2024 ARONIA. All rights reserved.</p>
                            <p>
                                <a href="tel:+254758355325">+254758355325</a> |
                                <a href="mailto:info@aroniatravel.com">info@aroniatravel.com</a>
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Admin email message
                admin_email = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>New Quote Inquiry • {tour.name}</title>
                    <style>
                        :root {{
                            --emerald: #0f463a;
                            --seafoam: #1c7a64;
                            --gold: #f7a934;
                            --mist: #f4f7f5;
                            --slate: #4d5a56;
                        }}
                        body {{
                            margin: 0;
                            padding: 0;
                            background: #e8efec;
                            font-family: "Segoe UI", "Inter", system-ui, sans-serif;
                            color: var(--slate);
                        }}
                        .shell {{
                            max-width: 660px;
                            margin: 0 auto;
                            padding: 32px 18px;
                        }}
                        .card {{
                            border-radius: 20px;
                            overflow: hidden;
                            background: #fff;
                            box-shadow: 0 25px 80px rgba(15, 70, 58, 0.12);
                        }}
                        .hero {{
                            text-align: center;
                            padding: 32px 24px 24px;
                            background: radial-gradient(circle at top, var(--seafoam), var(--emerald));
                            color: #fff;
                        }}
                        .hero img {{
                            width: 160px;
                            margin-bottom: 12px;
                        }}
                        h1 {{
                            margin: 10px 0 0;
                            font-size: 24px;
                            letter-spacing: .4px;
                        }}
                        .content {{
                            padding: 30px;
                        }}
                        .pill {{
                            display: inline-block;
                            background: rgba(247, 169, 52, 0.18);
                            color: var(--gold);
                            padding: 6px 16px;
                            border-radius: 999px;
                            font-size: 11px;
                            letter-spacing: 1px;
                            text-transform: uppercase;
                            margin-bottom: 18px;
                        }}
                        .info-block {{
                            background: var(--mist);
                            border-radius: 16px;
                            padding: 22px;
                            margin-bottom: 18px;
                        }}
                        .info-block h3 {{
                            margin-top: 0;
                            color: var(--emerald);
                            letter-spacing: .5px;
                        }}
                        .info-item {{
                            margin: 6px 0;
                        }}
                        .actions {{
                            border-radius: 16px;
                            padding: 22px;
                            border: 1px solid rgba(15, 70, 58, 0.15);
                            margin: 22px 0;
                        }}
                        .actions h3 {{
                            margin-top: 0;
                        }}
                        .actions ol {{
                            padding-left: 18px;
                            margin: 12px 0 0;
                        }}
                        .cta {{
                            display: inline-block;
                            margin-top: 22px;
                            padding: 14px 28px;
                            border-radius: 999px;
                            background: linear-gradient(120deg, var(--gold), #ffd885);
                            color: #fff;
                            text-decoration: none;
                            font-weight: 600;
                            letter-spacing: .4px;
                        }}
                        .footer {{
                            text-align: center;
                            background: var(--emerald);
                            color: rgba(255,255,255,.75);
                            padding: 26px;
                            font-size: 13px;
                        }}
                        .footer a {{
                            color: var(--gold);
                            text-decoration: none;
                        }}
                    </style>
                </head>
                <body>
                    <div class="shell">
                        <div class="card">
                            <div class="hero">
                                <img src="https://www.aroniatravel.com/static/assets4/img/logo/logo1.png" alt="Aronia Travel">
                                <h1>New Quote Inquiry</h1>
                                <p>{tour.name}</p>
                            </div>
                            <div class="content">
                                <span class="pill">Immediate follow-up</span>
                                <p>We’ve just received a premium guest inquiry. Kindly guide them with the Aronia experience in mind.</p>

                                <div class="info-block">
                                    <h3>Guest Profile</h3>
                                    <p class="info-item"><strong>Name:</strong> {quote_inquiry.full_name}</p>
                                    <p class="info-item"><strong>Email:</strong> {quote_inquiry.email}</p>
                                    <p class="info-item"><strong>Phone:</strong> {quote_inquiry.phone}</p>
                                    <p class="info-item"><strong>Nationality:</strong> {quote_inquiry.nationality}</p>
                                </div>

                                <div class="info-block">
                                    <h3>Journey Brief</h3>
                                    <p class="info-item"><strong>Reference:</strong> {quote_inquiry.inquiry_reference}</p>
                                    <p class="info-item"><strong>Preferred Tour:</strong> {tour.name}</p>
                                    <p class="info-item"><strong>Preferred Date:</strong> {quote_inquiry.preferred_date}</p>
                                    <p class="info-item"><strong>Duration:</strong> {tour.duration} days</p>
                                    <p class="info-item"><strong>Guests:</strong> {quote_inquiry.number_of_people}</p>
                                    <p class="info-item"><strong>Submitted:</strong> {quote_inquiry.inquiry_date.strftime('%Y-%m-%d %H:%M')}</p>
                                    <p class="info-item"><strong>Notes:</strong> {quote_inquiry.special_requirements if quote_inquiry.special_requirements else 'None provided'}</p>
                                </div>

                                <div class="actions">
                                    <h3>What to do now</h3>
                                    <ol>
                                        <li>Please respond to this inquiry within 2-24 hours to maintain our service standards..</li>
                                        <li>Craft a tailored quote (rates, accommodation, experiences) that fits their brief.</li>
                                    </ol>
                                </div>

                                <a class="cta" href="https://www.aroniatravel.com/admin/dede/quoteinquiry/{quote_inquiry.id}/change/">Open inquiry in admin</a>
                                <p style="margin-top:18px;">Need destination support? Loop in the product desk on Slack #journey-design.</p>
                            </div>
                            <div class="footer">
                                <p>Aronia Travel • Hotline <a href="tel:+254758355325">+254 758 355 325</a></p>
                                <p><a href="mailto:info@aroniatravel.com">info@aroniatravel.com</a> • www.aroniatravel.com</p>
                                <p>Aronia Travel. Designed for world-class journeys.</p>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Send customer confirmation email
                customer_success = send_email_via_mailtrap(
                    subject=f"Quote Request Received - Aronia Travel",
                    html_message=customer_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[quote_inquiry.email]
                )

                # Send admin notification email
                admin_success = send_email_via_mailtrap(
                    subject=f"New Quote Inquiry - {tour.name}",
                    html_message=admin_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["info@aroniatravel.com"]
                )

                if customer_success and admin_success:
                    print(f"SUCCESSFULLY SENT QUOTE EMAILS to {quote_inquiry.email} and info@aroniatravel.com for inquiry {quote_inquiry.inquiry_reference}")
                else:
                    print(f"Quote email sending partially failed for inquiry {quote_inquiry.inquiry_reference}")
            except Exception as e:
                # Log the error but don't stop the quote inquiry process
                print(f"Quote email sending failed: {str(e)}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {str(e)}")

            messages.success(request, 'Quote request submitted successfully! We will respond within 2-24 hours.')
            return redirect('aronia:tour_detail', tour_slug=tour_slug)

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'There was an error processing your quote request. Please try again.')
            print(f"Quote inquiry error: {str(e)}")  # For debugging

        # If there's an error, redirect back to tour detail with error message
        return redirect('aronia:tour_detail', tour_slug=tour_slug)

    # For GET requests, redirect to tour detail
    return redirect('aronia:tour_detail', tour_slug=tour_slug)


def booking_confirmation(request, booking_reference):
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    return render(request, 'users/aronia/booking-confirmation.html', {'booking': booking})
