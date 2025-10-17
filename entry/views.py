from datetime import datetime
import shutil
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .Image_making.pipeline import FINAL_MEDIA_SUBDIR
from .forms import AddForm, SignupForm
from .models import DiaryModel


def entry(request):
    form = AddForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            note = request.POST['note']
            content = request.POST['content']
            posted_date = datetime.now()
            productivity = request.POST['productivity']
            image_url = request.POST.get('image_url', '').strip()

            todays_diary = DiaryModel()
            todays_diary.note = note
            todays_diary.posted_date = posted_date
            todays_diary.content = content
            todays_diary.productivity = productivity
            if image_url:
                todays_diary.image_url = image_url

            todays_diary.save()

            # Pass diary id so the template can immediately trigger image generation
            form = AddForm()  # reset to blank form after saving
            return render(
                request,
                'entry/add.html',
                {
                    'title': 'Add Entry',
                    'subtitle': "Add what you feel and we'll store it for you.",
                    'add_highlight': True,
                    'addform': form,
                    'new_diary_id': todays_diary.id,
                }
            )

        # Invalid form: re-render page with errors
        return render(
            request,
            'entry/add.html',
            {
                'title': 'Add Entry',
                'subtitle': "Add what you feel and we'll store it for you.",
                'add_highlight': True,
                'addform': form,
            }
        )

    return render(
        request,
        'entry/add.html',
        {
            'title': 'Add Entry',
            'subtitle': 'Add what you feel and we\'ll store it for you.',
            'add_highlight': True,
            'addform': form,
        }
    )


def show(request):
    """
        We need to show the diaries sorted by date posted in descending order
        5:32 PM 10/19/19 by Arjun Adhikari
    """
    diaries = DiaryModel.objects.order_by('posted_date')
    icon = True if len(diaries) == 0 else None

    return render(
        request,
        'entry/show.html',
        {
            'show_highlight': True,
            'title': 'All Entries',
            'subtitle': 'It\'s all you\'ve written.',
            'diaries': reversed(diaries),
            'icon': icon
        }
    )


def detail(request, diary_id):
    diary = get_object_or_404(DiaryModel, pk=diary_id)

    return render(
        request,
        'entry/detail.html',
        {
            'show_highlight': True,
            'title': diary.note,
            'subtitle': diary.posted_date,
            'diary': diary
        }
    )


def productivity(request):
    
    """
        At max, draw chart for last 10 data.
        11:24 PM 10/19/19 by Arjun Adhikari
    """
    data = DiaryModel.objects.order_by('posted_date')[:10]
    icon = True if len(data) == 0 else None

    return render(
        request,
        'entry/productivity.html',
        {
            'title': 'Productivity Chart',
            'subtitle': 'Keep the line heading up always.',
            'data': data,
            'icon': icon
        }
    )


@require_POST
def generate_image(request, diary_id):
    try:
        from .Image_making.pipeline import generate_and_attach_image_to_diary

        _, temp_url, _ = generate_and_attach_image_to_diary(diary_id, language='en')
        diary = get_object_or_404(DiaryModel, pk=diary_id)
        response_url = temp_url or diary.temp_image_url
        return JsonResponse({'status': 'ok', 'temp_image_url': response_url})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def _resolve_media_path(url: str) -> Optional[Path]:
    if not settings.MEDIA_URL:
        return None
    media_url = settings.MEDIA_URL.rstrip('/')
    normalized_url = url.rstrip('/')
    if normalized_url.startswith(media_url):
        rel = normalized_url[len(media_url):].lstrip('/')
    elif settings.MEDIA_URL and normalized_url.startswith(settings.MEDIA_URL):
        rel = normalized_url[len(settings.MEDIA_URL):].lstrip('/')
    else:
        return None
    return Path(settings.MEDIA_ROOT) / rel


@require_POST
def finalize_image(request, diary_id):
    diary = get_object_or_404(DiaryModel, pk=diary_id)
    if not diary.temp_image_url:
        return JsonResponse({'status': 'error', 'message': '임시 이미지가 없습니다.'}, status=400)

    temp_url = diary.temp_image_url
    final_url = temp_url

    temp_path = _resolve_media_path(temp_url)
    if temp_path and temp_path.exists():
        final_dir = Path(settings.MEDIA_ROOT) / FINAL_MEDIA_SUBDIR
        final_dir.mkdir(parents=True, exist_ok=True)
        new_name = temp_path.name.replace('temp_', 'final_', 1)
        final_path = final_dir / new_name
        shutil.move(str(temp_path), final_path)
        rel_path = final_path.relative_to(Path(settings.MEDIA_ROOT))
        final_url = settings.MEDIA_URL.rstrip('/') + '/' + rel_path.as_posix()

    diary.image_url = final_url
    diary.temp_image_url = None
    diary.save(update_fields=['image_url', 'temp_image_url'])

    return JsonResponse({
        'status': 'ok',
        'image_url': final_url,
        'detail_url': reverse('detail', args=[diary.id]),
    })




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            authenticated_user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, '회원가입이 완료되었습니다.')
                return redirect('entry')

            messages.info(request, '회원가입이 완료되었습니다. 로그인해 주세요.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(
        request,
        'entry/signup.html',
        {
            'title': '회원가입',
            'subtitle': '새로운 일기장을 시작해 보세요.',
            'form': form,
        }
    )
