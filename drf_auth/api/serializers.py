from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'contactId')  # Не включайте пароль здесь
        ref_name = 'CustomUserSerializer'  # Уникальное имя для этого сериализатора


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'contactId')
        extra_kwargs = {
            'contactId': {'required': True},
            'password': {'write_only': True}
        }
        ref_name = 'CustomUserCreateSerializer'  # Уникальное имя для этого сериализатора