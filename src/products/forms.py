from typing import Any, Mapping
from django import forms
from django.forms import modelformset_factory,inlineformset_factory
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Products,ProductImages

input_css_class="form-control"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'handle', 'price']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['image','name', 'handle', 'price']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']=input_css_class

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['file','name', 'is_free', 'active']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['active','free']:
                continue
            self.fields[field].widget.attrs['class']=input_css_class            


ProductImagesModelFormset=modelformset_factory(ProductImages, 
                                               form=ProductImagesForm,
                                                fields=['file','name','active','is_free'],
                                                extra=0,
                                                can_delete=True
                                                )

ProductImagesInlineFormset=inlineformset_factory(Products,ProductImages,
                                                 form=ProductImagesForm, 
                                                 formset=ProductImagesModelFormset,
                                                fields=['file','name','active','is_free'],
                                                extra=0,
                                                can_delete=True)