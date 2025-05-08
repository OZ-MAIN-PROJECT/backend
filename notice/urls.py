from django.urls import path
from . import views

urlpatterns = [
    # 공지사항 목록 조회 (검색 포함, 로그인 유저만)
    path('', views.NoticeListView.as_view(), name='notice-list'),

    # 공지사항 상세 조회 (조회수 기록 포함)
    path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice-detail'),

    # 공지사항 등록 (관리자만)
    path('create/', views.NoticeCreateView.as_view(), name='notice-create'),

    # 공지사항 수정 (관리자만)
    path('<int:pk>/update/', views.NoticeUpdateView.as_view(), name='notice-update'),

    # 공지사항 삭제 (관리자만)
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice-delete'),

    # 공지사항 좋아요 토글 (로그인 유저만)
    path('<int:notice_id>/like/', views.NoticeLikeToggleView.as_view(), name='notice-like'),
]
