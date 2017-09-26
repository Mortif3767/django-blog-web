# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  #每页显示三个博客
    page = request.GET.get('page')   #flask里为request.args.get('page'):GET请求传參
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'page': page})        #留意这个传过去的posts，为何在页码模版中可以posts.page?(页面对象)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST) #注意django从表单中获取数据的方式，与flask不同
        if form.is_valid():
            cd = form.cleaned_data  #获取验证通过数据，返回一个表单字段和值的字典
            #send email part
            post_url = request.build_absolute_uri(post.get_absolute_url()) #构建uri，包含HTTP schema和URl
            subject = '{} ({}) 分享你阅读 "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'],
                cd['comments'])
            send_mail(subject, message, 'garryrich@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'cd':cd})


class PostListView(ListView):         #django定义了view视图的基础类
    queryset = Post.published.all()   #代替超类取回所有对象，默认django构建model.objects.all()
    context_object_name = 'posts'     #查询结果赋给变量posts，否则默认object_list
    paginate_by = 3                   #传给模板的页面对象为page_obj
    template_name = 'blog/post/list.html'
