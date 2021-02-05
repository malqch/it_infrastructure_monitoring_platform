import json

from rest_framework import serializers
from alarm.models import AlarmSeverity, AlarmStrategy, AlarmRule, AlarmDetail


class AlarmSeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmSeverity
        fields = '__all__'


class AlarmStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmStrategy
        fields = '__all__'


# class Jsonserializer(serializers.JSONField):
#     default_error_messages = {
#         'invalid_json': ('无效的json数据格式')
#     }
#
#     def to_representation(self, value):
#         return json.loads(value)
#
#     def to_internal_value(self, data):
#         try:
#             json.loads(data)
#         except (TypeError, ValueError):
#             self.fail('invalid_json')
#         return data


class AlarmRuleSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = AlarmRule
        fields = '__all__'


class AlarmDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlarmDetail
        fields = '__all__'



