from .models import *
# from .models import Product
#
#
# # instance = Image model instance
# def storage_dir(instance, filename) -> str:
#     product_instance = Product.objects.get(pk=instance.prod_id)
#     if not product_instance:
#         raise ValueError("Model received None as response")
#     brand_name = product_instance.get_brand_name.replace(" ", "_")
#     model_name = product_instance.model_name.replace(" ", "_")
#
#     return f"{brand_name}/{model_name}/{filename}"


# Todo: Ideal place for keeping model utilities like storage_dir but class "Product"
# Todo: keeps raising import errors.


# class Defaults:
#     def __init__(self):
#         self.kwargs = {"name": "Default"}
#         self.new_kwargs = None
#         self.cat_model = Category
#         self.subcat_model_1 = SubCategory1
#         self.subcat_model_2 = SubCategory2
#         self.brand_model = Brand
#
#     def get_default_category(self):
#         model = self.cat_model
#         obj = self.checker(model)
#         return self.finalize(obj, model)
#
#     def get_default_subcat_1(self):
#         model = self.subcat_model_1
#         obj = self.checker(model)
#         self.new_kwargs = {**self.kwargs, **{"cat_id": self.get_default_category()}}
#         return self.finalize(obj, model)
#
#     def get_default_subcat_2(self):
#         model = self.subcat_model_2
#         obj = self.checker(model)
#         self.new_kwargs = {**self.kwargs, **{"sub_cat_id": self.get_default_subcat_1()}}
#         return self.finalize(obj, model)
#
#     def get_default_brand(self):
#         model = self.brand_model
#         obj = self.checker(model)
#         return self.finalize(obj, model)
#
#     def checker(self, model):
#         try:
#             obj = model.objects.get(**self.kwargs)
#         except doesnt_exist:
#             obj = None
#         return obj
#
#     def finalize(self, obj, model):
#         if not obj:
#             if self.new_kwargs:
#                 new_obj = model(**self.new_kwargs)
#             else:
#                 new_obj = model(**self.kwargs)
#             new_obj.save()
#             self.new_kwargs = None
#             return new_obj
#         return obj
#
#
# default_cat = Defaults().get_default_category()
# default_subcat_1 = Defaults().get_default_subcat_1()
# default_subcat_2 = Defaults().get_default_subcat_2()
# default_brand = Defaults().get_default_brand()


# def get_default(self):
#     model = self
#     kwargs = {"name": "Default"}
#     try:
#         obj = model.objects.get(**kwargs)
#     except doesnt_exist:
#         obj = None
#
#     if not obj:
#         new_obj = model(**kwargs)
#         new_obj.save()
#         return new_obj
#     return obj