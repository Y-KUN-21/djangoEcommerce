from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('COD', 'Cash on Delivery'),
    ('GP', 'Google Pay'),
    ('PTM', 'Paytm'),
)


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': " 13th street", 'class': 'form-control'
    }))
    optional_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': " Apartment or suite", 'class': 'form-control'
    }))
    country = CountryField(blank_label='select country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-50'
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control d-block w-50'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_method = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
