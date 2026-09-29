# Recall API

학습 노트를 바탕으로 복습 문제를 생성하고 복습 일정을 관리하는 서비스입니다.

## 현재 구현

- FastAPI 초기 구성
- 상태 확인 API: GET /health
- 자동 API 문서: /docs
- PostgreSQL 연결 및 첫 `users` 테이블 migration
- 회원가입, 로그인, 현재 사용자 확인 API

## 개발 환경

- Python 3.13
- uv
- FastAPI
- Uvicorn
- PostgreSQL 17 (Docker Compose)

## 실행 방법

```powershell
uv sync
uv run uvicorn recall_api.main:app --reload --app-dir src
```

실행 후 http://127.0.0.1:8000/docs 에서 API를 확인할 수 있습니다. `/health`는 DB 연결 없이 응답합니다.

## 로컬 데이터베이스

1. `.env.example`을 `.env`로 복사하고 빈 값을 채웁니다. `POSTGRES_USER`, `POSTGRES_DB`와 `POSTGRES_PORT`는 원하는 로컬 값을 정하고, `POSTGRES_PASSWORD`에는 로컬 개발용 비밀번호를 지정합니다. `DATABASE_URL`에는 같은 값을 사용한 `postgresql+psycopg://사용자:비밀번호@127.0.0.1:포트/DB이름` 형식의 주소를 적습니다. 특수 문자가 들어간 비밀번호는 URL 인코딩이 필요합니다. `.env`는 Git에 포함되지 않습니다.
2. DB를 시작하고 첫 migration을 적용합니다.

```powershell
Copy-Item .env.example .env
# .env의 빈 값을 먼저 채우세요.
docker compose up -d db
uv sync --locked --dev
uv run --locked alembic upgrade head
uv run --locked alembic current
```

첫 migration은 계정의 이메일, 비밀번호 해시, 시간대와 생성 시각을 저장하는 `users` 테이블을 만듭니다. 실제 비밀번호나 노트 내용은 저장소에 넣지 마세요. `GET /health`는 DB 상태를 검사하는 API가 아닙니다.

DB를 중지할 때는 `docker compose down`을 사용합니다. 볼륨은 유지되므로 데이터는 남습니다. 되돌리기를 검증할 때는 **개발용 빈 DB에서만** `uv run --locked alembic downgrade base`를 실행하세요. 이 명령은 `users` 테이블을 삭제합니다. 이후 `upgrade head`로 다시 생성할 수 있습니다.

## 인증 API

`.env`의 `AUTH_SECRET_KEY`에 무작위로 생성한 최소 32바이트의 비밀 문자열을 설정합니다. 배포 환경에서는 secret 관리 기능으로 주입하고 저장소에 기록하지 않습니다. 이 값이 없으면 로그인과 인증 요청에서 설정 오류가 발생합니다.

- `POST /auth/register`: JSON `{"email":"person@example.com","password":"8자 이상"}`으로 가입합니다. 이메일은 앞뒤 공백을 제거하고 소문자로 저장하며, 중복 이메일은 409입니다.
- `POST /auth/login`: 같은 JSON으로 로그인해 30분 유효한 Bearer 토큰을 받습니다. 잘못된 이메일이나 비밀번호는 401입니다.
- `GET /auth/me`: `Authorization: Bearer <토큰>`으로 현재 계정을 확인합니다. 토큰이 없거나 유효하지 않으면 401입니다.

비밀번호는 Argon2로 해시해 저장합니다. 토큰에는 사용자 ID와 만료 시간만 들어가며 로그아웃·토큰 폐기는 아직 지원하지 않습니다. `/health`는 인증이나 DB 설정 없이 그대로 동작합니다.

## 검사 방법

```powershell
uv sync --locked --dev
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

첫 명령은 `uv.lock`에 기록된 개발 의존성을 설치합니다. `pytest`는 `/health`의 HTTP 응답을 확인하고, Ruff는 Python 코드의 정적 오류와 형식을 검사합니다. 같은 검사가 GitHub Actions에서도 실행됩니다.

외부 AI API 설정은 아직 필요하지 않습니다. 여러 컴퓨터에서 작업할 때는 GitHub의 최신 변경을 받은 뒤 위 명령으로 확인하세요. `.env`와 로컬 DB 데이터는 기기마다 별도로 준비해야 합니다. 현재 구현 구조는 `docs/ARCHITECTURE.md`, 작업 인수인계는 `docs/HANDOFF.md`에 기록합니다.
