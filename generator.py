import qrcode
import random
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageDraw
import numpy

class ImageFactory(qrcode.image.base.BaseImage):
    """
    PIL image builder, default format is PNG.
    """
    kind = "PNG"

    def new_image(self, **kwargs):
        back_color = kwargs.get("back_color", "white")
        fill_color = kwargs.get("fill_color", "black")

        img = Image.new("RGBA", (self.pixel_size, self.pixel_size), back_color)
        self.fill_color = fill_color
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        box = self.pixel_box(row, col)
        self._idr.rectangle(box, fill=self.fill_color)

    def save(self, stream, format=None, **kwargs):
        if format is None:
            format = kwargs.get("kind", self.kind)
        if "kind" in kwargs:
            del kwargs["kind"]
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)


class TextProvider:
    read = 0

    textFile = open("war.txt", "r")
    text = textFile.read()
    textFile.close()

    def get_text(self):
        length = random.randrange(20, 800)  # 20 -> 800
        qr_string = self.text[self.read: length + self.read]
        self.read += length
        return qr_string





def create_qr(data, back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(image_factory=ImageFactory, fill_color="black", back_color=back_color)

class Outputter:
    angle = 0
    onlyfiles = [f for f in listdir("backgrounds") if isfile(join("backgrounds", f)) and f.endswith(('jpg', 'JPG'))]

    textProvider = TextProvider()

    avarage_colors = {}

    def start(self):
        from PIL import ImageFilter
        bound = 10
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
                average_color = background.resize((1, 1), Image.ANTIALIAS).getpixel((0, 0))

            background = background.convert('RGBA')

            img = create_qr(text, average_color)

            img = self.perspective(img)
            # blurValue = random.randrange(0, 2)
            # img = img.filter(ImageFilter.GaussianBlur(blurValue))
            img = img.rotate(self.angle, expand=1, fillcolor=None)

            dest = self.destination_point(background, img)

            background.alpha_composite(img, dest=dest)
            file_name = self.number_string(i, bound)
            result = background.convert('RGB')
            masked = self.masked_image(background, img, dest)
            result.save("./output/qr_" + file_name + ".image" + ".jpg", format="JPEG")
            masked.save("./output/qr_" + file_name + ".mask" + ".jpg", format="JPEG")
            self.angle += 1
            if self.angle > 360:
                self.angle = bound % 360

    def perspective(self, img):
        width, height = img.size
        m = 0.1
        xshift = abs(m) * width
        new_width = int(width - width / 5)
        coeffs = self.find_coeffs(
            [(0, 0), (256, 0), (256, 256), (0, 256)],
            [(0, 0), (256, 0), (new_width, height), (xshift, height)])
        return img.transform((width * 3, height * 3),
                                Image.PERSPECTIVE,
                                coeffs,
                                Image.BICUBIC)

    def find_coeffs(self, pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(pb).reshape(8)
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


Outputter().start()

