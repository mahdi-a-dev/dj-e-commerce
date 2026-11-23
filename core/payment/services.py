from orders.models import Order
from django.db import transaction
from payment.models import Payment
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from orders.services import cancel_order

PAYMENT_DURATION = 5

def get_user_order(user, order_key):
    """
    Return user's order.
    
    Raises:
        ValidationError: If the order status is not PENDING_PAYMENT
        or the expired date has passed.
    """
    order = Order.objects.select_for_update().get(
        user=user,
        order_key=order_key
    )
    
    if order.status != Order.Status.PENDING_PAYMENT:
        raise ValidationError(
            "این سفارش قابل پرداخت نیست."
        )
    
    if order.expired <= timezone.now():
        raise ValidationError(
            "سفارش منقضی شده است."
        )
    
    return order

def get_payment_for_form(user, order_key, payment_id):
    """
    Retrieve a payment for displaying its information in the payment form
    """
    return Payment.objects.get(
        pk=payment_id,
        order__user=user,
        order__order_key=order_key
    )
    
@transaction.atomic
def initiate_payment(user, order_key):
    """
    Create new payment attempt or reuse an existing valid one.
    
    Raises:
        ValidationError: If Order has already successful payment.
    """
    order = get_user_order(user, order_key)
    
    payment = order.payments
    now = timezone.now()
    
    if payment.filter(status=Payment.Status.SUCCESS).exists():
        raise ValidationError(
            "این سفارش قبلاً با موفقیت پرداخت شده است."
        )
    
    pending_payments = (
        Payment.objects.select_for_update().filter(
            order=order,
            status = Payment.Status.PENDING
        )
        .order_by("-pk")
    )
    
    for payment in pending_payments:
        if payment.expired > now:
            return payment
        
        cancel_order(order)
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])

    
    return Payment.objects.create(
        order=order,
        amount=order.total,
        status=Payment.Status.PENDING,
        expired=now + timedelta(minutes=PAYMENT_DURATION)
    )

@transaction.atomic
def complete_payment(user, order_key, payment_id, provider_status):
    """
    Complete a payment attempt using the result returend by the provider.
    
    Raises:
        ValidationError: If the payment does not exists.
        ValidationError: If the payment already been proccessed.
        ValidationError: If the provider result is invalid.
    """
    
    # get user payments
    payment_info = (
        Payment.objects.filter(
            pk=payment_id,
            order__user=user,
            order__order_key=order_key
        )
        .values("order_id")
        .first()
    )
    
    if payment_info is None:
        raise ValidationError("پرداخت یافت نشد.")
    
    order = Order.objects.select_for_update().get(
        pk=payment_info["order_id"]
    )
    
    payment = Payment.objects.select_for_update().get(
        pk=payment_id,
        order=order
    )
    
    if payment.status != Payment.Status.PENDING:
        raise ValidationError(
            "این پرداخت قبلاً پردازش شده است."
        )
    
    if provider_status not in (
        Payment.Status.SUCCESS,
        Payment.Status.FAILED
    ):
        raise ValidationError(
            "نتیجه ارائه‌دهنده نامعتبر است."
        )
    
    now = timezone.now()
    
    if payment.expired <= now:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])
        
        return payment
    
    if order.expired and order.expired <= now:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])
        
        cancel_order(order)
        
        order.status = Order.Status.CANCELED
        order.save(update_fields=["status"])
        
        return payment
    
    if order.status != Order.Status.PENDING_PAYMENT:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])
        
        return payment
    
    if provider_status == Payment.Status.SUCCESS:
        another_success = (
            order.payments.filter(status=Payment.Status.SUCCESS).exclude(pk=payment_id).exists()
        )
        
        if another_success:
            raise ValidationError(
                "این سفارش قبلاً پرداخت موفقی داشته است."
            )
            
        payment.status = Payment.Status.SUCCESS
        order.status = Order.Status.PROCESSING
        
        payment.save(update_fields=["status"])
        order.save(update_fields=["status"])
        
    else:
        payment.status = Payment.Status.FAILED
        payment.save(update_fields=["status"])
    
    return payment

@transaction.atomic
def cancel_expireds():
    """
    Cancel expired pending payment attempts.
    """
    now = timezone.now()
    
    Payment.objects.filter(
        status=Payment.Status.PENDING,
        expired__lt=now
    ).update(
        status=Payment.Status.CANCELED
    )
    
        