from django.urls import path

from storefront import views

app_name = "storefront"

urlpatterns = [
    path("", views.front_view, name="front")
]