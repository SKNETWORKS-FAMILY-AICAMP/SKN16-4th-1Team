# ADR-0004: 요구사항(Requirements) 레이아웃 결정

Status: Accepted
Date: 2025-10-14

## Context
- 루트의 `requriment.txt`는 삭제하고, 표준화된 위치인 `cartoon_diary/requirements/`에서 관리.
- FastAPI 및 실행 필수 패키지를 추가해야 함.

## Decision
- `base.txt`에 공통 의존성 추가: `fastapi`, `PyJWT`, `passlib[bcrypt]`, `python-multipart`, `email-validator`.
- `prod.txt`는 `uvicorn[standard]` 유지. `dev.txt`는 `-r base.txt`로 상속.

## Consequences
- 장점: 개발/운영 환경 분리와 일관성 확보, 의존성 관리 단순화.
- 단점: 루트에서 설치하던 습관과 경로가 달라져 문서/가이드 정비 필요.

