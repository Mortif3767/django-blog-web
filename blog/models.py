# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone             #django的时间工具
from django.contrib.auth.models import User   #auth应用
from django.core.urlresolvers import reverse


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

    class Meta:
        ordering = ('-publish',)  #查询返回顺序为publish列降序排列

    def get_absolute_url(self):   #模型标准urls
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    def __str__(self):
        return self.title
