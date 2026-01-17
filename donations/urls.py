
from django.contrib import admin
from django.urls import path, include
from .views import donate, payment, donations_list

from home.views import home


urlpatterns = [
    # path('', home, name='home'),
    path('donate/<int:case_id>/', donate, name='donate'),
    path('payment/<int:donation_id>/', payment, name='payment'),
    path('donations/', donations_list, name='donations_list'),


]
