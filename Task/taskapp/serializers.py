from rest_framework import serializers
from .models import User, Role, UserRole



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True,read_only = True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','roles', 'is_active']

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['user', 'role', 'is_active']

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)