import json
from typing import Union

from django.db import models
from django.core.exceptions import ObjectDoesNotExist as doesnt_exist
from django.contrib.postgres.fields import ArrayField, HStoreField

from .utils.model_utils import CrossModelUniqueNameValidator
from .utils.manager_utils import SearchResult
from .managers import ProductManager, CategoryManagers


def json_default():
    return json.dumps(None)


def storage_dir(instance, filename) -> str:
    brand_name = instance.brand
    model_name = instance.model_name.name.replace(" ", "_")

    return f"{brand_name}/{model_name}/{filename}"


class UniqueCategory(models.Model):
    """
    Category name should be unique even across different category models,
    this model is used as a backend for the cross_model_validator (see below)
    to validate names as unique before saving.

    A post_save signal has been set up on all category models, to automatically
    populate this model.
    """
    name = models.CharField(max_length=200, unique=True)
    model_name = models.CharField(max_length=200)
    cat_id = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "unique_category"
        constraints = [
            models.UniqueConstraint(name="whatever", fields=["model_name", "cat_id"])
        ]


cross_model_validator = CrossModelUniqueNameValidator(UniqueCategory)


# Abstract model for categories
class CategoriesAbstractModel(models.Model):

    objects = CategoryManagers()

    def save(self, *args, **kwargs):
        # When creating model instances from the application or shell, full_clean method
        # which validates field input is bypassed. This hook ensures it's still checked
        # before save. For forms, validation will be done twice, small price to pay.
        cross_model_validator(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# Category
class Category(CategoriesAbstractModel):
    name = models.CharField(
        validators=[cross_model_validator],
        max_length=100, unique=True, null=False
    )
    alias = ArrayField(models.CharField(max_length=50, null=True, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=50, blank=False))

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

    def __str__(self):
        return f"Accessory for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_accessories"
        verbose_name_plural = "category_accessories"
        constraints = [
            models.UniqueConstraint(
                fields=["cat_id", "accessory_id"], name="cat_acc_join"
            )
        ]


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

    def __str__(self):
        return f"Frequently bought together for {self.cat_id.name}" if self.cat_id else "Null"

    class Meta:
        db_table = "category_bought_together"
        verbose_name_plural = "category_bought_together"
        constraints = [
            models.UniqueConstraint(
                fields=["cat_id", "bought_together_id"], name="cat_b2g_join"
            )
        ]


# Subcategory 1
class SubCategory1(CategoriesAbstractModel):
    cat_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="subcategory_1", null=True
    )
    name = models.CharField(
        validators=[cross_model_validator],
        max_length=100, unique=True, null=False
    )
    alias = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=50, blank=True), default=list)

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

    def __str__(self):
        return f"Accessory for {self.subcat_1_id.name}" if self.subcat_1_id else "Null"

    class Meta:
        db_table = "subcategory_1_accessories"
        verbose_name_plural = "subcategory_1_accessories"
        constraints = [
            models.UniqueConstraint(
                fields=["subcat_1_id", "accessory_id"], name="subcat1_acc_join"
            )
        ]


class Subcat1BoughtTogetherJoin(models.Model):
    subcat_1_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="bought_together_join",
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        SubCategory1, on_delete=models.CASCADE, related_name="bought_join",
        blank=False,
    )

    def __str__(self):
        return f"Frequently bought together for {self.subcat_1_id.name}" if self.subcat_1_id else "Null"

    class Meta:
        db_table = "subcategory_1_bought_together"
        verbose_name_plural = "subcategory_1_bought_together"
        constraints = [
            models.UniqueConstraint(
                fields=["subcat_1_id", "bought_together_id"], name="subcat1_b2g_join"
            )
        ]


# Subcategory 2
class SubCategory2(CategoriesAbstractModel):
    subcat_1_id = models.ForeignKey(
        SubCategory1, on_delete=models.SET_NULL, related_name="subcategory_2", null=True
    )
    name = models.CharField(
        validators=[cross_model_validator],
        max_length=100, unique=True, null=False
    )
    alias = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    main_features = ArrayField(models.CharField(max_length=50, blank=True), default=list)

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

    def __str__(self):
        return f"Accessory for {self.subcat_2_id.name}" if self.subcat_2_id else "Null"

    class Meta:
        db_table = "subcategory_2_accessories"
        verbose_name_plural = "subcategory_2_accessories"
        constraints = [
            models.UniqueConstraint(
                fields=["subcat_2_id", "accessory_id"], name="subcat2_acc_join"
            )
        ]


class Subcat2BoughtTogetherJoin(models.Model):
    subcat_2_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="bought_together_join",
        blank=False,
    )
    bought_together_id = models.ForeignKey(
        SubCategory2, on_delete=models.CASCADE, related_name="bought_join",
        blank=False,
    )

    def __str__(self):
        return f"Frequently bought together for {self.subcat_2_id.name}" if self.subcat_2_id else "Null"

    class Meta:
        db_table = "subcategory_2_bought_together"
        verbose_name_plural = "subcategory_2_bought_together"
        constraints = [
            models.UniqueConstraint(
                fields=["subcat_2_id", "bought_together_id"], name="subcat2_b2g_join"
            )
        ]


def search_all_categories(value) -> Union[SearchResult, None]:
    all_categories = [Category, SubCategory1, SubCategory2]
    for cat in all_categories:
        result = cat.objects.full_search(value)
        if result:
            return result


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


# Abstract model for Products
class ProductAbstractModel(models.Model):

    cat_id = models.ForeignKey(
        Category, models.SET_NULL, null=True, related_name="products"
    )
    subcat_1_id = models.ForeignKey(
        SubCategory1, models.SET_NULL, null=True, blank=True, related_name="products"
    )

    subcat_2_id = models.ForeignKey(
        SubCategory2, models.SET_NULL, null=True, blank=True, related_name="products"
    )
    # Variants are used to determine the final name of the product.
    # Sometimes a variant key might have possible multiple values, hence the product - other
    # possible names e.g. generation can be "G3, 3rd Gen, 3G, Gen 3, or 3rd Generation"
    # This field stores those names for search purposes.
    # other_possible_names = ArrayField(
    #     models.CharField(max_length=20, blank=True), default=list
    # )
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


def get_generic_brand():
    return Brand.objects.get_or_create(name="Generic")[0]

# Todo: Add array field that contains other
class Product(ProductAbstractModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.SET(get_generic_brand), related_name="products",
        null=True,
    )
    model_name = models.ForeignKey(
        ModelName, on_delete=models.SET_NULL, related_name="products", null=True,
    )
    full_name = models.CharField(max_length=200, blank=True, null=False, unique=True)

    image = models.ImageField(null=True, upload_to=storage_dir, blank=True)

    short_desc = models.CharField("Short Description", max_length=200)
    # Todo add a comma separated price field in admin_utils, hint: use regex
    price = models.FloatField(null=False)
    available = models.BooleanField(default=True)
    in_the_box = models.JSONField(default=json_default)
    specs = models.JSONField(default=json_default)
    package_dimensions = models.CharField(max_length=200, null=True, blank=True,)
    weight = models.CharField(max_length=200, null=True, blank=True,)
    date_created = models.DateTimeField(auto_now=True)
    # Todo: Enforce during model save.
    # Todo: Might refactor into an H-store of main_f : alias
    # If specs_from_bhpv is False, map these fields
    features_alias = ArrayField(
        models.CharField(max_length=20, blank=True), default=list
    )
    # Proper admin widget needed to facilitate this
    # Todo: Ensure value for keys like 'generation', 'version' etc are properly inputed in admin
    variants = HStoreField(default=dict)

    objects = ProductManager()

    def get_brand_name(self) -> str:
        brand_obj = Brand.objects.get(pk=self.brand.id)
        return brand_obj.name

    def product_name(self) -> str:
        brand_name = self.get_brand_name()
        # model_name can be null/None if deleted
        return f"{brand_name} {self.model_name if self.model_name else ''}"

    def save(self, *args, **kwargs):
        full_name = self.product_name()
        self.full_name = full_name
        super().save(*args, **kwargs)

    def __str__(self):
        cat_name = self.return_appropriate_category()
        return f"{self.product_name()} in {cat_name}"

    class Meta:
        db_table = "products"
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "model_name", "variants"], name="product_variants"
            )
        ]



