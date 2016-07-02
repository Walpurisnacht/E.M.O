import os
import dlib
import glob
from skimage import io
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
from math import *
import numpy as np
from affine import Affine as af

# Extract facial landmark from image
def im_read():
    app = QApplication([])

    predictor_path = str(QFileDialog.getOpenFileName(None, 'Model'))
    faces_folder_path = str(QFileDialog.getExistingDirectory(None, 'Img'))

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    # win = dlib.image_window()

    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = io.imread(f)

        # win.clear_overlay()
        # win.set_image(img)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            #     k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            # print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
            #                                           shape.part(1)))

            # Draw the face landmarks on the screen.
            # win.add_overlay(shape)
            if len(dets) > 0:
                with open(f[:-4] + ".pts", 'w') as fout:
                    data = "version: 1\nn_points: 68\n{\n"
                    for x in range(68):
                        data += str(shape.part(x))[1:-1].replace(',', '')
                        if not x == 67:
                            data += "\n"
                    data += "}"
                    fout.write(data)
                    fout.close()
                print("Printed to" + f[:-4] + ".pts")


                # win.add_overlay(dets)
                # dlib.hit_enter_to_continue()

    print("PROCESS COMPLETED")

# Process image base on landmark position
def im_proc(flag=False):
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
        img = cv2.imread(flist+str(limg[i]))
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

def im_view(img,raw,_log):
    raw = tuple(map(tuple,raw.astype(int)))

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

def getAngle(x_ori, y_ori, x_lan, y_lan):
    dX = y_lan - y_ori
    dY = x_lan - x_ori
    #return degrees(angle_trunc(atan2(dY,dX)))
    return degrees(atan2(dY, dX))

# Feature extraction
def eccentricity_calc(a, b):
    return np.sqrt(abs(a * a - b * b)) / a

def linear_calc_3(shape):
    res = []

    res.append((shape.part(37).y - shape.part(19).y) / (shape.part(8).y - shape.part(27).y))

    res.append((shape.part(51).y - shape.part(33).y) / (shape.part(8).y - shape.part(27).y))

    res.append((shape.part(57).y - shape.part(33).y) / (shape.part(8).y - shape.part(27).y))

    return res

def eccentricities_calc(shape):
    res = []

    # upper mouth 1
    res.append(eccentricity_calc((shape.part(54).x - shape.part(48).x) / 2,
                                 (shape.part(54).y - shape.part(48).y) / 2 - shape.part(51).y))

    # upper mouth 2
    res.append(eccentricity_calc((shape.part(54).x - shape.part(48).x) / 2,
                                 (shape.part(54).y - shape.part(48).y) / 2 - shape.part(62).y))

    # lower mouth 1
    res.append(eccentricity_calc((shape.part(54).x - shape.part(48).x) / 2,
                                 (shape.part(54).y - shape.part(48).y) / 2 - shape.part(66).y))

    # lower mouth 2
    res.append(eccentricity_calc((shape.part(54).x - shape.part(48).x) / 2,
                                 (shape.part(54).y - shape.part(48).y) / 2 - shape.part(57).y))

    # upper left eye
    res.append(eccentricity_calc((shape.part(39).x - shape.part(36).x) / 2,
                                 (shape.part(39).y - shape.part(36).y) / 2 - (shape.part(38).y + shape.part(37).y / 2)))

    # lower left eye
    res.append(eccentricity_calc((shape.part(39).x - shape.part(36).x) / 2,
                                 (shape.part(39).y - shape.part(36).y) / 2 - (shape.part(41).y + shape.part(40).y / 2)))

    # upper right eye
    res.append(eccentricity_calc((shape.part(45).x - shape.part(42).x) / 2,
                                 (shape.part(45).y - shape.part(42).y) / 2 - (shape.part(44).y + shape.part(43).y / 2)))

    # lower right eye
    res.append(eccentricity_calc((shape.part(45).x - shape.part(42).x) / 2,
                                 (shape.part(45).y - shape.part(42).y) / 2 - (shape.part(47).y + shape.part(46).y / 2)))

    # left eyebrown
    res.append(eccentricity_calc((shape.part(21).x - shape.part(17).x) / 2,
                                 (shape.part(21).y - shape.part(17).y) / 2 - shape.part(19).y))

    # right eyebrown
    res.append(eccentricity_calc((shape.part(26).x - shape.part(22).x) / 2,
                                 (shape.part(26).y - shape.part(22).y) / 2 - shape.part(24).y))

    return res

def feature_calc(shape):
    res = []

    # open mouth
    res.append((shape.part(57).y - shape.part(51).y) / (shape.part(54).x - shape.part(48).x))
    # open left eye
    res.append((shape.part(41).y - shape.part(37).y) / (shape.part(39).x - shape.part(36).x))
    # open right eye
    res.append((shape.part(47).y - shape.part(43).y) / (shape.part(45).x - shape.part(42).x))
    # distances
    vecaa = np.array([shape.part(54).x - shape.part(48).x, shape.part(54).y - shape.part(48).y])
    modulus_vecaa = np.sqrt(np.dot(vecaa, vecaa))
    vecbb = np.array([shape.part(57).x - shape.part(51).x, shape.part(57).y - shape.part(51).y])

    for i in range(0, 9):
        vec = np.array([shape.part(48).x - shape.part(i).x, shape.part(48).y - shape.part(i).y])
        modulus_vec = np.sqrt(np.dot(vec, vec))
        dot = np.dot(vec, vecaa)
        cos_angle = dot / modulus_vec / modulus_vecaa
        res.append(modulus_vec)
        res.append(cos_angle)

    for i in range(8, 17):
        vec = np.array([shape.part(54).x - shape.part(i).x, shape.part(54).y - shape.part(i).y])
        modulus_vec = np.sqrt(np.dot(vec, vec))
        dot = np.dot(vec, vecaa)
        cos_angle = dot / modulus_vec / modulus_vecaa
        res.append(modulus_vec)
        res.append(cos_angle)

    a = np.array([shape.part(48).x,shape.part(48).y])
    b = np.array([shape.part(51).x,shape.part(51).y])
    nvecaa = np.array([vecaa[1], -vecaa[0]])
    nvecbb = np.array([vecbb[1], -vecbb[0]])

    if nvecbb[0] == 0 and nvecbb[1] == 0:
        nvecbb = np.array((1, 0))

    c = np.dot(nvecaa, a)
    d = np.dot(nvecbb, b)
    matrix = np.matrix((nvecaa, nvecbb))
    free_col = np.matrix(([c], [d]))
    cross = np.linalg.inv(matrix) * free_col

    for i in range(48, 68):
        # print(cross)
        vec = np.array([cross.item(0) - shape.part(i).x, cross.item(1) - shape.part(i).y]) / modulus_vecaa
        modulus_vec = np.sqrt(np.dot(vec, vec))
        if modulus_vec == 0:
            modulus_vec = 1
        dot = np.dot(vec, vecaa)
        cos_angle = dot / modulus_vec / modulus_vecaa
        res.append(modulus_vec)
        res.append(cos_angle)

    res += eccentricities_calc(shape)
    res += linear_calc_3(shape)

    with open(sys.argv[1]) as fin:
        data = fin.read()
        ldata = np.fromstring(data, sep=",")

        for i in range(len(ldata)):
            res.append(res[i] - ldata[i])

    print("Size of feature: {}".format(len(res)))
    return res

# Dataset generator
def gen_train(path,label):
    res = ""
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(sys.argv[2])
    for f in glob.glob(os.path.join(path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = io.imread(f)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            #     k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            # print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
            #                                           shape.part(1)))
            val = feature_calc(shape)
            res += str(label) + ' '
            for x in range(1,len(val)+1):
                res += str(x) + ':' + str(val[x-1])
                if x != len(val):
                    res += ' '
                else:
                    res += '\n'
    with open(str(label)+'.csv','w') as fout:
        fout.write(res)