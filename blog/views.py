# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post


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


class PostListView(ListView):         #django定义了view视图的基础类
    queryset = Post.published.all()   #代替超类取回所有对象，默认django构建model.objects.all()
    context_object_name = 'posts'     #查询结果赋给变量posts，否则默认object_list
    paginate_by = 3                   #传给模板的页面对象为page_obj
    template_name = 'blog/post/list.html'