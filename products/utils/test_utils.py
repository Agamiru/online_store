from ..models import *
from ..utils.general_utils import BhphotovideoTableConverter
from django.db import models
from typing import Union, List


html = """
<div class="fader_SupTjLNRI5T781t8hgAfj"><div class="leftPanel_3i7hVcv5SxC5_NRIXMU8Wz"><div><div class="title_1tNQ83iPOOgJ6m5fVkxmSw"><h2 data-selenium="specsItemTitle" class="title1_17KKS47kFEQb7ynVBsRb_5 reset_gKJdXkYBaMDV-W3ignvsP primary_ELb2ysditdCtk24iMBTUs">Alesis V25 Specs</h2></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc firstGroupInItem_k8WqCFToyTsIW3AYbSuui" data-selenium="specsItemGroupName">USB / MIDI Controller</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Keyboard</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>25&nbsp;Full-Size&nbsp;Keys,&nbsp;Synth&nbsp;Action&nbsp;with&nbsp;Velocity</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">MIDI Control Surfaces</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>Wheel&nbsp;(Pitch-Bend)<br><b>1 x </b>Wheel&nbsp;(Modulation)<br><b>8 x </b>Pads&nbsp;(Velocity-Sensitive)<br><b>4 x </b>Rotary Encoders<br><b>4 x </b>Buttons&nbsp;(Assignable)</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Performance Functions</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>Octave Shift, Transport Controls</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Connectivity</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">I/O</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span><b>1 x </b>USB Type-B&nbsp;</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">OS Compatibility</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>macOS&nbsp;10<br>Windows</span></td></tr></tbody></table></div><div class="group_K7YrQottgVsRZ4B6zAaGG"><div class="name_3mapjiENorVzh8SvFyXVPc" data-selenium="specsItemGroupName">Packaging Info</div><table class="table_o418fscimQZEg1oshu4aX" data-selenium="specsItemGroupTable"><tbody><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL " data-selenium="specsItemGroupTableColumnLabel">Package Weight</td><td class="value_11Av1yGkVYn9TX48mQeu9v " data-selenium="specsItemGroupTableColumnValue"><span>5.2 lb</span></td></tr><tr class="pair_3u9fnESIQrtuEu6ye_zM4k" data-selenium="specsItemGroupTableRow"><td class="label_3bLwbW8ibvYc5tUwpKVQsL" data-selenium="specsItemGroupTableColumnLabel">Box Dimensions (LxWxH)</td><td class="value_11Av1yGkVYn9TX48mQeu9v" data-selenium="specsItemGroupTableColumnValue"><span>24.5 x 10 x 5"</span></td></tr></tbody></table></div></div></div></div>
"""

audio_int_main_f = [
    "Analog Audio I/O", "Host Connection / USB",
    "Sample Rates", "Power Requirements"
]

midi_keyboard_main_f = [
    "Keyboard", "MIDI Control Surfaces", "I/O",
]


class CreateProduct:
    """
    Class that helps create a full product instance and other model objects
    for testing purposes.
    """
    def __init__(self, html_string=html):
        self.html = html_string
        self.kwargs = {}
        self.prod_instance = None
        self.features_kwargs = []

    def create_products_w_defaults(self, cat_kwargs: dict, brand: str):
        self.cat_id(**cat_kwargs)
        self.brand(brand)
        self.model_name()
        self.short_desc()
        self.price()
        self.specs()
        self.package_dimensions()
        self.weight()

        prod_instance, created = Product.objects.get_or_create(**self.kwargs)
        self.prod_instance = prod_instance

    @staticmethod
    def kwargs_checker(model, kwargs) -> None:
        """
        Raises AttributeError if given kwargs are not valid for ahe given model.
        """
        field_names = [field.name for field in model()._meta.fields]
        for key in kwargs.keys():
            if key not in field_names:
                raise AttributeError(f"'{key}' is not a known model field name")

    def dependency_checker(
            self, dependency_field_name: str, dependency_obj_name: str, kwargs
    ) -> None:
        """
        Checks if dependent field name is in kwargs and also confirms
        if its value is same with this class'es representation of it.
        """
        try:
            if kwargs[dependency_field_name] == getattr(self, dependency_obj_name):
                if kwargs[dependency_field_name]:   # In case they are both of None type
                    return
            raise AttributeError(f"Product has no valid '{dependency_field_name}' instance")
        except KeyError as e:
            raise e

    def cat_id(self, **kwargs):
        # Validate kwargs
        self.kwargs_checker(Category, kwargs)
        if not kwargs.get("name"):      # Required field check
            raise AttributeError("'name' is a required field")

        cat_obj, created = Category.objects.get_or_create(**kwargs)
        self.cat_obj = cat_obj
        self.kwargs.update({"cat_id": cat_obj})

    def subcat_1_id(self, **kwargs):
        # Validate kwargs
        self.kwargs_checker(SubCategory1, kwargs)
        if not kwargs.get("name"):   # Required field check
            raise AttributeError("'name' is a required field")
        # Dependency check
        self.dependency_checker("cat_id", "cat_obj", kwargs)
        subcat1_obj, created = SubCategory1.objects.get_or_create(**kwargs)
        self.subcat_1_obj = subcat1_obj     # Will be defined on the fly
        self.kwargs.update({"subcat_1_id": subcat1_obj})

    def subcat_2_id(self, **kwargs):
        # Validate kwargs
        self.kwargs_checker(SubCategory2, kwargs)
        if not kwargs.get("name"):  # Required field check
            raise AttributeError("'name' is a required field")
        # Dependency check
        self.dependency_checker("subcat_1_id", "subcat_1_obj", kwargs)
        subcat2_obj, created = SubCategory2.objects.get_or_create(**kwargs)
        self.subcat_2_obj = subcat2_obj     # Will be defined on the fly
        self.kwargs.update({"subcat_2_id": subcat2_obj})

    def brand(self, name):
        brand_obj, created = Brand.objects.get_or_create(name=name)
        self.brand_obj = brand_obj
        self.kwargs.update({"brand": brand_obj})

    def model_name(self, **kwargs):
        if not kwargs:
            kwargs["name"] = "Generic"
            kwargs["brand_id"] = self.brand_obj
            if not kwargs.get("brand_id"):
                raise AttributeError("Brand object is a required dependency")
            self.kwargs_checker(ModelName, kwargs)
        else:
            # Validate kwargs
            self.kwargs_checker(ModelName, kwargs)
        # Dependency check
        self.dependency_checker("brand_id", "brand_obj", kwargs)
        model_name_obj, created = ModelName.objects.get_or_create(**kwargs)
        self.kwargs.update({"model_name": model_name_obj})

    def short_desc(self, desc="A very nice audio gear"):
        self.kwargs.update({"short_desc": desc})

    def price(self, price: float = 45000):
        self.kwargs.update({"price": price})

    def specs(self, html=None):
        if html:
            specs_json = BhphotovideoTableConverter(html).to_python_dict()
            self.kwargs.update({"specs": specs_json})
            self.specs_dict = BhphotovideoTableConverter(html).to_python_dict()
        else:
            specs_json = BhphotovideoTableConverter(self.html).to_python_dict()
            self.kwargs.update({"specs": specs_json})
            self.specs_dict = BhphotovideoTableConverter(self.html).to_python_dict()

    def print_specs(self):
        if not self.kwargs.get("specs"):
            self.specs(html)
        print(self.kwargs.get("specs"))

    def package_dimensions(self, html=None):
        if not self.kwargs.get("specs"):
            self.specs(html)
        try:
            package_dims = self.specs_dict["Box Dimensions (LxWxH)"][0]
            self.kwargs.update({"package_dimensions": package_dims})
        except KeyError:
            pass

    def weight(self, html=None):
        if not self.kwargs.get("specs"):
            self.specs(html)
        try:
            package_weight = self.specs_dict["Package Weight"][0]
            self.kwargs.update({"weight": package_weight})
        except KeyError:
            pass

    def features_alias(self, array=list):
        self.kwargs["features_alias"] = array

    def specs_from_bhpv(self, val=True):
        self.kwargs["specs_from_bhpv"] = val


    def create_product(self):
        prod_instance, created = Product.objects.get_or_create(**self.kwargs)
        self.prod_instance = prod_instance





