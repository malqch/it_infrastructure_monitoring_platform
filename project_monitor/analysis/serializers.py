from rest_framework import serializers
from analysis.models import ServerAnalysis


class ServerAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerAnalysis
        fields = '__all__'

