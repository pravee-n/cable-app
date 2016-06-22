import settings
import datetime
import json
from operator import itemgetter
from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    vc_no = models.CharField(max_length=200, null=False)
    stb_no = models.CharField(max_length=200, null=False)
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=1000, null=False)
    subscription_date = models.TextField()
    phone = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20, null=False)
    monthly_charge = models.IntegerField(max_length=20, null=False)
    payment_history = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=True)