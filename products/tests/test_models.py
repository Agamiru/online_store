from django.test import TestCase
from ..models import Category
from django.db.utils import ProgrammingError



class TestModels(TestCase):

    def setUp(self) -> None:
        self.params = {
            "name": "cables", "alias": ["wires", "cords"],
            "main_features": ["type", "gender"]
        }

    def test_json_array_field(self):
        cat_obj, created = Category.objects.get_or_create(**self.params)
        self.assertTrue(isinstance(cat_obj.alias, list))
        self.params["alias"] = {"wires": "cords"}
        self.params["main_features"] = "shell"
        self.assertRaisesMessage(
            ProgrammingError, "can't adapt type 'dict'",
            Category.objects.get_or_create, **self.params
        )


