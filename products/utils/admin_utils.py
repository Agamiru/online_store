import json
from typing import Iterable, Optional, Tuple

from django.forms import fields
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm, ModelFormMetaclass
from django.contrib.postgres.forms import HStoreField
from django.core.validators import URLValidator

from ..utils.general_utils import BhphotovideoTableConverter


def create_pub_ids(
        brand: str, model_name: str, var_values: list) -> Tuple[str, str, str]:
    """
    Returns public ids for product images.
    If variants are available, include them else, ignore them.
    It only caters for one variant for now.
    It is naive of whether image urls actually exists for these fields.
    """
    _ = f"{brand}/{model_name}"  # Just to keep things short
    if var_values:
        var = var_values[0]
        return f"{_}/{var}/image_1", f"{_}/{var}/image_2", f"{_}/{var}/image_3"
    return f"{_}/image_1", f"{_}/image_2", f"{_}/image_3"


class FormSpecsField(fields.JSONField):
    # Check for 3 possibilities:
    # 1. Value wasn't filled, return None
    # 2. Value comes in HTML, convert to JSON compatible python type and return.
    # 3. Value is string from database, return "in_database".

    widget = widgets.Textarea(attrs={
        "placeholder": "Insert HTML specs here",
    })

    def to_python(self, value):
        if value in self.empty_values:
            return None

        value = str(value)
        if value.startswith("<") and value.endswith(">"):  # html check
            converter_obj = BhphotovideoTableConverter(value)
            python_data = converter_obj.to_python_dict()
            # print(f"python_data: {python_data}")
            if isinstance(python_data, (list, dict, int, float, fields.JSONString)):
                return python_data
            else:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        if value.startswith("{") and value.endswith("}"):
            return "in_database"

        raise ValidationError("Invalid input type")

    def prepare_value(self, value):
        if value is None:
            return
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return json.dumps(value, cls=self.encoder)


class FormCommaNewLineSeparatedField(fields.JSONField):
    widget = widgets.Textarea(attrs={
        "placeholder": "Comma or new line separated values",
    })

    def to_python(self, value):
        if value in self.empty_values:
            return [""]

        items = value.split("\n")       # For lists delimited by a new line character
        items_2 = value.split(",")      # For lists delimited by a comma

        # The longer of the two will be the final list
        items = [item.strip() for item in items] if len(items) > len(items_2) else [item.strip() for item in items_2]

        if isinstance(items, (list, dict, int, float, fields.JSONString)):
            return items
        else:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def prepare_value(self, value):
        if value is None:
            return
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return ', '.join(value)


class CustomUrlField(fields.URLField):
    # Set to null rather than empty strings.
    # Product model URL Fields are nullable.
    def to_python(self, value):
        if value == "":
            return None
        return value


class MultiWidgetForHstore(widgets.MultiWidget):
    """
    Key/value multi widgets for HStore Fields
    """
    def __init__(self, widgets_: Optional[Iterable] = None, **kwargs):
        widgets_ = [
            widgets.TextInput(attrs={"placeholder": "Insert Key"}),
            widgets.TextInput(attrs={"placeholder": "Insert Value"}),
        ] if widgets_ is None else widgets_
        super().__init__(widgets_, **kwargs)

    def decompress(self, value):    # decompress stored database format to HTML form format
        if isinstance(value, dict):
            for k, v in value.items():  # Since its just one item to iterate over
                return k, v
        return None, None

    # Value sent to Field's `clean` method.
    def value_from_datadict(self, data, files, name):
        key, val = super().value_from_datadict(data, files, name)
        return {} if (key and val) == "" else {key: val}


class CustomHstoreField(HStoreField):
    """
    Custom HStore Field with key and value widgets
    """

    widget = MultiWidgetForHstore()

    # For aesthetics: Return placeholder value instead of empty curly braces
    def prepare_value(self, value):
        if not value:
            return
        if isinstance(value, dict):
            return value


class AbstractJoinForm(BaseModelForm, metaclass=ModelFormMetaclass):
    """
    A model form maker where categories and subcategories join models can inherit
    special form cleaning and validation abilities on the admin page.
    """

    # A product cannot be an accessory or be bought together with itself.
    def clean(self):
        self._validate_unique = True

        first_field_name, second_field_name = self.get_field_names()

        obj_1 = self.cleaned_data[first_field_name]  # Category or Subcategory Object
        obj_2 = self.cleaned_data[second_field_name]  # Category or Subcategory Object

        cat_id_1, cat_id_2 = obj_1.id, obj_2.id    # Category id pair

        if cat_id_1 == cat_id_2:   # A category item cannot be an accessory to itself
            self.add_error(
                f"{second_field_name}", f"{first_field_name} & {second_field_name} cannot have the same values"
            )
        return self.cleaned_data

    # Get the two important model field names
    def get_field_names(self):     # Tuple[str, str]
        # Actually second and third field names considering the index/id
        # field, but for readability let it be first and second
        first_field_name = self._meta.model()._meta.fields[1].name
        second_field_name = self._meta.model()._meta.fields[2].name

        return first_field_name, second_field_name


class AbstractCategoryForm(BaseModelForm, metaclass=ModelFormMetaclass):
    """
    A model form maker where categories and subcategories models can inherit
    special form fields to avoid duplication.
    """
    alias = FormCommaNewLineSeparatedField(required=False)
    main_features = FormCommaNewLineSeparatedField(required=False)
