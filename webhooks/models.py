from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Webhooks(models.Model):
    data = models.CharField(max_length=2000)
    headers = models.CharField(max_length=2000)
    body = models.CharField(max_length=2000)

class Insights(models.Model):
    comments = models.IntegerField(_("Number of comments "))
    def __str__(self) -> str:
        return str(self.comments)