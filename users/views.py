from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from users.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from rest_framework.permissions import AllowAny


class DuplicateCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        nickname = request.query_params.get('nickname')

        if email and User.objects.filter(email=email).exists():
            return Response({"email": "이미 사용 중인 이메일입니다."}, status=status.HTTP_200_OK)

        if nickname and User.objects.filter(nickname=nickname).exists():
            return Response({"nickname": "이미 사용 중인 닉네임입니다."}, status=status.HTTP_200_OK)

        return Response({"message": "사용 가능한 이메일 및 닉네임입니다."}, status=status.HTTP_200_OK)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        nickname = data.get("nickname")

        try:
            user = User.objects.create(
                email=email,
                name=data["name"],
                nickname=nickname,
                question=data["question"],
                answer=data["answer"],
                password=make_password(data["password"]),
                role=data.get("role", "user"),
            )
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user.lastlogin_at = timezone.now()
            user.save()
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'nickname': user.nickname,
                'role': user.role,
            })
        else:
            return Response({'error': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 완료"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)

class PasswordResetVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        question = request.data.get("question")
        answer = request.data.get("answer")

        try:
            user = User.objects.get(email=email)
            if user.question != question or user.answer != answer:
                return Response({"error": "입력하신 내용이 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "확인되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "해당 이메일의 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
