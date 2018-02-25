from __future__ import unicode_literals

import json
import logging
import os
from functools import wraps

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import *
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from requests.exceptions import ConnectionError

from deadsource.utils.logs_module import log_critical_decorator
from .forms import VideoDeleteForm, BotTaskForm, BotTaskRemoveForm, BotTaskInspectForm
from .models import Video, BotTask
from .utils import paginator_module
from .utils.bot_module import (
    ThreadDownloader,
    VideoRemover,
)
from .utils.categorys_handler_module import (
    remove_all_videos_from_category,
)
from .utils.logs_module import get_logs_from_file
from .utils.video_handler_module import delete_video_by_db_object

logger = logging.getLogger("deadsource")


@log_critical_decorator(logger)
def show_videos(request,
                category='webm',
                sort='date',
                order='ordered'):
    videos_filters = "video_status = 'Video is downloaded'"
    page_content = {'is_authenticated': request.user.is_authenticated()}
    sort_revert = not order == 'reversed'

    if category == 'webm':
        videos_filters += " and is_webm = 1"
        page_content['category_name'] = 'webm'
        page_content['hide_videos_link'] = 'category-hide-webm'
        page_content['delete_videos_link'] = 'category-delete-webm'

    elif category == 'mp4':
        videos_filters += " and is_mp4 = 1"
        page_content['category_name'] = 'mp4'
        page_content['hide_videos_link'] = 'category-hide-mp4'
        page_content['delete_videos_link'] = 'category-delete-mp4'

    elif category == 'adult':
        videos_filters += " and is_adult = 1"
        page_content['category_name'] = 'adult'
        page_content['hide_videos_link'] = 'category-hide-adult'
        page_content['delete_videos_link'] = 'category-delete-adult'

    elif category == 'hot':
        videos_filters += " and is_hot = 1"
        page_content['category_name'] = 'hot'
        page_content['hide_videos_link'] = 'category-hide-hot'
        page_content['delete_videos_link'] = 'category-delete-hot'

    else:
        return redirect('error404-page')

    if sort == 'date':
        videos_order = 'added_date DESC' if sort_revert else 'added_date ASC'
        page_content['current_filter_name'] = 'Newest'

    elif sort == 'likes':
        videos_order = 'video_likes DESC' if sort_revert else 'video_likes ASC'
        page_content['current_filter_name'] = 'Hottest'

    elif sort == 'views':
        videos_order = 'video_views DESC' if sort_revert else 'video_views ASC'
        page_content['current_filter_name'] = 'Most Viewed'


    else:
        return redirect('error404-page')

    videos = paginator_module.get_filtered_and_sorted_videos_page(request, videos_filters, videos_order)

    page_content['videos'] = videos
    return render(request, 'videos_page.html', page_content)

@log_critical_decorator(logger)
def show_faq(request):
    return render(request,
                  'faq_page.html',
                  {
                      'category_name': 'faq',
                      'is_authenticated': request.user.is_authenticated(),
                  })

@log_critical_decorator(logger)
@login_required
def show_all(request):
    list_of_grouped_videos = zip(
        *[iter(
            Video.objects.all().filter().order_by('-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 3)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'all',
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                  })

@log_critical_decorator(logger)
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

@log_critical_decorator(logger)
@login_required
def show_reported(request):

     try:
         page = int(request.GET.get('page', -1))
     except Exception as e:
         logging.error('error!{} '.format(e))
         page = -1

     all_videos = Video.objects.all().filter(is_reported=True, video_status=Video.STATUS_DOWNLOADED).order_by('-added_date')
     sorted_videos = sorted(all_videos, key=lambda y: y.get_reports, reverse=True)
     videos = sorted_videos

     return render(request,
                   'reports_page.html',
                   {
                       'is_authenticated': request.user.is_authenticated(),
                       'videos': videos,
                   })

@log_critical_decorator(logger)
@login_required
def delete_all_videos(request):
    videos = Video.objects.all()

    for video in videos:
        delete_video_by_db_object(video)

    return redirect('page-admin-new')

@log_critical_decorator(logger)
@login_required
def new_admin(request):
    return render(request, 'admin.html')

@log_critical_decorator(logger)
def new_error(request):
    return render(request, 'error404_page.html')

@log_critical_decorator(logger)
@login_required
def new_admin(request):
    bot_downloader = ThreadDownloader()
    bot_remover = VideoRemover()



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
                      'videos_weight': 'collecting',
                      'videos_count': 'collecting',
                      'form': form,
                      'bot_downloader': bot_downloader.instance,
                      'bot_remover': bot_remover.instance,
                      'is_authenticated': request.user.is_authenticated(),

                  })

@log_critical_decorator(logger)
@login_required
def get_videos_size_in_db(request):
    all_videos_weight = 0
    all_videos_weight_type = 'Kb'
    all_videos_in_db = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED)

    for video in all_videos_in_db:
        all_videos_weight += int(video.video_size)

    if all_videos_weight > 999999999:
        all_videos_weight = all_videos_weight / 1000000000
        all_videos_weight_type = 'Tb'
    elif all_videos_weight > 999999:
        all_videos_weight = all_videos_weight / 1000000
        all_videos_weight_type = 'Gb'
    elif all_videos_weight > 999:
        all_videos_weight = all_videos_weight / 1000
        all_videos_weight_type = 'Mb'

    size = '{}{}'.format(all_videos_weight, all_videos_weight_type)

    return HttpResponse(size)

@log_critical_decorator(logger)
@login_required
def get_videos_count_in_db(request):
    all_videos_in_db = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED)
    all_videos_count = all_videos_in_db.__len__()
    return HttpResponse(all_videos_count)

@log_critical_decorator(logger)
def handler404(request):
    return render(request, 'error404_page.html')

@log_critical_decorator(logger)
def logout_view(request):
    logout(request)
    return redirect('webm-page')

@log_critical_decorator(logger)
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

@log_critical_decorator(logger)
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

@log_critical_decorator(logger)
@login_required
def create_bot_downloader_view(request):
    if request.method == 'POST':
        form = BotTaskForm(request.POST)

        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_DOWNLOAD_2CH_WEBM
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('main-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_bot.html', {'form': form, 'messages': messages.get_messages(request)})

@log_critical_decorator(logger)
@login_required
def create_bot_remover_view(request):
    if request.method == 'POST':
        form = BotTaskRemoveForm(request.POST)
        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_REMOVE_WEBM
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('main-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_remove_bot.html', {'form': form, 'messages': messages.get_messages(request)})

@log_critical_decorator(logger)
@login_required
def create_bot_inspector_view(request):
    if request.method == 'POST':
        form = BotTaskInspectForm(request.POST)
        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_INSPECT_BANNED
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('main-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_inspect_bot.html', {'form': form, 'messages': messages.get_messages(request)})

@log_critical_decorator(logger)
@login_required
def category_delete(request, category):
    if category == 'hot':
        category_filter = 'is_hot'

    elif category == 'adult':
        category_filter = 'is_adult'

    elif category == 'webm':
        category_filter = 'is_webm'

    elif category == 'mp4':
        category_filter = 'is_mp4'

    else:
        return redirect('error404-page')

    remove_all_videos_from_category(category_filter)

    return redirect('videos-page', category=category)

@log_critical_decorator(logger)
@login_required
def admin_video_commands(request, pk, command):
    video = get_object_or_404(Video, pk=pk)

    if command.startswith('move/'):
        video.is_hot = False
        video.is_adult = False
        video.is_webm = False
        video.is_mp4 = False

        if command == 'move/hot':
            video.is_hot = True

        elif command == 'move/adult':
            video.is_adult = True

        elif command == 'move/webm':
            video.is_webm = True

        elif command == 'move/mp4':
            video.is_mp4 = True

        else:
            return redirect('error404-page')

        video.save()

    else:
        if command == 'delete':
            delete_video_by_db_object(video, remove_from_db=False, remove_from_drive=True)

        elif command == 'hide':
            video.video_status = Video.STATUS_HIDDEN
            video.save()

        elif command == 'reports/reset':
            video.reset_reports()

    return HttpResponse(True)


def user_video_commands(request, pk, command):
    video = get_object_or_404(Video, pk=pk)

    if command == 'view':
        result = video.view_video(request)

    elif command == 'like':
        result = video.like_video(request)

    elif command == 'report':
        result = video.report_video(request)

    else:
        return redirect('error404')

    return HttpResponse(result)

@log_critical_decorator(logger)
@login_required
def show_logs(request, file):
    log_file_path = os.path.join(settings.BASE_DIR, 'logs', str(file))

    if os.path.exists(log_file_path):
        result = get_logs_from_file(log_file_path)

    else:
        return HttpResponse("No logs file found '{}'".format(log_file_path))

    return render(request, 'logs.html', {'logs': result})

@log_critical_decorator(logger)
@login_required
def test(request):
    #print('kek')
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
    #for x in range(100):
    #    model = Video.objects.create_video()
    #    model.video_status = Video.STATUS_DOWNLOADED
    #    model.is_webm = True
    #    model.is_adult = True
    #    model.is_mp4 = True
    #    model.title = 'test{}'.format(x)
    #    model.save()
    #print(Video.objects.get_sorted_ids())
    #logging.error('new error')
    return HttpResponse()

@log_critical_decorator(logger)
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
