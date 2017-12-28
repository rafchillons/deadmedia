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
from .forms import VideoDeleteForm, BotTaskForm, BotTaskRemoveForm, BotTaskInspectForm
from .models import Video, BotTask, PaginatorModel
from .utils.bot_module import (
    ThreadDownloader,
    VideoRemover,
)
from .utils.video_handler_module import download_and_save_all_new_videos_2ch_b, delete_all_videos_by_added_date, \
    delete_video_by_db_object
from .utils.categorys_handler_module import (
    remove_all_videos_from_category,
)
from .utils.inspector_module import fined_banned_videos_and_delete_them
from .utils.parse_2ch_module import _find_files_in_thread
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



def main_page(request):
    videos = Video.objects.all().order_by('added_date')
    return render(request,
                  'main.html',
                  {
                      'videos': videos,
                      'count': videos.__len__(),
                  })


def show_webm(request):
    try:
        page = int(request.GET.get('page', 1))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = 1

    videos_to_show = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_webm=True).order_by(
        '-added_date')[24 * (page - 1):(24 * page) + 24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(videos_to_show)] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page + 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'webm',
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                      'hide_videos_link': 'category-hide-webm',
                      'delete_videos_link': 'category-delete-webm',
                  })


def show_adult(request):
    try:
        page = int(request.GET.get('page', 1))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = 1

    videos_to_show = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_adult=True).order_by(
        '-added_date')[24 * (page - 1):(24 * page) + 24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(videos_to_show)] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page + 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'adult',
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                      'hide_videos_link': 'category-hide-adult',
                      'delete_videos_link': 'category-delete-adult',
                  })


def show_hot(request):
    try:
        page = int(request.GET.get('page', 1))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = 1

    videos_to_show = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_hot=True).order_by(
            '-added_date')[24 * (page - 1):(24 * page) + 24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(videos_to_show)] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page + 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'hot',
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                      'hide_videos_link': 'category-hide-hot',
                      'delete_videos_link': 'category-delete-hot',
                  })


def show_mp4(request):
    try:
        page = int(request.GET.get('page', 1))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = 1

    videos_to_show = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_mp4=True).order_by(
            '-added_date')[24 * (page - 1):(24 * page) + 24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(videos_to_show)] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page + 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'mp4',
                      'videos': videos,
                      'is_authenticated': request.user.is_authenticated(),
                      'hide_videos_link': 'category-hide-mp4',
                      'delete_videos_link': 'category-delete-mp4',
                  })


def show_faq(request):
    return render(request,
                  'faq_page.html',
                  {
                      'category_name': 'faq',
                      'is_authenticated': request.user.is_authenticated(),
                  })


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


@login_required
def show_hidden(request):
    list_of_grouped_videos = zip(
        *[iter(
            Video.objects.all().filter(video_status=Video.STATUS_HIDDEN).order_by('-added_date'))] * 4)

    page = request.GET.get('page', 1)
    paginator = Paginator(list_of_grouped_videos, 1)

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,
                  'videos_page.html',
                  {
                      'category_name': 'hidden',
                      'videos': videos,
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


@login_required
def get_videos_size_in_db(request):
    all_videos_in_db = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED)
    all_videos_count = all_videos_in_db.__len__()
    return HttpResponse(all_videos_count)


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
def create_bot_inspector_view(request):
    if request.method == 'POST':
        form = BotTaskInspectForm(request.POST)
        if form.is_valid():
            bot = BotTask()

            bot.bot_task = BotTask.BOT_TASK_INSPECT_BANNED
            bot.task_data = json.dumps(form.cleaned_data)

            bot.save()
            return redirect('webm-page')

    else:
        form = BotTaskForm()

    return render(request, 'create_inspect_bot.html', {'form': form, 'messages': messages.get_messages(request)})



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
    delete_video_by_db_object(video, remove_from_db=False)
    return redirect('webm-page')

@login_required
def hide_video_id_view(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.video_status = Video.STATUS_HIDDEN
    video.save()
    return redirect('webm-page')



@login_required
def webm_category_hide(request):
    remove_all_videos_from_category('is_webm')
    return redirect('webm-page')

@login_required
def mp4_category_hide(request):
    remove_all_videos_from_category('is_mp4')
    return redirect('mp4-page')

@login_required
def adult_category_hide(request):
    remove_all_videos_from_category('is_adult')
    return redirect('adult-page')

@login_required
def hot_category_hide(request):
    remove_all_videos_from_category('is_hot')
    return redirect('hot-page')

@login_required
def webm_category_delete(request):
    remove_all_videos_from_category('is_webm')
    return redirect('webm-page')

@login_required
def mp4_category_delete(request):
    remove_all_videos_from_category('is_mp4')
    return redirect('mp4-page')

@login_required
def adult_category_delete(request):
    remove_all_videos_from_category('is_adult')
    return redirect('adult-page')

@login_required
def hot_category_delete(request):
    remove_all_videos_from_category('is_hot')
    return redirect('hot-page')


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


def view_video_by_id(request, pk):
    video = get_object_or_404(Video, pk=pk)
    views = video.view_video(request)
    return HttpResponse(views)


def like_video_by_id(request, pk):
    video = get_object_or_404(Video, pk=pk)
    likes = video.like_video(request)
    return HttpResponse(likes)


@login_required
def delete_category(request, pk):
    if pk == 'adult':
        videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_adult=True)
        for video in videos:
            video.is_adult = False
            video.save()
    elif pk == 'mp4':
        videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_mp4=True)
        for video in videos:
            video.is_mp4 = False
            video.save()
    elif pk == 'webm':
        videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_webm=True)
        for video in videos:
            video.is_webm = False
            video.save()
    else:
        return redirect('error404')

    return redirect('page-admin-new')


#@login_required
def test(request):
    #video = get_object_or_404(Video, pk=1)
    #return HttpResponse(video.check_if_video_been_viewed(request))
    #videos = Video.objects.all().filter(video_status=Video.STATUS_DOWNLOADED, is_webm=False, is_adult=False, is_mp4=False, is_hot=False)
    #for video in videos:
    #    video.is_webm = False
    #    video.save()

    #for x in range(10):
    #    model = Video.objects.create_video()
    #    model.video_status = Video.STATUS_DOWNLOADED
    #    model.is_webm = True
    #    model.title = 'test{}'.format(x)
    #    model.save()

    #print('HTTP_USER_AGENT:{}'.format(request.META['HTTP_USER_AGENT']))
    #print('REMOTE_ADDR:{}'.format(request.META['REMOTE_ADDR']))
    #print('HTTP_COOKIE:{}'.format(request.META['HTTP_COOKIE']))
    #print('REMOTE_ADDR:{}'.format(request.META['REMOTE_ADDR']))

    #video = get_object_or_404(Video, pk=7)
    #print('liked:{}'.format(video.is_liked(request)))

    #print('ip:{}'.format(get_client_ip(request)))
    #print('request: {}'.format(request.META.keys()))
    fined_banned_videos_and_delete_them()
    return redirect('webm-page')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
