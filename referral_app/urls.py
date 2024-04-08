from django.urls import path
from .views import *


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("user-details/", UserDetailsView.as_view(), name="user-details"),
    path("referrals/",UserReferralView.as_view(), name="referrals"),
]
