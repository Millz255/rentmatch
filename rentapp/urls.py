from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views  # Import all views
from .views import UserProfileView, base_view, contact_seller  # Import UserProfileView if used separately

urlpatterns = [
    # Home URL
    path('', views.home, name='home'),  # Home page view

    # Property URLs
    path('properties/', views.property_list, name='property_list'),  # Property list view
    path('contact_seller/', views.contact_seller, name='contact_seller'),
    path('properties/<int:owner_id>/contact_seller/', views.contact_seller, name='contact_seller'),
    path('properties/add/', views.add_property, name='add_property'),  # Add property view
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),  # Property detail view
    path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),  # Edit property view
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),  # Delete property view
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/confirm-email/<str:activation_key>/', views.confirm_email, name='confirm_email'),


    # Profile URLs
    path('profile/', views.user_profile, name='profile'),  # User profile view
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit profile view

    path('accounts/password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('messages/', views.message_box, name='message_box'),

    # Admin and Accounts URLs (Django Allauth)
    path('login/', include('allauth.urls')),
    path('accounts/', include('allauth.urls')),  # Django Allauth URLs

    path('', base_view, name='home'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
