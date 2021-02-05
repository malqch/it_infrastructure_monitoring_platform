from rest_framework import serializers
from script.models import Script, ScriptLog, ScriptTimedTask

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'

class ScriptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptLog
        fields = '__all__'

class ScriptTimedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptTimedTask
        fields = '__all__'