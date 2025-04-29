from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Swagger 세팅
schema_view = get_schema_view(
    openapi.Info(
        title="SSY API 문서",
        default_version='v1',
        description="SSY API 서버 문서입니다",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # 각 앱 API 연결
    path('api/accounts/', include('accounts.urls')),  # (원래 user -> accounts)
    path('api/wallet/', include('wallet.urls')),
    path('api/stats/', include('stats.urls')),        # (원래 statistics -> stats)
    path('api/community/', include('community.urls')),

    # JWT 토큰 발급 및 갱신
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger 문서
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
