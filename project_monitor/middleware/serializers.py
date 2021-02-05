from rest_framework import serializers
from middleware.models import Middleware, MiddlewareItem


class MiddlewareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Middleware
        fields = '__all__'


class MiddlewareItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddlewareItem
        fields = '__all__'
