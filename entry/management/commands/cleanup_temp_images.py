# entry/management/commands/cleanup_temp_images.py

from datetime import datetime, timedelta
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone 
from entry.models import DiaryModel


class Command(BaseCommand):
    help = '24시간 이상 된 임시 이미지 파일들을 삭제합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='몇 시간 이상 된 파일을 삭제할지 설정 (기본값: 24시간)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='실제 삭제하지 않고 삭제 대상만 확인'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']
        
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        self.stdout.write(f'{hours}시간 이상 된 임시 이미지를 정리합니다...')
        if dry_run:
            self.stdout.write('DRY RUN 모드: 실제 삭제하지 않습니다.')
        
        # 1. DB에서 오래된 임시 이미지가 있는 일기들 찾기
        old_temp_diaries = DiaryModel.objects.filter(
            temp_image_url__isnull=False,
            posted_date__lt=cutoff_time
        )
        
        deleted_count = 0
        error_count = 0
        
        for diary in old_temp_diaries:
            try:
                # 2. 파일 경로 확인
                temp_path = self._resolve_media_path(diary.temp_image_url)
                
                if temp_path and temp_path.exists():
                    if not dry_run:
                        # 3. 파일 삭제
                        temp_path.unlink()
                        self.stdout.write(f'파일 삭제: {temp_path}')
                    else:
                        self.stdout.write(f'삭제 대상: {temp_path}')
                
                if not dry_run:
                    # 4. DB에서 temp_image_url 제거
                    diary.temp_image_url = None
                    diary.save(update_fields=['temp_image_url'])
                
                deleted_count += 1
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'일기 ID {diary.id} 처리 중 오류: {str(e)}')
                )
        
        # 5. 결과 출력
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'정리 대상: {deleted_count}개 파일')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'성공적으로 {deleted_count}개 파일 삭제')
            )
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(f'오류 발생: {error_count}개')
            )

    def _resolve_media_path(self, url):
        """URL에서 실제 파일 경로를 추출"""
        if not settings.MEDIA_URL or not url:
            return None
        
        media_url = settings.MEDIA_URL.rstrip('/')
        normalized_url = url.rstrip('/')
        
        if normalized_url.startswith(media_url):
            rel_path = normalized_url[len(media_url):].lstrip('/')
            return Path(settings.MEDIA_ROOT) / rel_path
        
        return None