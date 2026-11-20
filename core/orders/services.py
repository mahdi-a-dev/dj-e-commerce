from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from orders.models import Order, OrderItem
from products.models import Product
from django.utils import timezone

from datetime import timedelta


@transaction.atomic
def get_user_cart(user):
    """
    Get user cart
    raise ValidationError if its empty.
    """
    if not user.cart:
        raise ValidationError(
            "You don't have shopping cart."
        )
    
    return user.cart

@transaction.atomic
def validate_cart(user, cart, address):
    """
    Validate user cart.
    """
    if not cart.items.exists():
        raise ValidationError(
            "Your shopping cart is empty."
        )
    
    if address.user_id != user.id:
        raise ValidationError(
            "The selected address does not belong to you."
        )
    
    for item in cart.items.select_related("product"):
        product = item.product
        
        if not product.is_active:
            raise ValidationError(
                f"{product.title} is not longer available."
            )

        if item.quantity <= 0:
            raise ValidationError(
                f"Invalid quantity for {product.title}."
            )
        
        if item.quantity > product.stock_quantity:
            raise ValidationError(
                f"Insufficient stock for {product.title}."
            )
    
    return True

@transaction.atomic
def create_order(user, cart, address):
    """
    Create order from user cart and address.
    """
    profile = user.profile
    
    if not profile.first_name or not profile.last_name:
        raise ValidationError(
            "Your personal information is not complete"
        )
    
    # user snapshot
    full_name = f"{user.profile.first_name} {user.profile.last_name}"
    phone_number = user.phone_number.as_national
    
    # address snapshot
    province = address.province
    city = address.city
    postal_code = address.postal_code
    full_address = address.full_address
    
    expired = timezone.now() + timedelta(minutes=15)
    
    subtotal = Decimal("0")
    discount_amount = Decimal("0")
    
    for item in cart.items.select_related("product"):
        product = item.product
        
        subtotal += product.price * item.quantity
        discount_amount += product.discount_amount * item.quantity
    
    # Calculating final price after discount.
    total = subtotal - discount_amount
    
    order = Order.objects.create(
        user=user,
        address=address,
        full_name=full_name,
        phone_number=phone_number,
        
        shipping_province=province,
        shipping_city=city,
        shipping_postal_code=postal_code,
        shipping_full_address=full_address,
        
        status=Order.Status.PENDING_PAYMENT,
        expired=expired,
        subtotal=subtotal,
        discount_amount=discount_amount,
        total=total
    )
    
    return order

@transaction.atomic
def create_order_items(order, cart):
    """
    Create OrderItems by every CartItems.
    """
    for item in cart.items.select_related("product"):
        product = item.product
        quantity = item.quantity
        
        discount_amount = product.discount_amount * quantity
        total_price = product.final_price * quantity
        
        OrderItem.objects.create(
            order=order,
            product=product,
            product_title=product.title,
            unit_price=product.price,
            quantity=quantity,
            discount_amount=discount_amount,
            total_price=total_price
        )

@transaction.atomic
def update_product_stock(cart):
    """
    Update product stock from user cartItems quantity.
    """
    for item in cart.items.select_related("product"):
        product = Product.objects.select_for_update().get(pk=item.product.pk, is_active=True)
        quantity = item.quantity
        
        if not product.is_in_stock:
            raise ValidationError(
                "This product is out of stock."
            )
        
        if quantity > product.stock_quantity:
            raise ValidationError(
                "Not enough stock"
            )
        
        product.stock_quantity -= quantity
        
        product.save(update_fields=["stock_quantity"])
    
@transaction.atomic
def checkout(user, address):
    """
    Main method for create order for user and delete items from cart.
    """
    cart = get_user_cart(user)
    
    validate_cart(user, cart, address)
    
    order = create_order(user, cart, address)
    
    create_order_items(order, cart)
    
    update_product_stock(cart)
    
    # delete items in cart after creating order
    cart.items.all().delete()
    
    return order


def cancel_expireds():
    orders = Order.objects.filter(expired__lt=timezone.now())
    
    for order in orders:
        order.status = Order.Status.CANCELED
        
        order.save(update_fields=["status"])