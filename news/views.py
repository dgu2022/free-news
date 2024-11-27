from django.shortcuts import render, redirect
from news.forms import UserForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Post
from datetime import datetime
from django.utils.dateformat import DateFormat

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'news/post_list.html', {'posts': posts})

def post_list2(request):
    # model(DB)처리
    # Post 생성하기
    post = Post()
    # 쓴 글 전체 정보 조회하기
    # - cart_cnt : 정수값
    # - cart_list : [{'컬럼명' : 값 , '컬럼명' : 값 ...},{},{}]
    cart_cnt, cart_list = post.getPost()
    # 반환
    return render(
        request,
        "mysqlapp/cart/cart_list.html",
        {"cart_cnt" : cart_cnt,
         "cart_list" : cart_list}
    )

def error(request):
    return render(request, 'news/error.html', {})

def index(request):
    list_day_kr = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    today = DateFormat(datetime.now()).format('Y-m-d')
    day = list_day_kr[datetime.now().weekday()]
    return render(request, 'news/index.html', {'today': today, 'day': day})

def contact(request):
    return render(request, 'news/contact.html', {})

def detail_page(request):
    return render(request, 'news/detail-page.html', {})

def signup(request):
    return "gg"

def login_view(request):
    return render(request, "news/login.html", {})
    '''
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        mas = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        print(form.is_valid())
        template = "login.html"
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = raw_password)
            if user is not None:
                msg = "로그인 성공!!"
                login(request, user)
                template = "index.html"
        return render(request, template, {"form": form, "msg": msg})
    else:
        form = AuthenticationForm()
        return render(request, "news/login.html", {"form": form})
    '''

def register_view(request):
    return render(request, "news/signup.html", {})
    '''
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        mas = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        print(form.is_valid())
        template = "login.html"
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = raw_password)
            if user is not None:
                msg = "로그인 성공!!"
                login(request, user)
                template = "index.html"
        return render(request, template, {"form": form, "msg": msg})
    else:
        form = AuthenticationForm()
        return render(request, "news/login.html", {"form": form})
    '''
def logout_view(request):
    return render(request, "news/signup.html", {})
    '''
    def logout_view(request):
        logout(request)
        return redirect("login")
    '''

'''
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            row_password = form.cleaned_data.get("password1")
            # 사용자 인증 담당 : 아이디와 비밀번호가 DB랑 같은지 비교
            user = authenticate(username=username , password=row_password)
            # 로그인 담당 : 사용자에게 입력받은 request와 인증기록인 user를 통해 로그인 허용 또는 거부
            login(request, user)
            return redirect("index")
    else: # Get 요청일 떄
        form = UserForm()
    return render(request, "common/signup.html", {"form": form})
'''