from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderList.as_view(), name="list"),
    path("<uuid:order_key>/detail/", views.OrderDetail.as_view(), name="detail"),
    
    path("checkout/", views.checkout, name="checkout"),
    path("place_order/", views.place_order, name="place-order")
]