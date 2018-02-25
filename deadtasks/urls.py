from django.conf.urls import url
from . import views

app_name = 'tasks'
urlpatterns = [
    url(r'^create/d/$', views.create_task_2ch_downloader_view, name='create-download'),
    url(r'^create/r/$', views.create_task_old_remover_view, name='create-remove'),

    url(r'^(?P<task_type>(r|d))/(?P<pk>[0-9]+)/(?P<command>(activate|deactivate|delete))/$',
        views.tasks_commands,
        name='commands'),

    url(r'^status/$', views.tasks_status_view, name='status'),
    url(r'^test/$', views.test),
]
