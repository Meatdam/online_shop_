from django.urls import path
from django.contrib.auth.decorators import login_required
from users.views import UserLoginView, UserRegistrationCreateView, ProfileUpdateView, logaut, EmailVerificationView, \
    EmailView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationCreateView.as_view(), name='registration'),
    path('profile/<int:pk>/', login_required(ProfileUpdateView.as_view()), name='profile'),
    path('logout/', logaut, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('email_ver/', EmailView.as_view(), name='email_ver'),
]
