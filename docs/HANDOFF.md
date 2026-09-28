# Current Development Status

## Current Issue

GitHub Issue #2 — 기본 테스트·Ruff·CI와 인수인계 문서 준비.

## Branch

`main`

## Completed

- FastAPI 초기 구성과 `GET /health`.
- 저장소의 개발 규칙을 `AGENTS.md`에 추가함(Issue #1).
- `/health` 테스트, 개발 검사 명령, GitHub Actions 구성.

## Verification

- 2026-09-28: `/health` 테스트 1개 통과. `uv run --locked pytest -q`는 이 PC의 애플리케이션 제어 정책이 `.venv/Scripts/python.exe`를 차단해 실행되지 않았다. uv가 설치한 Python 3.13과 동일한 `.venv` 패키지로 직접 실행해 확인했다.
- 2026-09-28: `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv lock --check` 통과.
- GitHub Actions 결과는 첫 push 후 확인한다.

## Current Problem

- 아직 PostgreSQL, 인증, 노트 기능이 없다.
- 이 PC에서는 `.venv/Scripts/python.exe`가 애플리케이션 제어 정책에 의해 차단된다. 다른 PC의 `uv run` 동작과 구분해서 확인한다.

## Next Step

Issue #2의 검사를 완료한 뒤 Stage 1의 DB 연결과 첫 Alembic migration 작업을 시작한다.

## Important Context

- 실제 앱 진입점은 `src/recall_api/main.py`다.
- 첫 버전의 목표 기술과 현재 구현은 `AGENTS.md`에서 구분한다.
- 복습 간격과 AI 호출 비용 상한은 아직 결정되지 않았다.
