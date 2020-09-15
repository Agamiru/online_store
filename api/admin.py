from django.contrib import admin
from .models import (
    Product, Brand, Category, SubCategory1,
    SubCategory2, ModelName, CategoryDouble, CategoryAccessoryJoin,
    CategoryBoughtTogetherJoin,
)
from django import forms
from django.forms.widgets import TextInput
from django.forms.fields import JSONField, JSONString
from django.core.exceptions import ValidationError, ObjectDoesNotExist as doesntExist
from django.contrib import messages
import zlib

from app_admin.utils import BhphotovideoTableConverter
import json

# from .models import json_default


class SpecsField(JSONField):
    # Check for 3 possibilities:
    # 1. Value wasn't filled.
    # 2. Value comes in expected format.
    # 3. Value is default-filled "null".
    def to_python(self, value):
        if not value:       # Value wasn't filled
            return None
        string_value = str(value)
        if string_value.startswith("<") and string_value.endswith(">"):  # html check
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
        if string_value == "null":      # Default value check
            return "null"

        return "in_database"


class InTheBoxField(JSONField):

    def to_python(self, value):
        if not value:
            return None
        value = str(value)
        if value.startswith("[") and value.endswith("]"):       # List checker
            return "in_database"

        if value == "null":     # default checker
            return "null"

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


class ProductForm(forms.ModelForm):

    specs = SpecsField()
    in_the_box = InTheBoxField()

    def clean(self):
        self._validate_unique = True
        specs = self.cleaned_data.get("specs")  # Can be None, Html or "null"
        # specs.pop("Box Dimensions (LxWxH)")
        # specs.pop("Package Weight")
        if not specs:       # Ideally, field validations should have checked for this already
            raise ValidationError("This field receives 'None' as value")

        if specs == "null":
            self.cleaned_data["specs"] = json.dumps(None)

        if self.cleaned_data["in_the_box"] == "null":
            self.cleaned_data["in_the_box"] = json.dumps(None)

        id = self.instance.id
        pd = self.cleaned_data.get("package_dimensions")  # Package Dimensions
        w = self.cleaned_data.get("weight")     # Weight

        try:
            obj = Product.objects.get(pk=id)    # Try fetching existing object
            model_specs = obj.specs      # Existing Object specs
            model_itb = obj.in_the_box      # Existing Object in_the_box
            if specs == "in_database":
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "short_desc")
    # list_display_links = ("brand", "model_name",)
    list_editable = ("price", "short_desc")

    form = ProductForm


class CategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        acc_instance = CategoryDouble.objects.create(cat_id=obj)
        acc_instance.save()


class CategoryAccessoryJoinForm(forms.ModelForm):

    def clean(self):
        self._validate_unique = True
        cat_id_1 = self.cleaned_data["cat_id"].id
        cat_id_2 = self.cleaned_data["accessory_id"].cat_id.id

        if cat_id_1 == cat_id_2:
            self.add_error("accessory_id", "Cannot add the same objects")

        hash_value = f"{cat_id_1}{cat_id_2}"
        # print(f"hash_value: {hash_value}\n")

        self.cleaned_data["hash_field"] = zlib.adler32(bytes(hash_value, encoding="utf-8"))
        # print(f"hash_field: {self.cleaned_data['hash_field']}")

        return self.cleaned_data

    class Meta:
        model = CategoryAccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class CategoryAccessoryJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]

    form = CategoryAccessoryJoinForm


class CategoryBoughtTogetherJoinForm(forms.ModelForm):

    def clean(self):
        self._validate_unique = True
        cat_id_1 = self.cleaned_data["cat_id"].id
        cat_id_2 = self.cleaned_data["bought_together_id"].cat_id.id

        if cat_id_1 == cat_id_2:
            self.add_error("bought_together_id", "Cannot add the same objects")

        hash_value = f"{cat_id_1}{cat_id_2}"
        # print(f"hash_value: {hash_value}\n")

        self.cleaned_data["hash_field"] = zlib.adler32(bytes(hash_value, encoding="utf-8"))
        # print(f"hash_field: {self.cleaned_data['hash_field']}")

        return self.cleaned_data

    class Meta:
        model = CategoryBoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "disabled": True})
        }


class CategoryBoughtTogetherJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]

    form = CategoryBoughtTogetherJoinForm




# admin.site.register(MainFeatures)
admin.site.register(Brand)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)
admin.site.register(ModelName)
# admin.site.register(CategoryAccessories)
admin.site.register(CategoryAccessoryJoin, CategoryAccessoryJoinAdmin)
# admin.site.register(Accessories)
admin.site.register(CategoryBoughtTogetherJoin, CategoryBoughtTogetherJoinAdmin)
