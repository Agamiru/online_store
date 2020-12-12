from typing import List
import json

from django.db.models.fields.json import JSONField


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
        return self.features_dict if self.values_list else {}

    # Refactoring this function causes dynamic references
    ### Do not Refactor name###
    def features(self):
        self.set_features_list()
        specs = self.product_instance.specs
        skipped: List[int] = []
        self.features_dict = {}
        count = 0
        for feat in self.features_list:
            try:
                self.features_dict.update({feat: specs[feat]})
                self.values_list.append(specs[feat])
                count += 1
            # If for some reason specs has no such features
            except KeyError:
                skipped.append(count)
                count += 1
                continue
        if skipped:
            self.skipped = skipped

    def set_features_list(self):
        approp_cat = self.return_appropriate_category_instance()
        if not self.product_instance.specs_from_bhpv:
            self.specs_key_switcher(approp_cat)
        self.features_list = approp_cat.main_features

    def specs_key_switcher(self, approp_cat):
        specs = self.product_instance.specs
        main_f = approp_cat.main_features
        alias_f = self.product_instance.features_alias
        assert len(main_f) == len(alias_f), "Lists must be of equal lengths"
        count = 0
        new_specs = {}
        for feature in alias_f:
            if feature in specs.keys():
                new_specs[main_f[count]] = specs.get(feature)
            count += 1
            # else:
            #     raise ImproperlyConfigured("Feature must be a valid key in specs")

        self.product_instance.specs = new_specs

    def return_appropriate_category_instance(self):
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
        # Check if values_list has been generated, attempt to generate it if it hasn't.
        # If values_list is still empty return empty string
        count = 0
        while not self.values_list:
            count += 1
            if count > 1:
                return ""
            self.features()

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


# Not Useful
class ListJSONField(JSONField):
    """
    Return a list or none rather than string
    """

    def value_from_object(self, obj):
        print("I ran")
        str_obj = getattr(obj, self.attname)
        list_obj = json.loads(str_obj)
        return list_obj




