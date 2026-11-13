from django.shortcuts import get_object_or_404
from products.models import Product, Category
from products.forms import ProductSortForm
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView
)

# ------------------- Product -------------------

class ProductList(ListView):
    """
    Display all active Products
    Ordering product by newest, price_asc, price_desc
    Paginated by 9 product.
    """
    context_object_name = "products"
    paginate_by = 9
    template_name = "products/product_list.html"
    ordering_options = {
        "newest": "-created",
        "price_asc": "price",
        "price_desc": "-price"
    }
    
    def get_queryset(self):
        search_query = self.request.GET.get("q")
                
        products = Product.active.all()
            
        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        self.sort_form = ProductSortForm(self.request.GET)
        
        
        if self.sort_form.is_valid():
            ordering = (
                self.sort_form.cleaned_data.get("ordering") or "newest"
            )
        
        products = products.order_by(self.ordering_options.get(ordering, "-created"))
        
        return products
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_form"] = self.sort_form
        context["count"] = self.get_queryset().count()

        return context


class ProductDetail(DetailView):
    """
    Display a single Product details
    """ 
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    

# ------------------- category -------------------

class CategoryList(ListView):
    """
    Display all active Products for a category
    Ordering product by newest, price_asc, price_desc

    """
    context_object_name = "products"
    paginate_by = 9
    template_name = "products/category/category_list.html"
    ordering_options = {
        "newest": "-created",
        "price_asc": "price",
        "price_desc": "-price"
    }
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        products = self.category.products.filter(is_active=True)
        
        self.sort_form = ProductSortForm(self.request.GET)
        
        if self.sort_form.is_valid():
            ordering = (
                self.sort_form.cleaned_data.get("ordering") or "newest"
            )
        
        products = products.order_by(self.ordering_options.get(ordering, "-created"))
        
        return products
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.get_queryset()
        
        context["category"] = self.category
        context["category_name"] = self.category.name
        context["sort_form"] = self.sort_form
        context["count"] = query.count()
        
        return context