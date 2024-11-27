from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('error', views.error, name='error'),
    path('contact', views.contact, name='contact'),
    path('detail-page', views.detail_page, name='detail-page'),
    path('index', views.index, name='index'),
    
    # REGISTER
    #path('register', views.register_view, name='register'),

    # LOGIN, LOGOUT
    path('login', views.login_view, name='login'),
    #path('logout', views.logout_view, name='logout'),
]
