from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.db.models import F
import json
# Create your views here.
def index(request, *args, **kwargs):
    condition={}
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None  # 获得请求中的数据
    if type_id:
        condition['article_type_id'] = type_id

    type_choices = models.Article.type_choices  # 获得菜单分类列表信息
    article_list = models.Article.objects.filter(**condition)   # 传入字典，获得分类对应的所有文章

    return render(request, 'index.html',{
        'type_choices_list':type_choices,
        'article_list': article_list,
        'type_id':type_id,
    })

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html',)
    else:
        input_code = request.POST.get('code')   # 用户提交的数据
        session_code = request.session.get('code')  # 通过用户cookies中的随机字符串找到对应存储空间，最终获得服务端session中的验证码
        if input_code.upper() == session_code.upper():
            pass
        else:
            pass

def check_code(request):
    # # # 以硬盘作为存储媒介的方式处理图片
    # # # 创建图片
    # # from PIL import Image
    # # f = open('code.png', 'wb')
    # # img = Image.new(mode='RGB', size=(120,30), color=(234,234,234))
    # # img.save(f, 'png')  # 将图片字节数据写入文件句柄中，文件格式为png到硬盘中存储起来
    # # f.close()
    # #
    # # # 从硬盘中读取图片成字节，将字节格式的内容发送给前端
    # # f = open('code.png','rb')
    # # data = f.read()
    #
    # # 以内存作为存储媒介的方式处理图片
    # from PIL import  Image,ImageDraw, ImageFont
    # from io import BytesIO
    # f = BytesIO()   # 开辟内存空间
    # img = Image.new(mode='RGB', size=(120,30), color=(184,146,141))
    # draw = ImageDraw.Draw(img, mode='RGB')  # 创建画笔
    # draw.point([10,10], fill='red') # 画圆点的位置及颜色
    # draw.point([20,20], fill=(120,250,51)) # RGB数值可以设置成随机颜色
    # draw.line([50,100,10,15], fill='red')  # 画线条
    # draw.arc([0,0,30,30], 0, 360, fill='red')   # 画圆
    # # font = ImageFont.truetype('kumo.ttf', 29)  # 设置字体及大小
    # # draw.text([0,0], 'python', 'black', font=font)   # 写字
    #
    # # 生成随机字符串
    # import random
    # # char_list = []
    # # for i in range(5):
    # #     char = chr(random.randint(65, 90))  # 随机生成整数
    # #     char_list.append(char)
    # #     v = ''.join(char_list)
    # #  生成随机字符串的简写方式
    # # v = ''.join([chr(random.randint65, 90) for i in range(5)])
    #
    # # 写随机字符
    # char_list = []
    # for i in range(5):
    #     char = chr(random.randint(65, 90))  # 随机生成整数
    #     char_list.append(char)
    #     font = ImageFont.truetype('kumo.ttf', 29)  # 设置字体及大小
    #     draw.text([i*24, 0], char, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), font=font)  # 写字
    # img.save(f, 'png')  # 将图片保存到内在中
    # data = f.getvalue()  #　从内存中读取出图片字节格式数据后发送给用户
    #
    # code = ''.join(char_list)   # 生成的随机字符串列表
    # request.session['code'] = code  # 保存到session中对用户输入的验证码进行匹配

    # 使用自定义验证码组件
    from io import BytesIO
    from utils.random_check_code import check_code
    img , code = check_code()   # 获得img对象及字符串内容
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code']= code
    return  HttpResponse(stream.getvalue())

    return HttpResponse(data)

from app01.forms import RegisterForm
from django.core.exceptions import NON_FIELD_ERRORS
def register(request):
    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request, 'register.html',{'obj':obj})
    else:
        # 验证码操作
        obj = RegisterForm(request,request.POST,request.FILES)
        if obj.is_valid():
            pass
        else:
            """
           {
               __all__: [错误1，错误2]
               user: [错误1，错误2]
               password: [错误1，错误2]
           }
            """
            # print(obj.errors['__all__'])
            # print(obj.errors[NON_FIELD_ERRORS])     # '__all__'
    return render(request, 'register.html', {'obj': obj})


def home(request, site):
    """
     访问个人博客主页 http://127.0.0.1:8000/fangshaowei/
    :param request: 请求相关信息
    :return: 个人博客后缀，如： www.xxx.com/xxxxx/
    """
    blog = models.Blog.objects.filter(site=site).first()    # 获得用户对应的博客
    if not blog:
        return redirect('/')

    # # 获取当前博客的所有文章
    # article = models.Article.objects.filter(blog = blog)    # 正向跨表操作
    # blog.article_set.all()  # 反向跨表操作
    #
    # # 以QuerySet对象格式为结果查询：一对一正向操作，通过博客后缀获取对应的用户名
    # obj = models.Blog.objects.filter(site=site).first()
    # print(obj.user.username)    # username = linhai
    # # 以QuerySet对象格式为结果查询：一对一反向操作，通过用户名获取博客后缀
    # obj = models.UserInfo.objects.filter(username='linhai').first()
    # print(obj.blog.site)    # site = LH
    #
    # # 以字典列表格式为结果查询：一对一正向操作，通过博客表，跨表到用户信息表获取对应的用户昵称
    # user_info = models.Blog.objects.filter(site=site).values('site', 'user__nickname')
    # # 以字典列表格式为结果查询：一对一反向操作，通过用户信息表，跨表到博客表(通过表名小写__字段，blog__site反向跨表)作为条件查询
    # v = models.UserInfo.objects.filter(blog__site=site).values('blog__site', 'nickname')
    # print(user_info)    # 两者结果一样  [{'blog__site': 'LH', 'nickname': '小清新'}]
    # print(v)        # 两者结果一样  [{'blog__site': 'LH', 'nickname': '小清新'}]

    # 当前博客所有分类（反向连表查询）
    # 第一种实现方式：
    # cate_list = models.Category.objects.filter(blog=blog)   # 获得博客所有目录
    # for item in cate_list:
    #     c = item.article_set.all().count()  # 反向操作获得目录对应的所有文章总数
    # # 第二种实现方式（分组）：
    # from django.db.models import Count
    # models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(c=Count('nid'))

    # 获取当前博客对应的标签分类（标签名+当前标签下的所有文章数量）:
    # 一：手动生成第3张关联表时的分组查询方式：（tag__blog=blog表示从关联表中跨表到tag表中的blog字段
    # models.Article2Tag.objects.filter(tag__blog=blog).values('tag_id','tag__title').annotate(c = Count('id'))
    # 二： 通过Article类中的m2m字段自动生成第3张关联表时的分组查询方式：
    # models.Article.objects.filter(blog=blog).values('tags__id', 'tags__title').annotate(c = Count('nid'))

    # 根据博客获得对应的时间分类目录
    # MySQL写法：
    # data_list= models.Article.objects.filter(blog=blog).extra(select={'c':"date_format(create_time,'%%Y-%%m')"}).values('c').annotate(ct=Count('nid'))
    #  select={'c':"date_format(create_time,'%%Y-%%m')" 等价于为查出的数据表添加一个函数处理后的新字段
    """
    nid xx    create_time            c
     1  x     2018-01-01 11:11    2018-01
    """
    # SQLlite写法：
    # date_list = models.Article.objects.filter(blog=blog).extra(select={'c': "strftime('%%Y-%%m',create_time)"}).values(
    #     'c').annotate(ct=Count('nid'))

    from django.db.models import Count
    # 获取博客对应的所有分类的字典列表(一对多)  <QuerySet [{'category_id': 1, 'category__title': 'python', 'ct': 1}, {'category_id': 2, 'category__title': 'java', 'ct': 1}]>
    category_list = models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct = Count('nid'))
    # 获取博客对应的所有标签（多对多）
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct = Count('id'))
    # 获取博客对应的所有时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m', create_time)"}).values('ctime').annotate(ct = Count('nid'))
    article_list = models.Article.objects.all() # 获得所有文章


    print('restult:',blog.theme)
    return render(request,'home.html',{
        'category_list':category_list,
        'tag_list':tag_list,
        'date_list':date_list,
        'blog':blog,
        'article_list':article_list,
    })

from django.db.models import Count
def filter(request, site, key, val):
    """
    文章筛选过滤
    :param request:
    :param site:
    :param key:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).first()    # 根据博客后缀获得博客
    if not blog:
        return redirect('/')    # 返回主站首页
    # 根据博客生成固定的栏目版块
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))
    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count('id'))
    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m', create_time)"}).values('ctime').annotate(ct = Count('nid'))


    # 博客的分类所对应的所有文章
    if key == 'category':
        article_list = models.Article.objects.filter(blog=blog, category_id=val)
    # 博客的标签所对应的所有文章
    elif key == 'tag':  #
        article_list = models.Article.objects.filter(blog=blog, tags__nid=val) # 通过M2M字段进行多对多查询，属于自动加手动生成第三张关联表
        # 延伸内容：如果是自动生成第3张关联表，需要反向跨表操作进行多对多查询(自定义的关联表小写表名__关联表字段__跨表后的字段),如下;
       # v= models.Article.objects.filter(blog=blog,article2tag__tag__nid=val)
    else:
    # 博客的日期所对应的所有文章
        article_list = models.Article.objects.filter(blog=blog).extra(where=['strftime("%%Y-%%m", create_time=%s)'], params=[val,])
    return render(request,'filter.html',{
        'blog':blog,
        'category_list': category_list,
        'tag_list': tag_list,
        'date_list': date_list,
        'article_list':article_list,
    })

#
def atricle(request, site, nid):
    """
    查看文章最终页
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    # 按照：分类，标签，时间(固定模块)
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count('id'))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count('nid'))
    # select xxx as x

    obj = models.Article.objects.filter(blog=blog, nid=nid).first() # 根据文章id，可通过反向操作获得文章最终页

    from utils.comment import comment_tree,comment
    # msg_list代表从数据库中获得的所有数据
    msg_list = [
        {'id': 1, 'content': '写的太好了', 'parent_id': None},
        {'id': 2, 'content': '你说得对', 'parent_id': None},
        {'id': 3, 'content': '顶楼上', 'parent_id': None},
        {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
        {'id': 5, 'content': '我看是', 'parent_id': 4},
        {'id': 6, 'content': '鸡毛', 'parent_id': 2},
        {'id': 7, 'content': '你是没呀', 'parent_id': 5},
        {'id': 8, 'content': '惺惺惜惺惺想寻', 'parent_id': 3},
        {'id': 9, 'content': '你眼瞎吗2', 'parent_id': 3},
    ]
    comment_list = comment(msg_list)   # 将数据进行重新组装成
    comment_str = comment_tree(comment_list)    #  组装成html格式数据

    return render(request, 'article.html',{
        'blog': blog,
        'category_list': category_list,
        'tag_list': tag_list,
        'date_list': date_list,
        'obj':obj,
        'comment_str':comment_str,
    })


def up(request):
    """
    点赞功能
    :param request:
    :return:
    """
    response = {'status': 1001, 'msg':None}     # 自定义返回结果,1001:失败
    try:
        user_id = request.session.get('user_id')  # 从session中获得用户登陆用户中的用户id
        article_id = request.POST.get('nid')     # 获得文章id
        val = request.POST.get('val') # 识别是赞还是踩
        obj = models.UpDown.objects.filter(user_id = user_id, article_id=article_id,).first()   # 查询点赞数据
        if obj:
            # 对象已经生成过该数据，表示该用户已经进行过踩或赞，前端不做任何处理
            pass
            response['status']=1000
        else:
            from django.db import transaction
            with transaction.atomic():  # 事务，当添加数据失败时回滚，同时会将错误信息给到异常处理
                if val:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)   # 表示赞
                    models.Article.objects.filter(nid = article_id).update(up_count=F('up_count')+1)    # 原有赞的基础上加1
                    response['status']=1001
                else:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=False)  # 表示踩
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count') + 1)  # 原有赞的基础上减1
                    response['status']=1002
    except Exception as e:
        response['status']=1003
        response['msg']=e

    return HttpResponse(json.dumps(response))


# 组合筛选
def query(request, **kwargs):
    # 处理请求中的参数,组装成数据库的查询条件
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)  # 将请求中的值转换为整数类型，用于前端进行值的比较
        if v != '0':
            condition[k]= v # 组装成字典传入查询条件中
    print(kwargs)


    # 从内存中读取所有内容展示
    type_list = models.Article.type_choices

    # 个人分类：临时用blog_id = 1代替blog对象
    category_list = models.Category.objects.filter(blog_id=1)
    # 个人标签：
    tag_list = models.Tag.objects.filter(blog_id=1)
    tag_list = models.Tag.objects.all()

    # from django.core import serializers
    # print(serializers.serialize('json',tag_list))
    # print('restult:',json.dumps(tag_list))

    # 组装筛选条件进行查找
    condition['blog_id']=1
    article_list = models.Article.objects.filter(**condition)
    return render(request, 'query.html',{
        'type_list':type_list,
        'category_list':category_list,
        'tag_list':tag_list,
        'kwargs':kwargs,
        'article_list':article_list,
    })

Content=''
def kindeditor(request):
    if request.method == 'GET':
        return render(request,'kindeditor.html')
    else:
        content = request.POST.get('content')
        print(content)
        global Content
        Content=content

        return HttpResponse('...')

# 查看通过kindeditor插件提交过来的数据
def see_content(request):
    return render(request, 'seeContent.html',{'Content':Content})


# Kindeditor实现图片上传
def upload_img(request):
    import os
    upload_type = request.GET.get('dir')  # 获得请求中的文件类型，图片/视频/文件等
    file_obj = request.FILES.get('imgFile')  #  从上传文件字典中获取内容{'imgFile': [<InMemoryUploadedFile: timg.jpg (image/jpeg)>]}
    file_path= os.path.join('static/imgs', file_obj.name)  # 组装文件保存的相对路径
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks(): # 将文件对象中的块循环定入文件句柄中
            f.write(chunk)

    dic = {      # 返回信息给kindedtor，（固定写法）
        'error': 0,
        'url': '/' + file_path,     # 返回文件所在路径
        'message': '错误了...'
    }
    import json
    return HttpResponse(json.dumps(dic))

