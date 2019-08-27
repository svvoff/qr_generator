import random

class TextProvider:
    read = 0

    textFile = open("./war.txt", "r")
    text = textFile.read()
    textFile.close()

    def get_text(self):
        length = random.randrange(20, 800)  # 20 -> 800
        qr_string = self.text[self.read: length + self.read]
        self.read += length
        if len(qr_string) < length:
            self.read = 0
        return qr_string