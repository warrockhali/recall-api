# 현재 구조

이 문서는 구현된 구조를 기록한다. 목표 기능과 개발 원칙은 `AGENTS.md`를 참고한다.

## API

`src/recall_api/main.py`의 FastAPI 앱은 현재 `GET /health`만 제공한다. 이 경로는 DB에 연결하지 않으므로 프로세스가 요청에 응답하는지만 확인한다. DB 상태 확인 API는 아직 없다.

## 데이터베이스

`src/recall_api/db/session.py`는 `.env` 또는 환경 변수의 `DATABASE_URL`을 읽어 동기 SQLAlchemy 엔진을 만든다. DB를 처음 사용할 때만 주소가 필요하다. 연결의 세션 시간대는 UTC이며, 연결 상태를 재사용하기 전에 확인한다.

이후 DB를 사용하는 요청은 `get_session()`으로 요청별 Session을 받아야 한다. Session은 요청이 끝나면 닫힌다. 이 의존성은 자동으로 commit하지 않는다. 서비스 로직이 데이터 변경의 성공 범위를 정하고 commit하거나 실패 시 rollback해야 한다. Worker를 추가할 때도 작업별로 별도 Session을 만든다.

`src/recall_api/db/models.py`의 첫 모델은 `users`다. 이메일은 유일하며, 비밀번호 해시와 사용자 시간대(기본 UTC), 생성 시각을 저장한다. 회원가입·로그인 로직은 아직 없다.

## 스키마 변경

`migrations/versions/`의 Alembic migration이 DB 스키마를 변경한다. 앱 시작 시 테이블을 자동 생성하지 않는다. 새 환경에서는 `alembic upgrade head`를 적용하고, 모델과 DB의 차이는 `alembic check`로 확인한다. 첫 migration은 `users` 테이블을 만들며, `downgrade base`는 이 테이블을 삭제한다.

## 다음 단계

인증 기능을 만들 때 이메일 정규화, 비밀번호 해시 방식, 사용자별 접근 제한을 정하고 테스트한다. 노트 테이블과 API는 그다음 단계에서 추가한다.
