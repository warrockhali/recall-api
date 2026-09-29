# 현재 구조

이 문서는 구현된 구조를 기록한다. 목표 기능과 개발 원칙은 `AGENTS.md`를 참고한다.

## API

`src/recall_api/main.py`의 FastAPI 앱은 `GET /health`와 인증 라우터를 제공한다. `/health`는 DB에 연결하지 않으므로 프로세스가 요청에 응답하는지만 확인한다. DB 상태 확인 API는 아직 없다.

## 인증

`auth/schemas.py`는 이메일·비밀번호 입력을 검증하고 이메일을 정규화한다. `auth/router.py`는 회원가입·로그인·현재 사용자 조회 HTTP 응답과 Bearer 인증 의존성을 담당한다. `auth/service.py`는 Argon2 해시, 사용자 저장·조회, 30분 만료 서명 토큰을 담당한다. 토큰에는 사용자 ID와 만료 시간만 담고, 인증 요청마다 토큰을 검증한 뒤 DB에서 사용자를 다시 찾는다. 자세한 선택 이유와 한계는 `docs/decisions/001-auth-tokens.md`에 기록한다.

## 데이터베이스

`src/recall_api/db/session.py`는 `.env` 또는 환경 변수의 `DATABASE_URL`을 읽어 동기 SQLAlchemy 엔진을 만든다. DB를 처음 사용할 때만 주소가 필요하다. 연결의 세션 시간대는 UTC이며, 연결 상태를 재사용하기 전에 확인한다.

이후 DB를 사용하는 요청은 `get_session()`으로 요청별 Session을 받아야 한다. Session은 요청이 끝나면 닫힌다. 이 의존성은 자동으로 commit하지 않는다. 서비스 로직이 데이터 변경의 성공 범위를 정하고 commit하거나 실패 시 rollback해야 한다. Worker를 추가할 때도 작업별로 별도 Session을 만든다.

`src/recall_api/db/models.py`의 첫 모델은 `users`다. 이메일은 유일하며, 비밀번호 해시와 사용자 시간대(기본 UTC), 생성 시각을 저장한다. 회원가입에서 한 행을 insert하고 commit하며, 중복 이메일이면 rollback한다. 로그인과 현재 사용자 조회는 읽기만 한다.

## 스키마 변경

`migrations/versions/`의 Alembic migration이 DB 스키마를 변경한다. 앱 시작 시 테이블을 자동 생성하지 않는다. 새 환경에서는 `alembic upgrade head`를 적용하고, 모델과 DB의 차이는 `alembic check`로 확인한다. 첫 migration은 `users` 테이블을 만들며, `downgrade base`는 이 테이블을 삭제한다.

## 다음 단계

노트 테이블과 API를 추가할 때 인증 의존성을 적용하고 다른 사용자의 데이터 접근을 막는다.
