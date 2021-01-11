from django.contrib import admin
from .models import (
    Product, Brand, Category, SubCategory1,
    SubCategory2, ModelName, CategoryAccessoryJoin,
    CategoryBoughtTogetherJoin, Subcat1AccessoryJoin,
    Subcat1BoughtTogetherJoin, Subcat2AccessoryJoin,
    Subcat2BoughtTogetherJoin,
)

from django import forms
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError, ObjectDoesNotExist as doesntExist
from django.forms.models import ModelForm

from .utils.admin_utils import (
    FormSpecsField, FormCommaNewLineSeparatedField, AbstractJoinForm
)

################### PRODUCT ######################


class ProductForm(forms.ModelForm):

    specs = FormSpecsField()
    in_the_box = FormCommaNewLineSeparatedField()
    features_alias = FormCommaNewLineSeparatedField()

    def clean(self):
        self._validate_unique = True
        specs = self.cleaned_data.get("specs")  # Can be "in_database", json or None

        if not specs:       # Ideally, field validations should have checked for this already
            raise ValidationError("This field receives 'None' as value")

        id_ = self.instance.id
        pd = self.cleaned_data.get("package_dimensions")  # Package Dimensions
        w = self.cleaned_data.get("weight")     # Weight

        try:
            obj = Product.objects.get(pk=id_)    # Try fetching existing object
            instance_specs = obj.specs      # Existing Object specs
            instance_itb = obj.in_the_box      # Existing Object in_the_box
            if specs == "in_database":
                # Sometimes, artifacts are introduced in the field input while displaying
                # existing values (bound_data).
                # It's best to use values from the model itself while saving to avoid this
                self.cleaned_data["specs"] = instance_specs

                # Sets appropriate package dimensions and weight using existing specs data
                instance_specs_pd = instance_specs.get("Box Dimensions (LxWxH)")
                instance_specs_pd = instance_specs_pd[0] if instance_specs_pd else None
                instance_specs_w = instance_specs.get("Package Weight")
                instance_specs_w = instance_specs_w[0] if instance_specs_w else None

                # In case package dimension and weight fields are empty during updating
                # use values from existing specs
                if not pd and instance_specs_pd is not None:
                    self.cleaned_data["package_dimensions"] = instance_specs_pd
                if not w and instance_specs_w is not None:
                    self.cleaned_data["weight"] = instance_specs_w

            # Use existing objects itb if available
            if self.cleaned_data.get("in_the_box") == "in_database":
                self.cleaned_data["in_the_box"] = instance_itb

        except doesntExist:    # For newly saved products
            try:
                package_dims = specs["Box Dimensions (LxWxH)"]
                # Use filled package dimensions if available, else take from specs
                if not pd:
                    self.cleaned_data["package_dimensions"] = package_dims[0]

            # Key error in case specs has no package dimensions
            # Type error in case "null" is returned as string indices must be integers
            except (KeyError, TypeError, IndexError) as e:
                # self.cleaned_data["specs"] = None
                pass
                self.add_error("package_dimensions", f"No package dimensions provided for reason '{e.__str__()}'")
                # Todo: Should display a message notifying the user there are no package_dimensions
                # self.add_error("package_dimensions", f"Specs has no {e}")

            try:
                weight = specs["Package Weight"]
                # Confirm weight from spec are same as filled, else use weight from specs
                if not w:
                    self.cleaned_data["weight"] = weight[0]
            except (KeyError, TypeError, IndexError) as e:
                self.add_error("weight", f"No weight provided for reason '{e.__str__()}'")
                pass
                # Todo: Should display a message notifying the user there is no weight
                # self.add_error("weight", f"Specs has no {e}")

        return self.cleaned_data

    class Meta:
        model = Product
        fields = "__all__"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "short_desc")
    # list_display_links = ("brand", "model_name",)
    list_editable = ("price", "short_desc")

    form = ProductForm


###################### CATEGORY #######################

class CategoryForm(ModelForm):
    alias = FormCommaNewLineSeparatedField()
    main_features = FormCommaNewLineSeparatedField()

    class Meta:
        model = Category
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm


class CategoryAccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = CategoryAccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }


class CategoryBoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = CategoryBoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }


@admin.register(CategoryAccessoryJoin)
class CategoryAccessoryJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]
    form = CategoryAccessoryJoinForm


@admin.register(CategoryBoughtTogetherJoin)
class CategoryBoughtTogetherJoinAdmin(admin.ModelAdmin):
    # list_display = ["cat_id", "accessory_id", "hash_field"]
    form = CategoryBoughtTogetherJoinForm


################# SUB CATEGORY 1 #########################

class SubCategory1Form(ModelForm):
    alias = FormCommaNewLineSeparatedField()
    main_features = FormCommaNewLineSeparatedField()

    class Meta:
        model = SubCategory1
        fields = "__all__"


@admin.register(SubCategory1)
class Subcat1Admin(admin.ModelAdmin):
    form = SubCategory1Form


class Subcat1AccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat1AccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }


class Subcat1BoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat1BoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }


@admin.register(Subcat1AccessoryJoin)
class Subcat1AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat1AccessoryJoinForm


@admin.register(Subcat1BoughtTogetherJoin)
class Subcat1BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat1BoughtTogetherJoinForm


################# SUB CATEGORY 2 #########################

class SubCategory2Form(ModelForm):
    alias = FormCommaNewLineSeparatedField()
    main_features = FormCommaNewLineSeparatedField()

    class Meta:
        model = SubCategory2
        fields = "__all__"


@admin.register(SubCategory2)
class Subcat2Admin(admin.ModelAdmin):
    form = SubCategory2Form


class Subcat2AccessoryJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat2AccessoryJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }


class Subcat2BoughtTogetherJoinForm(AbstractJoinForm):

    class Meta:
        model = Subcat2BoughtTogetherJoin
        fields = "__all__"
        widgets = {
            "hash_field": TextInput(attrs={"placeholder": "Do not fill", "hidden": True})
        }



@admin.register(Subcat2AccessoryJoin)
class Subcat2AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat2AccessoryJoinForm


@admin.register(Subcat2BoughtTogetherJoin)
class Subcat2BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat2BoughtTogetherJoinForm



admin.site.register(Brand)
admin.site.register(ModelName)



