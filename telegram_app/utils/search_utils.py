from products.models import Product, search_all_categories

# Types
django_model = Product


def search_products(search_value: str):
    prod_res = Product.objects.full_search(search_value)
    cat_res = search_all_categories(search_value)

    if prod_res:
        if not hasattr(prod_res, "suggestions"):
            for prod_obj in prod_res.results:
                markup = ProductMarkup(prod_obj).message()
        elif not hasattr(cat_res, "suggestions"):
            for cat_obj in cat_res.results:
                cat_obj.products.all()


class ProductMarkup:
    def __init__(self, inst: Product):
        self.full_name = inst.full_name
        self.short_desc = inst.short_desc
        self.price = inst.price
        self.category = inst.return_appropriate_category().name

    def message(self):
        markup = f"**Product:** *{self.full_name}* \n" \
            f"**Overview:** *{self.short_desc}* \n" \
            f"**Price:** *{self.price}* \n" \
            f"**Category:** *{self.category}*"

        return markup
