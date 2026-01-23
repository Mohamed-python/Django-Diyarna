"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from accounts.views import dashboard, logout_get, signup
from django.contrib.auth import views as auth_views
from checkout.views import kashier_webhook

urlpatterns = [
    path("kashier_webhook/", kashier_webhook, name="kashier_webhook"),

    path('i18n/', include('django.conf.urls.i18n')),  # تغيير اللغة
]

urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('', include('donations.urls')),
    path('', include('checkout.urls')), #checkout


    ##########################################
    path('accounts/', include('accounts.urls')),  # لو عندك app login/signup
    path('products/', include('products.urls')),
    path('donations/', include('donations.urls')),
    path('news/', include('news.urls')),
    path('volunteer/', include('volunteers.urls')),
    path('admin/', admin.site.urls),
    path('profile/', include('user_profile.urls')),  # /profile/

    ###############################################
    path('signup/',signup ,name='signup'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_get, name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
