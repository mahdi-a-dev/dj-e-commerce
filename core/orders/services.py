from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from orders.models import Order, OrderItem
from products.models import Product
from django.utils import timezone
from datetime import timedelta
from django.db.models import F

ORDER_DURATION = 15

def get_user_cart(user):
    """
    Return user's cart.
    
    Raises:
        ValidationError: If the user does not have a shopping cart.
    """
    if not user.cart:
        raise ValidationError(
            "شما سبد خریدی ندارید."
        )
    
    return user.cart

def validate_cart(user, cart, address):
    """
    Validate user's cart and its cart items.
    
    Raises:
        ValidationError: If cart does not have any items.
        ValidationError: If product is inactive or product quantity is invalid.
    """
    if not cart.items.exists():
        raise ValidationError(
            "سبد خرید شما خالی است."
        )
    
    if address.user_id != user.id:
        raise ValidationError(
            "آدرس انتخاب‌ شده متعلق به شما نیست."
        )
    
    for item in cart.items.select_related("product"):
        product = item.product
        
        if not product.is_active:
            raise ValidationError(
                f"{product.title} دیگر در دسترس نیست."
            )

        if item.quantity <= 0:
            raise ValidationError(
                f"مقدار نامعتبر برای {product.title}."
            )
        
        if item.quantity > product.stock_quantity:
            raise ValidationError(
                f"موجودی ناکافی برای {product.title}."
            )

@transaction.atomic
def create_order(user, cart, address):
    """
    Create user order.
    
    Take snapshots from profile and address informations.
    
    Returns: The created order.
    
    Raises:
        ValidationError: If profile info is incomplete.
    """
    profile = user.profile
    
    if not profile.first_name or not profile.last_name:
        raise ValidationError(
            "اطلاعات شخصی شما کامل نیست"
        )
    
    # user snapshot
    full_name = f"{user.profile.first_name} {user.profile.last_name}"
    phone_number = user.phone_number.as_national
    
    # address snapshot
    province = address.province
    city = address.city
    postal_code = address.postal_code
    full_address = address.full_address
    
    subtotal = Decimal("0")
    discount_amount = Decimal("0")
    
    for item in cart.items.select_related("product"):
        product = item.product
        
        subtotal += product.price * item.quantity
        discount_amount += product.discount_amount * item.quantity
    
    # Calculating final price after discount.
    total = subtotal - discount_amount
    
    now = timezone.now()
    
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
        expired=now + timedelta(minutes=ORDER_DURATION),
        subtotal=subtotal,
        discount_amount=discount_amount,
        total=total
    )
    
    return order

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

def update_product_stock(cart):
    """
    Update product stock quantity.
    
    Raises:
        ValidationError: If the product is unavailable or the stock is insufficient.
    """
    for item in cart.items.select_related("product"):
        product = Product.objects.select_for_update().get(
            pk=item.product.pk,
            is_active=True
        )
        quantity = item.quantity
        
        if not product.is_in_stock:
            raise ValidationError(
                "این محصول موجود نیست."
            )
        
        if quantity > product.stock_quantity:
            raise ValidationError(
                "موجودی کافی نیست"
            )
        
        product.stock_quantity -= quantity
        
        product.save(update_fields=["stock_quantity"])
    
@transaction.atomic
def checkout(user, address):
    """
    Main method for process checkout.
    """
    cart = get_user_cart(user)
    
    validate_cart(user, cart, address)
    
    order = create_order(user, cart, address)
    
    create_order_items(order, cart)
    
    update_product_stock(cart)
    
    # delete items in cart after creating order
    cart.items.all().delete()
    
    return order

@transaction.atomic
def cancel_order(order):
    order = Order.objects.select_for_update().get(pk=order.pk)
    
    if order.status != Order.Status.PENDING_PAYMENT:
        raise ValidationError(
            "امکان لغو این سفارش وجود ندارد."
        )
        
    for item in order.items.select_related("product"):
        Product.objects.filter(
            pk=item.product_id
        ).update(
            stock_quantity=F("stock_quantity") + item.quantity
        )
        
    order.status = Order.Status.CANCELED
    order.save(update_fields=["status"])

@transaction.atomic
def cancel_expireds():
    """
    Changes the status of PENDING_PAYMENT orders that have passed their due time to "cancelled." 
    """
    orders = Order.objects.filter(status=Order.Status.PENDING_PAYMENT, expired__lt=timezone.now())
    
    for order in orders:
        cancel_order(order)
        
        order.status = Order.Status.CANCELED
        
        order.save(update_fields=["status"])