# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from functools import wraps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
import deadmedia.settings
from .forms import VideoDeleteForm, BotTaskForm
from .models import Video, BotTask
from .utils.bot_module import ThreadDownloader, VideoRemover
from .utils.video_handler_module import download_and_save_all_new_videos_2ch_b, delete_all_videos_by_added_date, delete_video_by_db_object
from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.contrib import messages
import json


def main_page(request):
    videos = Video.objects.all().order_by('added_date')
    return render(request,
                  'main.html',
                  {
                      'videos': videos,
                      'count': videos.__len__(),
                  })


def show_webm(request):
    list_of_grouped_videos = zip(*[iter(reversed(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED,
                                                                   is_adult=False,
                                                                   is_music=False).order_by('added_date')))] * 4)

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
                                                                   is_adult=True,
                                                                   is_music=False).order_by('added_date'))] * 4)

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
    return render(request,
                  'hot_page.html',
                  {
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_faq(request):
    return render(request,
                  'faq_page.html',
                  {
                      'is_authenticated': request.user.is_authenticated(),
                  })


def show_mp4(request):
    return render(request,
                  'mp4_page.html',
                  {
                      'is_authenticated': request.user.is_authenticated(),
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
def download_all_videos_from_2ch(request):
    download_and_save_all_new_videos_2ch_b()
    return redirect('main-page')


def show_maksim_page2(request, page):
    videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED).order_by('added_date')

    rows_of_videos = zip(*[iter(videos)] * 4)

    return render(request,
                  'index.html',
                  {
                      'rows_of_videos': rows_of_videos,
                  })


@login_required
def delete_all_videos(request):
    delete_all_videos_by_added_date()
    return redirect('page-admin-new')


@login_required
def show_maksim_page(request):
    all_videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED).order_by('added_date')
    groups_of_videos = zip(*[iter(all_videos)] * 4)
    page = request.GET.get('page', 1)
    paginator = Paginator(groups_of_videos, 3)
    try:
        rows_of_videos = paginator.page(page)
    except PageNotAnInteger:
        rows_of_videos = paginator.page(1)
    except EmptyPage:
        rows_of_videos = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'numbers': rows_of_videos})


"""
def home(request):
    numbers_list = zip(
        *[iter(Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED).order_by('added_date'))] * 4)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 3)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'webm_page.html', {'numbers': numbers})
"""


@login_required
def start_downloading_bot(request):
    bot = ThreadDownloader()
    bot.start()

    return redirect('page-admin-new')


@login_required
def stop_downloading_bot(request):
    bot = ThreadDownloader()
    bot.stop()

    return redirect('page-admin-new')


@login_required
def start_removing_bot(request):
    bot = VideoRemover()
    bot.start()

    return redirect('page-admin-new')


@login_required
def stop_removing_bot(request):
    bot = VideoRemover()
    bot.stop()

    return redirect('page-admin-new')


@login_required
def new_admin(request):
    return render(request, 'admin.html')


@login_required
def new_error(request):
    return render(request, 'error404_page.html')


#@login_required
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
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
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


def create_bot_view(request):
    if request.method == 'POST':
        form = BotTaskForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            bot = form.save()
            bot.bot_status = bot.BOT_STATUS_STOPPED
            bot.task_data = json.dumps(form.cleaned_data)
            bot.save()
            return redirect('webm-page')

    else:
        form = BotTaskForm()

    print(form.is_valid())

    return render(request, 'create_bot.html', {'form': form, 'messages': messages.get_messages(request)})


def bot_status_view(request):
    bots = BotTask.objects.all()

    bots_list = []
    for bot in bots:
        bots_list.append({
            'db_object': bot,
            'data_dict': json.loads(str(bot.task_data)),
        })

    return render(request, 'botstatus.html', {'bots': bots_list})


def bot_start_view(request):
    bot = BotTask()

    data = {
        'is_max_time': False,
        'is_max_iter': False,
        'interval': 10,
        'iters_to_do': 1,
        'working_time': 0,
        'with_words': ('fap', u'фап'),  # (u'вебм', 'webm'),
        'without_words': (u'музыкальный',),  # 'fap'),
        'max_videos_count': None,
        'is_music': False,
        'is_adult': True,
    }

    bot.task_data = json.dumps(data)
    bot.bot_status = bot.BOT_STATUS_STOPPED
    bot.bot_task = bot.BOT_TASK_DOWNLOAD_2CH_WEBM
    bot.save()

    bot.start_bot()

    return redirect('create-bot')


def bot_delete_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.delete()
    return redirect('status-bot')


def bot_start_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.start_bot()
    return redirect('status-bot')


def bot_stop_id(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.stop_bot()
    return redirect('status-bot')


def bot_pause_off(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.pause_off()
    return redirect('status-bot')


def bot_pause_on(request, pk):
    bot = get_object_or_404(BotTask, pk=pk)
    bot.pause_on()
    return redirect('status-bot')


def delete_video_id_view(request, pk):
    video = get_object_or_404(Video, pk=pk)
    delete_video_by_db_object(video)
    return redirect('webm-page')