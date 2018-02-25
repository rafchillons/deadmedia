#! /usr/bin/env python
# -*- coding: utf-8 -*-
from deadmedia.celery import app
from deadtasks.models import DownloadDvachTask, RemoveOldTask
from deadtasks.utils.video_handler_module import download_and_save_all_new_videos_2ch_b, delete_all_videos_by_added_date
import logging

logger = logging.getLogger("deadtasks")


@app.task(ignore_result=True)
def do_2ch_download_tasks():
    logger.info("do_2ch_download_tasks(): started.")

    try:
        for task in DownloadDvachTask.objects.filter(is_active=True):
            task.update_last_launch_date()

            download_and_save_all_new_videos_2ch_b(with_words=task.get_required_words_list,
                                                   without_words=task.get_banned_words_list,
                                                   is_adult=task.video_category == task.CATEGORY_ADULT,
                                                   is_webm=task.video_category == task.CATEGORY_WEBM,
                                                   is_hot=task.video_category == task.CATEGORY_HOT,
                                                   is_mp4=task.video_category == task.CATEGORY_MP4,
                                                   video_formats=task.get_formats_to_download_list)
    except Exception as e:
        logger.critical(e)
        logger.info("do_2ch_download_tasks(): finished with error.")

    else:
        logger.info("do_2ch_download_tasks(): finished.")


@app.task(ignore_result=True)
def do_remove_old_tasks():
    logger.info("do_remove_old_tasks(): started.")

    try:
        for task in RemoveOldTask.objects.filter(is_active=True):
            task.update_last_launch_date()

            delete_all_videos_by_added_date(ignore_time=task.video_age,
                                            is_adult=task.video_category == task.CATEGORY_ADULT,
                                            is_webm=task.video_category == task.CATEGORY_WEBM,
                                            is_hot=task.video_category == task.CATEGORY_HOT,
                                            is_mp4=task.video_category == task.CATEGORY_MP4)
    except Exception as e:
        logger.critical(e)
        logger.info("do_remove_old_tasks(): finished with error.")

    else:
        logger.info("do_remove_old_tasks(): finished.")