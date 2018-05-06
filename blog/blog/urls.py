"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app01 import views
from app02 import views as views2
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth-login.html$', views2.login),
    url(r'^auth-index.html$', views2.index),


    url(r'^login/', views.login),
    url(r'^check_code/', views.check_code),
    url(r'^register/', views.register),
    url(r'^all/(?P<type_id>\d+)/', views.index), # 正则接收分类菜单值
    url(r'^up.html/', views.up),

    url(r'^kindeditor.html$', views.kindeditor),
    url(r'^see_content.html$', views.see_content),
    url(r'^upload_img.html$', views.upload_img),

    # 组合筛选，?P<tags__nid>等对应数据库字段名
    url(r'^blog_name-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', views.query),

    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', views.atricle),
    url(r'^(?P<site>\w+)/(?P<key>((tag)|(data)|(category)))/(?P<val>\w+-*\w*)/',views.filter),
    url(r'(\w+)/', views.home),  # 接收博客名参数
    url(r'',views.index),

]
