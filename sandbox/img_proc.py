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

#Mkdir
if not os.path.exists(flist + "Cropped"):
    os.mkdir(flist + "Cropped")

#Check cropped dir list file
clist = str(QFileDialog.getExistingDirectory(None,"Select crop folder")) + "/"
cname = QDir(clist)

#cimg = cname.entryList(["*.jpg","*.png"], QDir.Files, QDir.Name)

#Crop image and save new point position
"""""" 
for i in range(len(limg)):
#for i in range(2,3):
    #print("Read point " + str(i))
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
    #raw = tuple(map(tuple,raw))

    _x = []
    _y = []

    for x in range(68):
        _x.append(raw[x][0])
        _y.append(raw[x][1])

    #Bounding box
    min_x, max_x = min(_x),max(_x)
    min_y, max_y = min(_y),max(_y)

    print("Read img " + str(limg[i]))
    img = cv2.imread(flist+limg[i])
    #print(img.shape)

    if (min_x-10 <= 0 or min_y-10 <= 0
        or max_x >= img.shape[1] or max_y >= img.shape[0]):
        continue

    #print("Crop img")
    #Crop
    img = img[min_y-10:max_y+10, min_x-10:max_x+10]
    #print(img.shape)

    #print("Resize img")
    #Resize
    r = 100.0 / img.shape[1]
    dim = (100, int(img.shape[0]*r))

    crop = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    #print("Save img")
    #Save img
    cv2.imwrite(clist + str(limg[i]), crop)

    #Calculate new point
    for x in range(68):
        _x[x] -= (min_x-10)
        _x[x] *= r
        _y[x] -= (min_y-10)
        _y[x] *= r
        raw[x][0] = _x[x]
        raw[x][1] = _y[x]

    #print("Write point")
    #Save point
    cimg = cname.entryList(["*.jpg","*.png"], QDir.Files, QDir.Name)
    with open(clist + str(cimg[-1])[:-4] + ".pts",'w') as fout:
        data = "version: 1\nn_points: 68\n{\n"
        for x in range(68):
            data += str(raw[x][0])
            data += " "
            data += str(raw[x][1])
            data += "\n"
        data += "}"
        fout.write(data)
        fout.close()

    """
    traw = tuple(map(tuple,raw))
    
    img = cv2.imread(clist+cimg[i])
    
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
    cv2.waitKey(0)
    """
    
""""""
print("DONE")
