from django.contrib import admin
from .models import (
    Product, Brand, Category, SubCategory1,
    SubCategory2, ModelName, CategoryDouble, CategoryAccessoryJoin,
    CategoryBoughtTogetherJoin, Subcat1AccessoryJoin, Subcat1Double,
    Subcat1BoughtTogetherJoin, Subcat2Double, Subcat2AccessoryJoin,
    Subcat2BoughtTogetherJoin, CategoryMainFeatures,
    SubCategory1MainFeatures, SubCategory2MainFeatures,
)

from django import forms
from django.forms.widgets import TextInput
from django.forms.fields import JSONField, JSONString
from django.core.exceptions import ValidationError, ObjectDoesNotExist as doesntExist
from django.contrib import messages
import zlib
from django.forms.models import BaseModelForm, ModelFormMetaclass

from app_admin.utils import BhphotovideoTableConverter
import json
from typing import List, Tuple, Any

# from .models import json_default


################### PRODUCT ######################


class SpecsField(JSONField):
    # Check for 3 possibilities:
    # 1. Value wasn't filled.
    # 2. Value comes in expected format.
    # 3. Value is default-filled "null".
    def to_python(self, value):
        if value in self.empty_values:
            return None
        value = str(value)
        if value.startswith("<") and value.endswith(">"):  # html check
            converter_obj = BhphotovideoTableConverter(value)
            python_data = converter_obj.to_python_dict()
            # print(f"python_data: {python_data}")
            if isinstance(python_data, (list, dict, int, float, JSONString)):
                return python_data
            else:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        if value == "null":      # Default value check
            return "null"

        return "in_database"

    def prepare_value(self, value):
        if value == "null":
            return json.dumps(None, cls=self.encoder)
        # Todo: Calling super here brings funny behaviour, dont know why
        # super().prepare_value(value)
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return json.dumps(value, cls=self.encoder)


class CommaNewLineSeparatedField(JSONField):
    widget = TextInput(attrs={
        "placeholder": "Comma or new line separated values",
        "size": "40",
    })

    def to_python(self, value):
        if value in self.empty_values:
            return None

        if value.startswith("[") and value.endswith("]"):       # List checker
            return "in_database"

        if value == "null":     # default checker
            return value

        print("Preparing List\n")
        items = value.split("\n")       # For lists delimited by a new line character
        items_2 = value.split(",")      # For lists delimited by a comma

        # The longer of the two will be the final list
        items = [item.strip() for item in items] if len(items) > len(items_2) else [item.strip() for item in items_2]

        if isinstance(items, (list, dict, int, float, JSONString)):
            return items
        else:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def prepare_value(self, value):
        if value == "null":
            return json.dumps(None, cls=self.encoder)
        # Todo: Calling super here brings funny behaviour, dont know why
        # super().prepare_value(value)
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return json.dumps(value, cls=self.encoder)


class ProductForm(forms.ModelForm):

    specs = SpecsField()
    in_the_box = CommaNewLineSeparatedField()

    def clean(self):
        self._validate_unique = True
        specs = self.cleaned_data.get("specs")  # Can be "in_database", json or "null"

        if not specs:       # Ideally, field validations should have checked for this already
            raise ValidationError("This field receives 'None' as value")

        id = self.instance.id
        pd = self.cleaned_data.get("package_dimensions")  # Package Dimensions
        w = self.cleaned_data.get("weight")     # Weight

        try:
            obj = Product.objects.get(pk=id)    # Try fetching existing object
            model_specs = obj.specs      # Existing Object specs
            model_itb = obj.in_the_box      # Existing Object in_the_box
            if specs == "in_database":
                # Sometimes, artifacts are introduced in the field input while displaying
                # existing values (bound_data).
                # It's best to use values from the model itself while saving to avoid this.
                self.cleaned_data["specs"] = model_specs

                model_specs_pd = model_specs.get("Box Dimensions (LxWxH)")
                model_specs_pd = model_specs_pd[0] if model_specs_pd else None
                model_specs_w = model_specs.get("Package Weight")
                model_specs_w = model_specs_w[0] if model_specs_w else None

                if not pd and model_specs_pd is not None:
                    self.cleaned_data["package_dimensions"] = model_specs_pd
                if not w and model_specs_w is not None:
                    self.cleaned_data["weight"] = model_specs_w

            if self.cleaned_data.get("in_the_box") == "in_database":
                self.cleaned_data["in_the_box"] = model_itb

        except doesntExist:    # For newly saved products

            try:
                package_dims = specs["Box Dimensions (LxWxH)"]
                # Use filled package dimensions if available, else take from specs
                if not pd:
                    self.cleaned_data["package_dimensions"] = package_dims[0]

            # Key error in case specs has no package dimensions
            # Type error in case "null" is returned as string indices must be integers
            except (KeyError, TypeError):
                self.cleaned_data["specs"] = None
                pass
                # Todo: Should display a message notifying the user there are no package_dimensions
                # self.add_error("package_dimensions", f"Specs has no {e}")

            try:
                weight = specs["Package Weight"]
                # Confirm weight from spec are same as filled, else use weight from specs
                if not w:
                    self.cleaned_data["weight"] = weight[0]
            except (KeyError, TypeError):
                pass
                # Todo: Should display a message notifying the user there is no weight
                # self.add_error("weight", f"Specs has no {e}")

        return self.cleaned_data

    class Meta:
        model = Product
        fields = "__all__"


# Abstract Model Form Maker with custom methods
# To be inherited by Categories and Subcategories
class AbstractJoinForm(BaseModelForm, metaclass=ModelFormMetaclass):

    def clean(self):
        self._validate_unique = True

        first_field_name, second_field_name = self.get_field_names()

        obj_1 = self.cleaned_data[first_field_name]  # Category or Subcategory Object
        obj_2 = self.cleaned_data[second_field_name]  # Category or Subcategory Object Double

        obj_2_field_name = obj_2._meta.fields[1].name  # Category or Subcategory Object Double main field name

        cat_id_1 = obj_1.id
        try:
            cat_id_2 = getattr(obj_2, obj_2_field_name).id   # Check to ensure object has a double indeed
        except AttributeError:
            self.add_error(obj_2_field_name, "Record doesn't exist")
        else:
            if cat_id_1 == cat_id_2:   # A category item cannot be an accessory to itself
                self.add_error(
                    f"{second_field_name}", f"{first_field_name} & {second_field_name} cannot have the same values"
                )

            hash_value = f"{cat_id_1}{cat_id_2}"
            # print(f"hash_value: {hash_value}\n")

            # Create a unique hash for the combination
            self.cleaned_data["hash_field"] = zlib.adler32(bytes(hash_value, encoding="utf-8"))
            # print(f"hash_field: {self.cleaned_data['hash_field']}")

        return self.cleaned_data

    # Get the two important model field names
    def get_field_names(self):     # Tuple[str, str]
        # Actually second and third field names considering the index/id field
        # But for readability let it be first and second
        first_field_name = self._meta.model()._meta.fields[1].name
        second_field_name = self._meta.model()._meta.fields[2].name

        return first_field_name, second_field_name


class AbstractMainFeaturesForm(BaseModelForm, metaclass=ModelFormMetaclass):

    def clean(self):  # Can receive "in_database", "null", or List
        self._validate_unique = True
        second_field_name = self.get_field_name()
        # Todo: Something has to be done about this null field
        if self.cleaned_data.get(second_field_name) == "null":
            pass

        if self.cleaned_data.get(second_field_name) == "in_database":
            # Sometimes, artifacts are introduced in the field input while displaying
            # existing values (bound_data).
            # It's best to use values from the model itself while saving to avoid this.
            try:
                obj_instance = CategoryMainFeatures.objects.get(pk=self.instance.id)
                obj_features = getattr(obj_instance, second_field_name)
                self.cleaned_data["features"] = obj_features
            except doesntExist:     # Shouldn't happen but just in case
                self.cleaned_data["features"] = "null"

    def get_field_name(self):     # Tuple[str, str]
        # Actually third field name considering the index/id field
        # but for readability let it be second
        second_field_name = self._meta.model()._meta.fields[2].name

        return second_field_name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "short_desc")
    # list_display_links = ("brand", "model_name",)
    list_editable = ("price", "short_desc")

    form = ProductForm


###################### CATEGORY #######################

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        acc_instance = CategoryDouble.objects.create(cat_id=obj)
        acc_instance.save()


class CategoryAccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = CategoryAccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class CategoryBoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = CategoryBoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class CategoryMainFeaturesForm(AbstractMainFeaturesForm):
    features = CommaNewLineSeparatedField()

    class Meta:
        model = CategoryMainFeatures
        fields = "__all__"


@admin.register(CategoryAccessoryJoin)
class CategoryAccessoryJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]
    form = CategoryAccessoryJoinForm


@admin.register(CategoryBoughtTogetherJoin)
class CategoryBoughtTogetherJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]
    form = CategoryBoughtTogetherJoinForm


@admin.register(CategoryMainFeatures)
class CategoryMainFeaturesAdmin(admin.ModelAdmin):
    form = CategoryMainFeaturesForm


################# SUB CATEGORY 1 #########################


@admin.register(SubCategory1)
class Subcat1Admin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        acc_instance = Subcat1Double.objects.create(subcat_1_id=obj)
        acc_instance.save()


class Subcat1AccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat1AccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class Subcat1BoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat1BoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class SubCategory1MainFeaturesForm(AbstractMainFeaturesForm):
    features = CommaNewLineSeparatedField()

    class Meta:
        model = SubCategory1MainFeatures
        fields = "__all__"


@admin.register(Subcat1AccessoryJoin)
class Subcat1AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat1AccessoryJoinForm


@admin.register(Subcat1BoughtTogetherJoin)
class Subcat1BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat1BoughtTogetherJoinForm


@admin.register(SubCategory1MainFeatures)
class Subcategory1MainFeaturesAdmin(admin.ModelAdmin):
    form = SubCategory1MainFeaturesForm


################# SUB CATEGORY 2 #########################

@admin.register(SubCategory2)
class Subcat2Admin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        acc_instance = Subcat2Double.objects.create(subcat_1_id=obj)
        acc_instance.save()


class Subcat2AccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat2AccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class Subcat2BoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat2BoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class SubCategory2MainFeaturesForm(AbstractMainFeaturesForm):
    features = CommaNewLineSeparatedField()

    class Meta:
        model = SubCategory2MainFeatures
        fields = "__all__"


@admin.register(Subcat2AccessoryJoin)
class Subcat2AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat2AccessoryJoinForm


@admin.register(Subcat2BoughtTogetherJoin)
class Subcat2BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat2BoughtTogetherJoinForm


@admin.register(SubCategory2MainFeatures)
class Subcategory2MainFeaturesAdmin(admin.ModelAdmin):
    form = SubCategory2MainFeaturesForm


# admin.site.register(MainFeatures)
admin.site.register(Brand)
admin.site.register(ModelName)

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(CategoryAccessoryJoin, CategoryAccessoryJoinAdmin)
# admin.site.register(CategoryBoughtTogetherJoin, CategoryBoughtTogetherJoinAdmin)
#
# admin.site.register(SubCategory1, Subcat1Admin)
# admin.site.register(Subcat1AccessoryJoin, Subcat1AccessoryJoinAdmin)
# admin.site.register(Subcat1BoughtTogetherJoin, Subcat1BoughtTogetherJoinAdmin)
#
# admin.site.register(SubCategory2, Subcat2Admin)
# admin.site.register(Subcat2AccessoryJoin, Subcat2AccessoryJoinAdmin)
# admin.site.register(Subcat2BoughtTogetherJoin, Subcat2BoughtTogetherJoinAdmin)

