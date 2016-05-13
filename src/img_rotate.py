from math import *
import cv2
import numpy as np
from itertools import islice
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import sys
from affine import Affine as af

def execute(flag=False):
    app = QApplication([])

    flist = str(QFileDialog.getExistingDirectory(None,"Select img folder")) + "/"
    fname = QDir(flist)

    limg = fname.entryList(["*.jpg","*.png"], QDir.Files, QDir.Name)
    lann = fname.entryList(["*.pts"], QDir.Files, QDir.Name)

    if not os.path.exists(flist + "Processed"):
        os.mkdir(flist + "Processed")

    clist = str(QFileDialog.getExistingDirectory(None,"Select proc folder")) + "/"
    cname = QDir(clist)

    #Processing
    for i in range(len(limg)):
        if flag:
            print("Read point " + str(i))

        lines = open(flist + lann[i]).read().split("\n")
        lines = lines [3:71]

        raw = np.array(np.fromstring(lines[0], sep=" "))

        for x in lines[1:]:
            try:
                x1 = np.fromstring(x, sep=" ")
                raw = np.vstack((raw,x1))
            except:
                pass

        #raw = raw.astype(int)

        _x = []
        _y = []

        for x in range(68):
            _x.append(raw[x][0])
            _y.append(raw[x][1])

        angle = getAngle(_y[31], _x[31], _y[35], _x[35])

        if angle > 180.0:
            continue

        for x in range(68):
            _x[x] = _y[x]*sin(angle) + _x[x]*cos(angle)
            _y[x] = _y[x]*cos(angle) - _x[x]*sin(angle)
            raw[x][0] = _x[x]
            raw[x][1] = _y[x]

def imgview(path,raw,angle):
    raw = tuple(map(tuple,raw.astype(int)))

    print(raw)

    img = cv2.imread(path)

    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # img = cv2.warpAffine(img, M, (w, h))

    for x in range(1, 17):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)

    for x in range(28, 31):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)

    for x in range(18, 22):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)

    for x in range(23, 27):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)

    for x in range(31, 36):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)
    cv2.line(img, raw[30], raw[35], (0, 255, 0), 1)

    for x in range(37, 42):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)
    cv2.line(img, raw[36], raw[41], (0, 255, 0), 1)

    for x in range(43, 48):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)
    cv2.line(img, raw[42], raw[47], (0, 255, 0), 1)

    for x in range(49, 60):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)
    cv2.line(img, raw[48], raw[59], (0, 255, 0), 1)

    for x in range(61, 68):
        cv2.line(img, raw[x], raw[x - 1], (0, 255, 0), 1)
    cv2.line(img, raw[60], raw[67], (0, 255, 0), 1)

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





imgpath = "/media/DATA/Training/IBUG/image_007.jpg"
ptspath = "/media/DATA/Training/IBUG/image_007.pts"


def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return a

def getAngle(x_ori, y_ori, x_lan, y_lan):
    dX = y_lan - y_ori
    dY = x_lan - x_ori
    return degrees(angle_trunc(atan2(dY,dX)))

img = cv2.imread(imgpath)

lines = open(ptspath).read().split("\n")
lines = lines[3:71]

raw = np.array(np.fromstring(lines[0], sep=" "))

for x in lines[1:]:
    try:
        x1 = np.fromstring(x, sep=" ")
        raw = np.vstack((raw, x1))
    except:
        pass

_x = []
_y = []

for x in range(68):
    _x.append(raw[x][0])
    _y.append(raw[x][1])

angle = getAngle(_y[31], _x[31], _y[35], _x[35])
print(angle)

# for x in range(68):
#     pts = af.rotation(angle) * (_x[x],_y[x])
#     raw[x][0] = pts[0]
#     raw[x][1] = pts[1]

imgview(imgpath,raw,angle)

# (h,w) = img.shape[:2]
# center = (w/2, h/2)
#
# M = cv2.getRotationMatrix2D(center, angle, 1.0)
# fix = cv2.warpAffine(img, M, (w,h))
#
# cv2.imshow("Rotated",fix)
# cv2.waitKey(0)