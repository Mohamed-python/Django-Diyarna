from django.urls import path
from .views import login_view, logout_get, dashboard
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

app_name = 'accounts'  # مهم جدًا

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_get, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # صفحة تغيير كلمة السر
    path('password_change/', auth_views.PasswordChangeView.as_view(
        # template_name='password_change/password_change_form.html',
        # success_url='/password_change/done/'
    ), name='password_change'),

    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
        ),
        name='password_change_done'
    ),

    path('dashboard/', dashboard, name='dashboard'),


]
