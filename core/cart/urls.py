from django.urls import path
from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("<int:product_pk>/add/", views.AddItem.as_view(), name="add"),
    path("<int:product_pk>/remove/", views.RemoveItem.as_view(), name="remove"),
    path("<int:pk>/update_quantity/", views.UpdateQuantity.as_view(), name="update-quantity")
]