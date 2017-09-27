# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone             #django的时间工具
from django.contrib.auth.models import User   #auth应用
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,       #slug短标签，只包含字母、数字、下划线连接线
                            unique_for_date='publish')#用（唯一）日期和slug构建url
    author = models.ForeignKey(User,
                               related_name='blog_posts') #多对一的关系，在多的一方定义反向属性
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  #创建时自动添加
    updated = models.DateTimeField(auto_now=True)      #修改时自动添加
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')         #传入元组，只能选其一
    objects = models.Manager()  #默认管理器
    published = PublishedManager() #自定义管理器
    tags = TaggableManager()    #插件会自建一个tag表，这是一个多对多关系

    class Meta:
        ordering = ('-publish',)  #查询返回顺序为publish列降序排列

    def get_absolute_url(self):   #模型标准urls
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    def __str__(self):         #这个的意思是查询行结果时，用title表示此行
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments') #如果没有comments设定，django默认为comment_set
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)  #self.post虽然为行对象，但是显示的是title
