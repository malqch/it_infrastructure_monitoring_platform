from rest_framework import serializers
from databases.models import Databases, DBItem


class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Databases
        fields = '__all__'


class DBItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBItem
        fields = '__all__'
