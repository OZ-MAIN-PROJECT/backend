from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    PasswordResetVerifyView,
    DuplicateCheckView,
    MyPageView,
    ChangePasswordView,
    MyCommunityPageView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('find-password/', PasswordResetVerifyView.as_view(), name='password_verify'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),



    path('mypage/', MyPageView.as_view(), name='mypage'),  # 유저 정보 수정 및 탈퇴
    path('mypage/check-duplicate/', DuplicateCheckView.as_view(), name='check_duplicate'),  # 이메일/닉네임 중복 확인
    path('mypage/change-password/', ChangePasswordView.as_view(), name='change_password'),  # 비밀번호 변경
    path('mypage/posts/', MyCommunityPageView.as_view(), name='mypage_posts'), # 내가작성한글및좋아요한글 갯수랑 게시글보기
]
