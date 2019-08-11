import qrcode
from imageFactory import ImageFactory

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

