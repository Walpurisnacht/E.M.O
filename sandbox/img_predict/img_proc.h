#include <dlib/image_processing/render_face_detections.h>
#include <dlib/geometry/vector.h>

#include <dlib/opencv.h> //opencv core included
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;
using namespace dlib;
using namespace cv;

inline bool comp(long a, long b) { return a < b;}

dlib::point rotatePoint(dlib::point pivot, float angle, dlib::point pts);

void rotateImg(cv::Mat &src, float angle);

float getAngle(dlib::point p0, dlib::point p1);

std::vector<long> getVector(dlib::full_object_detection shape, bool x);

cv::Mat cropFace(cv::Mat src, dlib::full_object_detection shape);

float resizeImg(cv::Mat &src);

void overlayImage(const cv::Mat &background, const cv::Mat &foreground, cv::Mat &output, cv::Point2i location);
