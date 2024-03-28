from django.db import models
from django.conf import settings
from django.utils import timezone
import pathlib
import uuid

import stripe
import requests
from cfehome.env import config

STRIPE_SECRET_KEY= config("STRIPE_SECRET-KEY",default=None)
stripe.api_key=STRIPE_SECRET_KEY

from django.core.files.storage import FileSystemStorage




PROTECTED_MEDIA_ROOT=settings.PROTECTED_MEDIA_ROOT

protected_storage=FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

# Create your models here.

class Products(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	stripe_product_id=models.CharField(max_length=220,blank=True,null=True)
	mpesa_product_id=models.CharField(max_length=220,blank=True,null=True)
	image=models.ImageField(upload_to='products/',blank=True,null=True)
	description=models.TextField(max_length=220, blank=True, null=True)
	name=models.CharField(max_length=20)
	handle=models.SlugField(unique=True)
	price=models.DecimalField( max_digits=10, decimal_places=2,default=9.99)
	og_price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
	stripe_price_id=models.CharField(max_length=220,blank=True, null=True)
	mpesa_price_id=models.CharField(max_length=220,blank=True, null=True)
	mpesa_price=models.IntegerField(default=1000)
	stripe_price=models.IntegerField(default=1000)
	price_change_timestamp=models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
	timestamp=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	@property
	def display_name(self):
		return self.name
	
	@property
	def display_price(self):
		return self.price

	def	__str__(self):
		return self.display_name




	def save(self,*args,**kwargs):
		if self.price !=self.mpesa_price:
			self.price=self.mpesa_price
		if not self.mpesa_price:
			self.mpesa_price=int(self.price)
		if self.name:
			stripe_product_r=stripe.Product.create(name=self.name)
			self.stripe_product_id=stripe_product_r.id
		if not self.mpesa_product_id:
			self.mpesa_product_id=self.generate_mpesa_product_id


		if not self.mpesa_price_id:
			self.mpesa_price_id=self.generate_mpesa_price_id	

		if not self.stripe_price_id:
			stripe_price_obj=stripe.Price.create(
					product=self.stripe_product_id,
					unit_amount=self.stripe_price,
					currency="usd")
		
		if self.price !=self.og_price:
			self.og_price=self.price
			#it will trigger an api request
			self.stripe_price=int(self.price * 100)
			
			if self.stripe_product_id:
				stripe_price_obj=stripe.Price.create(
					product=self.stripe_product_id,
					unit_amount=self.stripe_price,
					currency="usd")
			self.stripe_price_id=stripe_price_obj.id	
			self.price_change_timestamp=timezone.now()
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/products/product-detail/{self.handle}"
	def get_manage_url(self):
		return f"/products/product-manage-detail/{self.handle}"
	def	generate_mpesa_product_id(self):
		return "MPESA_PROD" + str(uuid.uuid4())
	
	def	generate_mpesa_price_id(self):
		return "MPESA_PRICE" + str(uuid.uuid4())





def handle_product_images_upload(instance,filename):
	return f"products/product-detail/{instance.product.handle}/attachments/{filename}"		

class ProductImages(models.Model):
	product=models.ForeignKey(Products,on_delete=models.CASCADE)
	file=models.FileField(upload_to=handle_product_images_upload,storage=protected_storage)
	name=models.CharField(max_length=50, blank=True,null=True)
	is_free=models.BooleanField(default=False)
	active=models.BooleanField(default=True)
	timestamp=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)


	def save(self,*args, **kwargs):
		if not self.name:
			self.name=pathlib.Path(self.file.name).name
			super().save(*args, **kwargs)
			
	@property
	def display_name(self):
		return self.name or pathlib.Path(self.file.name).name

	def get_download_url(self):
		return f"/products/product-detail/{self.product.handle}/download/{self.pk}/"		
			
