
from django.contrib import admin
from django.urls import path, include
from . import views
# from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    # path("payment/", views.start_payment, name="start_payment"),
    # path('checkout/', views.checkout, name='checkout'),
    # path('order_completed/', views.order_completed, name='order_completed'),
    # path('success/', views.donations_success, name='donations_success'),






    ######################################################
    path("payment/", views.start_payment, name="start_payment"),
    path('payment/callback/', views.kashier_callback, name='kashier_callback'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('payment_success', views.payment_success, name='payment_success'),


]

