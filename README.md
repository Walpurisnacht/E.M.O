EMO Version 1.2
===============================

-----Feature-----
Recognize human's facial emotion through facial landmark.
All emotions are categorized into 3 primal type: positive, neutral, negative

-----Build tips-----
- Include dlib source.cpp to compile dlib library (no static/shared lib in source code)
- Include opencv through pkg-config
- Enable AVX instructions for better performance

Sample build: g++ -pg -g -O3 -std=c++11 -mavx -DDLIB_JPEG_SUPPORT -I /usr/include/ cam_overlay.cc feature_calculator.cc img_proc.cc /usr/include/dlib/all/source.cpp libsvm.a -o cam_overlay `pkg-config opencv --cflags --libs` -lpthread -lX11 -ljpeg

-----Usage-----
Call the app like this
./app [path to face model] [path to svm model] [path to neutral.csv] [record flag 0/1] [path to save img in record mode]

EX: ./app ./model.dat ./pk.model ./neutral.csv 0

-----Unsolved bug-----
Throw exception in cv::VideoCapture when given a half face