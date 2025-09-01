# forms.py
from django import forms
from .models import Task, product, show_product_list, hide_product_list
from Account.models import account

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description']
'''
class ProductForm(forms.ModelForm):
    # Field for showing the product to specific users
    users = forms.ModelMultipleChoiceField(
        queryset=account.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'user-search'}),
        required=False,
        label="Only Show To"
    )

    class Meta:
        model = product
        fields = [
            'product_image',
            'product_name',
            'product_price',
            'commission_rate',
            'premium_product',
            'negative_amount',
            'task',
        ]

    def __init__(self, *args, **kwargs):
        # Retrieve the product instance if it's being edited
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if instance:
            # Pre-fill the `users` field with already associated accounts in `show_product_list`
            self.fields['users'].initial = show_product_list.objects.filter(
                product_id=instance.id
            ).values_list('user_account', flat=True)

        # Make other fields required
        self.fields['product_image'].required = True
        self.fields['product_name'].required = True
        self.fields['product_price'].required = True
        self.fields['commission_rate'].required = True
        self.fields['task'].required = True

    def save(self, commit=True):
        # Save the product instance
        product_instance = super().save(commit=commit)

        # Handle the users selected for the `show_product_list`
        if commit:
            selected_users = self.cleaned_data.get('users')
            existing_show_users = show_product_list.objects.filter(
                product_id=product_instance.id
            ).values_list('user_account', flat=True)

            # Add new users who are not already associated
            for user in selected_users:
                if user.pk not in existing_show_users:
                    show_product_list.objects.create(
                        user_account=user,
                        product_id=product_instance.id,
                        client_pk=user.pk
                    )

            # Remove users who were deselected
            show_product_list.objects.filter(
                product_id=product_instance.id
            ).exclude(user_account__in=selected_users).delete()

        return product_instance
'''

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['product_image', 'product_name', 'product_price', 'commission_rate', 'premium_product', 'negative_amount', 'task']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_image'].required = True
        self.fields['product_name'].required = True
        self.fields['product_price'].required = True
        self.fields['commission_rate'].required = True
        self.fields['task'].required = True