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

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'news/post_list.html', {'posts': posts})

def error(request):
    return render(request, 'news/404.html', {'today': today, 'day': day})

def mypage(request):
    #'''
    if request.method == "GET":  # 요청하는 방식이 GET 방식인지 확인하기
        user_name = request.session.get('user')
        user_info = request.session.get('info')
        if user_name:  # 로그인 한 사용자라면
            return render(request, 'news/mypage.html', {'today': today, 'day': day, 'user_info': user_info})
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'news/login.html', {'today': today, 'day': day})
    #'''
    return render(request, 'news/login.html', {'today': today, 'day': day})

def index(request):
    base_dict = {'today': today, 'day': day}
    post_dict = {}
    if request.method == "GET":  # 요청하는 방식이 GET 방식인지 확인하기
        user_name = request.session.get('user')
        user_info = request.session.get('info')
        user_id = user_info[0]
        if user_name:  # 로그인 한 사용자라면
            base_dict.update({'user_info': user_info})
            post = MyPost()
            my_post1 = post.get_my_post(user_id) #자신이 쓴 기사 최신 순으로 1개
            post = MyPost()
            my_post2 = post.getMyPostMain1(user_id) #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 가장 조회수 높은 기사
            post = MyPost()
            my_post3 = post.getMyPostMain2(user_id) #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 댓글이 가장 많은 포스트 불러오기
            post = MyPost()
            my_post4 = post.get_random_articles_from_latest(user_id) #최신 10개 중 랜덤 4개 기사 조회
            post = MyPost()
            my_post4_2 = post.get_top_articles_today() #오늘 올라온 조회수 높은 3개 기사 조회
            post = MyPost()
            my_post4 += my_post4_2
            my_post5 = post.get_latest_articles_by_category() #분야별 전체 기자들이 쓴 최신 기사 3개
            post = MyPost()
            my_post5_2 = post.get_unread_top_articles_today_by_category(user_id) #분야별 내가 읽지 않은 오늘 올라온 조회수 높은 기사 3개
            post = MyPost()
            my_post5 += my_post5_2
            my_post6 = post.getHotPostToday() #전체 기자들이 쓴 기사 중 작성일이 하루가 지나지 않은 기사 중 조회수 가장 높은 기사
            post = MyPost()
            my_post7 = post.getHotPostWeek() #전체 기자들이 쓴 기사 중 작성일이 일주일이 지나지 않은 기사 중 조회수 높은 순으로 2개
            post = MyPost()
            my_post8 = post.get_unread_popular_article(user_id) #구독한 기자들의 읽지 않은 조회수 높은 기사
            post_dict = {'post1':my_post1, 'post2':my_post2, 'post3':my_post3, 'post4':my_post4, 'post5':my_post5, 'post6':my_post6, 'post7':my_post7, 'post8':my_post8}
    #post = FullPost()
    #full_post1 = post
    print(post_dict)
    base_dict.update(post_dict)
    return render(request, 'news/index.html', base_dict)

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
        email = request.POST['email']
        password = request.POST['password']
        login = Login()
        is_authenticated, result = login.authenticate_member(email, password)

        if is_authenticated:
            print("Authentication successful!") # 성공
            print("User Info:", result) # result에 user에 관한 정보 들어있어
            request.session['user'] = result[1]
            request.session['info'] = result
            return render(request,'news/index.html', {'user_info' : result, 'today': today, 'day': day})
        else:
            print("Authentication failed:", result) # 실패
            return render(request,'news/404.html', {'today': today, 'day': day})
    else:
        return render(request,'news/login.html', {'today': today, 'day': day})

def logout(request):
    return render(request, "news/index.html", {'user_info' : None, 'today': today, 'day': day})
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