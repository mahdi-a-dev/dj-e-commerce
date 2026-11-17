from django import forms


class ProductSortForm(forms.Form):
    """
    This form shows ordering choises for products
    """
    ORDERING_CHOICES = [
        ("all", "همه"),
        ("newest", "جدید ترین"),
        ("price_asc", "ارزان ترین"),
        ("price_desc", "گران ترین"),
    ]

    ordering = forms.ChoiceField(
        choices=ORDERING_CHOICES,
        required=False,
        widget=forms.Select(),
    )
