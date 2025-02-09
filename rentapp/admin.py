from django.contrib import admin
from .models import Property, PropertyImage, UserProfile

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'seller')
    inlines = [PropertyImageInline]
    search_fields = ('title', 'location')
    list_filter = ('location', 'price')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__title',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'address', 'country', 'city', 'dob')
    search_fields = ('user__username', 'address', 'contact_number')

