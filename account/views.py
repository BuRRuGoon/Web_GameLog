from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth

from .models import BoardMember
from .forms import LoginForm

import re

# Create your views here.
def signup(request):
    if request.method == "GET":
        return render(request, 'account/signup.html')

    elif request.method == "POST":
        # 회원가입 폼에 빈값이 있는지 검사
        username    = request.POST.get('username', None)
        password    = request.POST.get('password1', None)
        re_password = request.POST.get('password2', None)
        email       = request.POST.get('email', None)
        nickname    = request.POST.get('nickname', None)
        signup_db = BoardMember.objects.all()
        print(type(username))
        # email 검증
        email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        regex = re.compile(email_reg)

        # 에러 메세지를 담을 변수
        res_data = {
            'username':username,
            'email':email,
            'nickname':nickname,
            'password':password,
            're_password':re_password,
        }
        if not (username and password and re_password and email and nickname):
            res_data['error'] = '빈값이 존재합니다 모든 값을 입력해주세요.'

        elif password != re_password:
            res_data['error'] = '비밀번호가 서로 다릅니다. 다시 입력해주세요.'
        
        elif signup_db.filter(username = request.POST.get('username', None)).exists():
            res_data['error'] = '동일한 아이디가 이미 존재합니다. 다시 입력해주세요.'

        elif signup_db.filter(email = request.POST.get('email', None)).exists():
            res_data['error'] = '동일한 이메일이 이미 존재합니다. 다시 입력해주세요.'
        
        elif signup_db.filter(nickname = request.POST.get('nickname', None)).exists():
            res_data['error'] = '동일한 닉네임이 이미 존재합니다. 다시 입력해주세요.'
        
        elif not regex.match(email):
            res_data['error'] = '유효한 이메일의 형식이 아닙니다. 다시 입력해주세요.'

        elif len(password) <= 7:
            res_data['error'] = '패스워드가 너무 짧습니다. 다시 입력해주세요.'
        
        else:
            member = BoardMember(
                username=username,
                password=make_password(password),
                email=email,
                nickname=nickname,
            )
            member.save()
            return render(request, 'account/signup_success.html')
        return render(request, 'account/signup.html', res_data)

def signup_success(request):
    return render(request, 'account/signup_success.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # session_code 검증하기
            request.session['user'] = form.user_id
            request.session['nickname'] = form.nickname
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})
    
def logout(request):
    request.session.clear()
    return redirect('/')

