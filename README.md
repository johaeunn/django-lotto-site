# Django Lotto Site

Django와 Docker를 사용하여 구현한 6/45 로또 웹 사이트입니다.  
일반 사용자는 로또를 수동 또는 자동으로 구매하고, 구매 내역과 당첨 결과를 확인할 수 있습니다.  
관리자는 판매 내역 확인, 추첨 실행, 판매/당첨 통계 확인 기능을 사용할 수 있습니다.

---

## 주요 기능

### 일반 사용자

- 회원가입, 로그인, 로그아웃
- 수동 로또 구매
- 자동 로또 구매
- 내 구매 내역 확인
- 당첨 결과 확인
- 당첨번호 및 보너스 번호 일치 표시

### 관리자

- Django Admin 접속
- 관리자 대시보드 확인
- 전체 판매 내역 확인
- 추첨 실행
- 회차별 판매/당첨 통계 확인

---

## 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Django |
| Database | PostgreSQL |
| Container | Docker, Docker Compose |
| Frontend | HTML, CSS, JavaScript |

---

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/본인아이디/django-lotto-site.git
cd django-lotto-site
```

### 2. 환경변수 파일 생성

```bash
cp .env.example .env
```

Windows PowerShell에서는 다음 명령어를 사용할 수 있습니다.

```powershell
copy .env.example .env
```

`.env` 예시:

```env
DB_NAME=lotto_db
DB_USER=lotto_user
DB_PASSWORD=lotto_password
DB_HOST=db
DB_PORT=5432
```

### 3. Docker 컨테이너 실행

```bash
docker compose up --build
```

### 4. DB 마이그레이션

새 터미널에서 실행합니다.

```bash
docker compose exec web python manage.py migrate
```

### 5. 관리자 계정 생성

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. 접속

```text
http://localhost:8000/
```

---

## 주요 URL

| URL | 설명 |
|---|---|
| `/` | 메인 페이지 |
| `/signup/` | 회원가입 |
| `/login/` | 로그인 |
| `/buy/manual/` | 수동 로또 구매 |
| `/buy/auto/` | 자동 로또 구매 |
| `/tickets/` | 내 구매 내역 |
| `/results/` | 당첨 결과 확인 |
| `/admin/` | Django Admin |
| `/admin/dashboard/` | 관리자 대시보드 |
| `/admin/draw/` | 추첨 실행 |
| `/admin/results/` | 판매/당첨 통계 |

---

## 프로젝트 구조

```text
LOTTOPROJECT/
├── config/
├── lotto/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── registration/
│       └── login.html
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── .env.example
└── README.md
```

---

## 당첨 등수 기준

| 등수 | 조건 |
|---|---|
| 1등 | 당첨번호 6개 일치 |
| 2등 | 당첨번호 5개 일치 + 보너스 번호 일치 |
| 3등 | 당첨번호 5개 일치 |
| 4등 | 당첨번호 4개 일치 |
| 5등 | 당첨번호 3개 일치 |
| 낙첨 | 그 외 |
