from rest_framework import serializers
from storage.models import StorageItem


class StorageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageItem
        fields = '__all__'
