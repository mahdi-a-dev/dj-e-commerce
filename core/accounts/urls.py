from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.account_register, name="register"),
    path("login/", views.account_login, name="login"),
    path("logout/", views.account_logout, name="logout"),
    
    path("profile/", views.ProfileView.as_view(), name="profile"),
    
    path("personal/edit", views.EditPersonal.as_view(), name="edit-personal"),
    path("personal/edit/email/", views.EditEmail.as_view(), name="edit-email"),
    
    path("addresses/", views.UserAddresses.as_view(), name="addresses"),
    path("addresses/add/", views.AddAddress.as_view(), name="add"),
    path("addresses/<int:pk>/edit/", views.EditAddress.as_view(), name="edit"),
    path("addresses/<int:pk>/delete/", views.DeleteAddress.as_view(), name="delete")
]