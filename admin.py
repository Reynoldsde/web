from django.contrib import admin
from .models import product, Task, show_product_list, hide_product_list
# Register your models here.

admin.site.register(product)
admin.site.register(Task)
admin.site.register(show_product_list)
admin.site.register(hide_product_list)