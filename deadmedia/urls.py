"""deadmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from deadsource import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', admin.site.urls),

    url(r'^$', views.show_videos, {'category': 'hot'}, name='main-page'),

    url(r'^(?P<category>(hot|adult|webm|mp4|all|hidden))/$',
        views.show_videos,
        {'sort': 'date', 'order': 'ordered'},
        name='videos-page'),

    url(r'^video/(?P<pk>[0-9]+)/(?P<command>(view|like|report))/$',
        views.user_video_commands,
        name='video-user-command'),

    url(r'^(?P<category>(hot|adult|webm|mp4|all|hidden))/sort/(?P<sort>(date|likes|views))/'
        r'(?P<order>(ordered|reversed))/$',
        views.show_videos,
        name='videos-page-sort'),

    url(r'^video/(?P<pk>[0-9]+)/(?P<command>(move/(hot|adult|webm|mp4))|delete|hide|reports/reset)/$',
        views.admin_video_commands,
        name='video-move-category'),

    url(r'^(?P<category>(hot|adult|webm|mp4|all|hidden))/category/delete$',
        views.category_delete,
        name='category-delete'),

    url(r'^reports/$', views.show_reported, name='reported-page'),
    url(r'^faq/$', views.show_faq, name='faq-page'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.login_view, name='login-page'),
    url(r'^accounts/login/$', views.login_view, name='login-page'),


    url(r'^bot/downloader/create/$', views.create_bot_downloader_view, name='create-downloader-bot'),
    url(r'^bot/inspector/create/$', views.create_bot_inspector_view, name='create-inspector-bot'),

    url(r'^bot/create/remover$', views.create_bot_remover_view, name='create-bot-remover'),

    #url(r'^page/admin/$', views.show_admin_page, name='page-admin'),
    url(r'^delete/$', views.delete_all_videos, name='delete-all'),

    url(r'^newadmin$', views.new_admin, name='page-admin-new'),
    url(r'^videos/size$', views.get_videos_size_in_db, name='page-admin-videos-size'),
    url(r'^videos/count$', views.get_videos_count_in_db, name='page-admin-videos-count'),
    url(r'^error404$', views.handler404, name='error404-page'),
    url(r'^error500$', views.handler404, name='error500-page'),

    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    url(r'^test$', views.test, name='test'),

    url(r'^logs/(?P<file>.*)$',
        views.show_logs,
        name='show-logs'),


    #url(r'^tasks/', include('taskmanager.urls')),
    url(r'^tasks/', include('deadtasks.urls', namespace='tasks')),
    url(r'^.*$', views.handler404),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webms.views.handler404'
