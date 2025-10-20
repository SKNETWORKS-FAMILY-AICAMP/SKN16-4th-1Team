from datetime import datetime
import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages

from .forms import AddForm
from .models import DiaryModel


@login_required
def entry(request):
    form = AddForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            note = request.POST['note']
            content = request.POST['content']
            selected_date = request.POST.get('selected_date', None)
            if selected_date:
                # 날짜 문자열을 datetime으로 변환
                posted_date = datetime.strptime(selected_date, '%Y-%m-%d')
            else:
                # 날짜 선택 안 했으면 오늘
                posted_date = datetime.now()
                
            productivity = request.POST['productivity']

            image_url = request.POST.get('image_url', '').strip()

            # ✅ 같은 날짜의 일기가 있는지 확인
            today_date = posted_date.date()
            existing_diary = DiaryModel.objects.filter(
                author=request.user,
                posted_date__date=today_date
            ).first()

            if existing_diary:
                # 기존 일기 수정
                existing_diary.note = note
                existing_diary.content = content
                existing_diary.productivity = productivity
                if image_url:
                    existing_diary.image_url = image_url
                existing_diary.save()
                todays_diary = existing_diary
            else:
                # 새 일기 생성
                todays_diary = DiaryModel()
                todays_diary.author = request.user
                todays_diary.note = note
                todays_diary.posted_date = posted_date
                todays_diary.content = content
                todays_diary.productivity = productivity
                if image_url:
                    todays_diary.image_url = image_url
                todays_diary.save()

            form = AddForm()
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


@login_required
def show(request):
    # ✅ 자신의 일기만 조회
    diaries = DiaryModel.objects.filter(author=request.user).order_by('posted_date')
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


@login_required
def detail(request, diary_id):
    # ✅ 자신의 일기만 조회
    diary = get_object_or_404(DiaryModel, pk=diary_id, author=request.user)

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
    
def download_image(request, diary_id):
    """이미지를 로컬 PC에 PNG로 다운로드"""
    try:
        # ✅ 자신의 일기만 조회
        diary = get_object_or_404(DiaryModel, pk=diary_id, author=request.user)
        
        if not diary.image_url:
            return HttpResponse('이미지가 없습니다.', status=404)
        
        # S3에서 이미지 가져오기
        response = requests.get(diary.image_url)
        
        if response.status_code == 200:
            # PNG 파일로 다운로드
            http_response = HttpResponse(response.content, content_type='image/png')
            http_response['Content-Disposition'] = f'attachment; filename="네컷일기_{diary.posted_date.strftime("%Y%m%d")}.png"'
            return http_response
        else:
            return HttpResponse('이미지를 가져올 수 없습니다.', status=500)
            
    except Exception as e:
        print(f"[DOWNLOAD] ❌ 에러: {str(e)}")
        return HttpResponse(f'다운로드 실패: {str(e)}', status=500)

@login_required
def productivity(request):
    # ✅ 자신의 일기만 조회
    data = DiaryModel.objects.filter(author=request.user).order_by('posted_date')[:10]
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


@login_required
def generate_image(request, diary_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        from .Image_making.pipeline import generate_and_attach_image_to_diary

        # ✅ 자신의 일기만 처리
        diary = get_object_or_404(DiaryModel, pk=diary_id, author=request.user)
        
        generate_and_attach_image_to_diary(diary_id, language='en')
        diary.refresh_from_db()
        return JsonResponse({'status': 'ok', 'temp_image_url': diary.temp_image_url})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def save_image(request, diary_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        from .Image_making.pipeline import save_temp_image_to_s3

        # ✅ 자신의 일기만 처리
        diary = get_object_or_404(DiaryModel, pk=diary_id, author=request.user)
        
        s3_url = save_temp_image_to_s3(diary_id)

        if s3_url:
            return JsonResponse({'status': 'ok', 'image_url': s3_url})
        else:
            return JsonResponse({'status': 'error', 'message': 'S3 upload failed'}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


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


def signup(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"[SIGNUP] 닉네임: {nickname}")
        print(f"[SIGNUP] 이메일: {email}")
        
        if not email or not password:
            messages.error(request, '이메일과 비밀번호를 입력해주세요.')
            return render(request, 'entry/signup.html')
        
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, '이미 사용 중인 이메일입니다.')
                return render(request, 'entry/signup.html')
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            if nickname:
                user.first_name = nickname
                user.save()
            
            print(f"[SIGNUP] ✅ 회원가입 성공! User ID: {user.id}")
            
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('login')
            
        except Exception as e:
            print(f"[SIGNUP] ❌ 에러: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'회원가입 중 오류가 발생했습니다: {str(e)}')
            return render(request, 'entry/signup.html')
    
    return render(request, 'entry/signup.html')


@login_required
def profile_view(request):
    return render(request, 'entry/profile.html')


@login_required
def settings_view(request):
    return render(request, 'entry/settings.html')


# ✅ API 함수들
@login_required
def diary_dates_api(request):
    """사용자의 모든 일기 작성 날짜를 반환"""
    try:
        # ✅ 자신의 일기만 조회
        diary_dates = DiaryModel.objects.filter(author=request.user).values_list('posted_date__date', flat=True).distinct()
        date_list = [str(date) for date in diary_dates if date]
        
        return JsonResponse({
            'status': 'ok',
            'dates': date_list
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
def diary_by_date_api(request, date):
    """특정 날짜의 일기 데이터를 반환"""
    try:
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # ✅ 자신의 일기만 조회
        diary = DiaryModel.objects.filter(
            author=request.user,
            posted_date__date=target_date
        ).order_by('-posted_date').first()
        
        if diary:
            print(f"[API] ✅ 일기 발견")
            print(f"[API] ID: {diary.id}")
            print(f"[API] 작성자: {diary.author.username}")
            print(f"[API] 제목: {diary.note}")
            print(f"[API] S3 이미지 URL: {diary.image_url if diary.image_url else '없음'}")
            
            return JsonResponse({
                'status': 'ok',
                'data': {
                    'id': diary.id,
                    'note': diary.note,
                    'content': diary.content,
                    'productivity': diary.productivity,
                    'image_url': diary.image_url if diary.image_url else None,
                    'date': diary.posted_date.strftime('%Y-%m-%d')
                }
            })
        else:
            return JsonResponse({
                'status': 'empty',
                'message': '해당 날짜의 일기가 없습니다.'
            })
            
    except Exception as e:
        print(f"[API] ❌ 에러: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
