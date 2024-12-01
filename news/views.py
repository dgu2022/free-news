from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .model.post_list import *
from datetime import datetime
from django.utils.dateformat import DateFormat
import pymysql

list_day_kr = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
today = DateFormat(datetime.now()).format('Y-m-d')
day = list_day_kr[datetime.now().weekday()]

def example(request):
    # model(DB)처리
    # Cart 생성하기
    post = MyPost()
    # 장바구니 전체 정보 조회하기
    # - cart_cnt : 정수값
    # - cart_list : [{'컬럼명' : 값 , '컬럼명' : 값 ...},{},{}]
    example_cnt = post.example()
    # 반환
    return render(
        request,
        "news/example.html",
        {"example_cnt" : example_cnt}
    )

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
    return render(request, 'news/404.html', {'today': today, 'day': day})

def mypage(request):
    return render(request, 'news/mypage.html', {'today': today, 'day': day})

def index(request):
    return render(request, 'news/index.html', {'today': today, 'day': day})

def contact(request):
    return render(request, 'news/contact.html', {'today': today, 'day': day})

def detail_page(request):
    return render(request, 'news/detail-page.html', {'today': today, 'day': day})

def register(request):
    if request.method == "POST":
        #username = request.POST['username']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']

        register = Register()
        #is_authenticated, result = Register.insert_member(self, username, password, email, role)
        register.insert_member(username, password, email, role)

        '''
        if is_authenticated:
            print("Authentication successful!") # 성공
            print("User Info:", result) # result에 user에 관한 정보 들어있어
            return render(request,'news/login.html', {'user' : result})
        else:
            print("Authentication failed:", result) # 실패
            return render(request,'news/404.html')
        '''
        print("회원가입이 완료됐습니다.")
        return render(request,'news/login.html',{'today': today, 'day': day})
    else:
        return render(request,'news/login.html',{'today': today, 'day': day})

def login(request):
    if request.method == "POST":
        #username = request.POST['username']
        username = request.POST['username']
        password = request.POST['password']
        login = Login()
        is_authenticated, result = login.authenticate_member(username, password)

        if is_authenticated:
            print("Authentication successful!") # 성공
            print("User Info:", result) # result에 user에 관한 정보 들어있어
            return render(request,'news/login.html', {'user' : result, 'today': today, 'day': day})
        else:
            print("Authentication failed:", result) # 실패
            return render(request,'news/404.html', {'today': today, 'day': day})
    else:
        return render(request,'news/login.html', {'today': today, 'day': day})

def logout_view(request):
    return render(request, "news/login.html", {})
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
    return render(request, "common/login.html", {"form": form})
'''