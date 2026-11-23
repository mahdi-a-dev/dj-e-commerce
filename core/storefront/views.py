from django.shortcuts import render
from products.models import Product, Category
from django.utils import timezone
    

def front_view(request):
    """
    Front View contains leatest products and discounts and also main categories.
    """
    # leatest products
    products = Product.objects.get_actives()[0:5]

    # leatest discounts
    now = timezone.localdate()
    latest_discounted_products = Product.objects.get_actives().filter(
        discount__is_active=True,
        discount__start_date__lte=now,
        discount__end_date__gt=now,
        stock_quantity__gte=1,
    ).select_related("discount")[0:5]
    
    # main categories
    main_categories = Category.objects.filter(parent__isnull=True)
    
    context = {
        "products": products,
        "latest_discounted_products": latest_discounted_products,
        "main_categories": main_categories
    }
    return render(request, "front/front.html", context)
