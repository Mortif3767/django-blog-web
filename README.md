## 基于Django的小型博客网站  
  
django框架的第一次尝试，初步对：django项目和应用的创建，模型`models`的设计，数据库迁移，数据库查询`QuerySet`，管理站点，视图`views`，模板`templates` 标签`tags` 过滤器`filters`，`URLs`，表单`forms`等功能进行尝试，制作出的博客应用。  
  
### 博客主要功能  
**1.博客列表页面：**  
构建`Post`模型，**分页**展示博客名称、内容概述；运用第三方标签应用`django-taggit`，增加标签分类浏览功能；支持`markdown`显示。  
  
**2.博客详情页面：**  
通过email分享博客；构建`Comment`模型提供评论表单，显示博客评论；当前博客根据相同标签`tag`，推荐相似博客；自定义模板标签`template tags`，显示博客总数、最新博客和最多评论博客；支持`markdown`显示。  
  
**3.管理员页面**  
定制`models`管理员编辑页面。

**4.扩展功能**  
为搜索引擎创建了一个站点地图`sitemap`，爬取你的站点以及一个`RSS feed `给用户来订阅。在项目中集成`Slor`和`Haystack`为blog应用构建了一个搜索引擎。  
  
```  
|- django-blog-web  
    |- blog\      #应用目录
    |- mysite\    #项目目录
    #...
```
