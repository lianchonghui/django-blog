# Title
---
**关键词**
```
django
```
---
**环境**
> - Python3.5
> - django 1.10.6

---
**目录**
[TOC]
---

## Title2
### sslserver
#### 参考文档
1. [官方文档][1]
#### 安装sslserver
> $ pip install django-sslserver

#### 使用sslserver
1. 在django项目的settings.py中的`INSTALLED_APP`中添加`sslserver`
2. 使用ssl方式启动服务 
   > $ python manage.py runsslserver

    **指定证书启动**
   > $ python manage.py runsslserver --certificate /path/to/certificate.crt --key /path/to/key.key

### haystack
#### 参考文档
1. [官方文档][2]
2. [追梦人物haystack教程][3]
#### 安装haystack及jieba、whoosh
- whoosh 英文分词
- jieba 中文分词
    > $ pip install django-haystack jieba whoosh

#### 使用haystack
1. 在settings.py中添加配置如下
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    #...
    'haystack',
]

# haystack的各项配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```
2. 配置url
```python
urlpatterns = [
    # ...
    url(r'^search/', include('haystack.urls')),
]
```
3. 创建索引文件
根据django haystack 的规定。要相对某个 app 下的数据进行全文检索，就要在该 **app** 下创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post），并且继承 SearchIndex 和 Indexable。
**示例如下**
```python

from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
```
4. 配置网页表单action
   主要是把表单的 action 属性改为 `{% url 'haystack_search' %}`

5. 添加search.html
 搜索结果会渲染模板文件夹下的`search/serach.html`
```html
{% load highlight %}
    <!-- highlight 用于高亮关键词 -->
    <!-- 配置高亮的css -->
<head>
    <title>Black &amp; White</title>
    <style>
        span.highlighted {
            color: red;
        }
    </style>
    ...
</head>
    <!-- 以下是用于渲染结果的主要代码-->
{% block main %}
    {% if query %}
        {% for result in page.object_list %}
            <article class="post post-{{ result.object.pk }}">
                <header class="entry-header">
                    <h1 class="entry-title">
                        <a href="{{ result.object.get_absolute_url }}">{% highlight result.object.title with query %}</a>
                    </h1>
                    <div class="entry-meta">
                    <span class="post-category">
                        <a href="{% url 'blog:category' result.object.category.pk %}">
                            {{ result.object.category.name }}</a></span>
                        <span class="post-date"><a href="#">
                            <time class="entry-date" datetime="{{ result.object.created_time }}">
                                {{ result.object.created_time }}</time></a></span>
                        <span class="post-author"><a href="#">{{ result.object.author }}</a></span>
                        <span class="comments-link">
                        <a href="{{ result.object.get_absolute_url }}#comment-area">
                            {{ result.object.comment_set.count }} 评论</a></span>
                        <span class="views-count"><a
                                href="{{ result.object.get_absolute_url }}">{{ result.object.views }} 阅读</a></span>
                    </div>
                </header>
                <div class="entry-content clearfix">
                    <p>{% highlight result.object.body with query %}</p>
                    <div class="read-more cl-effect-14">
                        <a href="{{ result.object.get_absolute_url }}" class="more-link">继续阅读 <span
                                class="meta-nav">→</span></a>
                    </div>
                </div>
            </article>
        {% empty %}
            <div class="no-post">没有搜索到你想要的结果！</div>
        {% endfor %}
        {% if page.has_previous or page.has_next %}
            <div>
                {% if page.has_previous %}
                    <a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">{% endif %}&laquo; Previous
                {% if page.has_previous %}</a>{% endif %}
                |
                {% if page.has_next %}<a href="?q={{ query }}&amp;page={{ page.next_page_number }}">{% endif %}Next
                &raquo;{% if page.has_next %}</a>{% endif %}
            </div>
        {% endif %}
    {% else %}
        请输入搜索关键词，例如 django
    {% endif %}
{% endblock main %}
```
6. 使用jieba分词
从你安装的 haystack 中把 haystack/backends/whoosh_backends.py 文件拷贝到 blog/ 下，重命名为 whoosh_cn_backends.py（之前我们在 settings.py 中 的 HAYSTACK_CONNECTIONS 指定的就是这个文件）
**修改whoosh_cn_backends.py如下**
```python
from jieba.analyse import ChineseAnalyzer

#...
#注意先找到这个再修改，而不是直接添加  
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(),field_boost=field_class.boost, sortable=True)  
```

## Title2
### Title3
#### Title4

---
## 可能遇到的问题
暂无



--------------------

文章引用和转载请注明出处，如果有什么问题欢迎交流！

作者 [@练崇辉][101]
Email: `lianchonghui@foxmail.com`
2018 年 07月 07日 


[1]: https://pypi.python.org/pypi/django-sslserver/0.12
[2]: http://django-haystack.readthedocs.io/en/master/index.html
[3]: https://www.zmrenwu.com/post/45/
[101]: https://www.lianch.com

<!-- 21
![图片备注][1]
[文章应用，此处输入链接的描述][2]
[超链接(https://raw.githubusercontent.com/lianchonghui/photorepository/master/markdown/2018/1/30/bydyungui01.jpg)
- [ ] 改进 Cmd 渲染算法，使用局部渲染技术提高渲染效率
- [x] 新增 Todo 列表功能
7. 绘制表格

| 项目        | 价格   |  数量  |
| --------   | -----:  | :----:  |
| 计算机     | \$1600 |   5     |
| 手机        |   \$12   |   12   |
| 管线        |    \$1    |  234  |

高亮一段代码[^code]

[^code]: 代码高亮功能支持包括 Java, Python, JavaScript 在内的，**四十一**种主流编程语言。

[1]: https://raw.githubusercontent.com/lianchonghui/photorepository/master/markdown/2018/1/30/bydyungui01.jpg
[2]: http://news.ifeng.com/a/20180207/55848550_0.shtml
-->
