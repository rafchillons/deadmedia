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
    url(r'^adult$', views.show_adult, name='adult-page'),
    url(r'^faq$', views.show_faq, name='faq-page'),
    url(r'^hot$', views.show_hot, name='hot-page'),
    url(r'^mp4$', views.show_mp4, name='mp4-page'),

    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^login$', views.login_view, name='login-page'),

    url(r'^create$', views.create_bot_view, name='create-bot'),
    url(r'^start$', views.bot_start_view, name='start-bot'),
    url(r'^status$', views.bot_status_view, name='status-bot'),

    url(r'^bot/(?P<pk>[0-9]+)/start/$', views.bot_start_id, name='start-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/stop/$', views.bot_stop_id, name='stop-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/delete/$', views.bot_delete_id, name='delete-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/pause/on/$', views.bot_pause_on, name='pause-on-bot-id'),
    url(r'^bot/(?P<pk>[0-9]+)/pause/off/$', views.bot_pause_off, name='pause-off-bot-id'),

    url(r'^video/(?P<pk>[0-9]+)/delete/$', views.delete_video_id_view, name='video-delete-id'),

    url(r'^maksim$', views.show_maksim_page, name='page-maksim'),
    url(r'^page/admin/$', views.show_admin_page, name='page-admin'),
    url(r'^delete/$', views.delete_all_videos, name='delete-all'),
    url(r'^page/admin/download/all$', views.download_all_videos_from_2ch, name='page-admin-download-all'),
    url(r'^page/admin/download/startbot$', views.start_downloading_bot, name='page-admin-download-start-bot'),
    url(r'^page/admin/download/stopbot$', views.stop_downloading_bot, name='page-admin-download-stop-bot'),
    url(r'^page/admin/remove/startbot$', views.start_removing_bot, name='page-admin-remove-start-bot'),
    url(r'^page/admin/remove/stopbot$', views.stop_removing_bot, name='page-admin-remove-stop-bot'),

    url(r'^newadmin$', views.new_admin, name='page-admin-new'),
    url(r'^error404$', views.handler404, name='error404-page'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webms.views.handler404'
