from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class confirm_email(models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    token   = models.CharField(max_length=250 , unique=True)
    created = models.DateTimeField(default=now)