# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests.exceptions import ConnectionError
from functools import wraps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
import deadmedia.settings
from .forms import VideoDeleteForm, BotTaskForm, BotTaskRemoveForm
from .models import Video, BotTask
from .utils.bot_module import (
    ThreadDownloader,
    VideoRemover,
)
from .utils.video_handler_module import download_and_save_all_new_videos_2ch_b, delete_all_videos_by_added_date, \
    delete_video_by_db_object
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages
import logging
import json

from hitcount.models import HitCount
from hitcount.views import HitCountMixin
import hitcount


def main_page(request):
    videos = Video.objects.all().order_by('added_date')
    return render(request,
                  'main.html',
                  {
                      'videos': videos,
                      'count': videos.__len__(),
                  })


def show_webm(request):
    list_of_grouped_videos = zip(*[iter(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED,
                                                                   is_webm=True).order_by(
        '-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 3)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request,
                  'webm_page.html',
                  {
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_adult(request):
    list_of_grouped_videos = zip(*[iter(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED,
                                                                   is_adult=True).order_by(
        '-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 3)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,
                  'adult_page.html',
                  {
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_hot(request):
    list_of_grouped_videos = zip(*[iter(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED,
                                                                   is_hot=True).order_by('-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 3)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,
                  'hot_page.html',
                  {
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_mp4(request):
    list_of_grouped_videos = zip(
        *[iter(
            Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED,
                                       is_mp4=True).order_by('-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 3)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,
                  'mp4_page.html',
                  {
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_faq(request):
    return render(request,
                  'faq_page.html',
                  {
                      'is_authenticated': request.user.is_authenticated(),
                  })


@login_required
def show_all(request):
    videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED).order_by('added_date')

    return render(request,
                  'all_page.html',
                  {
                      'videos': videos,
                  })


@login_required
def show_admin_page(request):
    bot_downloader = ThreadDownloader()
    bot_remover = VideoRemover()

    if request.method == 'POST':
        form = VideoDeleteForm(request.POST)

        if form.is_valid():
            video = get_object_or_404(Video, pk=int(form.cleaned_data['storage_name']))
            video.delete()
            return redirect('page-admin-new')

    else:
        form = VideoDeleteForm()

    return render(request,
                  'admin_page.html',
                  {
                      'form': form,
                      'bot_downloader': bot_downloader.instance,
                      'bot_remover': bot_remover.instance,
                  })


@login_required
def delete_all_videos(request):
    videos = Video.objects.all()

    for video in videos:
        delete_video_by_db_object(video)



    return redirect('page-admin-new')


@login_required
def new_admin(request):
    return render(request, 'admin.html')


def new_error(request):
    return render(request, 'error404_page.html')


@login_required
def new_admin(request):
    bot_downloader = ThreadDownloader()
    bot_remover = VideoRemover()

    all_videos_in_db = list(reversed(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED)))
    all_videos_count = all_videos_in_db.__len__()

    all_videos_weight = 0
    for video in all_videos_in_db:
        all_videos_weight += int(video.video_size)

    videos_weight = {}
    if all_videos_weight > 999999999:
        videos_weight['size'] = all_videos_weight / 1000000000
        videos_weight['type'] = 'Tb'
    elif all_videos_weight > 999999:
        videos_weight['size'] = all_videos_weight / 1000000
        videos_weight['type'] = 'Gb'
    elif all_videos_weight > 999:
        videos_weight['size'] = all_videos_weight / 1000
        videos_weight['type'] = 'Mb'
    else:
        videos_weight['size'] = all_videos_weight
        videos_weight['type'] = 'Kb'

    if request.method == 'POST':
        form = VideoDeleteForm(request.POST)

        if form.is_valid():
            video = get_object_or_404(Video, pk=int(form.cleaned_data['storage_name']))
            delete_video_by_db_object(video)
            return redirect('page-admin-new')

    else:
        form = VideoDeleteForm()

    return render(request,
                  'admin.html',
                  {
                      'videos_weight': videos_weight['size'],
                      'videos_weight_type': videos_weight['type'],
                      'videos_count': all_videos_count,
                      'form': form,
                      'bot_downloader': bot_downloader.instance,
                      'bot_remover': bot_remover.instance,
                  })


def handler404(request):
    return render(request, 'error404_page.html')


def logout_view(request):
    logout(request)
    return redirect('webm-page')


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            try:
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()

                if result['success']:
                    request.recaptcha_is_valid = True
                else:
                    request.recaptcha_is_valid = False
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            except ConnectionError as e:
                request.recaptcha_is_valid = False
                messages.error(request, 'Can not check reCAPTCHA (connection error). Please try again.')
            except Exception as e:
                logging.error('check_recaptcha():{}'.format(e))
                request.recaptcha_is_valid = False
                messages.error(request, 'Unknown reCAPTCHA error. Please try again.')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


@check_recaptcha
def login_view(request):
    logout(request)

    username = password = ''
    if request.method == 'POST' and request.recaptcha_is_valid:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('page-admin-new')

        messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'sign.html', {'messages': messages.get_messages(request)})


@login_required
def create_bot_downloader_view(request):
    if request.method == 'POST':
        form = BotTaskForm(request.POST)

        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_DOWNLOAD_2CH_WEBM
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('webm-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_bot.html', {'form': form, 'messages': messages.get_messages(request)})


@login_required
def create_bot_remover_view(request):
    if request.method == 'POST':
        form = BotTaskRemoveForm(request.POST)

        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_REMOVE_WEBM
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('webm-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_remove_bot.html', {'form': form, 'messages': messages.get_messages(request)})


@login_required
def bot_status_view(request):
    bots = BotTask.objects.all()

    bots_list = []
    for bot in bots:
        bots_list.append({
            'db_object': bot,
            'data_dict': json.loads(str(bot.task_data)),
        })

    return render(request, 'botstatus.html', {'bots': bots_list})


@login_required
def bot_delete_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.delete()
    return redirect('status-bot')


@login_required
def bot_start_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.start_bot()
    return redirect('status-bot')


@login_required
def bot_stop_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.stop_bot()
    return redirect('status-bot')


@login_required
def bot_pause_off(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.pause_off()
    return redirect('status-bot')


@login_required
def bot_pause_on(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.pause_on()
    return redirect('status-bot')


@login_required
def delete_video_id_view(request, pk):
    video = get_object_or_404(Video, pk=pk)
    delete_video_by_db_object(video)
    return redirect('webm-page')


@login_required
def test(request):
    video = get_object_or_404(Video, pk=1620)
    name = video.get_description()['fullname']
    print("name: {}".format(name))
    print("title: {}".format(video.title))
    return HttpResponse(0)


def hit_video_view(request, pk):
    video = get_object_or_404(Video, pk=pk)
    hit_count = HitCount.objects.get_for_object(video)
    hit_count_before = hit_count.hits
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    hit_count_after = hit_count.hits

    if type(hit_count_after) is not int:
        hit_count_after = hit_count_before + 1
    else:
        hit_count_after = -1


    print(type(HttpResponse(hit_count_after)))
    return HttpResponse(hit_count_after)