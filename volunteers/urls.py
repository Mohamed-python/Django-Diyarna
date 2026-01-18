from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteer_create, name='volunteer_create'),
    path('success/', views.volunteer_success, name='volunteer_success'),
]
