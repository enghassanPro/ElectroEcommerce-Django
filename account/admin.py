from django.contrib import admin
from account.models.confirm_email import confirm_email
from account.models.old_password import old_password

# Register your models here.

admin.site.register(confirm_email)
admin.site.register(old_password)