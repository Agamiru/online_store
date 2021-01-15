from django.test import TestCase
from ..models import Category
from django.db.utils import ProgrammingError



class TestModels(TestCase):

    def setUp(self) -> None:
        self.params = {
            "name": "cables", "alias": ["wires", "cords"],
            "main_features": ["type", "gender"]
        }


