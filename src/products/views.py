import mimetypes
from django.http import FileResponse,HttpResponseBadRequest
from django.shortcuts import render,redirect,get_object_or_404
from .models import Products,ProductImages
from .forms import ProductForm,ProductUpdateForm,ProductImagesInlineFormset


# Create your views here.
def create_product(request):
	form=ProductForm()
	if request.method=='POST':
		form=ProductForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			if request.user.is_authenticated:
				obj.user=request.user
				obj.save()
				return redirect(obj.get_manage_url())
			else:
				form.add_error(None,'user must be logged in')
	context={'form':form}		
	return render(request,'products/create.html',context)

def list_product(request):
	product_list=Products.objects.all()
	context={'product_list':product_list}
	return render(request,'products/list.html',context)	
def product_manage_detail(request,handle):
	product=get_object_or_404(Products,handle=handle)
	product_images=ProductImages.objects.filter(product=product)
	is_manager= False
	if request.user.is_authenticated:
		is_manager=product.user==request.user
	if not is_manager:
		return HttpResponseBadRequest()
	form=ProductUpdateForm()
	formset=ProductImagesInlineFormset()

	
	if request.method=='POST':
		form=ProductUpdateForm(request.POST,request.FILES,instance=product)
		formset=ProductImagesInlineFormset(request.POST , request.FILES ,queryset=product_images )
		if form.is_valid() and formset.is_valid():
			instance=form.save(commit=False)
			instance.save()
				#return redirect('products/create')
			formset.save()
			product_obj=formset.save(commit=False)
			for _form in formset:
				
				is_delete=form.cleaned_data.get('DELETE')
				try:
					product_obj=_form.save(commit=False)
				except:
					product_obj=None	
				if is_delete:
					if product_obj is not None:
						if product_obj.pk:
							product_obj.delete()
				else:
					if product_obj is not None:		
						product_obj.save()
						product_obj.product=instance
						product_obj.save()
	
			return redirect(product.get_manage_url())


				
	context={'product':product,'form':form,'formset':formset}		
	return render(request,'products/manager.html',context)

def product_detail(request,handle):
	product=get_object_or_404(Products,handle=handle)
	product_images=ProductImages.objects.filter(product=product)
	is_owner= False
	if request.user.is_authenticated:
		is_owner=request.user.purchase_set.all().filter(product=product,completed=True).exists()
	
				#return redirect('products/create')
				
	context={'product':product,'is_owner':is_owner,'product_images':product_images}		
	return render(request,'products/detail.html',context)


def product_images_download_view(request,handle=None,pk=None):
	product_image=get_object_or_404(ProductImages , product__handle=handle,pk=pk)
	can_download=product_image.is_free or False
	if request.user.is_authenticated:
		can_download=True
	if can_download is False:
		return HttpResponseBadRequest()
	file=product_image.file.open(mode='rb')
	filename=product_image.file.name
	content_type,_=mimetypes.guess_type(filename)
	response=FileResponse(file)
	response['Content-Type']=content_type or 'application/octet-stream'
	response['Content-Disposition']=f'product_image;filename={filename}'

	return response
		
	