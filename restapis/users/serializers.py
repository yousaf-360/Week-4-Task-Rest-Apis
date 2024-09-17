from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the `CustomUser` model.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'specialization', 'is_staff', 'is_superuser', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Create and return a new `CustomUser` instance, given the validated data.
        """
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `CustomUser` instance, given the validated data.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
