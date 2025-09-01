from django import forms
from adminpanel.models import WithdrawalRequest

class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['wallet_address', 'amount']
        widgets = {
            'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wallet address'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
        }
