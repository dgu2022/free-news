from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('news.urls', 'news'), namespace='news')),
    path('accounts/', include('allauth.urls')),
]