from django.contrib import admin
from .models import Product, AudioInterfaceFeatures, Brand, Category, Image

# Register your models here.

admin.site.register(Product)
admin.site.register(AudioInterfaceFeatures)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Image)

