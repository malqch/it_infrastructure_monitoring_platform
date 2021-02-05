from rest_framework import serializers
from sys_auth.models import User, Role, Token, Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(read_only=True, many=True)

    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Token
        fields = '__all__'
