import csv
import os

class CSVManager:

    fileName = 'output.csv'
    file

    def __init__(self):
        shouldAddTitles = True
        try:
            self.file = open(self.fileName, 'w')
            self.writer = csv.DictWriter(f=self.file, fieldnames=['image','id','name','xMin','xMax','yMin','yMax'])
            if shouldAddTitles:
                self.write(imageName='name', id='id', name='label', xMin='xMin', xMax='xMax', yMin='yMin', yMax='yMax')
        except IOError:
            print('can not open file: ' + self.fileName)
            
    
    def write(self, imageName, xMin, xMax, yMin, yMax, name='qr', id=1):
        self.writer.writerow({
            'image': imageName,
            'id': id,
            'name': name,
            'xMin': xMin,
            'xMax': xMax,
            'yMin': yMin,
            'yMax': yMax

        })
