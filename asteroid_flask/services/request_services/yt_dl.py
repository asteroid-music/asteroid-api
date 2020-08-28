from __future__ import unicode_literals
import json
import subprocess
import os

from flask import current_app

import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'prefer_ffmpeg': True,
    'postprocessor': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'forcetitle': True,
    'quiet': True,
    # 'forcejson': True,
    'forcefilename': True,
    'forceduration': True,
    'restrictfilenames': True,
    'noplaylist': True
}

class RequestYT():

    def __init__(self):
        self.ydl_opts = {
            **ydl_opts,
            'logger': current_app.logger,
            'progress_hooks': [self._proxy_hook],
            'outtmpl': current_app.config["MUSIC_DIR"] + '/%(title)s.%(ext)s'
        }

        self.title = ""
        self.duration = 0
        self.file_name = ""
        self.artist = ""
        self.album = ""

        self.status = "init"

    def _proxy_hook(self, data):
        """ callback for youtube-dl once download is finished """
        self.status = data['status']
        self.file_name = data['filename']

    def _post_process(self):
        """ use native ffmpeg to convert file to mp3 """
        filename, _ = os.path.splitext(self.file_name)
        new_filename = filename + '.mp3'
        subprocess.run(
            ['ffmpeg', '-i', self.file_name, new_filename, '-y']
        )
        os.remove(self.file_name)
        self.file_name = new_filename

    def _encode_info(self, track=None, artist=None, album=None, **kwargs):
        """ extract song, artist, album, else use defaults """
        if track is not None:
            self.title = track
        if artist is not None:
            self.artist = artist
        else:
            # use uploader
            self.artist = kwargs['uploader']
        if album is not None:
            self.album = album
        else:
            # default to youtube
            self.album = 'youtube'

    def download(self, url):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True, process=True)
        except youtube_dl.utils.ExtractorError as e:
            self.status = "extractError"
            return {}
        except youtube_dl.utils.DownloadError as e:
            self.status = "downloadError"
            return {}
        except Exception as e:
            urrent_app.logger.error(e)

        else:
            # youtube-dl post processor doesn't always seem to work
            if self.file_name[-3:] != 'mp3':
                self._post_process()

            self.title = info['title']
            self.duration = info['duration']

            self._encode_info(**info)

            self.status = 'done'
            return {
                'song': self.title,
                'file': self.file_name,
                'duration': self.duration,
                'artist': self.artist,
                'album': self.album,
                'url': url
            }
