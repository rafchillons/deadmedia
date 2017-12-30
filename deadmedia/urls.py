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

    url(r'^$', views.show_webm, name='webm-page'),
    url(r'^adult/$', views.show_adult, name='adult-page'),
    url(r'^faq/$', views.show_faq, name='faq-page'),
    url(r'^hot/$', views.show_hot, name='hot-page'),
    url(r'^mp4/$', views.show_mp4, name='mp4-page'),
    url(r'^all/$', views.show_all, name='all-page'),
    url(r'^hidden/$', views.show_hidden, name='hidden-page'),
    url(r'^report/$', views.show_reported, name='reported-page'),

    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.login_view, name='login-page'),
    url(r'^accounts/login/$', views.login_view, name='login-page'),


    url(r'^bot/downloader/create/$', views.create_bot_downloader_view, name='create-downloader-bot'),
    url(r'^bot/inspector/create/$', views.create_bot_inspector_view, name='create-inspector-bot'),
    url(r'^status/$', views.bot_status_view, name='status-bot'),

    url(r'^bot/create/remover$', views.create_bot_remover_view, name='create-bot-remover'),

    url(r'^bot/(?P<pk>[0-9]+)/start/$', views.bot_start_id, name='start-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/stop/$', views.bot_stop_id, name='stop-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/delete/$', views.bot_delete_id, name='delete-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/pause/on/$', views.bot_pause_on, name='pause-on-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/pause/off/$', views.bot_pause_off, name='pause-off-bot-id'),

    url(r'^video/(?P<pk>[0-9]+)/delete/$', views.delete_video_id_view, name='video-delete-id'),
    url(r'^video/(?P<pk>[0-9]+)/hide/$', views.hide_video_id_view, name='video-hide-id'),

    #url(r'^page/admin/$', views.show_admin_page, name='page-admin'),
    url(r'^delete/$', views.delete_all_videos, name='delete-all'),

    url(r'^newadmin$', views.new_admin, name='page-admin-new'),
    url(r'^videos/size$', views.get_videos_size_in_db, name='page-admin-videos-size'),
    url(r'^videos/count$', views.get_videos_count_in_db, name='page-admin-videos-count'),
    url(r'^error404$', views.handler404, name='error404-page'),

    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    url(r'^video/(?P<pk>[0-9]+)/view/$', views.view_video_by_id, name='video-view'),

    url(r'^video/(?P<pk>[0-9]+)/like/$', views.like_video_by_id, name='video-like'),

    url(r'^video/(?P<pk>[0-9]+)/report/$', views.report_video_by_id, name='video-report'),

    url(r'^category/hide$', views.webm_category_hide, name='category-hide-webm'),
    url(r'^adult/category/hide$', views.adult_category_hide, name='category-hide-adult'),
    url(r'^hot/category/hide$', views.hot_category_hide, name='category-hide-hot'),
    url(r'^mp4/category/hide$', views.mp4_category_hide, name='category-hide-mp4'),

    url(r'^category/delete$', views.webm_category_delete, name='category-delete-webm'),
    url(r'^adult/category/delete$', views.adult_category_delete, name='category-delete-adult'),
    url(r'^hot/category/delete$', views.hot_category_delete, name='category-delete-hot'),
    url(r'^mp4/category/delete$', views.mp4_category_delete, name='category-delete-mp4'),


    url(r'^test$', views.test, name='test'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webms.views.handler404'
