# ADR-0005: 작업(Task) 처리 스텁 로직

Status: Accepted
Date: 2025-10-14

## Context
- 카툰 생성/재생성 요청은 비동기적으로 처리되며, PRD 11.5의 상태 폴링 규격을 맞춰야 함.

## Decision
- `docs/api/common.py`의 `new_task`, `maybe_complete_task`로 대기열/완료를 모사한다.
- `/api/tasks/{task_id}` 또는 `/api/cartoons/{diary_id}` 조회 시 일정 시간(약 1.5초) 경과 후 `succeeded` 상태와 패널 결과를 반환하도록 한다.

## Consequences
- 장점: 프론트엔드/클라이언트가 폴링/상태 전이를 미리 통합 테스트 가능.
- 단점: 실제 모델 호출/워커 분산/재시도 로직은 포함되지 않음.
- 향후: Celery/RQ/Arq 등 워커와 메시지 브로커(예: Redis)로 전환하고, 태스크 영속화/로깅 강화.

