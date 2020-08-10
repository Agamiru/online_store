from django.db import models

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = "categories"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "brands"


class AudioInterfaceFeatures(models.Model):
    cat_id = models.ForeignKey(
        Category, related_name="audio_interface_features",
        on_delete=models.CASCADE, null=False
    )
    # features = models.JSONField()
    # inputs = models.JSONField()
    # outputs = models.JSONField()
    connection_type = models.CharField(max_length=200)
    sample_rate = models.CharField(max_length=200)
    version = models.CharField(max_length=200)      # 2nd Gen, MKI, MK2
    power_source = models.CharField(max_length=200)

    class Meta:
        db_table = "audio_interface_features"


class Products(models.Model):
    cat_id = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE, null=False
    )
    features_id = models.OneToOneField(
        AudioInterfaceFeatures, on_delete=models.CASCADE,
        related_name="products", null=False, default=1
    )
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.CASCADE, default="Generic"
    )
    model_name = models.CharField(max_length=200, null=False)
    short_desc = models.CharField("Short Description", max_length=200)
    # in_the_box = models.JSONField()
    # specs = models.JSONField()
    package_dimensions = models.CharField(max_length=200)
    weight = models.IntegerField()

    class Meta:
        db_table = "products"








