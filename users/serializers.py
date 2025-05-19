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
        fields = ['email', 'name', 'nickname', 'question', 'answer', 'password', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        is_superuser = validated_data.get('is_superuser', False)
        is_staff = validated_data.get('is_staff', False)
        role = 'admin' if is_superuser or is_staff else 'user'

        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            question=validated_data['question'],
            answer=validated_data['answer'],
            is_superuser=is_superuser,
            is_staff=is_staff,
            role=role,
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

# 비밀번호 찾기 변경용
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

