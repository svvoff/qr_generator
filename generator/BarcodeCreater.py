import barcode
from barcode.writer import ImageWriter
from barcode import generate
from PIL import Image, ImageColor
import random
import os

# print(barcode.PROVIDED_BARCODES)


def randomString(len=12):
    string = ""
    for i in range(len):
        string += str(random.randrange(0, 10))
    return string


def create_random_barcode(output, color='white', format='JPEG'):
    options = {
        'background': color,
        'format': format
    }
    
    try:
        os.makedirs(output)
    except OSError as e:
        if e.errno != 17:
            raise  # raises the error again
    generate('ean13', randomString(), writer=ImageWriter(), writer_options=options, output=output)


