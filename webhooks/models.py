from django.db import models

# Create your models here.
class Webhooks(models.Model):
    data = models.CharField(max_length=2000)