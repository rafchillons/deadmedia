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
    url(r'^admin/', admin.site.urls),
    url(r'^1$', views.main_page, name='main-page'),
    url(r'^maksim$', views.show_maksim_page, name='page-maksim'),
    url(r'^page/admin/$', views.show_admin_page, name='page-admin'),
    url(r'^delete/$', views.delete_all_videos, name='delete-all'),
    url(r'^page/admin/download/all$', views.download_all_videos_from_2ch, name='page-admin-download-all'),
    url(r'^page/admin/download/startbot$', views.start_downloading_bot, name='page-admin-download-start-bot'),
    url(r'^page/admin/download/stopbot$', views.stop_downloading_bot, name='page-admin-download-stop-bot'),
    url(r'^page/admin/remove/startbot$', views.start_removing_bot, name='page-admin-remove-start-bot'),
    url(r'^page/admin/remove/stopbot$', views.stop_removing_bot, name='page-admin-remove-stop-bot'),

    url(r'^newadmin$', views.new_admin, name='page-admin-new'),
    url(r'^newerror$', views.new_error, name='page-error'),

    url(r'^$', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webms.views.handler404'