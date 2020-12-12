import json
from typing import List, Tuple

from django.db import models
from django.core.exceptions import ObjectDoesNotExist as doesnt_exist
from django.contrib.postgres.fields import ArrayField


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
    # Todo: name should also be unique to Category and Subcat2 names, add validator.

    name = models.CharField(max_length=100, unique=True, null=False)
    alias = ArrayField(models.CharField(max_length=20, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=20, blank=False))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"


# Accessories for Categories
class CategoryAccessoryJoin(models.Model):
    cat_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="accessory_join",
        blank=False,
    )
    accessory_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Accessory for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_accessories"
        verbose_name_plural = "category_accessories"


# Bought Together for Categories
class CategoryBoughtTogetherJoin(models.Model):
    cat_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="bought_together_join",
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="bought_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Frequently bought together for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_bought_together"
        verbose_name_plural = "category_bought_together"


# Subcategory 1
class SubCategory1(models.Model):
    # Todo: name should also be unique to Category and Subcat2 names, add validator.

    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategory_1", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)
    alias = ArrayField(models.CharField(max_length=20, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=20, blank=True), default=list)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "subcategory_1"
        verbose_name_plural = "subcategories_1"


class Subcat1AccessoryJoin(models.Model):

    subcat_1_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="accessory_join",
        blank=False,
    )
    accessory_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="category_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Accessory for {self.subcat_1_id.name}" if self.subcat_1_id else "Null"

    class Meta:
        db_table = "subcategory_1_accessories"
        verbose_name_plural = "subcategory_1_accessories"


class Subcat1BoughtTogetherJoin(models.Model):
    subcat_1_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="bought_together_join",
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="bought_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Frequently bought together for {self.subcat_1_id.name}" if self.subcat_1_id else "Null"

    class Meta:
        db_table = "subcategory_1_bought_together"
        verbose_name_plural = "subcategory_1_bought_together"


# Subcategory 2
class SubCategory2(models.Model):
    # Todo: name should also be unique to Category and Subcat1 names, add validator.

    subcat_1_id = models.ForeignKey(
        SubCategory1, on_delete=models.SET_NULL, related_name="subcategory_2", null=True
    )
    name = models.CharField(max_length=100, unique=True, null=False)
    alias = ArrayField(models.CharField(max_length=20, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=20, blank=True), default=list)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "subcategory_2"
        verbose_name_plural = "subcategories_2"


class Subcat2AccessoryJoin(models.Model):

    subcat_2_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="accessory_join",
        blank=False,
    )
    accessory_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="category_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Accessory for {self.subcat_2_id.name}" if self.subcat_2_id else "Null"

    class Meta:
        db_table = "subcategory_2_accessories"
        verbose_name_plural = "subcategory_2_accessories"


class Subcat2BoughtTogetherJoin(models.Model):
    subcat_2_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="bought_together_join",
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="bought_join",
        blank=False,
    )
    hash_field = models.IntegerField(blank=True, unique=True)

    def __str__(self):
        return f"Frequently bought together for {self.subcat_2_id.name}" if self.subcat_2_id else "Null"

    class Meta:
        db_table = "subcategory_2_bought_together"
        verbose_name_plural = "subcategory_2_bought_together"


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

    class Meta:
        db_table = "model_name"


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

    comes_in_pairs = models.BooleanField(default=False)
    specs_from_bhpv = models.BooleanField(default=True)

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


class Product(AbstractModel):

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
    # If specs_from_bhpv is False, map these fields
    features_alias = ArrayField(
        models.CharField(max_length=20, blank=False), default=list
    )

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


