import random
from dataclasses import field
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from core.models import User, VerifyPhoneNumber


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "phone_number",
            "last_name",
            "user_type",
            "OTP",
        ]

    OTP = serializers.CharField(max_length=4)

    def validate(self, attrs):
        OTP = attrs.pop("OTP")
        validOTP = (
            VerifyPhoneNumber.objects.filter(phone_number=attrs.get("phone_number"))
            .filter(OTP=OTP)
            .filter(OTP_for=VerifyPhoneNumber.OTP_NEW_ACCOUNT)
            .filter(expire_at__gt=datetime.now())
            .exists()
        )
        if not validOTP:
            raise serializers.ValidationError("OTP Expires")
        return attrs

    # def create(self, validated_data):
    #     print(validated_data)
    #     raise serializers.ValidationError("My Error")
    #     # return Review.objects.create(product_id=product_id, **validated_data)
    #     return User.objects.create(**validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name", "phone_number"]


class VerifyPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPhoneNumber
        fields = ["phone_number", "OTP", "OTP_for"]

    OTP = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        phone_number = self.validated_data["phone_number"]
        try:  # update
            VerifyPhoneNumber_item = VerifyPhoneNumber.objects.get(
                phone_number=phone_number
            )
            VerifyPhoneNumber_item.OTP = random.randint(1000, 9999)
            VerifyPhoneNumber_item.expire_at = datetime.now() + timedelta(minutes=5)
            VerifyPhoneNumber_item.save()
            self.instance = VerifyPhoneNumber_item
        except VerifyPhoneNumber.DoesNotExist:
            # add
            self.instance = VerifyPhoneNumber.objects.create(**self.validated_data)

        return self.instance
