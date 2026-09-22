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