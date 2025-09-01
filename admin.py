from django.contrib import admin
from .models import invitation_code ,selection_log, WithdrawalRequest, finished_task, Terms_and_conditions
# Register your models here.

admin.site.register(invitation_code)
admin.site.register(selection_log)
admin.site.register(WithdrawalRequest)
admin.site.register(finished_task)
admin.site.register(Terms_and_conditions)