from orders.models import Order
from django.db import transaction
from payment.models import Payment
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

PAYMENT_DURATION = 5

def get_user_order(user, order_key):
    order = Order.objects.select_for_update().get(
        user=user,
        order_key=order_key
    )
    
    if order.status != Order.Status.PENDING_PAYMENT:
        raise ValidationError(
            "This order is not available to payment."
        )
    
    if order.expired <= timezone.now():
        raise ValidationError(
            "The order has expired."
        )
    
    return order

def get_payment_for_form(user, order_key, payment_id):
    return Payment.objects.get(
        pk=payment_id,
        order__user=user,
        order__order_key=order_key
    )
    
@transaction.atomic
def initiate_payment(user, order_key):
    order = get_user_order(user, order_key)
    
    payment = order.payments
    now = timezone.now()
    
    if payment.filter(status=Payment.Status.SUCCESS).exists():
        raise ValidationError(
            "This order already have a successfull payment."
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
        
        payment.status = Payment.Status.CANCELED

    
    return Payment.objects.create(
        order=order,
        amount=order.total,
        status=Payment.Status.PENDING,
        expired=now + timedelta(minutes=PAYMENT_DURATION)
    )

@transaction.atomic
def complete_payment(user, order_key, payment_id, provider_status):
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
        raise ValidationError("Payment was not found.")
    
    order = Order.objects.select_for_update().get(
        pk=payment_info["order_id"]
    )
    
    payment = Payment.objects.select_for_update().get(
        pk=payment_id,
        order=order
    )
    
    if payment.status != Payment.Status.PENDING:
        raise ValidationError(
            "This payment has already been processed."
        )
    
    if provider_status not in (
        Payment.Status.SUCCESS,
        Payment.Status.FAILED
    ):
        raise ValidationError(
            "Invalid provider result."
        )
    
    now = timezone.now()
    
    if payment.expired <= now:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])
        
        return payment
    
    if order.expired and order.expired <= now:
        payment.status = Payment.Status.CANCELED
        payment.save(update_fields=["status"])
        
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
                "This order already has a successfull payment."
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
    payments = Payment.objects.filter(status=Payment.Status.PENDING, expired__lt=timezone.now())
    
    for payment in payments:
        payment.status = Payment.Status.CANCELED
        
        payment.save(update_fields=["status"])
        