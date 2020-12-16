from django.test import TestCase
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist as doesnt_exist

from ..utils.test_utils import CreateProduct, UniqueCategory, Category


# Should be tested without '--keepdb' flag
class TestSignals(TestCase):

    def setUp(self) -> None:
        self.prod = CreateProduct()

    def test_save_or_update_unique_category(self):
        # Test for saving
        cat_kwargs = {
            "name": "Microphones", "main_features": ["type"]
        }
        self.prod.cat_id(**cat_kwargs)
        name = self.prod.cat_obj.name
        self.assertEqual(
            name,
            UniqueCategory.objects.get(name=name).name
        )
        # Test for saving on other models
        cat_kwargs["cat_id"] = self.prod.cat_obj
        cat_kwargs["name"] = "Mikes"
        self.prod.subcat_1_id(**cat_kwargs)
        self.assertEqual(
            UniqueCategory.objects.get(name="Mikes").model_name,
            self.prod.subcat_1_obj.__class__.__name__
        )
        # Test for updating
        old_id = UniqueCategory.objects.get(name=name).id
        self.prod.cat_obj.name = "Mics"
        self.prod.cat_obj.save()
        self.assertEqual(old_id, UniqueCategory.objects.get(name="Mics").id)

    def test_delete_unique_category(self):
        cat_kwargs = {
            "name": "Speakers", "main_features": ["type"]
        }
        self.prod.cat_id(**cat_kwargs)
        exists = UniqueCategory.objects.get(name=self.prod.cat_obj.name)
        self.prod.cat_obj.delete()
        self.assertRaises(
            doesnt_exist, UniqueCategory.objects.get, name=self.prod.cat_obj.name
        )






