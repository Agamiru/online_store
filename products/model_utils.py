from django.db.models import ObjectDoesNotExist as doesnt_exist
from typing import List
from .utils import string_list_to_list
import json


# Todo: Write tests for this
class GetMainFeatures:

    def __init__(self, product_instance):
        self.product_instance = product_instance
        self.has_features = False
        self.features_list = None
        self.values_list = []
        self.features_dict = None   # Final product
        self.skipped: List[int] = []   # List of index of skipped _features
        self.errors = []

    def __call__(self, *args, **kwargs):
        self._features()

    def _features(self):
        specs = self.product_instance.specs     # returns a str
        json_specs = json.loads(specs)      # converts string to dict
        print(f"specs: {type(json_specs)}\n")
        skipped: List[int] = []
        self.features_dict = {}
        self.get_features_list()
        if self.errors:
            return
        count = 0
        for feat in self.features_list:
            try:
                self.features_dict.update({feat: json_specs[feat]})
                self.values_list.append(json_specs[feat])
                count += 1
            # If for some reason specs has no such _features
            except KeyError:
                skipped.append(count)
                count += 1
                continue
        if skipped:
            self.skipped = skipped
            print(f"Skipped {len(skipped)} items")

    def get_features_list(self):
        """
        Updates self.features_list, self.errors and self.has_features
        """
        approp_cat_instance = self.return_appropriate_category_instance()
        print(f"approp_cat_instance: {approp_cat_instance}\n")
        # Backward relationship
        try:
            features = approp_cat_instance.main_features._features   # str
            print(f"_features: {features}\n")
            self.has_features = True
            print(f"_features: {type(features)}\n")
            print(f"_features: {features}")
            self.features_list = string_list_to_list(features)
        # Category has no _features
        except (doesnt_exist, AttributeError) as e:
            cat_name = approp_cat_instance.__class__.__name__
            self.errors.append({cat_name: e})
            print(f"errors: {self.errors}")

    def return_appropriate_category_instance(self):
        if self.product_instance.subcat_2_id:
            return self.product_instance.subcat_2_id
        elif self.product_instance.subcat_1_id:
            return self.product_instance.subcat_1_id
        else:
            approp_cat = self.product_instance.cat_id
            return approp_cat

    def to_string(self):
        if self.errors:
            return ""

        # Check if values_list has been generated, attempt to generate it if it hasn't.
        # If values_list is still empty return empty string
        count = 0
        while not self.values_list:
            count += 1
            if count > 1:
                return ""
            self._features()

        final_string = ""
        skipped_count = 0   # Count to check for skipped items
        for feat in self.features_list:
            count = 0       # Count to format indented items
            final_string += f"{feat}: "
            indent_length = len(final_string)
            # Check if feature was skipped
            if skipped_count in self.skipped:
                skipped_count += 1
                continue
            for inner_feat in self.values_list:
                count += 1
                if count > 1:
                    final_string += "" * indent_length + f"{inner_feat}\n"
                else:
                    final_string += f"{inner_feat}\n"

        return final_string



