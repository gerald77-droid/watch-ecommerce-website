

from django.urls import path

from . import views
app_name='purchases'

urlpatterns = [
    #path('', views.home_view),
    path('mpesa_start/',views.mpesa_purchase_start,name='mpesa_start'),
	path('stripe_start/',views.stripe_purchase_start,name='stripe_start'),
	path('mpesa_success/',views.mpesa_purchase_success,name='mpesa_success'),
	path('stripe_success/',views.stripe_purchase_success,name='stripe_success'),
	path('stripe_stopped/',views.stripe_purchase_stop,name='stripe_stopped'),
	path('mpesa_stopped/',views.mpesa_purchase_stop,name='mpesa_stopped'),
	
]
