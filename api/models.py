from django.db import models
# from .model_utils import *
# Create your models here.
import json


def json_default():
    null = json.dumps(None)

    return null


def storage_dir(instance, filename) -> str:
    product_instance = Product.objects.get(pk=instance.prod_id.id)
    if not product_instance:
        raise ValueError("Model received None as response")
    brand_name = product_instance.get_brand_name().replace(" ", "_")
    model_name = product_instance.model_name.name.replace(" ", "_")

    return f"{brand_name}/{model_name}/{filename}"


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


class SubCategory1(models.Model):

    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategory_1", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = "subcategory_1"
        verbose_name_plural = "subcategories_1"


class SubCategory2(models.Model):

    sub_cat_id = models.ForeignKey(
        SubCategory1, on_delete=models.SET_NULL, related_name="subcategory_2", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = "subcategory_2"
        verbose_name_plural = "subcategories_2"


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Generic")

    class Meta:
        db_table = "brands"


class ModelName(models.Model):
    brand_id = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="model",
    )
    name = models.CharField(max_length=100, unique=True)


class MainFeatures(models.Model):
    cat_id = models.ForeignKey(
        Category, related_name="features",
        on_delete=models.CASCADE, null=False
    )
    features = models.JSONField(default=json_default)

    class Meta:
        db_table = "features"


class Image(models.Model):
    full_image = models.ImageField(null=False, upload_to=storage_dir)
    date_uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "images"


class Accessories(models.Model):
    accessories = models.JSONField(default=json_default)

    class Meta:
        db_table = "accessories"
        verbose_name_plural = "accessories"


class BoughtTogether(models.Model):
    bought_together = models.JSONField(default=json_default)

    class Meta:
        db_table = "bought_together"
        verbose_name_plural = "bought_together"


# Todo: Create an admin page for adding products
class Product(models.Model):
    cat_id = models.ForeignKey(
        Category, related_name="product", on_delete=models.PROTECT, null=False
    )

    sub_cat_id_1 = models.ForeignKey(
        SubCategory1, on_delete=models.SET_NULL, related_name="product",
        null=True
    )

    sub_cat_id_2 = models.ForeignKey(
        SubCategory2, on_delete=models.SET_NULL, related_name="product",
        null=True
    )

    main_features = models.OneToOneField(
        MainFeatures, on_delete=models.SET_NULL,
        related_name="product", null=True,
    )

    brand = models.ForeignKey(
        Brand, related_name="product", on_delete=models.SET_DEFAULT, null=False,
        to_field="name", default="Generic",
    )

    model_name = models.OneToOneField(
        ModelName, on_delete=models.SET_NULL, related_name="product", null=True,
        to_field="name",
    )

    image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="product", null=True
    )

    accessories = models.ForeignKey(
        Accessories, on_delete=models.SET_NULL, related_name="product", null=True
    )

    bought_together = models.ForeignKey(
        BoughtTogether, on_delete=models.SET_NULL, related_name="product", null=True
    )

    short_desc = models.CharField("Short Description", max_length=200)
    price = models.FloatField(null=False)
    in_the_box = models.JSONField(default=json_default)
    specs = models.JSONField(default=json_default)
    package_dimensions = models.CharField(max_length=200, null=True)
    weight = models.CharField(max_length=200, null=True)

    def get_brand_name(self) -> str:
        brand_obj = Brand.objects.get(pk=self.brand.id)
        brand_name = brand_obj.name

        return brand_name

    def get_product_name(self) -> str:
        brand_name = self.get_brand_name()

        return f"{brand_name} {self.model_name}"

    class Meta:
        db_table = "products"



