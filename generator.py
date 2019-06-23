import qrcode
import random
from PIL import Image, ImageDraw

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


textProvider = TextProvider()


def create_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(image_factory=ImageFactory, fill_color="black", back_color="white")


for i in range(0, 10):
    text = textProvider.get_text()
    img = create_qr(text)
    angle = random.randrange(0, 360)
    img = img.rotate(angle, expand=1, fillcolor=None)
    img.save("" + str(i) + ".png")

