import numpy as np
import cv2
from itertools import islice
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import sys

app = QApplication([])

#Check original dir list file
flist = str(QFileDialog.getExistingDirectory(None,"Select img folder")) + "/"
fname = QDir(flist)

limg = fname.entryList(["*.jpg","*.png"], QDir.Files, QDir.Name)
lann = fname.entryList(["*.pts"], QDir.Files, QDir.Name)

for i in range(len(limg)):
    lines = open(flist+lann[i]).read().split("\n")
    lines = lines[3:71]

    raw = np.array(np.fromstring(lines[0], sep=" "))

    for x in lines[1:]:
        try:
            x1 = np.fromstring(x, sep=" ")
            raw = np.vstack((raw,x1))
        except:
            pass

    raw = raw.astype(int)
    traw = tuple(map(tuple,raw))

    img = cv2.imread(flist+limg[i])

    for x in range(1,17):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)

    for x in range(28,31):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)

    for x in range(18,22):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)

    for x in range(23,27):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)

    for x in range(31,36):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)
    cv2.line(img, traw[30], traw[35], (0,255,0), 1)

    for x in range(37,42):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)
    cv2.line(img, traw[36], traw[41], (0,255,0), 1)

    for x in range(43,48):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)
    cv2.line(img, traw[42], traw[47], (0,255,0), 1)
    
    for x in range(49,60):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)
    cv2.line(img, traw[48], traw[59], (0,255,0), 1)
    
    for x in range(61,68):
        cv2.line(img, traw[x], traw[x-1], (0,255,0), 1)
    cv2.line(img, traw[60], traw[67], (0,255,0), 1)
    
    cv2.imshow("Image",img)
    cv2.waitKey(200)
    cv2.destroyAllWindows()
