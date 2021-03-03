from typing import List

from django.test import TestCase

from ..models import Product, search_all_categories, Category, SubCategory1


class TestProductManager(TestCase):

    # Very important:
    # You might need to call the command below when changes has been made to models in products app:
    # py manage.py dumpdata products --exclude=products.UniqueCategory --indent=4 > product_fixtures.json
    # It excludes UniqueCategory model which could cause db integrity errors
    fixtures = ["product_fixtures.json"]

    def setUp(self) -> None:
        pass

    def test_full_search(self):
        value = "soundcard"
        prod_search = Product.objects.full_search(value)
        cat_search = search_all_categories(value)
        if cat_search:
            print(f"Cat_list: {(cat_search, cat_search.query_type) if not hasattr(cat_search, 'suggestions') else (cat_search, 'These are suggestions')}")
        else:
            print("No Category items found")
        if prod_search:
            print(f"Prod_list: {(prod_search, prod_search.query_type) if not hasattr(prod_search, 'suggestions') else (prod_search, 'These are suggestions')}")
        else:
            print("No Products found")


class TestCategoryManager(TestCase):
    fixtures = ["product_fixtures.json"]

    def test_get_product_list(self):
        audio_int_cat = Category.objects.get(name="Audio Interfaces")
        midi_keyboard_subcat = SubCategory1.objects.get(name="Active")
        list_ = audio_int_cat.get_product_list()
        self.assertEqual(len(list_), len(audio_int_cat.products.all()))
        list_ = midi_keyboard_subcat.get_product_list()
        self.assertEqual(len(list_), len(midi_keyboard_subcat.products.all()))



