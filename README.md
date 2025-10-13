# SKN16-4th-1Team
SKN 16기 4차 단위프로젝트

# Cartoon Diary Scaffold

4컷 일기 카툰 생성 웹앱의 Django 기반 코드 스캐폴드를 정의하고 있습니다. 사용자가 작성한 일기를 기반으로 OpenAI GPT 프롬프트와 Hugging Face Qwen/Qwen-Image 모델을 활용해 4컷 카툰을 자동 생성하는 제품을 목표로 합니다. 자세한 제품 요구사항은 `prd.md`를 참고하세요.

## 주요 기능 로드맵
- 이메일 기반 회원가입/로그인 및 프로필 관리
- 일기 CRUD와 월간 캘린더 뷰
- 일기 → GPT 프롬프트 → 이미지 4컷 생성 → 합성 파이프라인
- 생성 이력 조회, 재생성, 다운로드 기능 (확장 예정)

## 기술 스택
- Python 3.11+, Django 5, Django REST Framework
- Celery + Redis(브로커/결과 저장소)
- OpenAI API, Hugging Face Hub (`Qwen/Qwen-Image`)
- Pillow, Requests, pytest/pytest-django

## 디렉터리 구조
```text
cartoon_diary/
├─ config/                 # 프로젝트 설정, Celery 초기화
├─ apps/
│  ├─ accounts/           # 사용자 인증/회원정보 API
│  ├─ profiles/           # 프로필 모델 및 API
│  ├─ diaries/            # 일기 도메인, REST API, 캘린더 뷰
│  ├─ generation/         # 프롬프트·이미지 생성 파이프라인
│  ├─ dashboard/          # 요약/대시보드 템플릿 뷰
│  └─ core/               # 공통 추상 모델·유틸리티
├─ integrations/           # OpenAI/HF 래퍼, 이미지 합성 등
├─ services/               # 도메인 오케스트레이션 레이어
├─ workers/                # Celery 큐/스케줄 정의
├─ templates/, static/, media/
├─ tests/                  # pytest 기반 테스트 스켈레톤
└─ scripts/                # 개발용 스크립트
```

## 로컬 개발 환경 구성
1. Python 3.11 이상을 준비합니다.
2. 가상환경 생성 및 활성화 후 의존성을 설치합니다.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r cartoon_diary/requirements/dev.txt
   ```
3. 환경 변수를 설정합니다.
   - `.env` 등을 활용해 `DJANGO_SECRET_KEY`, `OPENAI_API_KEY`, `HUGGINGFACE_TOKEN`, `CELERY_BROKER_URL` 등을 지정하세요.
4. 데이터베이스 마이그레이션과 슈퍼유저를 생성합니다.
   ```bash
   cd cartoon_diary
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. 개발 서버와 Celery 워커를 실행합니다.
   ```bash
   python manage.py runserver
   celery -A config.celery worker -l INFO
   ```

## 테스트 실행
```bash
pytest
```

## 추가 문서
- `prd.md`: 제품 요구사항 정리
- `docs/adr/`: 아키텍처 의사결정 기록(초안)
- `docs/api/`: API 스펙 및 예제(작성 예정)

기여 시에는 PR 템플릿과 코딩 컨벤션을 추가로 정의할 예정이며, 이 문서를 최신 상태로 유지해 주세요.
