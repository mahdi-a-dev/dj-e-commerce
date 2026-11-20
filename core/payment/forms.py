from django import forms

class PaymentStatusForm(forms.Form):
    STATUS_CHOICES = [
        ("success", "موفق"),
        ("failed", "ناموفق")
    ]
    
    payment_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=True,
        widget=forms.RadioSelect()
    )
    