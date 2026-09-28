# Recall API

학습 노트를 바탕으로 복습 문제를 생성하고 복습 일정을 관리하는 서비스입니다.

## 현재 구현

- FastAPI 초기 구성
- 상태 확인 API: GET /health
- 자동 API 문서: /docs
- PostgreSQL 연결 및 첫 `users` 테이블 migration (인증 API는 아직 없음)

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

## 검사 방법

```powershell
uv sync --locked --dev
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

첫 명령은 `uv.lock`에 기록된 개발 의존성을 설치합니다. `pytest`는 `/health`의 HTTP 응답을 확인하고, Ruff는 Python 코드의 정적 오류와 형식을 검사합니다. 같은 검사가 GitHub Actions에서도 실행됩니다.

외부 AI API 설정은 아직 필요하지 않습니다. 여러 컴퓨터에서 작업할 때는 GitHub의 최신 변경을 받은 뒤 위 명령으로 확인하세요. `.env`와 로컬 DB 데이터는 기기마다 별도로 준비해야 합니다. 현재 구현 구조는 `docs/ARCHITECTURE.md`, 작업 인수인계는 `docs/HANDOFF.md`에 기록합니다.
