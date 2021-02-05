from rest_framework import serializers
from sys_relation.models import User, Role


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = '__all__'

