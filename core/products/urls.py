from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.ProductList.as_view(), name="product-list"),
    path('<int:pk>/<slug:slug>/', views.ProductDetail.as_view(), name="product-detail"),
    
    path("category/<slug:slug>/", views.CategoryProductList.as_view(), name="category-list")
]
