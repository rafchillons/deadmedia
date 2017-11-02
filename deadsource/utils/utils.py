# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urllib2 import Request, urlopen
import urllib2
import threading
import time
from datetime import datetime
from deadsource.models import Video
from deadmedia.settings import MEDIA_ROOT
from os.path import (
    join,
)


def find_threads_by_word_in_comments(words_to_find=(u'вебм', 'webm'),
                                     return_numb=False):
    response = urllib2.urlopen('https://2ch.hk/b/catalog.json')
    catalog = json.loads(response.read().decode('utf-8'))

    result = []
    for thread in catalog['threads']:
        lower_comment = thread['comment'].lower()
        if any(map(lambda x: x in lower_comment, words_to_find)):
            result.append(thread['num'] if return_numb else
                          "https://2ch.hk/b/res/{}.json".format(thread['num']))

    return result


def find_files_in_thread(thread_url):
    response = urllib2.urlopen(thread_url)
    thread = json.loads(response.read().decode('utf-8'))

    result = []
    for post in filter(lambda x: x['files'], thread['threads'][0]['posts']):
        result.extend(post['files'])

    return result


def find_files_in_threads(threads_url):
    result = []

    for thread_url in threads_url:
        result.extend(find_files_in_thread(thread_url))

    return result


def download_from_url(url):
    r = Request(url=url)
    return urlopen(r).read()


def download_and_save_video_write_db(url_to_download,
                             title,
                             video_format):
    """video = Video()
    video.title = title
    video.downloaded_url = url_to_download
    video.video_status = Video.STATUS_DOWNLOADING
    video.save()

    try:
        file_name = "{}.{}".format(video.id, video_format)

        r = Request(url=video.downloaded_url)
        with open(join(MEDIA_ROOT, file_name), str('wb')) as f:
            f.write(urlopen(r).read())

        video.src_webm = file_name
        video.save()
    except Exception as e:
        pass
"""


class ThreadDownloader(object):
    class __ThreadDownloader(threading.Thread):
        def __init__(self,
                     is_working=False,
                     is_max_iter=True,
                     is_max_time=True,
                     max_working_iter=1,
                     max_working_time=1,
                     interval=10):
            threading.Thread.__init__(self)
            self.is_working = is_working
            self.is_max_iter = is_max_iter
            self.is_max_time = is_max_time
            self.max_working_iter = max_working_iter
            self.max_working_time = max_working_time
            self.interval = interval
            self.iters_done = 0
            self.created_date = datetime.now()
            self.started_date = None
            self.last_iter = None

        def __str__(self):
            return repr(self) + str(self.is_working)

        def run(self):
            self.started_date = datetime.now()
            self.iters_done = 0
            self.is_working = True
            while self.is_working:
                self.last_iter = datetime.now()
                self.iters_done += 1

                if self.is_max_iter \
                        and self.max_working_iter < self.iters_done:
                    break
                if self.is_max_time \
                        and self.max_working_time < (datetime.now() - self.started_date).seconds:
                    break

                time.sleep(self.interval - (datetime.now() - self.last_iter).seconds)

        def stop_iter(self):
            self.is_working = False

    instance = None

    def __init__(self, **kwargs):
        if not ThreadDownloader.instance:
            ThreadDownloader.instance = ThreadDownloader.__ThreadDownloader(**kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)
