from typing import Tuple

from django.contrib import admin
from .models import (
    Product, Brand, Category, SubCategory1,
    SubCategory2, ModelName, CategoryAccessoryJoin,
    CategoryBoughtTogetherJoin, Subcat1AccessoryJoin,
    Subcat1BoughtTogetherJoin, Subcat2AccessoryJoin,
    Subcat2BoughtTogetherJoin,
)

from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError, ObjectDoesNotExist as doesntExist

from .utils.admin_utils import (
    FormSpecsField, FormCommaNewLineSeparatedField, AbstractJoinForm,
    AbstractCategoryForm, CustomHstoreField, CustomUrlField, create_pub_ids,
)
from .utils.image_utils import upload_image_or_error
################### PRODUCT ######################


class ProductForm(forms.ModelForm):
    """
    Special clean method implemented for product form to auto-fill 'weight'
    and 'package_dimensions' and also handle other intricacies that could occur
    while retrieving and saving specs from database.
    """

    specs = FormSpecsField()
    in_the_box = FormCommaNewLineSeparatedField()
    features_alias = FormCommaNewLineSeparatedField(required=False)
    full_name = fields.CharField(disabled=True, required=False)
    variants = CustomHstoreField(required=False)
    image_1 = CustomUrlField(required=False)
    image_2 = CustomUrlField(required=False)
    image_3 = CustomUrlField(required=False)

    def clean(self):
        self._validate_unique = True
        specs = self.cleaned_data.get("specs")  # Can be "in_database", json or None

        # Image Processing
        brand, model_name = self.cleaned_data["brand"], self.cleaned_data.get("model_name", "Generic")
        # Todo: For now variants are just one dict, update to cater for more in the future
        variants = [v for v in self.cleaned_data.get("variants", {}).values()]
        for i, pub_id in enumerate(create_pub_ids(brand, model_name, variants)):
            i += 1
            self.upload_images_from_form(i, pub_id)

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
                # It's best to use values from the instance itself while saving to avoid this
                self.cleaned_data["specs"] = instance_specs

                # Sets appropriate package dimensions and weight using existing specs data
                instance_specs_pd = instance_specs.get("Box Dimensions (LxWxH)")
                instance_specs_pd = instance_specs_pd[0] if instance_specs_pd else None
                instance_specs_w = instance_specs.get("Package Weight")
                instance_specs_w = instance_specs_w[0] if instance_specs_w else None

                # In case package dimension and weight fields are empty during updating
                # use values from existing specs if available
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

    def upload_images_from_form(self, idx: int, pub_id: str) -> None:
        """
        Checks for image urls in form, compares them with product instance version if any
        and uploads to cloudinary servers if form img url is different or the first upload.
        It is to be run from a loop, hence it only breaks after uploads.
        """

        # Upload to cloudinary servers or add field error
        def upload_image_(self, img_url_, pub_id_):
            upload_or_err = upload_image_or_error(img_url_, pub_id_)  # Returns a dict of cloudinary image details
            if isinstance(upload_or_err, Exception):
                self.add_error(f"image_{idx}", upload_or_err.__str__())
            else:
                url = upload_or_err.get("secure_url")
                if url is None:
                    # Remember, this automatically pops given field from self.cleaned_data
                    self.add_error(f"image_{idx}", "This image wasn't successfully uploaded")
                else:
                    self.cleaned_data[f"image_{idx}"] = url

        # Check form image urls for disparities with instance urls if any
        inst_img_url = getattr(self.instance, f"image_{idx}")
        for k, img_url in self.cleaned_data.items():
            # Check for new product and upload as appropriate
            if k == f"image_{idx}" and img_url is not None and \
                    inst_img_url is None:   # Instance has no such url, first upload
                upload_image_(self, img_url, pub_id)
                break
            # Check for existing product uploads
            else:
                if k == f"image_{idx}" and img_url is not None and \
                        inst_img_url is not None:  # Image instance has a value for this form field
                    # Compare images
                    if img_url != inst_img_url:
                        upload_image_(self, img_url, pub_id)
                    break

    class Meta:
        model = Product
        fields = "__all__"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "short_desc",)
    # list_display_links = ("brand", "model_name",)
    list_editable = ("price", "short_desc")

    form = ProductForm


###################### CATEGORY #######################

class CategoryForm(AbstractCategoryForm):
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


class CategoryBoughtTogetherJoinForm(AbstractJoinForm):
    class Meta:
        model = CategoryBoughtTogetherJoin
        fields = "__all__"


@admin.register(CategoryAccessoryJoin)
class CategoryAccessoryJoinAdmin(admin.ModelAdmin):
    form = CategoryAccessoryJoinForm


@admin.register(CategoryBoughtTogetherJoin)
class CategoryBoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = CategoryBoughtTogetherJoinForm


################# SUB CATEGORY 1 #########################

class SubCategory1Form(AbstractCategoryForm):
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


class Subcat1BoughtTogetherJoinForm(AbstractJoinForm):
    class Meta:
        model = Subcat1BoughtTogetherJoin
        fields = "__all__"


@admin.register(Subcat1AccessoryJoin)
class Subcat1AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat1AccessoryJoinForm


@admin.register(Subcat1BoughtTogetherJoin)
class Subcat1BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat1BoughtTogetherJoinForm


################# SUB CATEGORY 2 #########################

class SubCategory2Form(AbstractCategoryForm):
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


class Subcat2BoughtTogetherJoinForm(AbstractJoinForm):
    class Meta:
        model = Subcat2BoughtTogetherJoin
        fields = "__all__"


@admin.register(Subcat2AccessoryJoin)
class Subcat2AccessoryJoinAdmin(admin.ModelAdmin):
    form = Subcat2AccessoryJoinForm


@admin.register(Subcat2BoughtTogetherJoin)
class Subcat2BoughtTogetherJoinAdmin(admin.ModelAdmin):
    form = Subcat2BoughtTogetherJoinForm


admin.site.register(Brand)
admin.site.register(ModelName)



