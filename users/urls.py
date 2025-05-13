from django.urls import path
from .views import SignupView, LoginView, LogoutView, WithdrawView, PasswordResetVerifyView, DuplicateCheckView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('find-password/', PasswordResetVerifyView.as_view(), name='password_verify'),
    path('check-duplicate/', DuplicateCheckView.as_view(), name='check_duplicate'), # 닉네임 이메일 중복확인
    
    path('mypage/', WithdrawView.as_view(), name='withdraw'), #탈퇴는 임시
]
