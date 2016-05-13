import numpy as np
from skimage import io
import dlib
import cv2

predictor_path = "/home/walpurisnacht/Project Gesture/EMO/model/model.dat"

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
win = dlib.image_window()

while(True):
    ret, img = cap.read()

    #img = io.imread(frame)

    win.clear_overlay()
    win.set_image(img)

    dets = detector(img, 1)

    shape = predictor(img, dets[0])
    win.add_overlay(shape)

cap.release()

"""try:
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    win = dlib.image_window()
    win.wait_until_closed()

    frame = cap.read()"""
