#coding:utf-8
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django import forms
from django.conf.urls import url
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from blog.models import Post,Tag
from django.db.models import Count
from django.template import RequestContext
from rest_framework import viewsets
from forms import PostForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def ajax(request):
    return render_to_response('ajax.html')

def get_click(post):
    k = "CLICKS{:d}".format(post.id)
    if cache.has_key(k):
        return cache.get(k)
    else:
        cache.set(k, post.click)
        return post.click


class UserForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

def login(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        # print uf
        if uf.is_valid():
            # print uf.cleaned_data
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = User.objects.filter(username__exact = username,password__exact = password)
            if True:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/')

    else:
        uf = UserForm()
    return render_to_response('login1.html',{ 'uf': uf })


# def index(request):
#     blog_list=Post.objects.filter(published_date__isnull=False).order_by('-published_date')
#     # blog_list = Post.objects.all().order_by('-created_date')
#     # print blog_list
#     return render_to_response('index.html',{'blog_list':blog_list})

def index(request,after_range_num = 5,bevor_range_num = 4):
    """所有已发布文章"""
    postsAll = Post.objects.filter( published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(postsAll, 8
                          )  # 每页显示6条数据
    pageCount=paginator.num_pages       #总页数
    num_pages=10                        #每页显示10个
    try:
        page =int(request.GET.get('page',1))  #获取当前页码，默认为1
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except:
        posts = paginator.page(1)

    if page<=num_pages/2+1:
        pageStart = 1
        pageEnd  = num_pages+1
    elif page>num_pages/2+1:
        pageStart = page-num_pages/2
        pageEnd =page+num_pages/2
    if pageEnd > pageCount:
        pageStart = pageCount-9
        pageEnd = pageCount+1
    if pageEnd <= num_pages:
        pageStart=1
    page_range=xrange(pageStart,pageEnd)

    return render_to_response('index.html', {'blog_list': posts, 'page_range':page_range,'page': True},context_instance=RequestContext(request))




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render_to_response('post_detail.html', {'post': post},context_instance=RequestContext(request))

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             # return redirect('post_detail', pk=post.pk)
#             # return HttpResponseRedirect(reverse('blog.views.post_detail',args=(post.pk,)))
#             return HttpResponseRedirect('/post/%s' % post.pk )
#             # return HttpResponseRedirect(url('^$', post_detail))
#             # return render_to_response('post_detail.html', {'post': post})
#
#     else:
#         form = PostForm()
#     return render_to_response('post_edit.html', {'form': form})
@login_required
def post_new(request):
    """新建文章"""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # 开始处理标签
            print post.author
            ptags = request.POST['tags'].strip()
            all_tags = []
            if ptags:
                tags = ptags.split(',')
                for tag in tags:
                    try:
                        t = Tag.objects.get(name=tag)
                    except Tag.DoesNotExist:
                        t = Tag(name=tag)
                        t.save()
                    all_tags.append(t)
            post.save()
            for tg in all_tags:
                post.tags.add(tg)
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render_to_response('post_edit.html', {'form': form, 'is_new': True},context_instance=RequestContext(request))
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render_to_response('post_draft_list.html', {'posts': posts},context_instance=RequestContext(request))
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    # return redirect('post_detail', pk=pk)
    # return HttpResponseRedirect(reverse('blog.views.post_detail',args=(post.pk,)))
    return HttpResponseRedirect('/post/%s' % pk )
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render_to_response('post_edit.html', {'form': form},context_instance=RequestContext(request))

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.index')

# def rLogin(request):
#     """登录界面"""
#     error = ''
#     if request.method == 'GET':
#         return render_to_response('login.html')
#     else:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         if username and password:
#             user = authenticate(username=username, password=password)
#             print user
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     # c = {}
#                     # c.update(csrf(request))
#                     # request.session['csrf_token'] = str(c.get('csrf_token'))
#         # user_filter = User.objects.filter(username=username)
#         # if user_filter:
#         #     user = user_filter[0]
#         #     if PyCrypt.md5_crypt(password) == user.password:
#         #         request.session['user_id'] = user.id
#         #         user_filter.update(last_login=datetime.datetime.now())
#                 # response.set_cookie('username', username, expires=604800)
#                 # response.set_cookie('seed', PyCrypt.md5_crypt(password), expires=604800)
#                 # return response
#     return render_to_response('login.html', {'error': error})