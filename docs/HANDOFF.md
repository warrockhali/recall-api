# Current Development Status

## Current Issue

GitHub Issue #7 — Issue 제목 형식 통일. Issue #3의 DB PR #4와 Issue #5의 PR 규칙 PR #6은 머지되었다.

## Branch

`codex/7-issue-titles` (검토 대상: `main`)

## Completed

- FastAPI 초기 구성과 `GET /health`.
- 저장소의 개발 규칙을 `AGENTS.md`에 추가함(Issue #1).
- `/health` 테스트, 개발 검사 명령, GitHub Actions 구성.
- 동기 SQLAlchemy 연결, 요청별 Session 의존성, 첫 `users` 모델·migration, 로컬 PostgreSQL Compose 구성.
- PR #6에서 사용자 검토 후 Squash merge하는 규칙과 템플릿을 반영함. 저장소의 허용 머지 방식은 Squash merge만으로 설정함.
- 기존 Issue 제목을 커밋·PR과 같은 `type(scope): 설명` 형식으로 정리함.

## Verification

- 2026-09-28: `/health` 테스트 1개 통과. `uv run --locked pytest -q`는 이 PC의 애플리케이션 제어 정책이 `.venv/Scripts/python.exe`를 차단해 실행되지 않았다. uv가 설치한 Python 3.13과 동일한 `.venv` 패키지로 직접 실행해 확인했다.
- 2026-09-28: `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv lock --check` 통과.
- 2026-09-28: [GitHub Actions CI 실행](https://github.com/warrockhali/recall-api/actions/runs/36383145718) 통과. 의존성 설치, 테스트, Ruff 검사와 형식 검사 모두 성공.
- 2026-09-28: 로컬 PostgreSQL에서 `users` migration 적용 및 모델·스키마 비교 통과. 별도 빈 DB에서 적용 → 되돌리기 → 재적용을 검증했고, 세션의 UTC 설정과 데이터 쓰기·조회 후 rollback을 확인했다. 검증용 DB는 삭제했다.
- 2026-09-28: 변경 후 pytest 1개, Ruff 검사·형식 검사, lockfile·Compose 설정 검사 통과.
- 2026-09-28: [GitHub Actions CI 실행](https://github.com/warrockhali/recall-api/actions/runs/36387359846) 통과. 새 PostgreSQL에서 migration 적용·스키마 비교·되돌리기·재적용과 테스트·Ruff 검사 모두 성공.
- 2026-09-28: PR #4의 일반 머지를 동일한 파일 내용의 스쿼시 커밋으로 정리한 뒤 [main CI](https://github.com/warrockhali/recall-api/actions/runs/36389041526) 통과. 원래 머지 커밋은 `codex/backup-main-before-squash-pr4`에 보관함.
- 2026-09-28: [PR #6 CI](https://github.com/warrockhali/recall-api/actions/runs/36389229308) 통과 후 사용자에 의해 Squash merge됨.

## Current Problem

- 인증·노트 API는 아직 없다.
- 이 PC에서는 `.venv/Scripts/python.exe`가 애플리케이션 제어 정책에 의해 차단된다. 다른 PC의 `uv run` 동작과 구분해서 확인한다.
- 로컬 DB는 이 PC의 Docker Compose에서 실행 중이다. `.env`는 Git에서 제외되며 다른 기기에는 별도 설정이 필요하다.

## Next Step

Issue #7의 PR을 검토하고 사용자가 승인하면 Squash merge한다. 이후 인증 기능을 작은 Issue로 시작한다. 이메일 정규화와 비밀번호 해시 방식을 먼저 정하고, 사용자별 데이터 접근 제한을 검증한다.

## Important Context

- 실제 앱 진입점은 `src/recall_api/main.py`다.
- 첫 버전의 목표 기술과 현재 구현은 `AGENTS.md`에서 구분한다.
- 복습 간격과 AI 호출 비용 상한은 아직 결정되지 않았다.
