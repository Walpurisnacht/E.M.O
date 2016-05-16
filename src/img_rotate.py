from math import *
import cv2
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from affine import Affine as af

def execute(flag=False):
    #Init GUI
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
            print("Read img " + str(limg[i]))
            print("Read point " + str(i))

        #Read image
        img = cv2.imread(flist+limg[i])
        (h,w) = img.shape[:2]


        #Read .csv file
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

        # if flag:
        #     imgview(img, raw, "ORIGINAL")

        #Rotate picture to balance #31 #35 point
        angle = getAngle(_y[31], _x[31], _y[35], _x[35])
        if flag:
            print("Rotate: " + str(angle))

        M = cv2.getRotationMatrix2D((w/2,h/2), angle, 1.0)
        img = cv2.warpAffine(img, M, (w,h))

        # if angle > 180.0:
        #     continue

        #Update pts
        for x in range(68):
            pts = af.rotation(-angle,pivot=(w/2,h/2)) * (_x[x],_y[x])
            raw[x][0] = pts[0]
            raw[x][1] = pts[1]
            _x[x] = raw[x][0]
            _y[x] = raw[x][1]

        # if flag:
        #     imgview(img, raw, "ROTATE")

        #Face bounding box
        min_x, max_x = min(_x),max(_x)
        min_y, max_y = min(_y),max(_y)

        if (min_x-10 <= 0 or min_y-10 <= 0
            or max_x >= img.shape[1] or max_y >= img.shape[0]):
            continue

        #Cropping and resize image
        img = img[min_y-10:max_y+10, min_x-10:max_x+10]
        ratio = 100.0 / img.shape[1]
        dim = (100, int(img.shape[0]*ratio))

        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        #Save img
        cv2.imwrite(clist + str(limg[i]), img)

        #Update pts
        for x in range(68):
            _x[x] -= (min_x - 10)
            _x[x] *= ratio
            _y[x] -= (min_y - 10)
            _y[x] *= ratio
            raw[x][0] = _x[x]
            raw[x][1] = _y[x]

        if flag:
            imgview(img, raw, "CROPPED")

        #Write pts
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
    print("DONE")

def imgview(img,raw,_log):
    raw = tuple(map(tuple,raw.astype(int)))

    # print(raw)

    # (h, w) = img.shape[:2]
    # center = (w / 2, h / 2)
    #
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
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

    cv2.imshow(_log, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# def angle_trunc(a):
#     while a < 0.0:
#         a += pi * 2
#     return a

def getAngle(x_ori, y_ori, x_lan, y_lan):
    dX = y_lan - y_ori
    dY = x_lan - x_ori
    #return degrees(angle_trunc(atan2(dY,dX)))
    return degrees(atan2(dY, dX))

execute(False)