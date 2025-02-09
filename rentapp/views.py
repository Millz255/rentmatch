from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views import View
from .models import Profile, Property, PropertyImage, UserProfile
from .forms import ProfileForm, CustomUserCreationForm, PropertyForm, PropertyImageFormSet, UserProfileForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from allauth.account.utils import complete_signup
from django.contrib import messages
from .models import Message, Notification
from .forms import MessageForm
from pyfcm import FCMNotification


# Define the home view
def home(request):
    properties = Property.objects.all()  # Retrieve all properties
    return render(request, 'property_list.html', {'properties': properties})  # Assuming you have a home.html template


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('property_list')
        else:
            messages.error(request, form.errors)  # Display form errors as messages
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def confirm_email(request, activation_key):
    from allauth.account.models import EmailAddress
    email_address = EmailAddress.objects.filter(activation_key=activation_key).first()

    if email_address and not email_address.verified:
        email_address.verified = True
        email_address.save()
        return render(request, 'account/email_confirmed.html')

    messages.error(request, 'Invalid or expired activation key.')
    return redirect('account_login')  # Redirect to login page or elsewhere


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'user_profile.html'

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(instance=user_profile)
        user_properties = Property.objects.filter(seller=request.user)

        context = {
            'profile_form': profile_form,
            'user_profile': user_profile,
            'user_properties': user_properties
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_profile')

        user_properties = Property.objects.filter(seller=request.user)
        context = {
            'profile_form': profile_form,
            'user_profile': user_profile,
            'user_properties': user_properties
        }
        return render(request, self.template_name, context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('property_list')  # Redirect to the home page or wherever you want
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('account_login')  # Redirect to login page or elsewhere


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        image_formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and image_formset.is_valid():
            # Save the property instance
            property_instance = form.save(commit=False)
            property_instance.owner = request.user  # Set owner to the logged-in user
            property_instance.seller = request.user  # Set seller to the logged-in user
            property_instance.save()

            # Save the images related to this property
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image_instance = image_form.save(commit=False)
                    image_instance.property = property_instance  # Link image to the property
                    image_instance.save()

            return redirect('property_list')  # Redirect to the property list page after saving
    else:
        form = PropertyForm()
        image_formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'add_property.html', {'form': form, 'image_formset': image_formset})



@login_required
def edit_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_instance)
        if form.is_valid():
            form.save()
            return redirect('property_detail', pk=property_instance.pk)
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'edit_property.html', {'form': form})


@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, seller=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('profile')

    return render(request, 'confirm_delete.html', {'property': property})


def property_list(request):
    properties = Property.objects.prefetch_related(
        Prefetch('images_list', queryset=PropertyImage.objects.all())

    )

    unread_notifications_count = 0

    query = request.GET.get('q', '').strip()  # Get and strip any leading/trailing spaces
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    currency = request.GET.get('currency', 'TZS')

    if query:
        properties = properties.filter(location__icontains=query)

    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            if currency != 'TZS':
                min_price = convert_currency(min_price, currency)
                max_price = convert_currency(max_price, currency)
            properties = properties.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            # Handle potential conversion errors
            pass

    context = {
        'properties': properties,
        'unread_notifications_count': unread_notifications_count,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'currency': currency,
    }
    return render(request, 'property_list.html', context)



def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    images = property.images_list.all()
    context = {
        'property': property,
        'images': images,
    }
    return render(request, 'property_detail.html', context)


# Define the currency conversion function
def convert_currency(amount, currency):
    # Sample conversion rates, where 1 TZS is the base currency
    conversion_rates = {
        'USD': 0.00043,  # Example rate: 1 TZS = 0.00043 USD
        'EUR': 0.00040,  # Example rate: 1 TZS = 0.00040 EUR
        'GBP': 0.00035,  # Example rate: 1 TZS = 0.00035 GBP
        'TZS': 1  # Base rate: 1 TZS = 1 TZS
    }

    # Get the conversion rate; default to TZS if currency not found
    rate = conversion_rates.get(currency, 1)

    # Convert the amount
    converted_amount = amount * rate
    return converted_amount


@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user_properties = Property.objects.filter(owner=request.user)
    
    profile = request.user.profile  # Adjust as needed
    

    return render(request, 'profile.html', {
        'profile': profile,
        'user_properties': user_properties,
    })


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(pk=recipient_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=recipient, content=content)
        return redirect('property_list')  # Redirect to the property list or another appropriate page

    return render(request, 'send_message.html', {'recipient': recipient})

@login_required
def message_list(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messages/message_list.html', {'messages': messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)

    # Mark the message as read
    message.is_read = True
    message.save()

    return render(request, 'messages/message_detail.html', {'message': message})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

def base_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Fetch unread notifications count
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
        # Fetch all unread notifications for rendering
        unread_notifications = request.user.notifications.filter(is_read=False)
    else:
        unread_notifications_count = 0
        unread_notifications = []

    context = {
        'unread_notifications_count': unread_notifications_count,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'base.html', context)

@login_required
def contact_seller(request, owner_id):
    try:
        # Try to fetch the seller profile
        seller_profile = UserProfile.objects.get(user__id=owner_id)
    except UserProfile.DoesNotExist:
        # Handle the case where the seller does not exist
        return render(request, 'message_box.html', {'error': 'The seller you are trying to contact does not exist.'})

    # Handle POST request to send a message
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            Message.objects.create(
                sender=request.user,
                receiver=seller_profile.user,
                content=message_content
            )
            # Redirect the user to the profile page after sending the message
            return redirect('profile')  # Change this to any URL where users can see sent messages, etc.

    # Render a template for contacting the seller (replace 'contact_seller.html' with your actual form template)
    return render(request, 'contact_seller.html', {'seller': seller_profile})

def profile_view(request, sent_messages=None):
    profile = UserProfile.objects.get(user=request.user)
    messages = Message.objects.filter(receiver=request.user)

    context = {
        'profile': profile,
        'messages': sent_messages,

    }

    return render(request, 'profile.html', context)

@login_required
def message_box(request):
    user = request.user
    sent_messages = Message.objects.filter(sender=user)
    received_messages = Message.objects.filter(receiver=user)
    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages
    }
    return render(request, 'message_box.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_box')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})