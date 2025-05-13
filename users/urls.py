from django.urls import path
from .views import SignupView, LoginView, LogoutView, WithdrawView, PasswordResetVerifyView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('find-password/', PasswordResetVerifyView.as_view(), name='password_verify'),
    
    path('mypage/', WithdrawView.as_view(), name='withdraw'), #탈퇴는 임시
]
