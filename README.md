# Recall API

학습 노트를 바탕으로 복습 문제를 생성하고 복습 일정을 관리하는 서비스입니다.

## 현재 구현

- FastAPI 초기 구성
- 상태 확인 API: GET /health
- 자동 API 문서: /docs

## 개발 환경

- Python 3.13
- uv
- FastAPI
- Uvicorn

## 실행 방법

```powershell
uv sync
uv run uvicorn recall_api.main:app --reload --app-dir src
```

실행 후 http://127.0.0.1:8000/docs 에서 API를 확인할 수 있습니다.

## 검사 방법

```powershell
uv sync --locked --dev
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

첫 명령은 `uv.lock`에 기록된 개발 의존성을 설치합니다. `pytest`는 `/health`의 HTTP 응답을 확인하고, Ruff는 Python 코드의 정적 오류와 형식을 검사합니다. 같은 검사가 GitHub Actions에서도 실행됩니다.

현재 DB나 외부 API 설정은 필요하지 않습니다. 여러 컴퓨터에서 작업할 때는 GitHub의 최신 변경을 받은 뒤 위 명령으로 확인하세요. 작업 인수인계는 `docs/HANDOFF.md`에 기록합니다.
