from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('/404', views.error, name='error'),
    path('/contact', views.contact, name='contact'),
    path('/detail-page', views.detail-page, name='detail-page'),
    path('/index', views.index, name='index'),
]
