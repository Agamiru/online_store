from django.contrib import admin
from .models import (
    Product, MainFeatures, Brand, Category, Image, SubCategory1,
    SubCategory2, ModelName, Accessories, BoughtTogether
)
# Register your models here.

admin.site.register(Product)
admin.site.register(MainFeatures)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)
admin.site.register(ModelName)
admin.site.register(Accessories)
admin.site.register(BoughtTogether)

