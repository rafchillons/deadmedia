# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from deadsource.utils.logs_module import log_critical_decorator
from deadtasks.models import DownloadDvachTask, RemoveOldTask
from deadtasks.forms import DvachDownloadTaskForm, OldRemoveTaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging

logger = logging.getLogger('deadtasks')

@log_critical_decorator(logger)
@login_required
def create_task_2ch_downloader_view(request):
    if request.method == 'POST':
        form = DvachDownloadTaskForm(request.POST)

        if form.is_valid():
            task = form.save()
            task.save()

            return redirect('tasks:status')

    else:
        form = DvachDownloadTaskForm()

    return render(request, 'create_download.html', {'form': form, 'messages': messages.get_messages(request)})

@log_critical_decorator(logger)
@login_required
def create_task_old_remover_view(request):
    if request.method == 'POST':
        form = OldRemoveTaskForm(request.POST)

        if form.is_valid():
            task = form.save()
            task.save()

            return redirect('tasks:status')

    else:
        form = OldRemoveTaskForm()

    return render(request, 'create_remove.html', {'form': form, 'messages': messages.get_messages(request)})

@log_critical_decorator(logger)
@login_required
def tasks_status_view(request):
    tasks_download = DownloadDvachTask.objects.all()
    tasks_remove = RemoveOldTask.objects.all()

    return render(request,
                  'tasks_status.html',
                  {
                      'tasks_download': tasks_download,
                      'tasks_remove': tasks_remove,
                      'is_authenticated': request.user.is_authenticated()
                  })

@log_critical_decorator(logger)
@login_required
def tasks_commands(request, task_type, pk, command):
    if task_type == 'd':
        bot = get_object_or_404(DownloadDvachTask, pk=pk)

    elif task_type == 'r':
        bot = get_object_or_404(RemoveOldTask, pk=pk)

    else:
        return redirect('error404-page')

    if command == 'activate':
        bot.activate()

    elif command == 'deactivate':
        bot.deactivate()

    elif command == 'delete':
        bot.delete()

    else:
        return redirect('error404-page')

    return redirect('tasks:status')

@log_critical_decorator(logger)
@login_required
def test(request):
    from deadtasks.tasks import do_2ch_download_tasks
    raise Exception


    return HttpResponse(0)
