from django.db import models
from Account.models import account
from django.conf import settings

# Create your models here.
class invitation_code(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    activated = models.BooleanField(default=False)
    used_by = models.ForeignKey(account, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.code


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdrawal_requests')
    wallet_address = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Withdrawal Request by {self.user.username} - {self.amount}'

    class Meta:
        ordering = ['-request_date']

class selection_log(models.Model):
    client_id = models.ForeignKey(account, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    product_commission = models.FloatField(null=True, blank=True)
    total_received = models.FloatField(null=True, blank=True)

class finished_task(models.Model):
    user = models.ForeignKey(account, null=True, blank=True, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user) + " " + str(self.date)

class customer_service_link(models.Model):
    link = models.TextField(null=True, blank=True)

class Terms_and_conditions(models.Model):
    terms = models.TextField(null=True, blank=True)