# -*- coding: utf-8 -*-
from django import template

register = template.Library() #每个template_tag都要有的变量，用以表明有效标签库

from django.db.models import Count
from django.utils.safestring import mark_safe
from ..models import Post
import markdown


@register.simple_tag #注册标签，并表明标签类型；simpletag直接返回结果
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html') #包含标签必须返回一个字典值
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.assignment_tag   #将结果返回在变量中，用法{% template_tag as variable(变量) %}
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
