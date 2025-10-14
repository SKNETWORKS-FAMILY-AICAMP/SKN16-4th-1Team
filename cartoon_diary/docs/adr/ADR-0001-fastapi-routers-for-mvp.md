# ADR-0001: FastAPI Routers for API MVP

Status: Accepted
Date: 2025-10-14

## Context
- PRD 11에 정의된 API(Auth, Bootstrap, Profile, Diaries, Cartoons, Tasks)를 빠르게 제공해야 함.
- 프로젝트는 Django 기반이지만, 초기 MVP 단계에서 API를 빠르게 검증할 필요가 있음.

## Decision
- `cartoon_diary/docs/api` 디렉터리에 각 영역별 FastAPI `APIRouter`를 모듈로 구성한다.
  - `auth.py`, `Bootstrap.py`, `Profile.py`, `Diaries.py`, `Cartoons.py`, `Tasks.py`
- 라우터는 상위 앱에서 `app.include_router(...)` 형태로 조립하여 실행한다.
- Django와의 통합은 후속 단계에서 ASGI 마운트 또는 게이트웨이 선택 후 진행한다.

## Consequences
- 장점: 구현/변경 속도가 빠르고, 모듈 단위 테스트가 용이하다.
- 단점: 현재는 Django 프로젝트와 실행 경로가 분리되어 있으며, 통합 설계가 필요하다.
- 향후: 운영 단계에서 인증/세션, 로깅, 미들웨어 정책을 통합해야 한다.

