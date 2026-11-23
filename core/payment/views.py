from django.shortcuts import render
from payment import services
from payment.forms import PaymentStatusForm
from payment.providers.mock.mock_provider import mock_provider
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect 

@login_required
def payment_page(request, order_key):
    """
    Display the payment page and process a payment attempt.
    
    GET:
        initiate or reuse a pending payment attempt.
    
    POST:
        Validate the form, process the provider result and complete the payment attempt.
    """
    user = request.user
    
    # Get request
    if request.method == "GET":
        try:
            payment = services.initiate_payment(user, order_key)
            
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        
        form = PaymentStatusForm(
                initial={"payment_id": payment.pk}
        )
    
    # Post request
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
                
                return redirect("orders:detail", order_key=order_key)
        
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
    