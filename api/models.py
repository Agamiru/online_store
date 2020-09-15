from django.db import models
from django.core.exceptions import ObjectDoesNotExist as doesnt_exist
from .model_utils import *
# Create your models here.
import json
from typing import List, Tuple


def json_default():
    return json.dumps(None)


def storage_dir(instance, filename) -> str:
    brand_name = instance.brand
    model_name = instance.model_name.name.replace(" ", "_")

    return f"{brand_name}/{model_name}/{filename}"


def choices_getter(model, name_field: str = "name") -> List[Tuple[str, str]]:
    all_objects = model.objects.all()
    if not all_objects:
        return [("NONE", "None")]
    choices_list = []
    for obj in all_objects:
        try:
            choice = getattr(obj, name_field)
            choices_list.append(choice)
        except AttributeError:
            raise AttributeError(f"Your model has no such attribute <{name_field}>")

    choices_list = [(choice.upper(), choice.title()) for choice in choices_list]
    return choices_list


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


class CategoryDouble(models.Model):
    cat_id = models.OneToOneField(
        Category, on_delete=models.CASCADE,
    )

    def __str__(self):
        cat_name = Category.objects.get(pk=self.cat_id.id).name
        return f"{cat_name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_double"
        verbose_name_plural = "category_double"


class CategoryAccessoryJoin(models.Model):
    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="accessory_join", null=True,
        blank=False,
    )
    accessory_id = models.ForeignKey(
        CategoryDouble, on_delete=models.SET_NULL, related_name="category_join",
        null=True, blank=False, to_field="cat_id"
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Accessory for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_accessories"
        verbose_name_plural = "category_accessories"


class CategoryBoughtTogetherJoin(models.Model):
    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="bought_together_join", null=True,
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        CategoryDouble, on_delete=models.SET_NULL, related_name="bought_join",
        null=True, blank=False, to_field="cat_id"
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Frequently bought together for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_bought_together"
        verbose_name_plural = "category_bought_together"


class SubCategory1(models.Model):

    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategory_1", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "subcategory_1"
        verbose_name_plural = "subcategories_1"


class SubCategory2(models.Model):

    subcat_id = models.ForeignKey(
        SubCategory1, on_delete=models.SET_NULL, related_name="subcategory_2", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "subcategory_2"
        verbose_name_plural = "subcategories_2"


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Generic")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "brands"


class ModelName(models.Model):
    brand_id = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, related_name="model",
        null=True
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class AbstractModel(models.Model):

    cat_id = models.ForeignKey(
        Category, models.SET_NULL, null=True,
    )
    subcat_1_id = models.ForeignKey(
        SubCategory1, models.SET_NULL, null=True, blank=True,
    )

    subcat_2_id = models.ForeignKey(
        SubCategory2, models.SET_NULL, null=True, blank=True,
    )

    def return_appropriate_category(self):
        try:
            sub_cat_2_name = self.subcat_2_id.name
            return sub_cat_2_name
        except (doesnt_exist, AttributeError):  # Attribute error means it returned None type
            try:
                sub_cat_1_name = self.subcat_1_id.name
                return sub_cat_1_name
            except (doesnt_exist, AttributeError):
                try:
                    return self.cat_id.name
                except (doesnt_exist, AttributeError):
                    return None

    class Meta:
        abstract = True


# class MainFeatures(AbstractModel):
#
#     features = models.JSONField(default=json_default)
#
#     def __str__(self):
#         cat_name = self.return_appropriate_category()
#         return f"Main Features for '{cat_name}'"
#
#     class Meta:
#         db_table = "features"


# Todo: Create an admin page for adding products
class Product(AbstractModel):

    # main_features = models.OneToOneField(
    #     MainFeatures, on_delete=models.SET_NULL,
    #     related_name="product", null=True, blank=True,
    # )

    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, related_name="product",
        null=True, default="Generic"
    )

    model_name = models.OneToOneField(
        ModelName, on_delete=models.SET_NULL, related_name="product", null=True,
        to_field="name",
    )

    image = models.ImageField(null=True, upload_to=storage_dir, blank=True)

    short_desc = models.CharField("Short Description", max_length=200)
    price = models.FloatField(null=False)
    available = models.BooleanField(default=True)
    in_the_box = models.JSONField(default=json_default)
    specs = models.JSONField(default=json_default)
    package_dimensions = models.CharField(max_length=200, null=True, blank=True,)
    weight = models.CharField(max_length=200, null=True, blank=True,)
    date_created = models.DateTimeField(auto_now=True)

    def get_brand_name(self) -> str:
        try:
            brand_obj = Brand.objects.get(pk=self.brand.id)
            brand_name = brand_obj.name
        except AttributeError:
            return "None"

        return brand_name

    def product_name(self) -> str:
        brand_name = self.get_brand_name()

        return f"{brand_name} {self.model_name}"

    def __str__(self):
        cat_name = self.return_appropriate_category()
        return f"{self.product_name()} in {cat_name}"

    class Meta:
        db_table = "products"

