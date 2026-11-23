from cart.models import CartItem
from products.models import Product
from django.core.exceptions import ValidationError


def add_cart_item(cart, product_pk):
    """
    Add a product to the cart if it is not already present.
    
    Raises:
        Product.DoesNotExist: If the product does not exist.
        ValidationError: If the product is inactive or out of stock.
    """
    product = Product.objects.get(pk=product_pk)
    
    if not product.is_active or product.stock_quantity < 1:
        raise ValidationError(
            "محصول موجود نیست."
        )
        
    CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )
        
def remove_cart_item(cart, product_pk):
    """
    Remove a product from the specified cart.
    
    Does nothing if the product is not is the cart.
    """
    CartItem.objects.filter(
        cart=cart,
        product__pk=product_pk,
    ).delete()
        
def update_cart_item_quantity(cart, item_pk, quantity):
    """
    Set the quantity of a cart item.
    
    Raises:
        CartItem.DoesNotExist: If the item does not belong to the cart.
        ValidationError: If the product is inactive or the requested 
        quantity is outside the allowed range.
    """
    item = CartItem.objects.get(
        pk=item_pk,
        cart=cart
    )

    if not item.product.is_active:
        raise ValidationError(
            "محصول موجود نیست."
        )
        
    if quantity < 1:
        raise ValidationError("مقدار باید حداقل ۱ باشد.")
    
    if quantity > item.product.stock_quantity:
        raise ValidationError("موجودی کافی نیست.")

    item.quantity = quantity
    item.save(update_fields=["quantity"])