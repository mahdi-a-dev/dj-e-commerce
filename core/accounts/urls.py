from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    # user authentication
    path("register/", views.account_register, name="register"),
    path("login/", views.account_login, name="login"),
    path("logout/", views.account_logout, name="logout"),
]