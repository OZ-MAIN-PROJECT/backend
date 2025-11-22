# 써쓔 Backend – 감정을 기록하는 소비 가계부 API 서버

## ✏️ 프로젝트 소개

"써쓔" 백엔드는 감정 기반 소비 데이터를 안전하게 저장하고, 통계/리포트/커뮤니티 기능을 제공하는 **RESTful API 서버**입니다.  
---

## 📦 기술 스택

### Backend

- **Python 3.11+**
- **Django 4.x**
- **Django REST Framework (DRF)**

### Database

- **PostgreSQL**

### Infra / Tooling

- **AWS EC2**
- **Nginx** (리버스 프록시 & 정적 파일 서빙)
- **Gunicorn** (WSGI 서버)
- (선택) **Docker / Docker Compose**

### 기타

- **GitHub Actions** – CI/CD (테스트, 빌드, 배포 자동화)
- **.env** 환경 분리 – `local`, `dev`, `prod` 등
- **CORS / ALLOWED_HOSTS** – 환경별 허용 도메인 관리
- (선택) `django-environ` 또는 `python-dotenv` – 환경 변수 로딩

---

## 📁 폴더 구조

> 기본적인 Django + DRF 프로젝트 구조 예시입니다. 실제 앱 이름은 프로젝트 진행 중 조정될 수 있습니다.

```bash
ssusyeo-backend/
├── manage.py
├── pyproject.toml or requirements.txt
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py       # 공통 설정
│       ├── local.py      # 로컬 개발 환경
│       ├── dev.py        # 개발 서버 환경
│       └── prod.py       # 운영 서버 환경
├── apps/
│   ├── common/           # 공통 유틸, 공통 모델, 공통 응답/예외 처리
│   ├── users/            # 회원 도메인 (모델, 시리얼라이저, 뷰, 유스케이스)
│   ├── wallet/           # 지갑/계좌 도메인
│   ├── expenses/         # 지출 + 감정 기록 도메인
│   ├── categories/       # 카테고리 도메인
│   ├── reports/          # 통계/리포트 도메인
│   └── community/        # 커뮤니티 (게시글, 댓글, 좋아요)
├── scripts/              # 배포/마이그레이션 스크립트 등
└── .github/
    └── workflows/        # GitHub Actions 워크플로우
