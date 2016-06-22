import cv2
import dlib
import sys
import glob
import os
import numpy as np
from skimage import io

import cProfile
import re
from line_profiler import LineProfiler


from svmutil import *

if (len(sys.argv) == 1):
    print("[app] [face] [neu] [svm] [img] [output] [label]")

# Convert dlib.dlib.point to tuple
def totuple(part):
    return (part.x,part.y)

# Return image overlayed with outline of the face features
# defined by the part locations
def draw_img(inimg,shape):
    img = inimg
    for x in range(1, 17):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    for x in range(28, 31):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    for x in range(18, 22):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    for x in range(23, 27):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    for x in range(31, 36):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    img = cv2.line(img, totuple(shape.part(30)), totuple(shape.part(35)), (0, 255, 0))
    for x in range(37, 42):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    img = cv2.line(img, totuple(shape.part(36)), totuple(shape.part(41)), (0, 255, 0))
    for x in range(43, 48):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    img = cv2.line(img, totuple(shape.part(42)), totuple(shape.part(47)), (0, 255, 0))
    for x in range(49, 60):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    img = cv2.line(img, totuple(shape.part(48)), totuple(shape.part(59)), (0, 255, 0))
    for x in range(61, 68):
        img = cv2.line(img, totuple(shape.part(x)), totuple(shape.part(x - 1)), (0, 255, 0))
    img = cv2.line(img, totuple(shape.part(60)), totuple(shape.part(67)), (0, 255, 0))
    return img

# From this point are function for calculating features
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

    data = open(sys.argv[2]).read()
    ldata = np.fromstring(data, sep=",")

    for i in range(len(ldata)):
        res.append(res[i] - ldata[i])

    print("Size of feature: {}".format(len(res)))
    return res

# Convert python list to svmnode format
def svmnode_cvr(res):
    print("Length res = {}".format(len(res)))
    node = {}
    for i in range(1,105):
        node[i] = res[i]
    return node

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(sys.argv[1])
model = svm_load_model(sys.argv[3])
# win = dlib.image_window()

cv2.setUseOptimized(True)

# Record and predict through live camera
def enable_cam():
    cap = cv2.VideoCapture(0)

    a = []

    while (True):
        ret, img = cap.read()

        # win.clear_overlay()
        # win.set_image(img)

        dets = detector(img, 1)

        if len(dets) != 0:
            shape = predictor(img, dets[0])

            # a = shape
            # break
            x0, idx = gen_svm_nodearray(svmnode_cvr(feature_calc(shape)))
            print(libsvm.svm_predict(model, x0))

            img = draw_img(img, shape)

        # break

        # win.add_overlay(shape)

        cv2.imshow('cam', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()

    # tmp = feature_calc(a)

# Process image with input label from folder
def proc_img():
    data = ""
    for f in glob.glob(os.path.join(sys.argv[4], "*.jpg")):
        print("Processing file: {}".format(f))
        img = io.imread(f)

        dets = detector(img, 1)

        if len(dets) != 0:
            data += str(sys.argv[6]) + ' '
            shape = predictor(img, dets[0])
            result = feature_calc(shape)

            for i in range(1,len(result)+1):
                if i != len(result):
                    data += str(i) + ':' + str(result[i-1]) + ' '
                else:
                    data += str(i) + ':' + str(result[i-1]) + '\n'

    with open(sys.argv[5],'w') as fout:
        fout.write(data)
        print("Written to {}".format(sys.argv[5]))

# proc_img()

