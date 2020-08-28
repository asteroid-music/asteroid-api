from flask import g
from rethinkdb import r

from asteroid_flask.services.request_services.yt_dl import RequestYT

class Requester():

    def __init__(self, url):
        self.url = url
        self.song = {}

    def _is_duplicate(self):
        """ checks if the song already exists in the database
            naively does this by seeing if url is duplicate """
        res = r.table('music').filter(lambda doc:
            doc['url'] == self.url
        ).run(g.get_conn())
        if len(list(res)) > 1:
            return True
        else:
            return False

    def fetch(self):
        """ assume everything is youtube for now """
        if self._is_duplicate():
            return "duplicate"

        ryt = RequestYT()
        self.song = ryt.download(self.url)

        if ryt.status != 'done':
            return ryt.status
        else:
            print(self._add_to_database())
            return 'done'


    def _add_to_database(self):
        """ adds the song to the song database and extends the
            song dictionary with the returned id """
        info = r.table('music').insert(
            self.song
        ).run(g.get_conn())
        self.song['id'] = info['generated_keys'][0]


# check FFMPEG is native
import subprocess
try: 
    subprocess.run(['ffmpeg', '-h'], check=True, capture_output=True)
except Exception as e:
    print(e)
    print("NO NATIVE FFMPEG; QUITTING!")
    exit(1)

