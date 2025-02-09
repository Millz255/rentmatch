from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from django import forms
from .models import Property, PropertyImage, User, UserProfile, Profile
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message...'})
        }

class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'location']



class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

PropertyImageFormSet = modelformset_factory(
    PropertyImage,
    form=PropertyImageForm,
    extra=4,
    max_num=10
)

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    town = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Town'}))
    street_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Street Name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'city', 'town', 'street_name', 'password1', 'password2', 'is_seller', 'is_buyer']

    def clean(self):
        cleaned_data = super().clean()
        print(self.errors)  # This will print any form errors to the console
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'first_name', 'last_name', 'email', 'phone', 'address', 'country', 'city', 'dob']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'first_name', 'last_name', 'email', 'phone', 'address', 'country', 'city', 'dob']