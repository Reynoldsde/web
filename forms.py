from django import forms
from .models import invitation_code, WithdrawalRequest
from Account.models import account, vip_plans


class InvitationCodeForm(forms.ModelForm):
    class Meta:
        model = invitation_code
        fields = ['code', 'activated']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'custom-input', 'readonly': 'readonly'}),
            'activated': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        code = kwargs.pop('code', None)
        super().__init__(*args, **kwargs)
        if code:
            self.fields['code'].initial = code


class ClientForm(forms.ModelForm):
    class Meta:
        model = account
        fields = ['username', 'name', 'email', 'phone', 'balance', 'vip_plan', 'show_premium_products', 'assigned_task', 'is_active']  # List fields you want to allow editing
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'vip_plan': forms.Select(attrs={'class': 'form-control'}),
            'assigned_task': forms.NumberInput(attrs={'class': 'form-control'}),
            'assigned_task': forms.Select(attrs={'class': 'form-control'}),
        }


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['user', 'wallet_address' ,'amount', 'status', 'approval_date', 'rejection_reason']
        widgets = {
            'user': forms.Select(attrs={'class': 'custom-select'}),
            'amount': forms.NumberInput(attrs={'class': 'custom-input', 'placeholder': 'Amount'}),
            'status': forms.Select(attrs={'class': 'custom-select'}),
            'approval_date': forms.DateInput(attrs={'class': 'custom-input', 'type': 'date'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'custom-textarea', 'placeholder': 'Reason for rejection'}),
        }

class VipPlanForm(forms.ModelForm):
    class Meta:
        model = vip_plans
        fields = ['plan_name', 'sets_per_day', 'profit_per_submission', 'account_minimum_balance']
        widgets = {
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sets_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'profit_per_submission': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_minimum_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }