from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from products.models import Products
from .models import Purchase
import stripe
from cfehome.env import config
import requests
import base64
import datetime
import json

DARAJA_CONSUMER_KEY=config("DARAJA_CONSUMER_KEY",default=None)
DARAJA_CONSUMER_SECRET=config("DARAJA_CONSUMER_SECRET",default=None)
MPESA_PROCESS_REQUEST_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"



#initiate mpesa express payment


STRIPE_SECRET_KEY=config("STRIPE_SECRET-KEY",default=None)
stripe.api_key=STRIPE_SECRET_KEY
BASE_ENDPOINT="http://127.0.0.1:8000/"


mpesa_success_url=f"{BASE_ENDPOINT}/purchases/mpesa_success/"
mpesa_cancel_url=f"{BASE_ENDPOINT}/purchases/mpesa_stopped/"


def get_access_token(consumer_key, consumer_secret):
	auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
	auth_string=f"{consumer_key}:{consumer_secret}"
	encoded_auth=base64.b64encode(auth_string.encode()).decode()
	headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

    # Make a POST request to obtain the access token
	response = requests.post(auth_url, headers=headers)

    # Check if the request was successful
	if response.status_code == 200:
        # Extract the access token from the response

		try:
			access_token= response.json().get("access_token")
			return access_token
		except json.decoder.JSONDecodeError:
			print("Invalid JSON:", response.text)
			return None

	else:
        # If the request failed, print the error message
		print("Error:", response.text)
		return None
ACCESS_TOKENS=get_access_token(DARAJA_CONSUMER_KEY,DARAJA_CONSUMER_SECRET)

def	mpesa_purchase_start(request):
	if not request.method=="POST":
		return HttpResponseBadRequest()
	if not request.user.is_authenticated:
		return HttpResponseBadRequest()
	handle=request.POST.get("handle")
	product=Products.objects.get(handle=handle)
	mpesa_price_id=product.mpesa_price_id
	if mpesa_price_id is None:
		return HttpResponseBadRequest()
	
	# Create a purchase record
	mpesa_purchase = Purchase.objects.create(user=request.user, product=product)

	request.session['mpesa_purchase_id']=mpesa_purchase.id


	mpesa_payload = {
   "BusinessShortCode": "enter shortcode",
    "Password": "ENTER PASSWORD",
    "Timestamp": "20240326190652",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": str(product.mpesa_price),
    "PartyA": "Phone number",
    "PartyB": "number",
    "PhoneNumber": "PHONE NUMBER",
    "CallBackURL": mpesa_success_url,
    "AccountReference": "Gerald Inco",
    "TransactionDesc": "Payment of X" 
} 
	
	#authenticate your request

	# Authenticate your request
	mpesa_headers = {
        "Authorization": f"Bearer {get_access_token(DARAJA_CONSUMER_KEY, DARAJA_CONSUMER_SECRET)}"
    }


	mpesa_response = requests.post(mpesa_success_url, json=mpesa_payload, headers=mpesa_headers)

	if mpesa_response.status_code==200:
		mpesa_data=mpesa_response.json()
		mpesa_checkout_id=mpesa_data.get("CheckoutRequestID")
		if mpesa_checkout_id:
			mpesa_purchase=Purchase.objects.create(user=request.user,product=product)
			mpesa_purchase.mpesa_checkout_id=mpesa_checkout_id
			mpesa_purchase.save()
			return  HttpResponseRedirect(mpesa_success_url)
		else:
			return HttpResponseBadRequest(mpesa_cancel_url)
	return HttpResponseBadRequest("Failed to initiate M-Pesa payment")
		
	


# Create your views here.
def stripe_purchase_start(request):
	if not request.method=="POST":
		return HttpResponseBadRequest()
	if not request.user.is_authenticated:
		return HttpResponseBadRequest()
	handle=request.POST.get("handle")
	product=Products.objects.get(handle=handle)
	
	stripe_price_id=product.stripe_price_id
	if stripe_price_id is None:
		return HttpResponseBadRequest()

	stripe_purchase=Purchase.objects.create(user=request.user,product=product)
	
	
	request.session['stripe_purchase_id']=stripe_purchase.id
	success_url=f"{BASE_ENDPOINT}/purchases/stripe_success/"
	cancel_url=f"{BASE_ENDPOINT}/purchases/stripe_stopped/"
	print(success_url,cancel_url)


	checkout_session=stripe.checkout.Session.create(
		line_items=[
			{
				"price":stripe_price_id,
				"quantity":1

			}
		],
		mode="payment",
		success_url=success_url,
		cancel_url=cancel_url
	)
	stripe_purchase.stripe_checkout_session_id=checkout_session.id
	stripe_purchase.save()
	return HttpResponseRedirect(checkout_session.url)

	

def stripe_purchase_success(request):
	purchase_id=request.session.get("purchase_id")
	if purchase_id:
		purchase=Purchase.objects.get(id=purchase_id)
		purchase.completed=True
		purchase.save()
		del request.session['purchase_id']
		return HttpResponseRedirect(purchase.product.get_absolute_url())
	return HttpResponse(f'finished {purchase_id}')


def mpesa_purchase_success(request):
	mpesa_purchase_id=request.session.get("mpesa_purchase_id")
	if mpesa_purchase_id:
		purchase=Purchase.objects.get(id=mpesa_purchase_id)
		purchase.completed=True
		purchase.save()
		del request.session['mpesa_purchase_id']
		return HttpResponseRedirect(purchase.product.get_absolute_url())
	return HttpResponse(f'finished {mpesa_purchase_id}')



def stripe_purchase_stop(request):
	stripe_purchase_id=request.session.get("stripe_purchase_id")
	if stripe_purchase_id:
		purchase=Purchase.objects.get(id=stripe_purchase_id)
		product=purchase.product
		return HttpResponseRedirect(product.get_absolute_url())
	return HttpResponse('stopped')

def mpesa_purchase_stop(request):
	mpesa_purchase_id=request.session.get("mpesa_purchase_id")
	if mpesa_purchase_id:
		purchase=Purchase.objects.get(id=mpesa_purchase_id)
		product=purchase.product
		return HttpResponseRedirect(product.get_absolute_url())
	return HttpResponse('stopped')



