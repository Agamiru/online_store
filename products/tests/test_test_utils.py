from django.test import TestCase
from django.db.utils import IntegrityError

from ..utils.test_utils import *


class TestCreateProduct(TestCase):

    def setUp(self) -> None:
        self.html = html
        self.product = CreateProduct(html)

    def create_product_subcat_1_obj(self):
        self.product.cat_id(name="Guitars", main_features=["type"])
        self.product.subcat_1_id(
            cat_id=self.product.cat_obj, name="Electric Guitars",
            alias=["Ginta"]
        )

    def test_kwargs_checker(self):
        kwargs = {"name": "", "alias": "", "main_features": ""}
        false_kwargs = {"shell": "", "name": "shell"}
        self.assertIsNone(self.product.kwargs_checker(Category, kwargs))
        self.assertRaises(
            AttributeError, self.product.kwargs_checker,
            Category, false_kwargs
        )

    def test_dependency_checker(self):
        dep_field_name = "cat_id"
        dep_obj_name = "cat_obj"
        kwargs = {"shell": "camp", dep_field_name: "hello_string"}
        setattr(self.product, dep_obj_name, ["hello_list"])
        # Test for Attribute Error
        self.assertRaises(
            AttributeError,
            self.product.dependency_checker, dep_field_name, dep_obj_name, kwargs
        )
        # Test for Key Error
        kwargs.pop(dep_field_name)
        self.assertRaises(
            KeyError,
            self.product.dependency_checker, dep_field_name, dep_obj_name, kwargs
        )
        # Test for None
        kwargs[dep_field_name] = None
        setattr(self.product, dep_obj_name, None)
        self.assertRaises(
            AttributeError,
            self.product.dependency_checker, dep_field_name, dep_obj_name, kwargs
        )
        # Assert Passes
        kwargs[dep_field_name] = ["hello_list"]
        setattr(self.product, dep_obj_name, ["hello_list"])
        self.assertIsNone(
            self.product.dependency_checker(dep_field_name, dep_obj_name, kwargs)
        )

    def test_cat_id(self):
        # Check model with no main_features
        kwargs = {"name": "Guitars"}
        self.assertRaises(IntegrityError, self.product.cat_id, **kwargs)
        # Check model with only required field
        kwargs["main_features"] = ["strings", "eq"]
        self.product.cat_id(**kwargs)
        self.assertEqual(self.product.cat_obj, Category.objects.get(name="Guitars"))
        # Check model returns the correct type
        kwargs["name"] = "Mic Reflection Filter"
        kwargs["alias"] = ["Portable Booth", "Vocal Booth"]
        self.product.cat_id(**kwargs)
        self.assertEqual(
            ['Portable Booth', 'Vocal Booth'],
            Category.objects.get(name="Mic Reflection Filter").alias
        )
        # Check that self.product representation of model instance are identical
        self.assertEqual(self.product.cat_obj, Category.objects.get(name="Mic Reflection Filter"))
        # Check that self.product kwargs represent the object
        self.assertEqual(self.product.kwargs["cat_id"], self.product.cat_obj)

    def test_subcat_1_id(self):
        # Dependency test
        kwargs = {"name": "Electric Guitars", "alias": ["Ginta"]}
        self.assertRaises(KeyError, self.product.subcat_1_id, **kwargs)
        # Create dependency object
        self.product.cat_id(name="Guitars", main_features=["type"])
        kwargs["cat_id"] = self.product.cat_obj
        self.product.subcat_1_id(**kwargs)
        # Check that self.product representation of model instance are identical
        self.assertEqual(self.product.subcat_1_obj, SubCategory1.objects.get(name="Electric Guitars"))
        # Check model returns the correct type
        self.assertEqual(
            ['Ginta'], SubCategory1.objects.get(name="Electric Guitars").alias)
        # Check that self.product kwargs represent the object
        self.assertEqual(self.product.kwargs["subcat_1_id"], self.product.subcat_1_obj)

    def test_subcat_2_id(self):
        # Dependency test
        kwargs = {"name": "Bass Guitars", "alias": ["Base"]}
        self.assertRaises(KeyError, self.product.subcat_2_id, **kwargs)
        # Create dependency objects
        self.create_product_subcat_1_obj()
        kwargs["subcat_1_id"] = self.product.subcat_1_obj
        self.product.subcat_2_id(**kwargs)
        # Check that self.product representation of model instance are identical
        self.assertEqual(self.product.subcat_2_obj, SubCategory2.objects.get(name="Bass Guitars"))
        # Check model returns the correct type
        self.assertEqual(
            ['Base'], SubCategory2.objects.get(name="Bass Guitars").alias)
        # Check that self.product kwargs represent the object
        self.assertEqual(self.product.kwargs["subcat_2_id"], self.product.subcat_2_obj)

    def test_brand(self):
        self.product.brand("Focusrite")
        self.assertEqual(self.product.brand_obj, Brand.objects.get(name="Focusrite"))
        self.assertEqual(self.product.kwargs["brand"], self.product.brand_obj)

    def test_model_name(self):
        # No kwargs test, without dependency
        self.assertRaises(AttributeError, self.product.model_name)
        # Dependency test
        self.assertRaises(KeyError, self.product.model_name, name="Roadstar")
        # Test Default
        self.product.brand("Ibanez")
        self.product.model_name()
        self.assertEqual("Generic", self.product.kwargs["model_name"].name)
        # Check that self.product kwargs represent the object
        kwargs = {"brand_id": self.product.brand_obj, "name": "Roadstar"}
        self.product.model_name(**kwargs)
        self.assertEqual(self.product.kwargs["model_name"], ModelName.objects.get(name="Roadstar"))

    def test_print_specs(self):
        self.product.specs()
        self.assertTrue(isinstance(self.product.specs_dict, dict))

    # def test_create_main_features(self):
    #     self.product.create_main_features(CategoryMainFeatures, Category, [])

    def test_create_products_w_defaults(self):
        cat_kwargs = {
            "name": "keyboards", "main_features": ["octaves", "transpose"]
        }
        self.product.create_products_w_defaults(cat_kwargs, "Alesis")
        package_dims = self.product.specs_dict["Box Dimensions (LxWxH)"][0]
        weight = self.product.specs_dict["Package Weight"][0]

        self.assertEqual(self.product.prod_instance, Product.objects.get(cat_id=self.product.cat_obj))
        self.assertEqual(
            ['octaves', 'transpose'],
            self.product.prod_instance.cat_id.main_features
        )
        self.assertEqual(
            package_dims,
            Product.objects.get(cat_id=self.product.cat_obj).package_dimensions
        )
        self.assertEqual(
            weight,
            Product.objects.get(cat_id=self.product.cat_obj).weight)

    def test_create_product(self):
        cat_kwargs = {
            "name": "keyboards", "main_features": ["octaves", "transpose"]
        }
        self.product.create_products_w_defaults(cat_kwargs, "Alesis")
        subcat_1_kwargs = {
            "cat_id": self.product.cat_obj, "name": "Electric Guitars",
        }
        self.product.model_name(brand_id=self.product.brand_obj, name="V25")
        self.product.subcat_1_id(**subcat_1_kwargs)
        self.product.create_product()
        self.assertEqual(
            "Electric Guitars",
            self.product.prod_instance.subcat_1_id.name
        )




