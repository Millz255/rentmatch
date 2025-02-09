from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rentapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentapp.urls')),  # Make sure this matches your app's name

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
