import sys
import os
import dlib
import glob
from skimage import io
from PyQt4.QtGui import *
from PyQt4.QtCore import *

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
            with open(f[:-4] + ".pts",'w') as fout:
                data = "version: 1\nn_points: 68\n{\n"
                for x in range(68):
                    data += str(shape.part(x))[1:-1].replace(',','')
                    if not x == 67:
                        data += "\n"
                data += "}"
                fout.write(data)
                fout.close()
            print("Printed to" + f[:-4] + ".pts")


    # win.add_overlay(dets)
    # dlib.hit_enter_to_continue()

print("PROCESS COMPLETED")