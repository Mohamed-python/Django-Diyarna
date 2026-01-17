from django.urls import path, include
from . import views
from donations.views import donations_list



urlpatterns = [
    path('', views.home),
    path('donations/', donations_list, name='donations'),
    # path('<int:id>', views.news_detail),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),


]
