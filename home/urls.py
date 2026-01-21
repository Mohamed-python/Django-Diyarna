from django.urls import path, include
from . import views
from donations.views import donations_list

app_name = 'home'  # مهم جدًا



urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', include('donations.urls')), # الدفع
    path('donations/', donations_list, name='donations'),
    # path('<int:id>', views.news_detail),
    path('about/', views.about, name='about'),
    path('board/', views.board, name='board'),
    path('test/', views.test, name='test'),
]
