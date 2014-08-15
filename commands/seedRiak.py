from __future__ import print_function
from flask.ext.script import Command
from settings import APP_ROOT
from PIL import Image
import riak
import os
import json
import base64
import magic
import StringIO

class SeedRiak(Command):
    "Seeds the Riak server with some images"

    riak_handle = riak.RiakClient(pb_port=8087, protocol='pbc')
    riak_bucket = riak_handle.bucket('default')
    test_img_folder = os.path.join(APP_ROOT, 'test_img')

    def save_to_riak(self, key, json):
        img = self.riak_bucket.new(key, encoded_data=json)
        img.store()

    def run(self):
        for img in os.listdir(self.test_img_folder):

            # exclude system files
            if img.startswith('.'):
                continue

            img_path = os.path.join(self.test_img_folder, img)
            print('Uploading %s' % img_path)
            im = Image.open(img_path)
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(img_path)
            output = StringIO.StringIO()
            im.save(output, 'JPEG')
            json_repr = {
                'id': img,
                'title': img,
                'size': str(os.path.getsize(img_path)),
                'width': str(im.size[0]),
                'height': str(im.size[1]),
                'mimeType': mime_type,
                'imageBinary': base64.b64encode(output.getvalue()),
            }
            output.close()

            self.save_to_riak(img, json.dumps(json_repr))

