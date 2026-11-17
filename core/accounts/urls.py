from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    # registration
    path("register/", views.account_register, name="register"),
    path("login/", views.account_login, name="login"),
    path("logout/", views.account_logout, name="logout"),
    
    # profile page
    path("profile/", views.ProfileView.as_view(), name="profile"),
    
    path("profile/edit", views.EditProfile.as_view(), name="edit-profile"),
    
    # addresses CRUD
    path("addresses/", views.UserAddresses.as_view(), name="addresses"),
    path("addresses/add/", views.AddAddress.as_view(), name="add"),
    path("addresses/<int:pk>/edit/", views.EditAddress.as_view(), name="edit"),
    path("addresses/<int:pk>/delete/", views.DeleteAddress.as_view(), name="delete")
]