from ..models import *
from ..utils import BhphotovideoTableConverter
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


def create_product():
    cat_id, created = Category.objects.get_or_create(
        id=1, name="Keyboards",
    )
    subcat1_id, created = SubCategory1.objects.get_or_create(
        id=1, cat_id=cat_id, name="Midi Keyboards",
        alias=json.dumps(["midi controller"])
    )

    brand, created = Brand.objects.get_or_create(
        id=1, name="Alesis",
    )

    model_name, created = ModelName.objects.get_or_create(
        id=1, brand_id=brand, name="V25"
    )

    short_desc = "25-Key USB MIDI Keyboard Controller"
    price = 65000

    specs_json = BhphotovideoTableConverter(html).to_json()

    prod_instance, created = Product.objects.get_or_create(
        id=1, cat_id=cat_id, subcat_1_id=subcat1_id, brand=brand,
        model_name=model_name, short_desc=short_desc, price=price,
        specs=specs_json
    )

    subcat1_main_f, created = SubCategory1MainFeatures.objects.get_or_create(
        subcat_1_id=subcat1_id, features=json.dumps(midi_keyboard_main_f)
    )

    return prod_instance, subcat1_main_f


class CreateProduct:
    def __init__(self, html):
        self.html = html
        self.kwargs = {}
        self.prod_instance = None
        self.features_kwargs = []

    def create_products_w_defaults(
            self, cat_details: list, brand: str, subcat1_details: list = None,
            subcat2_details: list = None,

    ):
        # details must be lists or none
        self.list_or_none_checker(cat_details, subcat1_details, subcat2_details)

        self.cat_id(name=self.idx_checker(cat_details, 0), alias=self.idx_checker(cat_details, 1))
        self.subcat_1_id(name=self.idx_checker(subcat1_details, 0), alias=self.idx_checker(subcat1_details, 1))
        self.subcat_2_id(name=self.idx_checker(subcat2_details, 0), alias=self.idx_checker(subcat2_details, 1))
        self.brand(brand)
        self.model_name()
        self.short_desc()
        self.price()
        self.specs()
        self.package_dimensions()
        self.weight()
        # Todo: Package dims and Weight

        prod_instance, created = Product.objects.get_or_create(**self.kwargs)
        self.prod_instance = prod_instance

    @staticmethod
    def idx_checker(obj, idx):
        if not obj:
            return
        try:
            _ = obj[idx]
            return _
        except IndexError:
            return

    @staticmethod
    def list_or_none_checker(*args):
        for data_type in args:
            if not isinstance(data_type, list):
                if data_type is not None:
                    raise TypeError(f"data_type must be a List or None")

    def cat_id(self, name: str, alias: list = None):
        if not name:       # Runtime check
            return
        self.list_or_none_checker(alias)
        cat_obj, created = Category.objects.get_or_create(
            name=name, alias=json.dumps(alias)
        )
        self.cat_obj = cat_obj    # Will be defined on the fly
        self.kwargs.update({"cat_id": cat_obj})

    def subcat_1_id(self, name: str, alias: list = None):
        if not name:        # Runtime check
            return
        self.list_or_none_checker(alias)
        dependency_obj = "cat_obj"
        if hasattr(self, dependency_obj):
            subcat1_obj, created = SubCategory1.objects.get_or_create(
                cat_id=getattr(self, dependency_obj), name=name, alias=json.dumps(alias)
            )
            self.subcat_1_obj = subcat1_obj
            self.kwargs.update({"subcat_1_id": subcat1_obj})
        else:
            raise AttributeError(f"Product has no valid {dependency_obj}")

    def subcat_2_id(self, name: str, alias: list):
        if not name:        # Runtime check
            return
        self.list_or_none_checker(alias)
        dependency_obj = "subcat_1_obj"
        if hasattr(self, dependency_obj):
            subcat2_obj, created = SubCategory2.objects.get_or_create(
                subcat_1_id=getattr(self, dependency_obj), name=name, alias=json.dumps(alias)
            )
            self.subcat_2_obj = subcat2_obj
            self.kwargs.update({"subcat_2_id": subcat2_obj})
        else:
            raise AttributeError(f"Product has no valid {dependency_obj}")

    def brand(self, name):
        brand_obj, created = Brand.objects.get_or_create(name=name)
        self.brand_obj = brand_obj
        self.kwargs.update({"brand": brand_obj})

    def model_name(self, name="Generic"):
        dependency_obj = "brand_obj"
        if hasattr(self, dependency_obj):
            model_name_obj, created = ModelName.objects.get_or_create(
                brand_id=getattr(self, dependency_obj), name=name
            )
            self.kwargs.update({"model_name": model_name_obj})
        else:
            raise AttributeError(f"Product has no valid {dependency_obj}")

    def short_desc(self, desc="A very nice audio gear"):
        self.kwargs.update({"short_desc": desc})

    def price(self, price: float = 45000):
        self.kwargs.update({"price": price})

    def specs(self, html=None):
        if html:
            specs_json = BhphotovideoTableConverter(html).to_json()
            self.kwargs.update({"specs": specs_json})
            self.specs_dict = BhphotovideoTableConverter(html).to_python_dict()
        else:
            specs_json = BhphotovideoTableConverter(self.html).to_json()
            self.kwargs.update({"specs": specs_json})
            self.specs_dict = BhphotovideoTableConverter(self.html).to_python_dict()

    # Todo: self.package_dimensions and self.weight

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

    def create_main_features(self, main_f_model, features_for, features: list,):
        if not isinstance(features, list):
            raise TypeError("Must be a list")

        if not issubclass(main_f_model and features_for, models.Model):
            raise TypeError("Must be a django model instance")

        feat_cat_id_name = main_f_model()._meta.fields[1].name
        print(feat_cat_id_name)
        feat_feat_name = main_f_model()._meta.fields[2].name
        print(feat_feat_name)

        dic = {feat_cat_id_name: features_for, feat_feat_name: json.dumps(features)}
        print(f"features dic: {dic}")
        self.features_kwargs.append(dic)

        features_obj, created = main_f_model.objects.get_or_create(**dic)

        return features_obj




