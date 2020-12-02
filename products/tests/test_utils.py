from django.test import TestCase
import json

from .utils import *
from ..model_utils import GetMainFeatures
from ..utils import string_list_to_list

# Create your tests here.


class TestModelUtils(TestCase):

    def setUp(self) -> None:
        self.prod, self.subcat1_main_f = create_product()

    def test_get_main_features_util(self):
        main_f = GetMainFeatures(self.prod)
        main_f.features()
        self.assertEqual(midi_keyboard_main_f, main_f.features_list)


class TestTestUtils(TestCase):

    def setUp(self) -> None:
        self.html = html
        self.product = CreateProduct(html)

    def create_product_subcat_1_obj(self):
        self.product.cat_obj = self.product.cat_id("Guitars")
        self.product.subcat_1_obj = self.product.subcat_1_id("Electric Guitars", ["Ginta"])

    def test_create_product_alias_checker(self):
        self.assertRaises(TypeError, self.product.list_or_none_checker, "shell")
        self.assertIsNone(self.product.list_or_none_checker(None))

    def test_create_product_idx_checker(self):
        self.assertIsNone(self.product.idx_checker(["shell", "camp"], 2))
        self.assertEqual(self.product.idx_checker(["shell", "camp"], 1), "camp")

    def test_create_product_cat_id(self):
        self.product.cat_id("Guitars")
        self.assertEqual(self.product.cat_obj, Category.objects.get(name="Guitars"))
        self.product.cat_id("Mic Reflection Filter", ["Portable Booth", "Vocal Booth"])
        self.assertEqual(
            ["Portable Booth", "Vocal Booth"],
            string_list_to_list(Category.objects.get(name="Mic Reflection Filter").alias)
        )
        self.assertEqual(self.product.kwargs["cat_id"], self.product.cat_obj)

    def test_create_product_subcat_1_id(self):
        self.assertRaises(AttributeError, self.product.subcat_1_id, "Electric Guitars", ["Ginta"])
        # Create dependency object
        self.product.cat_obj = self.product.cat_id("Guitars")
        self.product.subcat_1_id("Electric Guitars", ["Ginta"])
        self.assertEqual(self.product.subcat_1_obj, SubCategory1.objects.get(name="Electric Guitars"))
        self.assertEqual(
            ["Ginta"],
            string_list_to_list(SubCategory1.objects.get(name="Electric Guitars").alias)
        )
        self.assertEqual(self.product.kwargs["subcat_1_id"], self.product.subcat_1_obj)

    def test_create_product_subcat_2_id(self):
        self.assertRaises(AttributeError, self.product.subcat_2_id, "Bass Guitars", ["Base"])
        # Create dependency objects
        self.create_product_subcat_1_obj()
        self.product.subcat_2_id("Bass Guitars", ["Base"])
        self.assertEqual(self.product.subcat_2_obj, SubCategory2.objects.get(name="Bass Guitars"))
        self.assertEqual(
            ["Base"],
            string_list_to_list(SubCategory2.objects.get(name="Bass Guitars").alias)
        )
        self.assertEqual(self.product.kwargs["subcat_2_id"], self.product.subcat_2_obj)

    def test_create_product_brand(self):
        self.product.brand("Focusrite")
        self.assertEqual(self.product.brand_obj, Brand.objects.get(name="Focusrite"))
        self.assertEqual(self.product.kwargs["brand"], self.product.brand_obj)

    def test_create_product_model_name(self):
        self.assertRaises(AttributeError, self.product.model_name, "Scarlett 2i2")
        # Create dependency object
        self.product.brand("Focusrite")
        self.product.model_name()
        self.assertEqual("Generic", self.product.kwargs["model_name"].name)
        self.product.model_name("Scarlett 2i2")
        self.assertEqual(self.product.kwargs["model_name"], ModelName.objects.get(name="Scarlett 2i2"))

    def test_print_specs(self):
        self.product.specs()
        print(self.product.kwargs["specs"])

    # def test_create_main_features(self):
    #     self.product.create_main_features(CategoryMainFeatures, Category, [])

    def test_create_products_w_defaults(self):
        self.product.create_products_w_defaults(
            cat_details=["Keyboard"], brand="Alesis",
            subcat1_details=["Midi Keyboards", ["Midi Controller", "Controller"]],
        )
        package_dims = self.product.specs_dict["Box Dimensions (LxWxH)"][0]
        weight = self.product.specs_dict["Package Weight"][0]

        self.assertEqual(self.product.prod_instance, Product.objects.get(cat_id=self.product.cat_obj))
        self.assertEqual(
            ["Midi Controller", "Controller"],
            string_list_to_list(self.product.prod_instance.subcat_1_id.alias)
        )
        self.assertEqual(
            package_dims,
            Product.objects.get(cat_id=self.product.cat_obj).package_dimensions
        )
        self.assertEqual(
            weight,
            Product.objects.get(cat_id=self.product.cat_obj).weight)






# Todo: Bhphotovideotableconverter and others
class TestUtils:
    pass

