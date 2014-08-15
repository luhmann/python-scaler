from __future__ import division
from PIL import Image
import settings


class Scaler:
    def __init__(self, riak_image, width):
        self.riak_image = riak_image
        self.source = Image.open(self.riak_image.img_binary)
        self.target_size = (width, None)

        self.src_aspect_ratio = self.source.size[0] / self.source.size[1]


    def scale(self):
        """Scales an image according to its original aspect ratio"""
        self.__calc_target_height()
        self.__calc_size_by_bounding_box()

        self.source.thumbnail(self._new_size)
        return self.source

    def crop(self, aspect_ratio):
        """Scales an image by its original aspect ratio to the desired width, then crops it to the box
        defined by the passed aspect_ratio"""
        self.__calc_target_height(aspect_ratio)
        self.__calc_size_by_aspect_ratio()

        self.source.thumbnail(self._new_size)
        return self.source.crop(self.__calc_crop_position())

    def letterbox(self, aspect_ratio):
        """Scales an image to a size so that fits into the box defined by width * aspect_ratio. then positions
        the scaled image centered into the target image with a black background"""
        self.__calc_target_height(aspect_ratio)
        self.__calc_size_by_bounding_box()

        self.source.thumbnail(self._new_size)
        output_size = (self.target_size[0], self.target_size[1])
        background = Image.new('RGBA', output_size, settings.LETTERBOX_BG)
        background.paste(self.source, (
            int((output_size[0] - self.source.size[0]) / 2),
            int((output_size[1] - self.source.size[1]) / 2))
        )
        return background

    def __calc_size_by_bounding_box(self):
        new_width = None
        new_height = None

        if self.src_aspect_ratio > 1:
            new_width = self.target_size[0]
            new_height = self.__calc_height(new_width, self.src_aspect_ratio)

            if new_height > self.target_size[1]:
                new_height = self.target_size[1]
                new_width = self.__calc_width(new_height, self.src_aspect_ratio)

        elif self.src_aspect_ratio <= 1:
            new_height = self.target_size[1]
            new_width = self.__calc_width(new_height, self.src_aspect_ratio)

            if new_width > self.target_size[0]:
                new_width = self.target_size[0]
                new_height = self.__calc_height(new_width, self.src_aspect_ratio)

        self._new_size = (int(new_width), int(new_height))

    def __calc_target_height(self, target_aspect_ratio=None):
        if not target_aspect_ratio:
            target_aspect_ratio = self.src_aspect_ratio

        self.target_size = (self.target_size[0], self.__calc_height(self.target_size[0], target_aspect_ratio))

    def __calc_size_by_aspect_ratio(self):
        self._new_size = (self.target_size[0], self.__calc_height(self.target_size[0], self.src_aspect_ratio))

    def __calc_crop_position(self):
        left = int((self._new_size[0] - self.target_size[0]) / 2)
        right = self.source.size[0] - left
        top = int((self._new_size[1] - self.target_size[1]) / 2)
        bottom = self.source.size[1] - top

        return left, top, right, bottom

    @staticmethod
    def __calc_width(height, aspect_ratio):
        return int(height * aspect_ratio)

    @staticmethod
    def __calc_height(width, aspect_ratio):
        return int(width / aspect_ratio)