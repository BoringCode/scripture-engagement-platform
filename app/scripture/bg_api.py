import requests
import json
import app
from werkzeug.contrib.cache import SimpleCache

class BGAPI(object):

    # Timeout (in minutes)
    cache_timeout = 1440

    def __init__(self):
        self.cache = SimpleCache()
        with open(app.app.config["BG_API_KEY"], "r") as f:
            self.auth_params = json.load(f)

    def get(self, url_path, params={}):
        """Build a simple cache of the requested data"""
        rv = self.cache.get(url_path)
        if rv is None:
            params.update(self.auth_params)
            url = "https://api.biblegateway.com/3/" + url_path

            response = requests.get(url, params=params)
            if response.status_code != 200:
                request = response.request
                raise RuntimeError("{} request {} returned {}".format(request.method, request.url, response.status_code))
            rv = response.json()
            self.cache.set(url_path, rv, timeout=self.cache_timeout*60)
        return rv

    def list_translations(self):
        return self.get('bible')['data']

    def get_translation(self, xlation):
        return self.get('bible/{}'.format(xlation))['data'][0]

    def get_book_info(self, xlation, book_osis):
        all_books = self.get_translation(xlation)['books']
        for book in all_books:
            if book['osis'] == book_osis:
                return book
        raise RuntimeError("Invalid book {} in translation {}".format(book_osis, xlation))

    def get_passage(self, xlation, passage_osis):
        verse_json = self.get("bible/{}/{}".format(passage_osis, xlation))['data'][0]
        passage_json = verse_json['passages'][0]
        return {'reference': passage_json['reference'],
                'content': passage_json['content']}

