

from .views import chat_api
from django.urls import path

urlpatterns = [
    path("api/", chat_api, name="chat_api"),
]