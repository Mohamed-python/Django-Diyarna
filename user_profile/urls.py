from django.urls import path
from .views import profile_view, profile_edit



app_name = 'user_profile'

urlpatterns = [
    path('', profile_view, name='profile'),  # /profile/
    path('edit/', profile_edit, name='edit'), # /profile/edit/
]
