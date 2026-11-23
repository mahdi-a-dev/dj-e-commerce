from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import CartItem
from cart.services import add_cart_item, remove_cart_item, update_cart_item_quantity
from django.views import View
from django.http import Http404
from django.core.exceptions import ValidationError
from django.contrib import messages
from products.models import Product


class CartDetailView(LoginRequiredMixin, ListView):
    """
    List of authenticated user's cart items.
    """
    context_object_name = "cart_items"
    template_name = "cart/detail.html"
    
    def get_queryset(self):
        user = self.request.user
        cart = user.cart
        
        
        return CartItem.objects.filter(
            cart=cart,
            cart__user=user
        ).select_related("product")
    

class AddItem(LoginRequiredMixin, View):
    """
    Handle adding products to the authenticated user's cart.
    """
    def post(self, request, product_pk):
        cart = request.user.cart

        try:
            add_cart_item(cart, product_pk)
        
        except Product.DoesNotExist:
            raise Http404
        
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        
        else:
            messages.success(
                request,
                "محصول با موفقیت به سبد خرید اضافه شد."
            )    
                
        return redirect("cart:detail")


class RemoveItem(LoginRequiredMixin, View):
    """
    Handle removing products from the authenticated user's cart.
    """
    def post(self, request, product_pk):
        cart = request.user.cart
        
        try:
            remove_cart_item(cart, product_pk)
        
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        
        else:
            messages.success(
                request,
                "محصول با موفقیت از سبد حرید حذف شد."
            )
            
        return redirect("cart:detail")


class UpdateQuantity(LoginRequiredMixin, View):
    """
    Handle updating products quantity from the authenticated user's cart.
    """
    def post(self, request, pk):
        cart = request.user.cart
        
        try:
            quantity = int(request.POST.get("quantity"))
            update_cart_item_quantity(cart, pk, quantity)
            
        except CartItem.DoesNotExist:
            raise Http404
        
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        
        else:
            messages.success(
                request,
                "نعداد محصول بروزرسانی شد."
            )
            
        return redirect("cart:detail")
        