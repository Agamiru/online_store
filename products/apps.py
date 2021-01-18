from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class ProductsConfig(AppConfig):
    name = 'products'

    def ready(self):
        from .models import Category, SubCategory1, SubCategory2
        from .signals import save_or_update_unique_category, delete_unique_category
        post_save.connect(save_or_update_unique_category, sender=Category, dispatch_uid="category")
        post_save.connect(save_or_update_unique_category, sender=SubCategory1, dispatch_uid="subcategory1")
        post_save.connect(save_or_update_unique_category, sender=SubCategory2, dispatch_uid="subcategory2")

        post_delete.connect(delete_unique_category, sender=Category, dispatch_uid="del_category")
        post_delete.connect(delete_unique_category, sender=SubCategory1, dispatch_uid="del_subcategory1")
        post_delete.connect(delete_unique_category, sender=SubCategory2, dispatch_uid="del_subcategory2")


