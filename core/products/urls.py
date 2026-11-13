from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.ProductList.as_view(), name="list"),
    path('<int:pk>/<slug:slug>/', views.ProductDetail.as_view(), name="detail"),
    
    path("category-<slug:slug>/", views.CategoryList.as_view(), name="category-list")
]
