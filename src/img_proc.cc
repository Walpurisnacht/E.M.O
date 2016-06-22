#include "img_proc.h"

//dlib::point rotatePoint(dlib::point pivot, float angle, dlib::point pts)
//{
//	float s = sin(angle);
//	float c = cos(angle);
//
//	pts.x() -= pivot.x();
//	pts.y() -= pivot.y();
//
//	float x1 = pts.x() * c - pts.y() * s;
//	float y1 = pts.x() * s + pts.y() * c;
//
//	return dlib::point(x1+pivot.x(),y1+pivot.y());
//}

bool checkShape(dlib::full_object_detection shape)
{
    std::vector<dlib::point> data;
    for (size_t i = 0; i < 68; i++)
        data.push_back(shape.part(i));
    return std::any_of(data.begin(), data.end(), any_comp);
}

void cv_rotatePoint(float angle, dlib::full_object_detection &shape, cv::Mat rot_mat)
{
    for (size_t i = 0; i < 68; i++)
        shape.part(i) = dlib::point(rot_mat.at<double>(0,0)*shape.part(i).x() + rot_mat.at<double>(0,1)*shape.part(i).y() + rot_mat.at<double>(0,2), rot_mat.at<double>(1,0)*shape.part(i).x() + rot_mat.at<double>(1,1)*shape.part(i).y() + rot_mat.at<double>(1,2));
}

cv::Mat rotateImg(cv::Mat &src, float angle)
{
    cv::Mat rot_mat = cv::getRotationMatrix2D(cv::Point(src.cols/2,src.rows/2), angle, 1.0);
    cv::warpAffine(src,src,rot_mat,src.size());
    return rot_mat;
}

float getAngle(dlib::point p0, dlib::point p1)
{
    dlib::point delta(p1.x()-p0.x(),p1.y()-p0.y());
    return (std::atan2(delta.y(),delta.x())*180)/(std::atan(1)*4);
}

std::vector<long> getVector(dlib::full_object_detection shape, bool x)
{
    std::vector<long> data;
    for (size_t i = 0; i < 68; i++)
    {
        if (x)
            data.push_back(shape.part(i).x());
        else
            data.push_back(shape.part(i).y());
    }
    return data;
}

bool cropFace(cv::Mat &src, dlib::full_object_detection shape, std::map<std::string,long> &data)
{
    std::vector<long> x = getVector(shape, true);
    std::vector<long> y = getVector(shape, false);

//    for (size_t i = 0; i < 68; i++)
//        cout << "Point " << i << " " << shape.part(i) << endl;

    long x_max = *std::max_element(x.begin(), x.end(), comp);
    long x_min = *std::min_element(x.begin(), x.end(), comp);
    long y_max = *std::max_element(y.begin(), y.end(), comp);
    long y_min = *std::min_element(y.begin(), y.end(), comp);

//    cout << "Source bounding box" << endl;
//    printf("%ld %ld %ld %ld\n",x_max,y_max,x_min,y_min);

    if (checkShape(shape))
        return false;

//    cout << "Dimension ";



    src = src(cv::Rect(x_min-10,y_min-10,x_max-x_min+20,y_max-y_min+20));
//    src = src(cv::Rect(box.top()-10,box.left()-10,box.bottom()-box.top()+10,box.right()-box.left()+10));

    data["x_max"] = x_max;
    data["y_max"] = y_max;
    data["x_min"] = x_min;
    data["y_min"] = y_min;

//    cout << src.cols << " " << src.rows << endl;

    return true;
}

float resizeImg(cv::Mat &src)
{
    float rat = 100.0 / src.cols;
    cv::Size dim(100, (int) src.rows*rat);
    cv::resize(src,src,dim);
    return rat;
}

void cv_draw_arc(size_t start, size_t end, cv::Mat &src, dlib::full_object_detection shape)
{
    for (size_t z = start; z <= end; ++z)
	{
		cv::line(src, cv::Point(shape.part(z).x(),shape.part(z).y()), cv::Point(shape.part(z-1).x(),shape.part(z-1).y()), cv::Scalar(0,255,0));
	}
}

void cv_render_face_detection(cv::Mat &src, dlib::full_object_detection shape)
{
    cv_draw_arc(1, 16, src, shape);
    cv_draw_arc(28, 30, src, shape);
    cv_draw_arc(18, 21, src, shape);
    cv_draw_arc(23, 26, src, shape);
    cv_draw_arc(31, 35, src, shape);
    cv::line(src, cv::Point(shape.part(30).x(),shape.part(30).y()), cv::Point(shape.part(35).x(),shape.part(35).y()), cv::Scalar(0,255,0));
    cv_draw_arc(37, 41, src, shape);
    cv::line(src, cv::Point(shape.part(36).x(),shape.part(36).y()), cv::Point(shape.part(41).x(),shape.part(41).y()), cv::Scalar(0,255,0));
    cv_draw_arc(43, 47, src, shape);
    cv::line(src, cv::Point(shape.part(42).x(),shape.part(42).y()), cv::Point(shape.part(47).x(),shape.part(47).y()), cv::Scalar(0,255,0));
    cv_draw_arc(49, 59, src, shape);
    cv::line(src, cv::Point(shape.part(48).x(),shape.part(48).y()), cv::Point(shape.part(59).x(),shape.part(59).y()), cv::Scalar(0,255,0));
    cv_draw_arc(61, 67, src, shape);
    cv::line(src, cv::Point(shape.part(60).x(),shape.part(60).y()), cv::Point(shape.part(67).x(),shape.part(67).y()), cv::Scalar(0,255,0));
}

void overlayImage(const cv::Mat &background, const cv::Mat &foreground, cv::Mat &output, cv::Point2i location)
{
  background.copyTo(output);


  // start at the row indicated by location, or at row 0 if location.y is negative.
  for(int y = std::max(location.y , 0); y < background.rows; ++y)
  {
    int fY = y - location.y; // because of the translation

    // we are done of we have processed all rows of the foreground image.
    if(fY >= foreground.rows)
      break;

    // start at the column indicated by location,

    // or at column 0 if location.x is negative.
    for(int x = std::max(location.x, 0); x < background.cols; ++x)
    {
      int fX = x - location.x; // because of the translation.

      // we are done with this row if the column is outside of the foreground image.
      if(fX >= foreground.cols)
        break;

      // determine the opacity of the foregrond pixel, using its fourth (alpha) channel.
      double opacity =
        ((double)foreground.data[fY * foreground.step + fX * foreground.channels() + 3])

        / 255.;


      // and now combine the background and foreground pixel, using the opacity,

      // but only if opacity > 0.
      for(int c = 0; opacity > 0 && c < output.channels(); ++c)
      {
        unsigned char foregroundPx =
          foreground.data[fY * foreground.step + fX * foreground.channels() + c];
        unsigned char backgroundPx =
          background.data[y * background.step + x * background.channels() + c];
        output.data[y*output.step + output.channels()*x + c] =
          backgroundPx * (1.-opacity) + foregroundPx * opacity;
      }
    }
  }
}
