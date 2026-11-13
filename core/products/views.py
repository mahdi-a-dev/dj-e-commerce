from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Product, Category
from django.views.generic import (
    ListView,
    DetailView
)


class ProductList(ListView):
    """
    Display all active Products
    """
    context_object_name = "products"
    paginate_by = 9
    template_name = "products/product_list.html"
    
    def get_queryset(self):
        search_query = self.request.GET.get("s")
        
        products = Product.active.all()
        
        if search_query:
            return products.filter(
                Q(title__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        return products
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        
        return context


class ProductDetail(DetailView):
    """
    Display a single Product details
    """ 
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_superuser:
            return queryset
        
        if user.is_authenticated:
            return queryset.filter(
                Q(is_active=True))
            
        return queryset.filter(is_active=True)


# ------------------- category -------------------

class CategoryList(ListView):
    """
    Display all active Products for a category
    """
    context_object_name = "products"
    paginate_by = 9
    template_name = "products/category/category_list.html"
    
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return category.products.filter(is_active=True)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.get_queryset()
        
        context["category"] = Category.objects.get(slug=self.kwargs["slug"])
        context["product_count"] = query.count()
        
        return context