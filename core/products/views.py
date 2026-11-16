from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from products.forms import ProductSortForm
from products.models import Category, Product


class ProductList(ListView):
    """
    Display all active Products
    Paginated by 30 object
    Ordering product by newest, price_asc, price_desc
    """
    context_object_name = "products"
    paginate_by = 30
    template_name = "products/product_list.html"

    def get_queryset(self):
        # active products
        products = Product.objects.get_actives()
        
        # search query
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        self.sort_form = ProductSortForm(self.request.GET)
        
        if self.sort_form.is_valid():
            ordering = (
                self.sort_form.cleaned_data.get("ordering") or "all"
            )
            
            if ordering == "all":
                return products.order_by("-created")
            
            # only available products
            products = products.filter(stock_quantity__gt=0)
        
        ordering_options = {
            "newest": "-created",
            "price_asc": "price",
            "price_desc": "-price"
        }
        
        return products.order_by(ordering_options.get(ordering))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sort_form"] = self.sort_form
        context["number_of_items"] = self.object_list.count()

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


class CategoryList(ProductList):
    """
    Inherited ProductList view
    Display all active Products for a category
    """
    def get_queryset(self):
        products = super().get_queryset()
        
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        
        return products.filter(category=self.category)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["category"] = self.category
        context["sort_form"] = self.sort_form
        context["number_of_items"] = self.object_list.count()
        
        return context