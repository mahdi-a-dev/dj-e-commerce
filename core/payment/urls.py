from django.urls import path

from payment import views

app_name = "payment"

urlpatterns = [
    path("<uuid:order_key>/payment_page/", views.payment_page, name="page")
]