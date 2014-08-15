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
    allowed_widths = []

    def __init__(self, riak_img, width):
        self.riak_img = riak_img
        self.width = self.validate_widths(width)
        self.scaler = Scaler(self.riak_img, self.width)

    def validate_widths(self, width):
        if width not in self.allowed_widths and width != '0' and width != 'unscaled':
            raise ValueError('You requested a width that is not allowed for this target')

        if width == '0' or width == 'unscaled':
            width = self.riak_img.width

        return int(width)


class ScaleTarget(DefaultTarget):
    allowed_widths = ['200', '400', '600', '800', '1400']

    def convert(self):
        return self.scaler.scale()


class CropTarget(DefaultTarget):
    allowed_widths = ['200', '400', '600', '800', '1400']
    aspect_ratio = 16/9

    def convert(self):
        return self.scaler.crop(self.aspect_ratio)


class LetterboxTarget(DefaultTarget):
    allowed_widths = ['200', '400', '600', '800', '1400']
    aspect_ratio = 16/9

    def convert(self):
        return self.scaler.letterbox(self.aspect_ratio)
