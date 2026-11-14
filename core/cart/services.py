from cart.models import CartItem

def add_cart_item(cart, product):
    CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )
        
def remove_cart_item(cart, product):
    CartItem.objects.filter(cart=cart, product=product).delete()
        
def update_cart_item_quantity(item, quantity):
    if quantity < 1:
        raise ValueError("Quantity must be at least 1.")
    if quantity > item.product.stock_quantity:
        raise ValueError("Not enough stock.")

    item.quantity = quantity
    item.save(update_fields=["quantity"])