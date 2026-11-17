from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, ListView
from accounts.models import Address
from orders import services
from django.views.decorators.http import require_POST

from orders.models import Order


class OrderList(LoginRequiredMixin, ListView):
    """
    List of user orders
    """
    template_name = "orders/list.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        return self.request.user.orders.all()
    

class OrderDetail(LoginRequiredMixin, DetailView):
    """
    Order details, contains user info, address and products details
    """
    model = Order
    template_name = "orders/detail.html"
    
    def get_object(self):
        # order page find by order_key
        return get_object_or_404(Order, order_key=self.kwargs["order_key"])
        
    def get_queryset(self):  
        return self.request.user.orders.all()

@login_required
def checkout(request):
    """
    This view show the cartItems details
    calculate the subtotal, discount_total and total price
    """
    user = request.user
    profile = user.profile
    addresses = user.addresses.all()
    
    cart = services.get_user_cart(user)
    
    subtotal = Decimal("0")
    discount_total = Decimal("0")
    
    number_of_items = 0
    
    items = cart.items.select_related("product")
    for item in items:
        product = item.product
        quantity = item.quantity
        
        subtotal += product.price * quantity
        discount_total += product.discount_amount * quantity
        
        number_of_items += 1 * quantity
        
    total = subtotal - discount_total
        
    context = {
        "profile": profile,
        "addresses": addresses,
        "number_of_items": number_of_items,
        "items": items,
        "subtotal": subtotal,
        "discount_total": discount_total,
        "total": total
    }
    
    return render(request, "orders/checkout.html", context)

@login_required
@require_POST
def place_order(request):
    address_id = request.POST.get("address")
    
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    order = services.checkout(request.user, address)
    
    return redirect("orders:detail", order.order_key)
    