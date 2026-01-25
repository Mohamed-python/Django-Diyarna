from django.urls import path, include
from . import views

# app_name = 'products'  # مهم جدًا



urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.donate_product, name='donate_product'),

]
