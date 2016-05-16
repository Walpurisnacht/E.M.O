from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

app = QApplication([])

label = QFileDialog.getOpenFileName(None, 'Open label')

lines = open(label).read().split("\n")

flist = str(QFileDialog.getExistingDirectory(None, 'Select folder')) + "/"
fname = QDir(flist)

limg = fname.entryList(["*.jpg","*.png"], QDir.Files, QDir.Name)

for x in range(len(lines)):
    lines[x] = lines[x][:-2].strip()

for line in lines:
    if not line in limg:
        print("Img missing " + line)

for line in limg:
    if not line in lines:
        print("Lbl missing " + line)
        line = line[:-4]
        #os.remove(flist+line+".jpg")
        #print("Removed " + flist+line+".jpg")
        #os.remove(flist+line+".pts")
        #print("Removed " + flist+line+".pts")
