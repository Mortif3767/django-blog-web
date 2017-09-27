# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
                   'tag': tag})        #留意这个传过去的posts，为何在页码模版中可以posts.page?(页面对象)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST) #留意ModelForm与Form取值的区别
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    #equal to [post_tag.id for post_tag in post.tags]
    #如果没有flat=True，返回元组列表
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,   #相当于post—share里的sent做标记用
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    
    cd = None
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
            sent = True  #通过这个变量标记确定页面“跳转”显示结果
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'cd':cd})


class PostListView(ListView):         #django定义了view视图的基础类
    queryset = Post.published.all()   #代替超类取回所有对象，默认django构建model.objects.all()
    context_object_name = 'posts'     #查询结果赋给变量posts，否则默认object_list
    paginate_by = 3                   #传给模板的页面对象为page_obj
    template_name = 'blog/post/list.html'
