from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
class Refer_Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refer_friend = models.TextField()
    refer_date = models.DateTimeField(auto_now_add=True)

class Digital_Check_In(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)