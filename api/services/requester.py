import logging

logger = logging.getLogger(__name__)

from api.services.subservice.yt_dl import RequestYT


class Requester:
    def __init__(self, url):
        self.url = url
        self.song = {}

    def fetch(self):
        """ assume everything is youtube for now """
        ryt = RequestYT()
        self.song = ryt.download(self.url)

        if ryt.status != "done":
            return ryt.status
        else:
            return "done"


# check FFMPEG is native
import subprocess

try:
    subprocess.run(["ffmpeg", "-h"], check=True, capture_output=True)
except Exception as e:
    logger.error(e)
    logger.fatal("NO NATIVE FFMPEG; QUITTING!")
    exit(1)
