# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urllib2 import Request, urlopen
import urllib2
import threading
import time
import logging
from datetime import datetime
from deadmedia.settings import MEDIA_ROOT
from os.path import (
    join,
)


CATALOG_URL = 'https://2ch.hk/b/catalog.json'


def find_all_files_with_formats_from_files(all_files, formats=('.webm',)):
    """
    This function returns all founded webms in file
    and changes their paths to absolute
    :param formats:
    :param all_files:
    :return:
    """
    logging.debug("Finding webms in files.")

    result = []

    if formats:
        for elem in all_files:
            for end in formats:
                if elem['path'].endswith(end):
                    elem['video_format'] = end
                    result.append(elem)
                    break

    else:
        result = all_files

        result = filter(lambda x: x['path'].endswith('.webm'), all_files)

    for elem in result:
        elem['source'] = 'https://2ch.hk{}'.format(elem['path'])
        elem['thumbnail_source'] = 'https://2ch.hk{}'.format(elem['thumbnail'])

    logging.debug("Finding webms inf files: complete.")
    return result


def find_threads_by_word_in_comments(with_words=(), without_words=()):
    """
    This function returns threads which have words_to_find in their head post

    :param without_words: list of words to ban
    :param with_words: list of world to find
    :return:
    """
    logging.debug("Finding thread by word in comments(word_to_find={}).".format(with_words))

    logging.debug("Getting response from {}".format(CATALOG_URL))
    #response = urllib2.urlopen(CATALOG_URL)
    catalog = json.loads(_download_from_url(CATALOG_URL).decode('utf-8'))

    threads_with_words = _get_threads_with_word_in_comments(catalog['threads'], words=with_words)
    threads_without_words = _get_threads_without_word_in_comments(threads_with_words, words=without_words)

    result = _get_links_from_thread_dicts(threads_without_words)

    logging.debug("Finding thread by word in comments: complete.")
    return result


def _get_threads_with_word_in_comments(all_threads, words=()):
    logging.debug("Getting thread with words({}).".format(words))

    if not words:
        return all_threads

    result = []
    for thread in all_threads:
        lower_comment = thread['comment'].lower()
        if any(map(lambda x: x in lower_comment, words)):
            result.append(thread)

    logging.debug("Getting thread with words: complete.")
    return result


def _get_threads_without_word_in_comments(all_threads, words=()):
    logging.debug("Getting thread without words({}).".format(words))

    if not words:
        return all_threads

    result = []
    for thread in all_threads:
        lower_comment = thread['comment'].lower()
        if not any(map(lambda x: x in lower_comment, words)):
            result.append(thread)

    logging.debug("Getting thread without words: complete.")
    return result


def _get_links_from_thread_dicts(all_threads):
    return ["https://2ch.hk/b/res/{}.json".format(thread['num']) for thread in all_threads]



def find_files_in_threads(threads_url):
    """
    This function returns all files found in threads

    :param threads_url: threads url
    :return:
    """

    logging.debug("Finding files in threads({})".format(threads_url))

    result = []
    for thread_url in threads_url:
        result.extend(_find_files_in_thread(thread_url))

    logging.debug("Finding files in threads: complete.")
    return result


def _find_files_in_thread(thread_url):
    """
    This function returns all files found in one thread

    :param thread_url:
    :return:
    """

    logging.debug("Finding files in thread({})".format(thread_url))

    logging.debug("Getting response from {}.".format(thread_url))
    response = urllib2.urlopen(thread_url)
    thread = json.loads(response.read().decode('utf-8'))

    logging.debug("Finding files in response.")
    result = []
    for post in filter(lambda x: x['files'], thread['threads'][0]['posts']):
        founded_files = post['files']
        result.extend(founded_files)
        logging.debug("Files found: {}".format(founded_files))

    logging.debug("Finding files in thread: complete.")
    return result


def _download_from_url(url):
    logging.debug("Downloading from {}.".format(url))

    r = Request(url=url)
    result = urlopen(r).read()

    logging.debug("Downloading from: complete.")
    return result


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


if __name__ == '__main__':
    threads = find_threads_by_word_in_comments()
    files = find_files_in_threads(threads)