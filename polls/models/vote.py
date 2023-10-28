from django.db import models
from django.contrib.auth.models import User
from . import Choice


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
