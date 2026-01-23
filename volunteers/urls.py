from django.urls import path
from .views import volunteer_create, volunteer_success


# app_name = 'volunteers'  # مهم جدًا

urlpatterns = [
    path('', volunteer_create, name='volunteer'),
    path('success/', volunteer_success, name='volunteer_success'),
]
