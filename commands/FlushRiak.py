from __future__ import print_function
import riak
from flask.ext.script import Command

class FlushRiak(Command):
    "Flushes all the keys in the default bucket. Might not work with large buckets"
    riak_handle = riak.RiakClient(pb_port=8087, protocol='pbc')
    riak_bucket = riak_handle.bucket('default')

    def run(self):
        for keys in self.riak_bucket.stream_keys():
            for key in keys:
                print('Deleting %s' % key)
                self.riak_bucket.delete(key)