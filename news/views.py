from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .model.post_list import *
from datetime import datetime
from django.utils.dateformat import DateFormat
import pymysql
from random import shuffle, sample

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

def get_post_safe(post, num):
    if not post[0] or not post[1]:
        print("여기서 에러?")
        post = FullPost()
        post_safe = random.sample(post.get_random_post(num)[1],num)
        print(post_safe)
        if not isinstance(post_safe, list):
            return [post_safe]
        return post_safe
    return post

'''
def set_post_safe(post):
    print("처음")
    print(post)
    unique_data = {}
    for article in post:
        article_id = article[num]
        unique_data[article_id] = article

    # 결과를 리스트로 변환
    result = list(unique_data.values())
    print("마지막")
    print(result)
    return result
'''



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
            my_post1 = get_post_safe(post.get_my_post(user_id), 1) #자신이 쓴 기사 최신 순으로 1개
            post = MyPost()
            my_post2 = get_post_safe(post.getMyPostMain1(user_id), 1) #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 가장 조회수 높은 기사
            post = MyPost()
            my_post3 = get_post_safe(post.getMyPostMain2(user_id), 1) #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 댓글이 가장 많은 포스트 불러오기
            post = MyPost()
            my_post4 = list(get_post_safe(post.get_random_articles_from_latest(user_id), 4)[1]) #최신 10개 중 랜덤 4개 기사 조회
            post = MyPost()
            print(4)
            print(my_post4)
            my_post4_2 = list(get_post_safe(post.get_top_articles_today(), 3)) #오늘 올라온 조회수 높은 3개 기사 조회
            post = MyPost()
            print("4_2")
            print(my_post4_2)
            #my_post4 = set_post_safe(list(set(my_post4 + my_post4_2)), 0)
            #shuffle(my_post4)
            my_post4 = list(set(my_post4 + my_post4_2))
            print("4_last")
            print(my_post4)
            my_post4_1 = my_post4[0]
            my_post4 = my_post4[1:]
            print("error?5")
            my_post5 = list(get_post_safe(post.get_latest_articles_by_category(), 3)[1]) #분야별 전체 기자들이 쓴 최신 기사 3개
            print(5)
            print(my_post5)
            post = MyPost()
            my_post5_2 = list(get_post_safe(post.get_unread_top_articles_today_by_category(user_id), 3)[1]) #분야별 내가 읽지 않은 오늘 올라온 조회수 높은 기사 3개
            print("5_2")
            print(my_post5_2)
            post = MyPost()
            #my_post5 = set_post_safe(list(set(my_post5 + my_post5_2)), 1)
            #my_post5 = shuffle(my_post5)
            my_post5 = list(set(my_post5 + my_post2))
            my_post5_1 = my_post5[0]
            my_post5 = my_post5[1:]
            my_post6 = get_post_safe(post.getHotPostToday(), 1) #전체 기자들이 쓴 기사 중 작성일이 하루가 지나지 않은 기사 중 조회수 가장 높은 기사
            post = MyPost()
            my_post7 = get_post_safe(post.getHotPostWeek(), 2) #전체 기자들이 쓴 기사 중 작성일이 일주일이 지나지 않은 기사 중 조회수 높은 순으로 2개
            post = MyPost()
            my_post8 = get_post_safe(post.get_unread_popular_article(user_id), 1) #구독한 기자들의 읽지 않은 조회수 높은 기사
            post_dict = {'post1':my_post1, 'post2':my_post2, 'post3':my_post3, 'post4':my_post4, 'post4_1':my_post4_1, \
                         'post5':my_post5, 'post5_1':my_post5_1, 'post6':my_post6, \
                         'post7':my_post7, 'post8':my_post8}
    #post = FullPost()
    #full_post1 = post
    print(post_dict)
    base_dict.update(post_dict)
    return render(request, 'news/index.html', base_dict)

def contact(request):
    return render(request, 'news/contact.html', {'today': today, 'day': day})

def detail_page(request):
    if request.method == "GET":
        user_name = request.session.get('user')
        user_info = request.session.get('info')
        user_id = user_info[0]
        article_id = request.GET['article_id']
        if user_name:  # 로그인 한 사용자라면
            post = FullPost()
            article = post.get_full_post(article_id)
            sub = Subscribe()
            jid = sub.get_journalist_id(article_id)
            cnt_sub = sub.get_subscriber_count(jid)
            sub.subscribe_journalist(user_id, jid)
            return render(request, 'news/detail-page.html', {'today': today, 'day': day, 'article': article, 'cnt_sub': cnt_sub})
        else:
            return render(request, 'news/login.html', {'today': today, 'day': day})
    elif request.method == "POST":        
        sub = Subscribe()
        jid = sub.get_journalist_id(article_id)
        cnt_sub = sub.get_subscriber_count(jid)
        sub.subscribe_journalist(user_id, jid)
        return render(request, 'news/detail-page.html', {'today': today, 'day': day, 'article': article, 'cnt_sub': cnt_sub})

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