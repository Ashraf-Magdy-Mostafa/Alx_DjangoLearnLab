"""advanced_project URL Configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ✅ include API app urls
    path('api/', include('api.urls')),
]
