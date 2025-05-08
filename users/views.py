from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                email=data["email"],
                name=data["name"],
                nickname=data["nickname"],
                question=data["question"],
                answer=data["answer"],
                password=make_password(data["password"]),
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
            })
        else:
            return Response({'error': '로그인 실패'}, status=status.HTTP_401_UNAUTHORIZED)
