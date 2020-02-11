from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from students.views import register
from django_otp.admin import OTPAdminSite


admin.site.site_title = "Cal Foscari"
admin.site.site_header = "Ca Foscari Calendar"
admin.site.index_title = "Calendar"
admin.site.__class__ = OTPAdminSite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', include('coursesCalendars.urls'))
]
