from django.test import TestCase
from django.db.models.expressions import Value as V
from django.db.models.functions import Cast, Greatest, Coalesce
from django.db.models import CharField, F, Func, Case, When, Value, Q, IntegerField as I
from django.contrib.postgres.search import TrigramSimilarity, SearchVector

from ..models import Product, search_all_categories, Category


class TestProductManager(TestCase):

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



