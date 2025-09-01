from django.db import models

# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=255, null=True, blank=True)
    task_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.task_name
    

class product(models.Model):
    product_image = models.ImageField(null=True, blank=True, upload_to="products/")
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    commission_rate = models.FloatField(null=True, blank=True)
    premium_product = models.BooleanField(default=False)
    negative_amount = models.FloatField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, null=True, blank=True)

class show_product_list(models.Model):
    user_account = models.ForeignKey('Account.account', null=True, blank=True, on_delete=models.CASCADE)
    product_id = models.IntegerField(null=True, blank=True)
    client_pk = models.IntegerField(null=True, blank=True)

class hide_product_list(models.Model):
    user_account = models.ForeignKey('Account.account', null=True, blank=True, on_delete=models.CASCADE)
    product_id = models.IntegerField(null=True, blank=True)
    client_pk = models.IntegerField(null=True, blank=True)