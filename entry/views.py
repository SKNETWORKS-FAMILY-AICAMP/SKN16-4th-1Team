from datetime import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .forms import AddForm
from .models import DiaryModel

from django.contrib.auth.models import User
from django.contrib.auth import login, logout

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

            # 저장 직후 동일 페이지에서 이미지 생성 트리거를 위해 id 전달
            form = AddForm()  # 새 폼으로 초기화
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

        # 유효하지 않으면 그대로 다시 렌더
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


def generate_image(request, diary_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    # OpenAI 파이프라인 실행 후 임시 URL을 모델에 저장
    try:
        from .Image_making.pipeline import generate_and_attach_image_to_diary

        generate_and_attach_image_to_diary(diary_id, language='en')
        diary = get_object_or_404(DiaryModel, pk=diary_id)
        return JsonResponse({'status': 'ok', 'temp_image_url': diary.temp_image_url})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def save_image(request, diary_id):
    """
    temp_image_url의 이미지를 S3에 업로드하고 image_url에 저장
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        from .Image_making.pipeline import save_temp_image_to_s3

        # S3에 업로드하고 URL 반환
        s3_url = save_temp_image_to_s3(diary_id)

        if s3_url:
            return JsonResponse({'status': 'ok', 'image_url': s3_url})
        else:
            return JsonResponse({'status': 'error', 'message': 'S3 upload failed'}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_http_methods(["GET"])
def get_diary_by_date(request, date_str):
    """
    특정 날짜의 일기 조회
    URL: /api/diary/<date_str>/
    예: /api/diary/2025-10-18/
    """
    try:
        from datetime import datetime
        
        # 날짜 문자열을 date 객체로 변환
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # ⭐ 해당 날짜의 일기 조회 (image_url 여부 상관없이 조회)
        diary = DiaryModel.objects.filter(
            posted_date__date=target_date
        ).order_by('-posted_date').first()
        
        if diary:
            print(f"[API] ✅ 일기 발견")
            print(f"[API] ID: {diary.id}")
            print(f"[API] 제목: {diary.note}")
            print(f"[API] S3 이미지 URL: {diary.image_url if diary.image_url else '없음'}")
            
            return JsonResponse({
                'status': 'ok',
                'data': {
                    'id': diary.id,
                    'note': diary.note,
                    'content': diary.content,
                    'productivity': diary.productivity,
                    'image_url': diary.image_url if diary.image_url else None,  # 있으면 S3 URL, 없으면 null
                    'posted_date': diary.posted_date.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        else:
            print(f"[API] ⚠️ 해당 날짜에 일기 없음")
            return JsonResponse({
                'status': 'empty',
                'message': '해당 날짜에 작성된 일기가 없습니다.'
            })
            
    except ValueError as e:
        print(f"[API] ❌ 날짜 형식 오류: {e}")
        return JsonResponse({
            'status': 'error',
            'message': '잘못된 날짜 형식입니다.'
        }, status=400)
    except Exception as e:
        import traceback
        print("[API] ❌ 예외 발생:")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_diary_dates(request):
    """
    일기가 작성된 모든 날짜 목록 조회
    URL: /api/diary/dates/
    """
    try:
        # 모든 일기의 날짜 조회 (posted_date__date로 날짜만 추출)
        diary_dates = DiaryModel.objects.values_list('posted_date__date', flat=True).distinct()
        
        # date 객체를 문자열로 변환
        date_list = [date.strftime('%Y-%m-%d') for date in diary_dates if date]
        
        return JsonResponse({
            'status': 'ok',
            'dates': date_list
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def login_view(request):
    if request.method == 'POST':
        email_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email_from_form)
            
            if user_obj.check_password(password_from_form):
                login(request, user_obj)
                return redirect('entry')
            else:
                return render(request, 'entry/login.html', {'error': '비밀번호를 잘못 입력했습니다.'})
        except User.DoesNotExist:
            return render(request, 'entry/login.html', {'error': '존재하지 않는 아이디(이메일)입니다.'})
    else:
        return render(request, 'entry/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    
def signup_view(request):
    return render(request, 'entry/signup.html')

def profile_view(request):
    return render(request, 'entry/profile.html')

def settings_view(request):
    return render(request, 'entry/settings.html')