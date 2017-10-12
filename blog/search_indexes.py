# -*- coding: utf-8 -*-
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #该索引必备字段包含document=true，为主要搜索字段
    #use_template用于渲染数据模板构建Document
    publish = indexes.DateTimeField(model_attr='publish')
    #模型的publish列也会被索引

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()