from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import AttendanceForm, PasswordForm
from .models import Attendance

def signup_password(request):
    error = None
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == 'hibari68th':
            request.session['is_user_authenticated'] = True
            return redirect('signup')
        error = 'パスワードが違います'
    else:
        form = PasswordForm()
    return render(request, 'attendance/password.html', {
        'form': form,
        'error': error
    })

def signup(request):
    # 出欠登録用パスワード認証チェック
    if not request.session.get('is_user_authenticated', False):
        return redirect('signup_password')

    error = None
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            student_class = form.cleaned_data['student_class']
            name          = form.cleaned_data['name']
            status        = form.cleaned_data['status']

            # --- 複数レコード対策: 先に既存レコードを全て削除 ---
            Attendance.objects.filter(
                student_class=student_class,
                name=name
            ).delete()

            # 新しく一件だけ作成
            Attendance.objects.create(
                student_class=student_class,
                name=name,
                status=status,
                created_at=timezone.now()
            )

            return render(request, 'attendance/thanks.html')
        # バリデーション失敗時
        error = '入力に誤りがあります'
    else:
        form = AttendanceForm()

    return render(request, 'attendance/signup.html', {
        'form': form,
        'error': error
    })

def admin_password(request):
    error = None
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == 'reunion':
            request.session['is_admin_authenticated'] = True
            return redirect('admin_list')
        error = 'パスワードが違います'
    else:
        form = PasswordForm()
    return render(request, 'attendance/password.html', {
        'form': form,
        'error': error
    })

from django.shortcuts import render, redirect
from django.db.models import Case, When, IntegerField
from .models import Attendance

def admin_list(request):
    if not request.session.get('is_admin_authenticated', False):
        return redirect('admin_password')

    sort = request.GET.get('sort')
    qs = Attendance.objects.all()

    if sort == 'student_class':
        order_case = Case(
            When(student_class='月', then=0),
            When(student_class='星', then=1),
            When(student_class='雪', then=2),
            When(student_class='虹', then=3),
            When(student_class='その他', then=4),
            output_field=IntegerField(),
        )
        qs = qs.annotate(cls_order=order_case).order_by('cls_order', 'name')
    else:
        qs = qs.order_by('-created_at')

    # カウント集計
    total_count   = qs.count()
    attend_count  = qs.filter(status='出席').count()
    absent_count  = qs.filter(status='欠席').count()

    return render(request, 'attendance/admin_list.html', {
        'records': qs,
        'current_sort': sort,
        'total_count': total_count,
        'attend_count': attend_count,
        'absent_count': absent_count,
    })