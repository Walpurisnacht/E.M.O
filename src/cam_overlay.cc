#include <dlib/opencv.h>
#include <opencv2/highgui/highgui.hpp>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <ctime>
#include "feature_calculator.h"
#include "svm.h"

using namespace std;
using namespace dlib;


void overlayImage(const cv::Mat &background, const cv::Mat &foreground, 
  cv::Mat &output, cv::Point2i location)
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

int main(int argc, char** argv)
{
	try
	{
		if (argc == 1)
		{
			cout << "Call this program like this:" << endl;
			cout << "[app] [face model] [svm model] [neutral.csv]" << endl;
			return 0;
		}
		
		cv::VideoCapture cap(0);
		image_window win;
		
		// Load face detection and pose estimation models.
        frontal_face_detector detector = get_frontal_face_detector();
        shape_predictor pose_model;
        deserialize(argv[1]) >> pose_model;
		
		// Load SVM model
		struct svm_model* model = svm_load_model(argv[2]);
		
		while (!win.is_closed())
		{
			cv::Mat temp;
			cap >> temp;
			
			//cv::Mat layer = cv::imread("sad.png",1);
			
			//overlayImage(temp, layer, temp, cv::Point(0,0));
			
			cv_image<bgr_pixel> cimg(temp);
			
			// Detect faces 
            std::vector<rectangle> faces = detector(cimg);
            // Find the pose of each face.
            std::vector<full_object_detection> shapes;
            for (unsigned long i = 0; i < faces.size(); ++i)
                shapes.push_back(pose_model(cimg, faces[i]));
			
			if (shapes.size() == 0)
			{
				win.clear_overlay();
				win.set_image(cimg);
			
				win.add_overlay(render_face_detections(shapes));
				continue;
			}
			//Feature calculator
			std::vector<double> feature = feature_calculator(shapes[0],argv[3]);
			
			size_t n = feature.size()+1;
			
			//Node preparation
			struct svm_node* node = new svm_node[n];
			for (size_t i = 0; i < n; i++)
			{
				node[i].index = i+1;
				node[i].value = feature[i];
			}
			node[n-1].index = -1;
			
			//Predict result + overlay cam
			double result = svm_predict(model,node);
			time_t now = time(0);
			char* dt = ctime(&now);
			std::cout << dt << " " << result << std::endl;
			if (result == -1)
				overlayImage(temp, cv::imread("sad.png",1), temp, cv::Point(0,0));
			else if (result == 0)
				overlayImage(temp, cv::imread("normal.png",1), temp, cv::Point(0,0));
			else if (result == 1)
				overlayImage(temp, cv::imread("smile.png",1), temp, cv::Point(0,0));
			
			win.clear_overlay();
			win.set_image(cimg);
			
			win.add_overlay(render_face_detections(shapes));
			//win.add_overlay(rectangle(0,0,0,0),rgb_pixel(255,0,0),"HELLO WORLD");
		}
								 
		delete model;
	}
	catch(serialization_error& e)
    {
        cout << "You need dlib's default face landmarking model file to run this example." << endl;
        cout << "You can get it from the following URL: " << endl;
        cout << "   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2" << endl;
        cout << endl << e.what() << endl;
    }
    catch(exception& e)
    {
        cout << e.what() << endl;
    }
}