from __future__ import unicode_literals

import logging

from urllib2 import Request, urlopen

logger = logging.getLogger('deadtasks')


def download_and_save_file(download_url, path_to_save):
    logger.debug("Downloading and saving file (url={}, path to save={}).".format(download_url, path_to_save))

    byte_code = download_file_from_url(download_url)
    save_bytecode_to_file(byte_code, path_to_save)

    logger.debug("Downloading and saving file: complete.")


def download_file_from_url(download_url):
    logger.debug("Downloading file(byte_code) form {}.".format(download_url))

    request = Request(url=download_url)
    result = urlopen(request).read()

    logger.debug("Downloading file: complete.")
    return result


def save_bytecode_to_file(byte_code, path_to_save, save_format=None):
    logger.debug("Saving file(byte_code) to {}.".format(path_to_save))

    with open(path_to_save, str('wb')) as f:
        f.write(byte_code)

    logger.debug("Saving file(byte_code).")





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