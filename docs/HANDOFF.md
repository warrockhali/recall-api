# Current Development Status

## Current Issue

GitHub Issue #9 — 회원가입·로그인과 현재 사용자 확인. 이전 Issue #7의 PR #8은 머지되었다.

## Branch

`codex/9-auth-api` (검토 대상: `main`)

## Completed

- 기존 FastAPI `/health`, 동기 SQLAlchemy 연결과 `users` migration, 기본 CI가 `main`에 반영되어 있다.
- Issue #9에서 이메일 정규화, Argon2 비밀번호 해시, 30분 유효한 Bearer 토큰과 현재 사용자 조회를 구현했다.
- 인증 설계 결정을 `docs/decisions/001-auth-tokens.md`에 기록했다. DB 스키마 변경은 없다.

## Verification

- 2026-09-29: `uv run --locked ... pytest tests/test_health.py -q` 1개 통과. Ruff 검사와 형식 검사 통과.
- 인증 통합 테스트는 새 PostgreSQL에서 실행하는 GitHub Actions CI 결과를 확인해야 한다. 이 PC에는 현재 Docker 엔진이 연결되어 있지 않다.

## Current Problem

- 노트 API와 사용자별 노트 접근 제한은 아직 없다.
- 토큰 폐기·갱신, 이메일 확인, 비밀번호 재설정은 첫 인증 작업 범위 밖이다.
- 이 PC에서는 `uv`의 Python 버전 링크가 깨져 명시적인 Python 경로로 `uv lock`과 `uv sync`를 실행했다.

## Next Step

Issue #9의 PR과 CI를 검토한다. 사용자가 머지를 요청하면 Squash merge한다. 다음 작업은 노트 및 노트 버전 모델·API와 사용자 소유권 검사를 작은 Issue로 진행한다.

## Important Context

- 실제 앱 진입점은 `src/recall_api/main.py`다.
- 배포 환경의 `AUTH_SECRET_KEY`는 최소 32바이트로 설정해야 하며 저장소에 기록하지 않는다.
- 복습 간격과 AI 호출 비용 상한은 아직 결정되지 않았다.
