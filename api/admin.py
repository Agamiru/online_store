from django.contrib import admin
from .models import (
    Product, MainFeatures, Brand, Category, SubCategory1,
    SubCategory2, ModelName, Accessories, BoughtTogether
)
from django import forms
from django.forms.widgets import TextInput
from django.forms.fields import JSONField, JSONString
from django.core.exceptions import ValidationError, ObjectDoesNotExist as doesnt_exist

from app_admin.utils import BhphotovideoTableConverter
import json

# from .models import json_default


class SpecsField(JSONField):

    def to_python(self, value):
        if not value:
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
        return "in_database"


class InTheBoxField(JSONField):

    def to_python(self, value):
        if not value:
            return None
        value = str(value)
        # print(f"str_value: {str_value}")
        if value.startswith("[") and value.endswith("]"):
            print("Im a list\n")
            return "in_database"
        items = value.split("\n")
        items_2 = value.split(",")
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
        specs = self.cleaned_data.get("specs")
        # specs.pop("Box Dimensions (LxWxH)")
        # specs.pop("Package Weight")
        if not specs:
            raise ValidationError("This field receives 'None' as value")

        id = self.instance.id
        pd = self.cleaned_data.get("package_dimensions", None)
        w = self.cleaned_data.get("weight")
        print(f"Instance ID: {id}\n")
        try:
            obj = Product.objects.get(pk=id)
            model_specs = obj.specs      # Existing Object specs
            model_itb = obj.in_the_box      # Existing Object in_the_box
            if specs == "in_database":
                self.cleaned_data["specs"] = model_specs

                model_specs_pd = model_specs.get("Box Dimensions (LxWxH)", None)
                model_specs_pd = model_specs_pd[0] if model_specs_pd else None
                model_specs_w = model_specs.get("Package Weight", None)
                model_specs_w = model_specs_w[0] if model_specs_w else None

                if not pd and model_specs_pd is not None:
                    self.cleaned_data["package_dimensions"] = model_specs_pd
                if not w and model_specs_w is not None:
                    self.cleaned_data["weight"] = model_specs_w

            if self.cleaned_data.get("in_the_box") == "in_database":
                self.cleaned_data["in_the_box"] = model_itb

        except doesnt_exist:    # For newly saved products

            try:
                package_dims = specs["Box Dimensions (LxWxH)"]
                # Confirm dims from spec are same as filled, else use dims from specs
                if not pd:
                    self.cleaned_data["package_dimensions"] = package_dims[0]
            except KeyError as e:
                self.add_error("package_dimensions", f"Specs has no {e}")

            try:
                weight = specs["Package Weight"]
                # Confirm weight from spec are same as filled, else use weight from specs
                if not w:
                    self.cleaned_data["weight"] = weight[0]
            except KeyError as e:
                self.add_error("weight", f"Specs has no {e}")

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






    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     pass

    # def add_html_table(self, obj):
    #     return obj.brand

    # add_html_table.empty_value_display = "???"

admin.site.register(MainFeatures)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)
admin.site.register(ModelName)
admin.site.register(Accessories)
admin.site.register(BoughtTogether)
