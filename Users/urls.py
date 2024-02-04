from django.urls import path, include
from Users import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.regPage,name='register'),
    path('password_reset/', PasswordResetView.as_view(template_name='Users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='Users/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='Users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='Users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/',views.userProfile,name='profile'),
    path('profile/edit_profile',views.editProfile,name='editprofile'),
    
]