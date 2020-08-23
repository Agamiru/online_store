from .models import *


# instance = Image model instance
def storage_dir(instance, filename) -> str:
    product_instance = Product.objects.get(pk=instance.prod_id)
    if not product_instance:
        raise ValueError("Model received None as response")
    brand_name = product_instance.get_brand_name.replace(" ", "_")
    model_name = product_instance.model_name.replace(" ", "_")

    return f"{brand_name}/{model_name}/{filename}"

