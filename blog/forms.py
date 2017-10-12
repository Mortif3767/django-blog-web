# -*- coding: utf-8 -*-
from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm): #django自带根据model自建表单，自动分析表单字段类型
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body') #fields包含要显示的内容，exclude用来表示剔除的内容


class SearchForm(forms.Form):
    query = forms.CharField()