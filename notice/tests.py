from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from notice.models import Notice, NoticeLike, NoticeView


class NoticeAPITestCase(APITestCase):

    def setUp(self):
        # 관리자 유저
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass',
            is_staff=True
        )

        # 일반 유저
        self.normal_user = User.objects.create_user(
            email='user@example.com',
            password='userpass'
        )

        # 공지사항 생성
        self.notice = Notice.objects.create(
            user=self.admin_user,
            title='테스트 공지',
            content='테스트 공지 내용'
        )

        # 엔드포인트 경로 설정
        self.list_url = reverse('notice-list')
        self.detail_url = reverse('notice-detail', args=[self.notice.pk])
        self.create_url = reverse('notice-create')
        self.update_url = reverse('notice-update', args=[self.notice.pk])
        self.delete_url = reverse('notice-delete', args=[self.notice.pk])
        self.like_url = reverse('notice-like', args=[self.notice.pk])

    def test_목록조회_로그인필요(self):
        # 비로그인 상태
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 로그인 후
        self.client.force_login(self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_공지사항_상세조회_조회수기록(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.notice.title)

        # 조회수가 기록되었는지 확인
        self.assertTrue(NoticeView.objects.filter(user=self.normal_user, notice=self.notice).exists())

    def test_공지사항_등록_관리자만(self):
        self.client.force_login(self.normal_user)  # 일반유저
        data = {'title': '신규 공지', 'content': '내용'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.admin_user)
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
