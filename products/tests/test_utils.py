from django.test import TestCase
import json

from .utils import create_product, midi_keyboard_main_f
from ..model_utils import GetMainFeatures

# Create your tests here.


class TestModelUtils(TestCase):

    def setUp(self) -> None:
        self.prod, self.subcat1_main_f = create_product()

    def test_get_main_features_util(self):
        main_f = GetMainFeatures(self.prod)
        main_f()
        self.assertEqual(midi_keyboard_main_f, main_f.features_list)


