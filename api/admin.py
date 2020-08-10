from django.contrib import admin
from .models import Products, AudioInterfaceFeatures, Brand, Category

# Register your models here.

admin.site.register(Products)
admin.site.register(AudioInterfaceFeatures)
admin.site.register(Brand)
admin.site.register(Category)
