import threading
import time
from datetime import datetime
import logging
from video_handler_module import download_and_save_all_new_videos, delete_all_videos_by_added_date


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
                    download_and_save_all_new_videos()
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
                    delete_all_videos_by_added_date(added_date=60*60*48)
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


class BotIsBusy(Exception):
    pass