import os
import errno
from os import listdir
from os.path import isfile, join

import numpy
from PIL import Image, ImageColor

from qrcreater import create_qr
from text_provider import TextProvider
import random


class Outputter:
    # angle = 0
    onlyfiles = [f for f in listdir("backgrounds") if isfile(
        join("backgrounds", f)) and f.endswith(('jpg', 'JPG'))]

    textProvider = TextProvider()

    def start(self):
        from PIL import ImageFilter
        data = {
            "train":    150000,
            "val":      40000,
            "test":     40000
        }
        for key, number in data.items():
            bound = number
            for i in range(0, bound):
                text = self.textProvider.get_text()
                index = random.randrange(0, len(self.onlyfiles))
                if index >= len(self.onlyfiles):
                    index = 0
                background_name = self.onlyfiles[index]
                background = Image.open("backgrounds/" + background_name, "r")
                average_color = background.resize(
                    (1, 1), Image.ANTIALIAS).getpixel((0, 0))
                if not isinstance(average_color, tuple) or (isinstance(average_color, tuple) and len(average_color) > 3):
                    print("can not to find average color in image named: " +
                        background_name + " under number: " + str(i))
                    # set background color from unreaded qr
                    average_color = ImageColor.getrgb('rgb(182,182,174)')

                img = create_qr(text, average_color)

                blureValue = random.randrange(0, 3)
                bluredImage = img.filter(ImageFilter.GaussianBlur(blureValue))
                width, height = img.size

                file_number = self.number_string(i, bound)
                file_name = 'qr_' + file_number + ".jpg"

                result = Image.new('RGBA', (width * 2, height))
                result.paste(img, (width, 0))
                result.paste(bluredImage, (0, 0))
                result = result.convert('RGB')
                path = 'output/' + key + "/"
                try:
                    os.makedirs(path)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                result.save(path + file_name, format="JPEG")

                print("\t" + key + " done: " + file_number + '/' + str(bound), end="", flush=True)
                if i != bound - 1:
                    backline()
                else:
                    print("\n")

           # self.angle += 1

    def number_string(self, number, bound):
        string = str(number)
        bound_string = str(bound)
        dif = len(bound_string) - len(string)
        if dif > 0:
            for i in range(0, dif + 1):
                string = "0" + string

        return string

def backline():        
    print('\r', end='')
