"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/',views.login),

    url(r'^$', views.index),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^ajax/$',views.ajax),
    # url(r'^login/$', auth_views.login, name='auth_view'),
    url('', include('django.contrib.auth.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# UNDERNEATH your urlpatterns definition, add the following two lines:

