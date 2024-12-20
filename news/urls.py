from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('404', views.error, name='error'),
    path('contact', views.contact, name='contact'),
    path('detail-page', views.detail_page, name='detail-page'),
    path('index', views.index, name='index'),
    path('mypage', views.mypage, name='mypage'),
    #path('subscribe', views.subscribe, name='subscribe'),
    path('detail-page/<int:article_id>/', views.detail_page),
    
    # REGISTER
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
