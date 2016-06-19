# coding=utf-8
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
class Tag(models.Model):
    class Meta:
        app_label = 'blog'
        verbose_name = '标签'
        verbose_name_plural = '标签'

    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

# class Category(models.Model):
#     class Meta:
#         app_label = 'blog'
#         verbose_name = '分类目录'
#         verbose_name_plural = '分类目录'
#
#     name = models.CharField(max_length=40)
#
#     def __unicode__(self):
#         return self.name

class Post(models.Model):
    class Meta:
        app_label = 'blog'
        verbose_name = '文章'
        verbose_name_plural = '文章'

    # 作者
    author = models.ForeignKey(User)
    # 标题
    title = models.CharField(max_length=200)
    # 正文
    # text = models.TextField()
    text = UEditorField('内容',width="mini",height="500",imagePath="static/uploadimg/",filePath="", upload_settings={"imageMaxSize":1204000},settings={},command=None,blank=True)
    # 标签
    tags = models.ManyToManyField(Tag)
    # 分类目录
    # category = models.ForeignKey(Category)
    # 点击量
    click = models.IntegerField(default=0)
    # 创建时间
    created_date = models.DateTimeField(default=timezone.now)
    # 发布时间
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title

