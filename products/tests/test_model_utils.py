from django.test import TestCase
from django.db.models import ForeignKey
from django.core.exceptions import ValidationError

from ..utils.test_utils import CreateProduct, SubCategory1
from ..utils.model_utils import GetMainFeatures as gmf
from ..utils.model_utils import CrossModelUniqueNameValidator
from ..models import UniqueCategory
from django.forms import models


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

    def test_specs_key_switcher(self):
        specs = {
            "key": ["Really dope stuff"],
            "midi": ["Nice Midi"], "fishes": ["Swim a lot"],
            "world": ["Messed up"], "os": ["Nice os", "Good os", "Lovely Os"]
        }
        main_f = [
            "Keyboard", "MIDI Control Surfaces", "OS Compatibility"
        ]
        alias_f = ["key", "midi", "os"]
        # Create product_instance class
        prod_inst = type("prod_inst", (), {"specs": specs, "features_alias": alias_f})
        main_f_obj = gmf(prod_inst)
        main_f_obj.specs_key_switcher(main_f, alias_f)
        self.assertEqual(
            main_f_obj.product_instance.specs["Keyboard"],
            ["Really dope stuff"]
        )
        self.assertEqual(
            main_f_obj.product_instance.specs["OS Compatibility"],
            ["Nice os", "Good os", "Lovely Os"]
        )

    def test_set_custom_alias(self):
        specs = {
            "key": ["Really dope stuff"],
            "midi": ["Nice Midi"], "fishes": ["Swim a lot"],
            "world": ["Messed up"], "os": ["Nice os", "Good os", "Lovely Os"]
        }
        main_f = [
            "Keyboard", "MIDI Control Surfaces", "OS Compatibility"
        ]
        alias_f = ["key", "midi", "os"]
        # Create product_instance class
        prod_inst = type("prod_inst", (), {"specs": specs, "features_alias": alias_f, "specs_from_bhpv": False})
        approp_cat = type("approp_cat", (), {"main_features": main_f})
        # Instantiate GMF class with custom_alias list
        main_f_obj = gmf(prod_inst, ["shell", "camp", "owerri"])
        # main_f_obj.features_list = main_f       # Bypass set_features_list
        main_f_obj.return_appropriate_category_instance = lambda: approp_cat    # set callable
        self.assertEqual(main_f_obj.return_appropriate_category_instance(), approp_cat)
        main_f_obj.final()
        self.assertEqual(
            main_f_obj.product_instance.specs["shell"], ['Really dope stuff']
        )
        self.assertEqual(
            main_f_obj.product_instance.specs["owerri"], ['Nice os', 'Good os', 'Lovely Os']
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
        self.product.specs_from_bhpv(False)
        self.product.features_alias(["key", "midi", "os"])
        self.product.kwargs["specs"] = specs
        self.product.create_product()
        main_f_obj = gmf(self.product.prod_instance)

        print(f"features dict:\n{main_f_obj.to_string()}\n")
        self.assertEqual(
            main_f_obj.features_dict.get("OS Compatibility"),
            specs.get("os")
        )

    def test_get_main_features_w_all_invalid_keys(self):
        cat_kwargs = {
            "name": "M Keyboard",
            "main_features": ["shell", "camp", "koun"]
        }
        self.product.create_products_w_defaults(cat_kwargs, "Motu")
        main_f_obj = gmf(self.product.prod_instance)
        main_f_obj.features()
        print(f"features dict:\n{main_f_obj.to_string()}\n")
        self.assertEqual(len(main_f_obj.skipped), 3)


    # def test_print_specs(self):
    #     self.product.print_specs()


class FakeModelForm(models.ModelForm):
    class Meta:
        exclude = ["id"]
        model = SubCategory1


class TestCrossModelUniqueNameValidator(TestCase):

    def setUp(self) -> None:
        self.prod = CreateProduct()

    def test_cross_model_unique_name_validator(self):
        cat_kwargs = {"name": "M Keyboard", "main_features": ["shell"]}
        self.prod.cat_id(**cat_kwargs)
        # Test validator in isolation
        validator = CrossModelUniqueNameValidator(UniqueCategory)
        self.assertRaises(ValidationError, validator, "M Keyboard")
        # Test validator in model
        cat_kwargs["cat_id"] = self.prod.cat_obj
        cat_kwargs["alias"] = ["koun"]
        self.assertRaises(
            ValidationError,
            self.prod.subcat_1_id, **cat_kwargs
        )
        # Test validator in model form
        form_instance = FakeModelForm(data=cat_kwargs)
        self.assertFalse(form_instance.is_valid())
        self.assertEqual(
            "Category object with name 'M Keyboard' already exists",
            form_instance.errors.get("name")[0]
        )














