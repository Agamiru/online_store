from typing import List
import json

from django.db.models.fields.json import JSONField
from django.db.models import ObjectDoesNotExist as doesnt_exist
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CrossModelUniqueNameValidator:
    """
    Check that model 'name' attribute is unique amongst other category
    models with same attribute name.

    :param model: Model backend to perform look up.
    """
    message = "%(category_name)s object with name '%(value)s' already exists"
    code = "invalid"

    def __init__(self, model, message=None, code=None):
        # if not isinstance(model, list) and (len(model) == 1):
        #     raise TypeError("'model' arg must be a one-item list")
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.model = model

    def __call__(self, value):
        value = str(value)
        try:
            unique_val = self.model.objects.get(name=value)
            model_name = unique_val.model_name
            raise ValidationError(
                message=self.message, code=self.code,
                params={"category_name": model_name, "value": value}
            )
        except doesnt_exist:
            pass

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.message == other.message and
                self.code == other.code
        )


class GetMainFeatures:
    """
    Uses the main_features attribute of different product categories
    to return the appropriate features for the product.

    It will skip keys it doesnt find in specs. In the future, this should
    warn the user.
    """

    def __init__(self, product_instance):
        self.product_instance = product_instance
        self.has_features = False
        self.features_list = None
        self.values_list = []
        self.features_dict = None   # Final product
        self.skipped: List[int] = []   # List of index of skipped features

    def final(self):
        """
        Main hook to get the final dict, do not use 'self.features_dict'
        """
        count = 0
        while not self.values_list:
            count += 1
            if count > 1:
                return {}
            self.features()
        return self.features_dict

    # Refactoring this function causes dynamic references
    ### Do not Refactor name###
    def features(self):
        """
        Creates the main_features final dict
        """
        self.set_features_list()
        specs = self.product_instance.specs
        skipped: List[int] = []
        self.features_dict = {}
        count = 0
        for feat in self.features_list:
            try:
                self.features_dict.update({feat: specs[feat]})
                self.values_list.append(specs[feat])
            # If for some reason specs has no such features
            except KeyError:
                skipped.append(count)
            count += 1

        if skipped:
            self.skipped = skipped

    def set_features_list(self):
        """
        Sets features list which will be used to create features_dict.
        """
        approp_cat = self.return_appropriate_category_instance()
        if not self.product_instance.specs_from_bhpv:
            self.specs_key_switcher(approp_cat)
        self.features_list = approp_cat.main_features

    def specs_key_switcher(self, approp_cat):
        """
        In the case of products with features_alias (i.e. specs_from_bhpv = False),
        format the main_features specs to use the keys provided in the
        main_features list, but have the values provided in the actual specs.

        It will skip missing key_values where necessary.
        """
        specs = self.product_instance.specs
        main_f = approp_cat.main_features
        alias_f = self.product_instance.features_alias
        assert len(main_f) == len(alias_f), "Lists must be of equal lengths"
        count = 0
        new_specs, specs_keys = {}, specs.keys()
        for feature in alias_f:
            if feature in specs_keys:
                new_specs[main_f[count]] = specs.get(feature)
            count += 1

        self.product_instance.specs = new_specs

    def return_appropriate_category_instance(self):
        """
        Returns lowest_level subcategory with valid main_features else,
        returns Category obj which will always have valid main_features attr.
        """
        if self.product_instance.subcat_2_id \
                and self.product_instance.subcat_2_id.main_features:
            return self.product_instance.subcat_2_id
        elif self.product_instance.subcat_1_id \
                and self.product_instance.subcat_1_id.main_features:
            return self.product_instance.subcat_1_id
        else:
            approp_cat = self.product_instance.cat_id
            return approp_cat

    def to_string(self):
        """
        Pretty print results of main_features.
        """
        # Check if values_list has been generated, attempt to generate it if it hasn't.
        # If values_list is still empty return empty string
        if not self.final():
            return ""

        final_string = ""
        skipped_count = 0   # Count to check for skipped items
        values_count = 0
        for feat in self.features_list:
            # Check if feature was skipped
            if skipped_count in self.skipped:
                skipped_count += 1
                continue
            skipped_count += 1
            count = 0       # Count to format indented items
            final_string += f"{feat}: "
            indent_length = len(feat)

            for inner_feat in self.values_list[values_count]:
                count += 1
                if count > 1:
                    final_string += " " * (indent_length + 2) + f"{inner_feat}\n"
                else:
                    final_string += f"{inner_feat}\n"
            values_count += 1

        return final_string












# Not Useful, kept because removal causes migration errors
class ListJSONField(JSONField):
    """
    Return a list or none rather than string
    """

    def value_from_object(self, obj):
        print("I ran")
        str_obj = getattr(obj, self.attname)
        list_obj = json.loads(str_obj)
        return list_obj




