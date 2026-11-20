from django.shortcuts import render, get_object_or_404
from orders.models import Order
from payment import services
from payment.forms import PaymentStatusForm
from payment.providers.mock.mock_provider import mock_provider
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect 

@login_required
def payment_page(request, order_key):
    user = request.user
    
    if request.method == "GET":
        try:
            payment = services.initiate_payment(user, order_key)
            
        except ValidationError as exc:
            messages.error(request, exc.message[0])
            return redirect("orders:detail", order_key=order_key)
        
        form = PaymentStatusForm(
                initial={"payment_id": payment.pk}
        )
        
    else:
        form = PaymentStatusForm(request.POST)
        
        if form.is_valid():
            try:
                provider_status = mock_provider.process(
                    form.cleaned_data["status"]
                )
                
                payment = services.complete_payment(
                    user=user,
                    order_key=order_key,
                    payment_id=form.cleaned_data["payment_id"],
                    provider_status=provider_status
                )
                
            except ValidationError as exc:
                form.add_error(None, exc)
            
            else:
                redirect("orders:deail", order_key=order_key)
        
        payment_id = (
            form.cleaned_data.get("payment_id")
            or request.POST.get("payment_id")
        )
        
        payment = services.get_payment_for_form(
            user=user,
            order_key=order_key,
            payment_id=payment_id
        )

    context = {
        "form": form,
        "payment": payment
    }
    
    return render(request, "payment/page.html", context)
    