from django.shortcuts import render,redirect,HttpResponse
from app02 import models

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login2.html')
    else:
    #     # 根据用户登录信息获得所有权限
    #     object = models.User.objects.filter(username='tom').first()  # 假定根据登陆信息获得用户名为tom
    #     # 根据用户对象获得对应的所有角色（有2种方式）
    #     role_list = models.User2Role.objects.filter(user_id=object.id)  # 方式一：正向操作 获得[User2Role,User2Role,User2Role]
    #     # 方式二：反向操作，通过users跨表到user表中的user_id字段，获得对应的role表的所有id，从而获得所有role（推荐该方法）
    #     role_list = models.Role.objects.filter(users__user_id=object.id)
    #
    #     # 根据角色对象，获得所有权限，并去重
    #     from django.db.models import Count
    #     # models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url', 'action__code').annotate(c = Count('id'))
    #     # 推荐下面方式，不会生成新的字段c
    #     permission_list = models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url', 'action__code').distinct()
    #     # 获得结果如下所示：
    #     """
    #     [
    #     {permission_url: '/index.html', action_code:'GET'},
    #     {permission_url: '/index.html', action_code:'POST'},
    #     {permission_url: '/index.html', action_code:'DEL'},
    #     {permission_url: '/index.html', action_code:'Edit'},
    #     {permission_url: '/order.html', action_code:'GET'},
    #     {permission_url: '/order.html', action_code:'POST'},
    #     {permission_url: '/order.html', action_code:'DEL'},
    #     {permission_url: '/order.html', action_code:'Edit'},
    # ]
    # """
        # 再通过for循环将数据库中查出的数据转换成如下格式：
        user_permission_dict = {
            '/ah-index.html': ["GET","POST","DEL","Edit"],
            '/order.html':  ["GET","POST","DEL","Edit"],
            '/auth-index-(\d+).html':  ["GET","POST","DEL","Edit"],
        }

        # 将用户的对应的权限放入session中，当访问其它链接时，可直接从session中进行校验是否存在该权限
        request.session['user_permission_dict'] = user_permission_dict
        return HttpResponse('登陆成功')

def index(request):
    return HttpResponse('登陆成功，你拥有了权限，恭喜你看见了我')



