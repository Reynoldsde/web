from django.contrib import admin
from django.contrib.auth.models import GroupManager
from .models import account

class Account(admin.ModelAdmin):
    list_display = ['pk', 'last_login' ,'email', 'userid', 'username', 'phone']
    
admin.site.register(account, Account)
# Register your models here.
