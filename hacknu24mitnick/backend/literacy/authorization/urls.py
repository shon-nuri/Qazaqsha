from django.urls import path

from authorization.views import *

app_name = "authorization"

urlpatterns = [
    path("login", UserLoginView.as_view(), name="login"),
    path("register", register, name="register"),
    path("logout", logout, name="logout")
]
