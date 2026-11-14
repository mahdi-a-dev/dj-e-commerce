from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import CartItem
from products.models import Product
from cart.services import add_cart_item, remove_cart_item, update_cart_item_quantity
from django.views import View


class CartDetailView(LoginRequiredMixin, ListView):
    context_object_name = "cart_items"
    template_name = "cart/detail.html"
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related("product")
    

class AddItem(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        cart = request.user.cart
        product = get_object_or_404(Product, id=product_pk)

        add_cart_item(cart, product)
        return redirect("cart:detail")


class RemoveItem(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        cart = request.user.cart
        product = get_object_or_404(Product, pk=product_pk)

        remove_cart_item(cart, product)
        return redirect("cart:detail")


class UpdateQuantity(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = CartItem.objects.get(pk=pk)
        
        quantity = int(request.POST.get("quantity"))
        update_cart_item_quantity(cart_item, quantity)
        return redirect("cart:detail")
        