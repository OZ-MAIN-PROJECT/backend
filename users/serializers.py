from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


# 유저 조회/수정용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'nickname', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'role', 'created_at', 'updated_at']


# 회원가입용
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'question', 'answer', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            question=validated_data['question'],
            answer=validated_data['answer'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# 비밀번호 변경용
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
