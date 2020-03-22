from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('COD', 'Cash on Delivery'),
    ('GP', 'Google Pay'),
    ('PTM', 'Paytm'),
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First name', 'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last name', 'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email Address', 'class': 'form-control'
    }))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone number', 'maxlength': '10', 'minlength': '10',
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': " Address", 'class': 'form-control'
    }))
    optional_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': " Address 2", 'class': 'form-control'
    }))
    country = CountryField(blank_label='country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Zip code", 'class': 'form-control d-block w-100'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_method = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES, required=True)