#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from datetime import datetime
import logging
from .video_handler_module import download_and_save_all_new_videos_2ch_b, delete_all_videos_by_added_date
from deadsource.models import BotTask
import json

class ThreadDownloader(object):
    class __ThreadDownloader(threading.Thread):
        def __init__(self,
                     is_max_iter=False,
                     is_max_time=False,
                     max_working_iter=1,
                     max_working_time=1,
                     interval=5):
            threading.Thread.__init__(self)
            self.is_working = False
            self.is_ready_for_work = True
            self.is_max_iter = is_max_iter
            self.is_max_time = is_max_time
            self.max_working_iter = max_working_iter
            self.max_working_time = max_working_time
            self.interval = interval
            self.iters_done = 0
            self.created_date = datetime.now()
            self.started_date = None
            self.last_iter = None
            self.last_thread = None

        def __str__(self):
            return repr(self) + str(self.is_working)

        def run(self, *args):
            logging.debug('Bot(downloader):started!'.format(self.iters_done))

            self.is_ready_for_work = False
            self.started_date = datetime.now()
            self.iters_done = 0
            self.is_working = True

            while self.is_working:
                self.last_iter = datetime.now()
                self.iters_done += 1

                try:
                    download_and_save_all_new_videos_2ch_b()
                except Exception as e:
                    logging.critical('Bot(remover): Error on {} iter: {}.'.format(self.iters_done, e))

                logging.debug('Bot(downloader):{} iter done!'.format(self.iters_done))

                sleep_time = self.interval - (datetime.now() - self.last_iter).seconds
                if sleep_time > 0:
                    time.sleep(self.interval - (datetime.now() - self.last_iter).seconds)

                if self.is_max_iter \
                        and self.max_working_iter < self.iters_done:
                    self.is_working = False
                if self.is_max_time \
                        and self.max_working_time < (datetime.now() - self.started_date).seconds:
                    self.is_working = False

            self.is_ready_for_work = True
            logging.debug('Bot(downloader):stopped!'.format(self.iters_done))

        def stop_iter(self):
            self.is_working = False

        def stop_iter_and_wait_bot_ready(self):
            self.stop_iter()

            while not self.last_thread.is_alive():
                time.sleep(0.1)

    instance = None

    def start(self):
        if self.instance.last_thread and self.instance.last_thread.is_alive():
            raise BotIsBusy

        thread = threading.Thread(target=self.instance.run, args=(self.instance,))
        self.instance.last_thread = thread
        thread.start()

    def stop(self, is_wait=False):
        if is_wait:
            self.instance.stop_iter_and_wait_bot_ready()
        else:
            self.instance.stop_iter()

    def __init__(self, **kwargs):
        if not ThreadDownloader.instance:
            ThreadDownloader.instance = ThreadDownloader.__ThreadDownloader(**kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class VideoRemover(object):
    class __VideoRemover(threading.Thread):
        def __init__(self,
                     is_max_iter=False,
                     is_max_time=False,
                     max_working_iter=1,
                     max_working_time=1,
                     interval=5):
            threading.Thread.__init__(self)
            self.is_working = False
            self.is_ready_for_work = True
            self.is_max_iter = is_max_iter
            self.is_max_time = is_max_time
            self.max_working_iter = max_working_iter
            self.max_working_time = max_working_time
            self.interval = interval
            self.iters_done = 0
            self.created_date = datetime.now()
            self.started_date = None
            self.last_iter = None
            self.last_thread = None

        def __str__(self):
            return repr(self) + str(self.is_working)

        def run(self, *args):
            logging.debug('Bot(remover):started!'.format(self.iters_done))
            self.is_ready_for_work = False
            self.started_date = datetime.now()
            self.iters_done = 0
            self.is_working = True

            while self.is_working:
                self.last_iter = datetime.now()
                self.iters_done += 1

                try:
                    delete_all_videos_by_added_date(ignore_time=60 * 60 * 48)
                except Exception as e:
                    logging.critical('Bot(remover): Error on {} iter: {}.'.format(self.iters_done, e))

                logging.debug('Bot(remover):{} iter done!'.format(self.iters_done))
                time.sleep(self.interval - (datetime.now() - self.last_iter).seconds)

                if self.is_max_iter \
                        and self.max_working_iter < self.iters_done:
                    self.is_working = False
                if self.is_max_time \
                        and self.max_working_time < (datetime.now() - self.started_date).seconds:
                    self.is_working = False

            self.is_ready_for_work = True
            logging.debug('Bot(remover):stopped!'.format(self.iters_done))

        def stop_iter(self):
            self.is_working = False

        def stop_iter_and_wait_bot_ready(self):
            self.stop_iter()

            while not self.last_thread.is_alive():
                time.sleep(0.1)

    instance = None
    last_thread = None

    def start(self):
        if self.instance.last_thread and self.instance.last_thread.is_alive():
            raise BotIsBusy

        thread = threading.Thread(target=self.instance.run, args=(self.instance,))
        self.instance.last_thread = thread
        thread.start()

    def stop(self, is_wait=False):
        if is_wait:
            self.instance.stop_iter_and_wait_bot_ready()
        else:
            self.instance.stop_iter()

    def __init__(self, **kwargs):
        if not VideoRemover.instance:
            VideoRemover.instance = VideoRemover.__VideoRemover(**kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class DeadBot(object):
    class __DeadBot(object):
        def __init__(self):
            pass

    instance = None
    last_thread = None

    def start(self):
        if self.instance.last_thread and self.instance.last_thread.is_alive():
            raise BotIsBusy

        thread = threading.Thread(target=self.instance.run, args=(self.instance,))
        self.instance.last_thread = thread
        thread.start()

    def create_task(self, task_description):
        pass

    def __init__(self, **kwargs):
        if not VideoRemover.instance:
            VideoRemover.instance = VideoRemover.__VideoRemover(**kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)


class Task(object):
    pass


def create_task():
    return bot_task_1


def bot_task_1(stop_event=threading.Event(),
               pause_event=threading.Event(),
               task_started_event=threading.Event(),
               task_collecting_videos_event=threading.Event(),
               task_waiting_nex_iter_event=threading.Event(),
               task_paused_event=threading.Event(),
               task_stopped_event=threading.Event(),
               is_max_time=False,
               is_max_iter=False,
               interval=10,
               iters_to_do=1,
               working_time=0,
               with_words=(u'вебм', 'webm'),
               without_words=('fap', u'музыкальный'),
               max_videos_count=None,
               is_music=False,
               is_adult=False,
               is_webm=False,
               is_hot=False,
               is_mp4=False,
               **kwargs):
    logging.debug('Task(download):started!')

    started_date = datetime.now()
    task_started_event.set()
    while True:
        last_iter = datetime.now()

        if is_max_iter and iters_to_do <= 0:
            break
        if is_max_time and working_time < (datetime.now() - started_date).seconds:
            break
        if pause_event.isSet():
            task_paused_event.set()
            pause_event.wait()
            task_paused_event.clear()
        if stop_event.isSet():
            break

        task_collecting_videos_event.set()

        try:
            download_and_save_all_new_videos_2ch_b(with_words=with_words,
                                                   without_words=without_words,
                                                   max_videos_count=max_videos_count,
                                                   is_music=is_music,
                                                   is_adult=is_adult,
                                                   is_webm=is_webm,
                                                   is_hot=is_hot,
                                                   is_mp4=is_mp4,
                                                   exit_event=stop_event)

        except Exception as e:
            logging.critical('Task(download): Error: {}.'.format(e))

        task_collecting_videos_event.clear()

        logging.debug('Task(download):{} iter done!')
        iters_to_do -= 1

        if is_max_iter and iters_to_do <= 0:
            break
        if is_max_time and working_time < (datetime.now() - started_date).seconds:
            break
        if pause_event.isSet():
            task_paused_event.set()
            pause_event.wait()
            task_paused_event.clear()
        if stop_event.isSet():
            break

        task_waiting_nex_iter_event.set()
        sleep_time = interval - (datetime.now() - last_iter).seconds
        if sleep_time > 0:
            time.sleep(interval - (datetime.now() - last_iter).seconds)
        task_waiting_nex_iter_event.clear()

    task_stopped_event.set()
    logging.debug('Task(download):stopped!')


def bot_task_2(stop_event=threading.Event(),
               pause_event=threading.Event(),
               task_started_event=threading.Event(),
               task_collecting_videos_event=threading.Event(),
               task_waiting_nex_iter_event=threading.Event(),
               task_paused_event=threading.Event(),
               task_stopped_event=threading.Event(),
               is_max_time=False,
               is_max_iter=False,
               ignore_time=None,
               interval=10,
               iters_to_do=1,
               working_time=0,
               max_videos_count=None,
               is_adult=False,
               is_webm=False,
               is_hot=False,
               is_mp4=False,
               **kwargs):
    logging.debug('Task(download):started!')

    started_date = datetime.now()
    task_started_event.set()
    while True:
        last_iter = datetime.now()

        if is_max_iter and iters_to_do <= 0:
            break
        if is_max_time and working_time < (datetime.now() - started_date).seconds:
            break
        if pause_event.isSet():
            task_paused_event.set()
            pause_event.wait()
            task_paused_event.clear()
        if stop_event.isSet():
            break

        task_collecting_videos_event.set()

        try:
            delete_all_videos_by_added_date(ignore_time=ignore_time,
                                            max_videos_count=max_videos_count,
                                            exit_event=stop_event,
                                            is_adult=is_adult,
                                            is_webm=is_webm,
                                            is_hot=is_hot,
                                            is_mp4=is_mp4,
                                            )

        except Exception as e:
            logging.critical('Task(download): Error: {}.'.format(e))

        task_collecting_videos_event.clear()

        logging.debug('Task(download):{} iter done!')
        iters_to_do -= 1

        if is_max_iter and iters_to_do <= 0:
            break
        if is_max_time and working_time < (datetime.now() - started_date).seconds:
            break
        if pause_event.isSet():
            task_paused_event.set()
            pause_event.wait()
            task_paused_event.clear()
        if stop_event.isSet():
            break

        task_waiting_nex_iter_event.set()
        sleep_time = interval - (datetime.now() - last_iter).seconds
        if sleep_time > 0:
            time.sleep(interval - (datetime.now() - last_iter).seconds)
        task_waiting_nex_iter_event.clear()

    task_stopped_event.set()
    logging.debug('Task(download):stopped!')



class BotIsBusy(Exception):
    pass


class TaskThread(threading.Thread):
    STATUS_WORKING = 'working'
    STATUS_PAUSED = 'paused'
    STATUS_STOPPED = 'stopped'

    PROCESS_STATUS_RESTING = 'resting'
    PROCESS_STATUS_COLLECTING = 'working'
    PROCESS_STATUS_WAITING = 'waiting'

    def __init__(self, name, target, data):
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.task_started_event = threading.Event()
        self.task_collecting_videos_event = threading.Event()
        self.task_waiting_nex_iter_event = threading.Event()
        self.task_paused_event = threading.Event()
        self.task_stopped_event = threading.Event()
        events = {
            'stop_event': self.stop_event,
            'pause_event': self.pause_event,
            'task_started_event': self.task_started_event,
            'task_collecting_videos_event': self.task_collecting_videos_event,
            'task_waiting_nex_iter_event': self.task_waiting_nex_iter_event,
            'task_paused_event': self.task_paused_event,
            'task_stopped_event': self.task_stopped_event,
        }
        data.update(events)
        threading.Thread.__init__(self, name=name, target=target, kwargs=data)

    def stop(self):
        self.stop_event.set()

    def pause_on(self):
        self.pause_event.set()

    def pause_off(self):
        self.pause_event.clear()

    def get_status(self):
        if self.stop_event.isSet() or not self.task_started_event.isSet():
            return self.STATUS_STOPPED
        if self.pause_event.isSet():
            return self.STATUS_PAUSED
        return self.STATUS_WORKING

    def get_process_status(self):
        if self.task_paused_event.isSet() or self.task_stopped_event.isSet() or not self.task_started_event.isSet():
            return self.PROCESS_STATUS_RESTING
        if self.task_collecting_videos_event.isSet():
            return self.PROCESS_STATUS_COLLECTING
        return self.PROCESS_STATUS_WAITING



