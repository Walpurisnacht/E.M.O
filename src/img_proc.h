#include <dlib/image_processing/render_face_detections.h>
#include <dlib/geometry/vector.h>

#include <dlib/opencv.h> //opencv core included
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
#include <string>
#include <map>

using namespace std;
using namespace dlib;
using namespace cv;

inline bool comp(long a, long b) { return a < b;}

inline bool any_comp(dlib::point pts) { return (pts.x() < 0 || pts.y() < 0);}

void cv_rotatePoint(float angle, dlib::full_object_detection &shape, cv::Mat rot_mat);

void cv_render_face_detection(cv::Mat &src, dlib::full_object_detection shape);

void cv_draw_arc(size_t start, size_t end, cv::Mat &src, dlib::full_object_detection shape);

cv::Mat rotateImg(cv::Mat &src, float angle);

float getAngle(dlib::point p0, dlib::point p1);

std::vector<long> getVector(dlib::full_object_detection shape, bool x);

bool cropFace(cv::Mat &src, dlib::full_object_detection shape, std::map<std::string,long> &data);

float resizeImg(cv::Mat &src);

void overlayImage(const cv::Mat &background, const cv::Mat &foreground, cv::Mat &output, cv::Point2i location);

bool checkShape(dlib::full_object_detection shape);

long getMax(dlib::full_object_detection shape,bool x);

long getMin(dlib::full_object_detection shape,bool x);
