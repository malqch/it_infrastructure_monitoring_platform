from rest_framework import serializers
from patrol.models import Patrol

class PatrolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrol
        fields = '__all__'
