from models import RiakImage
import requests
import settings
import base64
from io import BytesIO
from werkzeug.exceptions import HTTPException, NotFound

class ImageGetter:
    def __init__(self, key=None):
        if not key or not isinstance(key, basestring):
            raise ValueError('Passed key must be a valid string')

        self.key = key

    def query_riak(self):
        url = self.__build_url()
        r = requests.get(url)

        if r.status_code == 200 and r.headers['content-type'] == 'application/json':
            return r.json()
        elif r.status_code == 404:
            raise NotFound
        else:
            raise HTTPException

    def get(self):
        img_json = self.query_riak()
        img_binary = self.__decode_img_binary(img_json['imageBinary'])
        img_json.pop('imageBinary')

        return RiakImage(img_binary, img_json)

    def __build_url(self):
        return 'http://%s:%s/riak/%s' % (settings.RIAK_HOST, settings.RIAK_PORT, self.key)

    @staticmethod
    def __decode_img_binary(b64_string):
        try:
            return BytesIO(base64.b64decode(b64_string))
        except TypeError:
            raise HTTPException