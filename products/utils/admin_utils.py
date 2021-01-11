import json
import zlib

from django.forms import fields
from django import forms
from django.forms.widgets import Textarea
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm, ModelFormMetaclass


from ..utils.general_utils import BhphotovideoTableConverter


class FormSpecsField(fields.JSONField):
    # Check for 3 possibilities:
    # 1. Value wasn't filled, return None
    # 2. Value comes in HTML, convert to JSON compatible python type and return.
    # 3. Value is string from database, return "in_database".

    widget = Textarea(attrs={
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

        return "in_database"

    def prepare_value(self, value):
        if value is None:
            return
        if isinstance(value, forms.fields.InvalidJSONInput):
            return value
        return json.dumps(value, cls=self.encoder)


class FormCommaNewLineSeparatedField(fields.JSONField):
    widget = Textarea(attrs={
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


class AbstractJoinForm(BaseModelForm, metaclass=ModelFormMetaclass):
    """
    A model form maker where categories and subcategories join models can inherit
    special form cleaning and validation abilities on the admin page.
    """

    def clean(self):
        self._validate_unique = True

        first_field_name, second_field_name = self.get_field_names()

        obj_1 = self.cleaned_data[first_field_name]  # Category or Subcategory Object
        obj_2 = self.cleaned_data[second_field_name]  # Category or Subcategory Object Double

        cat_id_1, cat_id_2 = obj_1.id, obj_2.id    # Category id pair

        if cat_id_1 == cat_id_2:   # A category item cannot be an accessory to itself
            self.add_error(
                f"{second_field_name}", f"{first_field_name} & {second_field_name} cannot have the same values"
            )

        hash_value = f"{cat_id_1}{cat_id_2}"

        # Create a unique hash for the combination
        self.cleaned_data["hash_field"] = zlib.adler32(bytes(hash_value, encoding="utf-8"))
        print(f"hash_field: {self.cleaned_data['hash_field']}")

        return self.cleaned_data

    # Get the two important model field names
    def get_field_names(self):     # Tuple[str, str]
        # Actually third and fourth field names considering the index/id
        # field and hash_field, but for readability let it be first and second
        first_field_name = self._meta.model()._meta.fields[2].name
        second_field_name = self._meta.model()._meta.fields[3].name

        return first_field_name, second_field_name