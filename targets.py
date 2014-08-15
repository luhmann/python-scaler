from __future__ import division
from scaler import Scaler

class Target(object):
    def factory(key, width, riak_img):
        if key == 's':
            return ScaleTarget(riak_img, width)
        if key == 'c':
            return CropTarget(riak_img, width)
        if key == 'l':
            return LetterboxTarget(riak_img, width)
        else:
            raise ValueError('Invalid key passed')
    factory = staticmethod(factory)

    def convert(self):
        raise NotImplementedError('Please implement this method')


class DefaultTarget(Target):
    def __init__(self, riak_img, width):
        self.width = int(width)
        self.riak_img = riak_img
        self.scaler = Scaler(self.riak_img, self.width)

class ScaleTarget(DefaultTarget):
    def convert(self):
        return self.scaler.scale()

class CropTarget(DefaultTarget):
    aspect_ratio = 16/9
    def convert(self):
        return self.scaler.crop(self.aspect_ratio)

class LetterboxTarget(DefaultTarget):
    aspect_ratio = 16/9

    def convert(self):
        return self.scaler.letterbox(self.aspect_ratio)
