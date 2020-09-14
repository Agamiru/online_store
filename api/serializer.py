from rest_framework import serializers
from .models import FakeItem


class FakeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FakeItem
        fields = "__all__"

