
from django.contrib import admin
from django.urls import path, include
from . import views
from home.views import home
from django.urls import re_path

app_name = 'donations'  # مهم جدًا

urlpatterns = [
    path('', views.donations_list, name='donations_list'),

    # path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    re_path(r'^(?P<slug>[-\w\u0600-\u06FF]+)/$', views.case_detail, name='case_detail'),


    # path('payment/<int:donation_id>/', views.payment, name='payment'),
    ####################
]
