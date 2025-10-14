# ADR-0003: In-Memory Store 사용 (MVP)

Status: Accepted
Date: 2025-10-14

## Context
- 빠른 프로토타입을 위해 DB 스키마 및 마이그레이션 없이 API 동작을 검증해야 함.

## Decision
- `docs/api/common.py`에서 간단한 파이썬 딕셔너리 기반 저장소를 사용한다.
  - users, profiles, diaries, cartoons, tasks, 시퀀스 카운터 등 포함
- 작업(Tasks)은 요청 시점에 시간 경과를 확인하여 자동 완료로 전환하는 간단한 로직을 둔다.

## Consequences
- 장점: 개발 속도 극대화, 의존성 최소화, 즉시 테스트 가능.
- 단점: 휘발성 데이터로 서버 재시작 시 초기화됨. 동시성/다중 프로세스 환경에 부적합.
- 향후: Django ORM 또는 별도 서비스(DB/캐시/큐)로 단계적 이전 필요.

