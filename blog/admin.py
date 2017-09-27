# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin): #继承此类用来在管理页面中管理自建模型
    list_display = ('title', 'slug', 'author', 'publish', 'status')  #列表显示内容
    list_filter = ('status', 'created', 'publish', 'author')   #右侧过滤选项
    search_fields = ('title', 'body')     #增加搜索框
    prepopulated_fields = {'slug': ('title',)}   #自动填充slug
    raw_id_fields = ('author',) #作者可搜索
    date_hierarchy = 'publish' #时间快速导航栏
    ordering = ['status', 'publish'] #排序
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)
