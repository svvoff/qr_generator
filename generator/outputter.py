from qrcreater import create_qr
import numpy
from text_provider import TextProvider
from os import listdir
from os.path import isfile, join
from PIL import Image
import random


class Outputter:
    angle = 0
    onlyfiles = [f for f in listdir("backgrounds") if isfile(
        join("backgrounds", f)) and f.endswith(('jpg', 'JPG'))]

    textProvider = TextProvider()

    avarage_colors = {}

    def start(self):
        from PIL import ImageFilter
        bound = 20000
        for i in range(0, bound):

            text = self.textProvider.get_text()
            index = i
            if index >= len(self.onlyfiles):
                index = i % len(self.onlyfiles)
            background_name = self.onlyfiles[index]
            background = Image.open("backgrounds/" + background_name, "r")
            average_color = None
            if background_name in self.avarage_colors.values():
                average_color = self.avarage_colors[background_name]
            else:
                average_color = background.resize(
                    (1, 1), Image.ANTIALIAS).getpixel((0, 0))

            background = background.convert('RGBA')

            img = create_qr(text, average_color)

            # img = self.perspective(img)
            blurValue = random.randrange(0, 2)
            img = img.filter(ImageFilter.GaussianBlur(blurValue))
            img = img.rotate(self.angle, expand=1, fillcolor=None)
            try:
                dest = self.destination_point(background, img)
                background.alpha_composite(img, dest=dest)
            except:
                print("fail with " + background_name)

            file_name = self.number_string(i, bound)
            result = background.convert('RGB')
            masked = self.masked_image(background, img, dest)
            result.save("./output/qr_" + file_name +
                        ".image" + ".jpg", format="JPEG")
            masked.save("./output/qr_" + file_name +
                        ".mask" + ".jpg", format="JPEG")
            self.angle += 1
            if self.angle > 360:
                self.angle = bound % 360

    def perspective(self, img):
        width, height = img.size
        m = 0.1
        xshift = width * m
        yshift = height * m
        new_width = width - xshift
        new_height = height - yshift
        coeffs = self.find_coeffs(
            [(0, 0), (width, 0), (width, height), (0, height)],
            [(0, 0), (width, yshift), (width, height), (0, height)])
        return img.transform((width, height),
                             Image.PERSPECTIVE,
                             coeffs,
                             Image.BICUBIC)

    def find_coeffs(self, source_coords, target_coords):
        matrix = []
        for s, t in zip(source_coords, target_coords):
            matrix.append([
                t[0], t[1], 1,
                0, 0, 0,
                -s[0]*t[0], -s[0]*t[1]
            ])
            matrix.append([
                0, 0, 0,
                t[0], t[1], 1,
                -s[1]*t[0], -s[1]*t[1]
            ])
        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(source_coords).reshape(8)
        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    def masked_image(self, result, qr, destination):
        mask = Image.new('RGBA', size=qr.size, color="red")
        masked = result.copy()
        masked.paste(mask, box=destination, mask=qr)
        return masked.convert('RGB')

    def number_string(self, number, bound):
        string = str(number)
        bound_string = str(bound)
        dif = len(bound_string) - len(string)
        if dif > 0:
            for i in range(0, dif + 1):
                string = "0" + string

        return string

    def destination_point(self, background, qr):
        qr_size = qr.size

        background_size = background.size
        x_bound = background_size[0] - qr_size[0]
        y_bound = background_size[1] - qr_size[1]
        dest = (random.randrange(0, x_bound), random.randrange(0, y_bound))
        return dest