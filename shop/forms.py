from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('bank', 'Cuenta Bancaria'),
        ('credit_card', 'Tarjeta de Crédito'),
        ('paypal', 'PayPal')
    ]
    
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Método de Pago', widget=forms.Select(attrs={'class': 'form-control'}))
    account_number = forms.CharField(max_length=20, label='Número de Cuenta Bancaria', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit_card_number = forms.CharField(max_length=16, label='Número de Tarjeta de Crédito', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit_card_expiry = forms.CharField(max_length=5, label='Fecha de Expiración (MM/AA)', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit_card_cvv = forms.CharField(max_length=3, label='CVV', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    paypal_email = forms.EmailField(label='Email de PayPal', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))