from django.db import models
from django.conf import settings

# Create your models here.
from products.models import Products

class Purchase(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	product=models.ForeignKey(Products,null=True,on_delete=models.SET_NULL)
	mpesa_price=models.IntegerField(default=0)
	mpesa_checkout_id=models.CharField(max_length=50,null=True,blank=True)
	completed=models.BooleanField(default=False)
	stripe_checkout_session_id=models.CharField(max_length=100,null=True,blank=True)
	stripe_price=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now_add=True)
	

# Create your models here.
