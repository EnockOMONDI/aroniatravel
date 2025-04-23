import logging
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
import os
import smtplib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserBookings


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from adminside.models import *
from users.models import *
from .forms import UserRegisterForm
from .forms import UserBookingsForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.mail import send_mail 
from django.conf import settings
# Create your views here.

from tours_travels import mail as mail_f
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError 
from .utils import generate_token
from django.views import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import UserRegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import send_booking_confirmation_email
from events.views import EventListView
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.contrib.auth import login
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import User, Profile
import json
from django.views import View
from django.utils.http import urlsafe_base64_decode





# logger = logging.getLogger(__name__)

# users/views.py
# @csrf_protect
# def google_one_tap_login(request):
#     if request.method == 'POST':
#         try:
#             logger.debug('Received Google One Tap request')
#             logger.debug(f'Request body: {request.body}')
            
#             data = json.loads(request.body)
#             credential = data.get('credential')
            
#             if not credential:
#                 logger.error('No credential provided in request')
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'No credential provided'
#                 })

#             try:
#                 idinfo = id_token.verify_oauth2_token(
#                     credential,
#                     requests.Request(),
#                     settings.GOOGLE_CLIENT_ID
#                 )
#                 logger.debug('Token verified successfully')
                
#                 # Get user info from the token
#                 email = idinfo['email']
#                 first_name = idinfo.get('given_name', '')
#                 last_name = idinfo.get('family_name', '')
                
#                 # Check if user exists
#                 try:
#                     user = User.objects.get(email=email)
#                     logger.debug(f'Existing user found: {email}')
#                 except User.DoesNotExist:
#                     # Create new user
#                     logger.debug(f'Creating new user for: {email}')
#                     user = User.objects.create_user(
#                         username=email,  # Using email as username
#                         email=email,
#                         first_name=first_name,
#                         last_name=last_name,
#                         is_active=True  # Google users are pre-verified
#                     )
#                     # Create profile for new user
#                     Profile.objects.create(user=user)
#                     logger.debug(f'Created new user profile for: {email}')

#                 # Log the user in
#                 login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                 logger.debug(f'User logged in successfully: {email}')

#                 # Generate absolute redirect URL
#                 redirect_url = request.build_absolute_uri(reverse('dede:home'))
#                 logger.debug(f'Generated redirect URL: {redirect_url}')

#                 return JsonResponse({
#                     'success': True,
#                     'redirect_url': redirect_url,
#                     'message': f'Welcome {first_name}! Login successful.'
#                 })

#             except ValueError as e:
#                 logger.error(f'Token verification failed: {str(e)}')
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'Invalid token'
#                 })

#         except json.JSONDecodeError as e:
#             logger.error(f'JSON decode error: {str(e)}')
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Invalid JSON data'
#             })
#         except Exception as e:
#             logger.error(f'Unexpected error: {str(e)}')
#             return JsonResponse({
#                 'success': False,
#                 'error': str(e)
#             })

#     return JsonResponse({
#         'success': False,
#         'error': 'Invalid request method'
#     })

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)  # Save the user object in memory
#             user.is_active = False

#             # Save the user object to the database only when the form is valid
#             user.save()

#             current_site = get_current_site(request)
#             uid64 = urlsafe_base64_encode(force_bytes(user.pk))
#             token = PasswordResetTokenGenerator().make_token(user)
#             activation_link = f'http://{current_site.domain}/users/activate/{uid64}/{token}/'

#             mail_f.verification_mail(activation_link, user)

#             # Store username and email in session
#             request.session['username'] = form.cleaned_data['username']
#             request.session['email'] = form.cleaned_data['email']

#             # Redirect to the success message page
#             return redirect('users:success')

#     else:
#         form = UserRegisterForm()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            # Update the activation link to use the users namespace
            activation_link = f'http://{current_site.domain}/users/activate/{uid64}/{token}/'

            # Send verification email
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                
                msg = MIMEMultipart('alternative')
                msg['From'] = "ARONIA TRAVEL <aroniatravelke@gmail.com>"
                msg['To'] = user.email
                msg['Subject'] = "Activate Your ARONIA TRAVEL Account"
                
                html = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; }}
                        .content {{ padding: 20px; }}
                        .button {{ 
                            background-color: #007bff;
                            color: white;
                            padding: 10px 20px;
                            text-decoration: none;
                            border-radius: 5px;
                            display: inline-block;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Welcome to ARONIA TRAVEL!</h2>
                        </div>
                        <div class="content">
                            <p>Hi {user.username},</p>
                            <p>Thank you for registering with ARONIA TRAVEL. To activate your account, please click the button below:</p>
                            <p style="text-align: center;">
                                <a href="{activation_link}" class="button" style="color: white;">Activate Account</a>
                            </p>
                            <p>If the button doesn't work, copy and paste this link into your browser:</p>
                            <p>{activation_link}</p>
                            <p>This link will expire in 24 hours.</p>
                            <p>Best regards,<br>The ARONIA TRAVEL Team</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                msg.attach(MIMEText(html, 'html'))
                s.send_message(msg)
                s.quit()
                
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                messages.error(request, "There was an error sending the activation email. Please try again.")
                user.delete()  # Delete the user if email sending fails
                return render(request, 'users/register.html', {'form': form})

            # Store username and email in session
            request.session['username'] = form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']

            return redirect('users:success')

    else:
        form = UserRegisterForm()

    return render(request, 'users/dede/register.html', {'form': form})




def success(request):
    username = request.session.pop('username', None)
    email = request.session.pop('email', None)

    if username and email:
        success_message = f"Jambo! <b>{username}</b>, Your registration was successful! We've sent an email to <b>{email}</b>. Kindly click the received link to confirm and complete the registration. Remember to check your spam folder."
        messages.success(request, success_message)
    else:
        messages.error(request, 'Oops! Something is not right. Please start over.')

    return render(request, 'users/success.html')



@login_required
def profile(request):
    return render(request, 'users/dede/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:users-profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/dede/profile_edit.html', {'form': form})








def aboutus(request):
    
    return render(request, 'users/aboutus.html')



def corporate(request):
    
    return render(request, 'users/corporate.html')

def micepage(request):
    
    return render(request, 'users/mice.html')

def holidays(request):
    
    return render(request, 'users/holidays.html')

def contactus(request):
    
    return render(request, 'users/contactus.html')
		
def home(request):
	dests1 = Destination.objects.all()  # Retrieve all destinations from the database
	dests=Destination.objects.all()
	package1=Package.objects.all()
	packs=Package.objects.all().order_by('number_of_times_booked')
	nights=[]
	price=[]
	travel=[]
	
		
	destinations=zip(dests)

	for i in packs:
		nights.append(i.number_of_days-1)
		price.append(i.adult_price+i.accomodation.price_per_room)
		mode=i.travel.travelling_mode
		if(mode=="TN"):
			travel.append("Train")
		elif(mode=="FT"):
			travel.append("Flight")
		else:
			travel.append("Bus")
		

	
	packages=zip(packs,nights,price,travel)
	

	context={'dests':destinations,'dests1': dests1, 'package1':package1, 'packages':packages}
	print(packs)

	
	return render(request,'users/index.html',context)






def destination(request,id):
	id=id
	dest=Destination.objects.get(id=id)
	packs=dest.package_set.all()
	nights=[]
	price=[]
	travel=[]
	
	for i in packs:
		nights.append(i.number_of_days-1)
		price.append(i.adult_price+i.accomodation.price_per_room)
		mode=i.travel.travelling_mode
		if(mode=="TN"):
			travel.append("Train")
		elif(mode=="FT"):
			travel.append("Flight")
		else:
			travel.append("Bus")
	
	
	packages=zip(packs,nights,price,travel)




	context={'dest':dest,'packages':packages}
	
	return render(request,'users/destination.html',context)



def search(request):
	try:
		name=request.POST.get('search','')
		name=name.lstrip()
		name=name.rstrip()
		dest=Destination.objects.filter(city__icontains=name) | Destination.objects.filter(state__icontains=name) | Destination.objects.filter(city__icontains=name)	
		print(dest[0].id)
		return redirect('users-destination', id=dest[0].id)
	except:
		messages.error(request, 'No results found for your search request')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def all_packages(request):
    packages = Package.objects.all()
    return render(request, 'users/package_list.html', {'packages': packages})		

def detail_package(request, package_id):
    if request.user.is_authenticated:
        try:
            package = get_object_or_404(Package, id=package_id)
            package_name = package.package_name
            destination_name = package.destination.name
            booked = package.number_of_times_booked
            no_of_days = package.number_of_days
            destination_description = package.destination.dtn_description
            package_description = package.description

            # Travelling details
            travel_mode = package.travel.travelling_mode
            travel_price = package.travel.price_per_person

            # accomodation Details
            hotel_name = package.accomodation.hotel_name if package.accomodation else "N/A"
            hotel_description = package.accomodation.hotel_description
            price_per_room = package.accomodation.price_per_room

            # Inclusive
            inclusive = package.inclusive
            exclusive = package.exclusive

            # Itinerary
            itinerary = get_object_or_404(Itinerary, package=package)
            itinerary_description = itinerary.itinerarydescription_set.all() # list of itinerary days

            # Images
            package_image = package.Image

            context = {
                'package': package,
                'package_name': package_name,
                'destination_name': destination_name,
                'no_of_days': no_of_days,
                'destination_description': destination_description,
                'package_description': package_description,
                'travel_mode': travel_mode,
                'travel_price': travel_price,
                'hotel_name': hotel_name,
                'hotel_description': hotel_description,
                'price_per_room': price_per_room,
                'inclusive': inclusive,
                'exclusive': exclusive,
                'itinerary_description': itinerary_description,
                'package_image': package_image,
                'booked': booked  # Use the variable 'booked' here
            }
        except Package.DoesNotExist:
            raise Http404("Package does not exist.")
        except Itinerary.DoesNotExist:
            raise Http404("Itinerary does not exist.")
        except Exception as e:
            return HttpResponse(f"<h1>An error occurred in the database: {str(e)}</h1>")
    else:
        # Handle the case when the user is not authenticated
        return HttpResponse("<h1>You need to be logged in to view this page.</h1>")

    return render(request, 'users/packagedetail2.html', context)


 


@login_required
def bookings(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    form = UserBookingsForm(request.POST or None)
    context = {'form': form, 'package': package}

    if request.method == 'POST':
        if form.is_valid():
            print("Form is valid!")  # Debug print
            try:
                # Create the booking
                booking = UserBookings.objects.create(
                    user=request.user,
                    package=package,
                    full_name=form.cleaned_data['full_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    number_of_adults=form.cleaned_data['number_of_adults'],
                    number_of_children=form.cleaned_data.get('number_of_children', 0),
                    number_of_rooms=form.cleaned_data['number_of_rooms'],
                    include_travelling=form.cleaned_data['include_travelling'],
                )

                # Send email notification
                send_booking_email(booking)

                return redirect('users:users-booking-success', booking_id=booking.id)

            except Exception as e:
                print(f"Booking creation error: {e}")
                messages.error(request, f'Error creating booking: {e}')
        else:
            print("Form is NOT valid!")
            print(form.errors)
            messages.error(request, 'Please correct the form errors.')

    return render(request, 'users/UserBookingsForm.html', context)


def send_booking_email(booking):
    """Send an email notification about the new booking."""
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        # Email credentials
        sender_email = "aroniatravelke@gmail.com"
        password = "jzuy eqkw ovpu wcxv"

        s.login(sender_email, password)

        # Email content
        msg = MIMEMultipart()
        msg['From'] = "Novustell Travel"
        msg['To'] = "info@dedeexpeditions.com"
        msg['Subject'] = f"New Booking: {booking.full_name} for {booking.package.name}"

        message = f"""
        <p><strong>New Booking Alert</strong></p>
        <p><strong>Customer Name:</strong> {booking.full_name}</p>
        <p><strong>Phone Number:</strong> {booking.phone_number}</p>
        <p><strong>Package:</strong> {booking.package.name}</p>
        <p><strong>Adults:</strong> {booking.number_of_adults}</p>
        <p><strong>Children:</strong> {booking.number_of_children}</p>
        <p><strong>Rooms:</strong> {booking.number_of_rooms}</p>
        <p><strong>Include Travelling:</strong> {'Yes' if booking.include_travelling else 'No'}</p>
        """

        msg.attach(MIMEText(message, 'html'))

        # Send the email
        s.send_message(msg)
        s.quit()
        print("Booking email sent successfully!")

    except Exception as e:
        print(f"Error sending booking email: {e}")

def booking_success(request, booking_id):
    booking = get_object_or_404(UserBookings, id=booking_id)
    return render(request, 'users/booking_success.html', {'booking': booking})



def send_mice_email(request):
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        event_type = request.POST.get('event_type')
        attendees = request.POST.get('attendees')
        event_details = request.POST.get('event_details')

        # Compose email message
        subject = f'New MICE Inquiry from {company_name}'
        message = f"""
        New MICE Event Request Details:
        
        Company Name: {company_name}
        Contact Person: {contact_person}
        Email: {email}
        Phone: {phone}
        Event Type: {event_type}
        Expected Attendees: {attendees}
        
        Event Details:
        {event_details}
        """

        try:
            # Send email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['info@novustelltravel.com'],
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your request has been submitted successfully. We will contact you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your request. Please try again later.')
            
        return redirect('users:homepage')

    return redirect('users:micepage')


class ActivateAccountView(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(f"Activation error: {str(e)}")  # For debugging
            user = None

        if user is not None and generate_token.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been activated successfully! You can now log in.')
                return redirect('users:users-login')
            else:
                messages.info(request, 'Your account is already activated. You can log in.')
        else:
            return redirect('users:activation_failed')
