EMO Version 1.2
===============================

-----Feature-----
* Recognize human's facial emotion through facial landmark.
* All emotions are categorized into 3 primal type: positive, neutral, negative
* Possible inputs are live webcam or video input

-----Requirements-----
* OpenCV 2.x is required. Follow these instructions to install:
http://docs.opencv.org/2.4.13/doc/tutorials/introduction/linux_install/linux_install.html?highlight=install
* dlib 18.18 is required. Download the source code from dlib.net and follow build tips to include dlib library in project. More information:
http://dlib.net/compile.html

-----Build tips-----
* Run make to compile, by default dlib library is installed into root
* In case of linking to dlib specific folder, fix source.cpp and include files location in makefile
* Stand-alone build:
g++ -O3 -std=c++11 -mavx -DDLIB_JPEG_SUPPORT -I [path to dlib include files] [source codes] [dlib source.cpp] libsvm.a -o emo `pkg-config opencv --cflags --libs` -lpthread -lx11 -ljpeg

-----Usage-----
Call the app like this
./emo [options]

Options:
-s : data in different locations, set path to [face_model] [svm_model] [neutral.csv]
-r [path]: toggle frame extractor, set path to save image
-v [path]: video input from path
-a [path]: all data in [path]

Example:
./emo -a ~/EMO/src -r ~/EMO/save/