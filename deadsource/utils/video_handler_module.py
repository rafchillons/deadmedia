# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from deadsource.utils.download_and_save_module import download_and_save_file
from django.shortcuts import render, redirect, get_object_or_404
import json
from deadsource.utils import parse_2ch_module
from urllib2 import Request, urlopen
import urllib2
import threading
import logging
import time
from datetime import datetime
from deadsource.models import Video
from deadmedia.settings import MEDIA_ROOT
from os.path import (
    join,
    basename,
)
from os import remove


def download_and_save_all_new_videos_2ch_b(with_words=(u'вебм', 'webm'),
                                           without_words=(),
                                           max_videos_count=None,
                                           is_adult=False,
                                           is_webm=False,
                                           is_hot=False,
                                           is_mp4=False,
                                           video_formats=('.webm',),
                                           exit_event=threading.Event()):  # this function is not for release
    logging.debug("Downloading and saving all videos from 2ch.")

    founded_threads = parse_2ch_module.find_threads_by_word_in_comments(with_words=with_words,
                                                                        without_words=without_words)

    founded_files_description = parse_2ch_module.find_files_in_threads(founded_threads)

    webms_description = parse_2ch_module.find_all_files_with_formats_from_files(founded_files_description, formats=video_formats)
    webms_description = _get_videos_from_list_not_in_db(webms_description)

    if max_videos_count and max_videos_count < webms_description.__len__():
        webms_description = webms_description[:max_videos_count]

    for webm_description in webms_description:
        try:
            if exit_event.isSet():
                logging.warning('Downloading and saving all videos from 2ch: exit event.')
                break

            webm_description['is_adult'] = is_adult
            webm_description['is_webm'] = is_webm
            webm_description['is_hot'] = is_hot
            webm_description['is_mp4'] = is_mp4

            _download_and_save_webm_video_and_preview(webm_description)
        except urllib2.HTTPError as e:
            logging.warning('Can not download {}: {}'.format(webm_description['source'], e))
        except Exception as e:
            logging.critical("Download_and_save_new_videos: {}.".format(e))

    logging.debug("Downloading and saving all videos from 2ch: complete.")


def _download_and_save_webm_video_and_preview(webm_description):  # this function is not for release
    db_object = Video()
    db_object.save()

    download_url = webm_description['source']
    download_url_preview = webm_description['thumbnail_source']
    path_to_save = join(MEDIA_ROOT, '{}{}'.format(db_object.id, webm_description['video_format']))
    path_to_save_preview = join(MEDIA_ROOT, '{}.{}'.format(db_object.id, 'jpg'))

    download_and_save_file(download_url, path_to_save)
    download_and_save_file(download_url_preview, path_to_save_preview)
    _save_video_info_to_database(db_object,
                                 path_to_save,
                                 download_url,
                                 path_to_save_preview,
                                 webm_description)


def _save_video_info_to_database(video,
                                 storage_path,
                                 source_path,
                                 storage_path_preview,
                                 description_json):
    """
    This function saves video info to database object.
    :param storage_path_preview:
    :param description_json:
    :param source_path_preview:
    :param source_path:
    :param video: database object to save
    :param storage_path: video media path
    :return:
    """

    logging.debug("Saving video .")

    try:
        title = description_json['fullname'].rsplit('.', 1)[0]
        if title != ' ':
            title = 'Untitled'
        video.title = title
        video.description_json = json.dumps(description_json)
        video.video_height = description_json['height']
        video.video_width = description_json['width']
        video.video_duration_str = description_json['duration']
        video.video_size = description_json['size']
        video_size_str = (description_json['size'], 'Kb') \
            if description_json['size'] < 1000 \
            else (description_json['size'] / 1000, 'Mb')
        video.video_size_str = '{}{}'.format(*video_size_str)
        video.storage_path = storage_path
        video.storage_name = basename(storage_path)
        video.source_path = source_path
        video.source_thread_path = 'https://2ch.hk/b/res/{}.html'.format(source_path.rsplit('/', 2)[1])
        video.source_thread_number = source_path.rsplit('/', 2)[1]
        video.preview_storage_path = storage_path_preview
        video.preview_storage_name = basename(storage_path_preview)
        video.is_adult = description_json['is_adult']
        video.is_webm = description_json['is_webm']
        video.is_mp4 = description_json['is_mp4']
        video.is_hot = description_json['is_hot']
        video.video_status = video.STATUS_DOWNLOADED
    except Exception as e:
        logging.error('_save_video_info_to_database(): error while filling video info: {}.'.format(e))
        video.video_status = video.STATUS_ERROR

    video.save()

    logging.debug("Saving video: complete.")


def _get_videos_from_list_not_in_db(videos_description_json):
    logging.debug("Getting videos not in db.")

    video_in_db_sources = [x.source_path for x in Video.objects.filter(video_status=Video.STATUS_DOWNLOADED)]
    result = filter(lambda y: y['source'] not in video_in_db_sources, videos_description_json)

    logging.debug("Getting videos not in db: complete.")
    return result


def _get_videos_from_db_not_in_list(videos_description_json):
    logging.debug("Getting videos not in list.")

    video_in_db = Video.objects().filter(video_status=Video.STATUS_DOWNLOADED)
    videos_description_json_source = [x['source'] for x in videos_description_json]
    result = filter(lambda y: y.source_path not in videos_description_json_source, video_in_db)

    logging.debug("Getting videos not in list: complete.")
    return result


def delete_all_videos_by_added_date(ignore_time=None,
                                    max_videos_count=None,
                                    is_adult=False,
                                    is_webm=False,
                                    is_hot=False,
                                    is_mp4=False,
                                    exit_event=threading.Event()):
    logging.debug("Removing all videos by added date.")

    current_date = datetime.now()

    videos_to_delete = [video for video in Video.objects.all().order_by('-added_date')
                        if (current_date - video.added_date.replace(tzinfo=None)).seconds > ignore_time \
                        and video.is_mp4 == is_mp4 \
                        and video.is_hot == is_hot \
                        and video.is_webm == is_webm \
                        and video.is_adult == is_adult]

    if max_videos_count and max_videos_count < videos_to_delete.__len__():
        videos_to_delete = videos_to_delete[:max_videos_count]

    for video_to_delete in videos_to_delete:
        if exit_event.isSet():
            logging.warning('Removing all videos by added date: exit event.')
            break

        _remove_video_from_storage(video_to_delete)
        _remove_video_from_db(video_to_delete)

    logging.debug("Removing all videos by added date: complete.")


def delete_video_by_source_link(video_source_link):
    logging.debug('Removing video {}'.format(video_source_link))

    video_id = video_source_link.rsplit('/', 1)[1].rsplit('.', 1)[0]
    video = get_object_or_404(Video, pk=video_id)

    _remove_video_from_storage(video)
    _remove_video_from_db(video)

    logging.debug('Removing video: complete.')


def delete_video_by_db_object(db_object):
    logging.debug('Removing video {}'.format(db_object))

    _remove_video_from_storage(db_object)
    _remove_video_from_db(db_object)

    logging.debug('Removing video: complete.')


def _remove_video_from_db(video):
    logging.debug("Removing video from db({}).".format(video))

    video.delete()

    logging.debug("Removing video from db: complete.")


def _remove_video_from_storage(video):
    logging.debug("Removing video from media({}).".format(video))

    try:
        remove(video.storage_path)
    except OSError as e:
        if e.errno == 2:
            logging.error('Fail to remove: {}'.format(e))
        else:
            raise

    try:
        remove(video.preview_storage_path)
    except OSError as e:
        if e.errno == 2:
            logging.error('Fail to remove: {}'.format(e))
        else:
            raise

    logging.debug("Removing video from media: complete.")
