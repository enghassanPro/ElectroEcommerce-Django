from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

class old_password(models.Model):
    user_id = models.ForeignKey( User , on_delete=models.CASCADE )
    old_password = models.CharField(max_length=250 , unique=True)
    created = models.DateTimeField(default=now)