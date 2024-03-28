

from django.urls import path

from . import views
app_name='products'

urlpatterns = [
    #path('', views.home_view),
    path('create-product',views.create_product,name='create-product'),
	path('list-product',views.list_product,name='list-product'),
	path('product-detail/<slug:handle>/',views.product_detail,name='product-detail'),
	path('product-manage-detail/<slug:handle>/',views.product_manage_detail,name='product-manage-detail'),
	path('product-detail/<slug:handle>/download/<int:pk>/',views.product_images_download_view,name='download')
]
