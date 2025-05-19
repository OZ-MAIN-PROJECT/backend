from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import SignupSerializer, UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer
from community.serializers import CommunitySerializer
from community.models import Community

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"message": "비밀번호가 재설정되었습니다."}, status=200)
            except User.DoesNotExist:
                return Response({"error": "해당 이메일의 사용자가 존재하지 않습니다."}, status=404)

        return Response(serializer.errors, status=400)

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


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        written_count = Community.objects.filter(user=user).count()
        liked_count = Community.objects.filter(user=user).count()

        return Response({
            "nickname": user.nickname,
            "email": user.email,
            "written_count": written_count,
            "liked_count": liked_count,
        })

    def put(self, request):
        user = request.user
        data = request.data

        if 'nickname' in data:
            if User.objects.filter(nickname=data['nickname']).exclude(pk=user.pk).exists():
                return Response({"error": "이미 사용 중인 닉네임입니다."}, status=400)
            user.nickname = data['nickname']

        if 'email' in data:
            if User.objects.filter(email=data['email']).exclude(pk=user.pk).exists():
                return Response({"error": "이미 사용 중인 이메일입니다."}, status=400)
            user.email = data['email']

        user.save()
        return Response({"message": "회원정보 수정 완료"}, status=200)

    def delete(self, request):
        password = request.data.get("password")
        if not request.user.check_password(password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=400)

        request.user.delete()
        return Response({"message": "회원 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(current_password):
                return Response({"error": "현재 비밀번호가 일치하지 않습니다."}, status=400)

            user.set_password(new_password)
            user.save()
            return Response({"message": "비밀번호가 변경되었습니다."}, status=200)

        return Response(serializer.errors, status=400)

class MyCommunityPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'page': self.page.number,
            'size': self.page.paginator.per_page,
            'totalPages': self.page.paginator.num_pages,
            'totalElements': self.page.paginator.count
        })

class MyCommunityPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        filter_type = request.query_params.get('filter')
        paginator = MyCommunityPagination()

        if filter_type == 'liked':
            posts = Community.objects.filter(community_likes__user=user).order_by('-created_at')
        else:
            posts = Community.objects.filter(user=user).order_by('-created_at')

        result_page = paginator.paginate_queryset(posts, request)
        serialized = CommunitySerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serialized.data)