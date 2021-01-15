from django.db.models import ObjectDoesNotExist as doesnt_exist

from .models import UniqueCategory


# For post_save signals
def save_or_update_unique_category(sender, instance, created, **kwargs):
    inst_name, inst_id = instance.name, instance.id
    model_name = instance.__class__.__name__

    if created:
        UniqueCategory.objects.create(name=inst_name, model_name=model_name, cat_id=inst_id)
    else:
        # cat_id and model_name are Unique Together, else might return more than one result
        # We cannot use only inst_name for look up as that might have been updated.
        unique_obj = UniqueCategory.objects.get(cat_id=inst_id, model_name=model_name)
        if unique_obj.name != inst_name:
            unique_obj.name = inst_name
            unique_obj.save(update_fields=["name"])


# For post_delete signals
def delete_unique_category(sender, instance, **kwargs):
    inst_id = instance.id
    try:
        unique_obj = UniqueCategory.objects.get(cat_id=inst_id)
        unique_obj.delete()
    except doesnt_exist:
        pass

