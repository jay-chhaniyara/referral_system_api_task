from rest_framework import serializers
from .models import *

# Serializer of UserModel
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name', 'email', 'password', 'referral_code', 'timestamp']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  
        instance.save()
        return instance

# Serializer of Referral Model
class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
        fields = ['user', 'referred_by', 'timestamp']
        extra_kwargs = {'referred_by': {'write_only': True}, }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation
