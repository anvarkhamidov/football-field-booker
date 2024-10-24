from django.urls import path

from .views import ObtainAuthToken, UserRegistrationView

urlpatterns = [
    path("/auth", ObtainAuthToken.as_view(), name="user-auth"),
    path("/register", UserRegistrationView.as_view(), name="user-register"),
]
