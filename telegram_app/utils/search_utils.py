from typing import Iterable, Optional, Tuple

from django.db.models import QuerySet

from products.models import Product, search_all_categories
from .general_utils import markdown_sanitizer

# Types
prod_obj = Product


def search_products(search_value: str) -> Optional[Tuple[Iterable[prod_obj], bool]]:
    """
    Searches and returns a tuple of queryset and a boolean that indicates if the
    queryset are suggestions. If no results return None.
    """
    prod_res = Product.objects.full_search(search_value)
    cat_res = search_all_categories(search_value)
    cat_prod_set = set()
    sugg_set = set()        # Suggestion set, might need to add order if needed
    if prod_res and not hasattr(prod_res, "suggestions"):   # Suggestions are last resort
        return prod_res.results, False
    elif cat_res and not hasattr(cat_res, "suggestions"):
        for cat_obj in cat_res.results:
            cat_prod_set.update(cat_obj.get_product_list())
        return cat_prod_set, False
    elif prod_res and hasattr(prod_res, "suggestions"):
        return prod_res.results, True
    elif cat_res and hasattr(cat_res, "suggestions"):
        for cat_obj in cat_res.results:
            sugg_set.update(cat_obj.get_product_list())
        return sugg_set, True
    else:
        return


class ProductMarkup:
    def __init__(self, inst: Product):
        self.full_name = inst.full_name
        self.short_desc = inst.short_desc
        self.price = "{:,}".format(int(inst.price))
        self.category = inst.return_appropriate_category_name()

    def message(self):
        markup = f"**Product:** *{markdown_sanitizer(self.full_name)}* \n" \
            f"**Overview:** *{markdown_sanitizer(self.short_desc)}* \n" \
            f"**Price:** *{markdown_sanitizer(self.price)}* \n" \
            f"**Category:** *{markdown_sanitizer(self.category)}*"

        return markup
