from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, TemplateView

import markdown
from braces.views import SelectRelatedMixin, SetHeadlineMixin
from markdown.extensions.toc import TocExtension

from .models import Category, Post
from .view_mixins import PaginationMixin

'''
django-braces
http://django-braces.readthedocs.io/en/latest/index.html

ListView
django类视图之一
https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#listview

ListView，DetailView没有post方法
当post请求这两个类视图的时候，如果子类有定义post方法，则在dispatch方法后走post方法
'''
class BasePostListView(PaginationMixin, SelectRelatedMixin, SetHeadlineMixin, ListView):
    '''
    model,headline,template_name（模板名称）,paginate_by（分页，每页条数）...
    ListView指定模型，模板等属性
    '''
    model = Post
    paginate_by = 10
    '''
    django-braces简化了select_related查询
    关于django的select_related：
    https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related
    '''
    select_related = ('author', 'category')

    '''
    重写ListView的get_queryset方法,默认是all()

    annotate(comment_count=Count('comments'))
    django聚合函数
    https://docs.djangoproject.com/en/1.11/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset
    该函数返回的是QuerySet列表，该列表的QuerySet的每个model对象增加了一个comment_count的key，值为统计的comments数
    如果没有用comment_count接收，默认生成的key是comments__count

    '''
    def get_queryset(self):
        return super().get_queryset().annotate(comment_count=Count('comments'))


class IndexView(BasePostListView):
    template_name = 'blog/index.html'
    headline = '首页'


class PopularPostListView(IndexView):
    headline = '热门文章'

    def get_queryset(self):
        return super().get_queryset().order_by('-views')


class CategoryPostListView(BasePostListView):
    '''
    ListView的方法调用顺序
    dispath
    get
    get_queryset
    get_context_data
    get_headline

    业务逻辑：
        url请求category/slug
        如果slug的category是tutorial，则跳转到post/xxx
        如果slug的category非tutorial，则url仍然会category/slug，显示该slug的post列表
    '''
    template_name = 'blog/category_post_list.html'

    def dispatch(self, request, *args, **kwargs):
        '''
        在get/post方法前
        slug（WordPress的一个get请求参数）相当于分类名。
        get_object_or_404返回的是一个model对象而不是queryset
        每个category属于tutorial和collection
        如果category是tutorial，则使用tutorial_detail.html的模板，并且不分页
        '''
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))

        if self.category.genre == Category.GENRE_CHOICES.tutorial:
            self.template_name = 'blog/tutorial_detail.html'
            self.paginate_by = None

        return super().dispatch(request, *args, **kwargs)

    def get_headline(self):
        return '%s' % self.category

    def get(self, request, *args, **kwargs):
        '''
        dispatch方法之后，get_queryset前
        如果是教程且改分类下存在post则跳转到post的detail路径即post/xxx
        model_set方法获取该category下的post，如果存在则重定向,如果不存在调用父类的get方法
        redirect():http://blog.csdn.net/heatdeath/article/details/70832336
            redirect(to, permanent=False, *args, **kwargs)[source]
            将HttpResponseRedirect返回给传递的参数的相应URL。
            这个参数可能是：
            一个模型：模型的get_absolute_url（）函数将被调用。
            视图名称，可能使用参数：reverse（）将用于反向解析名称。
            一个绝对的或相对的URL，将按原样用于重定向位置。
            默认情况下会发出临时重定向; pass permanent = Tru发出永久重定向。
        
        
        '''
        if self.category.genre == Category.GENRE_CHOICES.tutorial:
            if self.category.post_set.exists():
                return redirect(self.category.post_set.last())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        '''
        get方法之后，getcontext_data之前
        如果不是tutorial
        则获取该category下的post的queryset(注意CategoryPostListView的model是Post，这里获取到的是post)
        '''
        qs = super().get_queryset()
        post_list = qs.filter(category=self.category)

        return post_list

    def get_context_data(self, **kwargs):
        '''
        get_queryset后
        调用父类get_context_data
        添加category的字典元素
        '''
        context = super().get_context_data(**kwargs)
        context['category'] = self.category

        return context


class PostDetailView(SetHeadlineMixin, DetailView):
    '''
    DetailView方法顺序：
        get
        get_object
        get_ocntext_data
        get_hadline
    '''
    model = Post
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        '''
        每次被请求的post，点击量+1
        '''
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_headline(self):
        '''
        设置行头
        '''
        if self.object.category:
            return '%s_%s' % (self.object.title, self.object.category.name)
        return '%s' % self.object.title

    def get_object(self, queryset=None):
        '''
        获取对象（不是queryset）
        使用markdown封装成html
        增加toc
        '''
        post = super().get_object(queryset=queryset)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    def get_context_data(self, **kwargs):
        '''
        通过某个字段查询获取上一个或下一个的对象
            get_previous_by_FILENAME()
            get_next_by_FILENAME()


        '''
        context = super().get_context_data(**kwargs)
        post = self.object

        try:
            previous_post = post.get_previous_by_created_time()
        except Post.DoesNotExist:
            previous_post = None

        try:
            next_post = post.get_next_by_created_time()
        except Post.DoesNotExist:
            next_post = None

        if post.category and post.category.genre == Category.GENRE_CHOICES.tutorial:
            self.template_name = 'blog/tutorial.html'
            '''
            将queryset转成list，使用list的index获取排序值
            给客户端返回post的list和上一个post和下一个post的index值
            '''
            post_list = list(post.category.post_set.all().order_by('created_time'))
            context['post_list'] = post_list

            idx = post_list.index(post)

            try:
                previous_post = post_list[idx - 1 if idx > 1 else None]
            except (IndexError, TypeError):
                previous_post = None

            try:
                next_post = post_list[idx + 1]
            except IndexError:
                next_post = None

        context['previous_post'] = previous_post
        context['next_post'] = next_post

        return context


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    return redirect(cate, permanent=True)


def django_advanced_blog_tutorial_redirect(request):
    cate = get_object_or_404(Category, slug='django-blog-tutorial')
    return redirect(cate, permanent=True)


class TutorialListView(SetHeadlineMixin, ListView):
    model = Category
    headline = '教程'
    template_name = 'blog/tutorial_list.html'
    context_object_name = 'tutorial_list'
    queryset = Category.objects.filter(genre=Category.GENRE_CHOICES.tutorial)


class CategoryListView(SetHeadlineMixin, ListView):
    model = Category
    headline = '分类'
    template_name = 'blog/category_list.html'
    queryset = Category.objects.exclude(
        genre=Category.GENRE_CHOICES.tutorial
    ).annotate(num_posts=Count('post'))


class PostArchivesView(SetHeadlineMixin, ListView):
    headline = '归档'
    model = Post
    template_name = 'blog/archives.html'


class DonateView(TemplateView):
    template_name = 'blog/donate.html'
