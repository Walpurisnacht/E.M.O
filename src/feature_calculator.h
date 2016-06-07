#ifndef FEARTURE_CALCULATOR_H_INCLUDED
#define FEARTURE_CALCULATOR_H_INCLUDED


#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#include <dlib/geometry/vector.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>


using namespace dlib;
using namespace std;

inline double eccentricity_calculator(double a, double b)
{
    return sqrt(abs(a*a - b*b))/a;
}

void eccentricities_calculator(full_object_detection shape, std::vector<double> &result);

void linear_calculator(full_object_detection shape, std::vector<double> &result);

//void feature_calculator_13(full_object_detection shape, std::vector<double> &result);

//void feature_calculator_26(full_object_detection shape, std::string path, std::vector<double> &result);

std::vector<double> feature_calculator(full_object_detection shape,std::string path);



#endif // FEARTURE_CALCULATOR_H_INCLUDED
