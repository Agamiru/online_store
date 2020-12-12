from django.test import TestCase

from ..utils.test_utils import CreateProduct
from ..utils.model_utils import GetMainFeatures as gmf


class TestGetMainFeatures(TestCase):
    def setUp(self) -> None:
        self.product = CreateProduct()

    def test_return_appropriate_category_instance(self):
        # Only Category given
        cat_kwargs = {"name": "Guitars", "main_features": ["type", "year"]}
        self.product.create_products_w_defaults(cat_kwargs, "Ibanez")
        main_f_obj = gmf(self.product.prod_instance)
        self.assertEqual(
            main_f_obj.return_appropriate_category_instance(),
            self.product.cat_obj
        )
        # Subcategory given but with no main_features
        subcat_1_kwargs = {
            "cat_id": self.product.cat_obj, "name": "Electric Guitars",
        }
        self.product.subcat_1_id(**subcat_1_kwargs)
        self.product.model_name(brand_id=self.product.brand_obj, name="Roadstar")
        self.product.create_product()
        main_f_obj = gmf(self.product.prod_instance)
        self.assertEqual(
            main_f_obj.return_appropriate_category_instance(),
            self.product.cat_obj
        )
        # Subcategory given and with main_features
        subcat_2_kwargs = {
            "subcat_1_id": self.product.subcat_1_obj, "name": "Bass Guitar",
            "main_features": ["strings", "eq"]
        }
        self.product.subcat_2_id(**subcat_2_kwargs)
        self.product.model_name(brand_id=self.product.brand_obj, name="Reels")
        self.product.create_product()
        main_f_obj = gmf(self.product.prod_instance)
        self.assertEqual(
            main_f_obj.return_appropriate_category_instance(),
            self.product.subcat_2_obj
        )

    def test_features(self):
        cat_kwargs = {
            "name": "Midi Keyboard",
            "main_features": [
                "Keyboard", "fishes", "MIDI Control Surfaces",
                "OS Compatibility", "clowns"
            ]
        }
        self.product.create_products_w_defaults(cat_kwargs, "Alesis")
        main_f_obj = gmf(self.product.prod_instance)
        main_f_obj.features()
        print(f"features dict:\n{main_f_obj.to_string()}\n")
        self.assertEqual(main_f_obj.skipped, [1, 4])

    def test_features_alias(self):
        specs = {
            "key": ["Really dope stuff"],
            "midi": ["Nice Midi"], "fishes": ["Swim a lot"],
            "world": ["Messed up"], "os": ["Nice os", "Good os", "Lovely Os"]
        }
        cat_kwargs = {
            "name": "Midi Keyboard",
            "main_features": [
                "Keyboard", "MIDI Control Surfaces", "OS Compatibility"
            ]
        }
        self.product.create_products_w_defaults(cat_kwargs, "M-Audio")
        self.product.model_name(brand_id=self.product.brand_obj, name="Rockstar")
        self.product.features_alias(["key", "midi", "os"])
        self.product.kwargs["specs"] = specs
        self.product.specs_from_bhpv(False)
        self.product.create_product()
        main_f_obj = gmf(self.product.prod_instance)
        print(f"features dict:\n{main_f_obj.to_string()}\n")
        self.assertEqual(
            main_f_obj.features_dict.get("OS Compatibility"),
            specs.get("os")
        )


    # def test_print_specs(self):
    #     self.product.print_specs()







