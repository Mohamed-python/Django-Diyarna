
from django.contrib import admin
from django.urls import path, include
from . import views
from home.views import home

app_name = 'donations'  # مهم جدًا

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('donate/<int:case_id>/', views.donate, name='donate'),
    path('payment/<int:donation_id>/', views.payment, name='payment'),
    path('donations/', views.donations_list, name='donations_list'),
    ####################
    path('order_completed/', views.order_completed, name='order_completed'),
    path('success/', views.donations_success, name='donations_success'),

]
