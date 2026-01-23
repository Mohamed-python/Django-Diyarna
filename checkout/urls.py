
from django.contrib import admin
from django.urls import path, include
from . import views
# from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path("payment/", views.start_payment, name="start_payment"),
    # path('start_payment/', views.start_payment, name='start_payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_completed/', views.order_completed, name='order_completed'),
    path('success/', views.donations_success, name='donations_success'),
    # path('kashier_webhook/', views.kashier_webhook, name='kashier_webhook'),

]

