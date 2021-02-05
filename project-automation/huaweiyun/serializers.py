from rest_framework import serializers
from huaweiyun.models import HuaweiyunManager

class HuaweiyunManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuaweiyunManager
        fields = '__all__'