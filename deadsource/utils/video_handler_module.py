# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from download_and_save_module import download_and_save_file
from django.shortcuts import render, redirect, get_object_or_404
import json
import parse_2ch_module
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
                                           is_music=False,
                                           is_adult=False):  # this function is not for release
    logging.debug("Downloading and saving all videos from 2ch.")

    founded_threads = parse_2ch_module.find_threads_by_word_in_comments(with_words=with_words,
                                                                        without_words=without_words)

    founded_files_description = parse_2ch_module.find_files_in_threads(founded_threads)

    webms_description = parse_2ch_module.find_all_webs_from_files(founded_files_description)
    webms_description = _get_videos_from_list_not_in_db(webms_description)

    if max_videos_count:
        webms_description = webms_description[:max_videos_count]

    for webm_description in webms_description:
        try:
            webm_description['is_music'] = is_music
            webm_description['is_adult'] = is_adult

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
    path_to_save = join(MEDIA_ROOT, '{}.{}'.format(db_object.id, 'webm'))
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

    video.title = description_json['fullname'].rsplit('.', 1)[0]
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
    video.preview_storage_path = storage_path_preview
    video.preview_storage_name = basename(storage_path_preview)
    video.is_adult = description_json['is_adult']
    video.is_music = description_json['is_music']
    video.video_status = video.STATUS_DOWNLOADED
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


def delete_all_videos_by_added_date(added_date=0):
    logging.debug("Removing all videos by added date.")

    current_date = datetime.now()
    videos_to_delete = [video for video in Video.objects.all() if
                        (current_date - video.added_date.replace(tzinfo=None)).seconds > added_date]

    for video_to_delete in videos_to_delete:
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


