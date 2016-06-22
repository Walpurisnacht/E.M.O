#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#include <iostream>
#include <cmath>

#include "svm.h"
#include "feature_calculator.h"
#include "img_proc.h"

using namespace dlib;
using namespace std;
using namespace cv;

void test_shape(full_object_detection &shape, cv::Mat &src)
{
    dlib::point mid(src.cols/2, src.rows/2);
	float angle = getAngle(shape.part(31),shape.part(35));
	cout << "Angle(rad) " << angle << endl;

    rotateImg(src, angle);
    cv::imshow("Rotated", src);
    cv::waitKey(0);
    cv::destroyAllWindows();

    for (size_t i = 0; i < 68; i++) {
        shape.part(i) = rotatePoint(mid, -angle, shape.part(i));
    }

    src = cropFace(src, shape);

    float rat = resizeImg(src);
    cout << "Ratio " << rat << endl;

    imshow("Processed", src);
    waitKey(0);
    destroyAllWindows();
}

void test()
{
	dlib::point pts(0,2);
	cout << rotatePoint(dlib::point(1,1),pi/4,pts) << endl;
}

int main(int argc, char** argv)
{
//	test();
//	return 1;
    cv::setUseOptimized(true);
	try
	{
		if (argc == 1)
		{
			cout << "Call this program like this:" << endl;
			cout << "[app] [model] [svm] [csv] [img]" << endl;
			return 0;
		}

		frontal_face_detector detector = get_frontal_face_detector();

		shape_predictor sp;
		deserialize(argv[1]) >> sp;

		struct svm_model* model = svm_load_model(argv[2]);

		image_window win, win_faces;
		for (int i = 4; i < argc; i++)
		{
			cout << "Processing image: " << argv[i] << endl;

			array2d<rgb_pixel> img;
			load_image(img, argv[i]);
			pyramid_up(img);

			std::vector<dlib::rectangle> dets = detector(img);
			cout << "Number of faces detected: " << dets.size() << endl;

			std::vector<full_object_detection> shapes;
			std::vector<std::vector<double>> features;
			for (size_t j = 0; j < dets.size(); j++)
			{
				full_object_detection shape = sp(img, dets[j]);
				features.push_back(feature_calculator(shape,argv[3]));
				//Debug
//				cv::Mat cv_img = dlib::toMat(img);
//				test_shape(shape, cv_img);
			}
			//Debug
//			continue;

			win.clear_overlay();
			win.set_image(img);
			win.add_overlay(render_face_detections(shapes));

			dlib::array<array2d<rgb_pixel>> face_chips;
			extract_image_chips(img, get_face_chip_details(shapes),face_chips);
			win_faces.set_image(tile_images(face_chips));

			if (dets.size() == 0) continue;

			size_t n = features[0].size()+1;

			struct svm_node* node = new svm_node[n];
			node[n-1].index = -1;

			for (size_t i = 0; i < features.size(); i++)
		   {
				for (size_t j = 0; j < features[i].size(); j++)
				{
					node[j].index = j+1;
					node[j].value = features[i][j];
				}
			   	cout << "Face " << i << " result: " << svm_predict(model,node) << endl;
		   }

			cout << "Hit enter to process next image..." << endl;
			cin.get();
			delete node;
		}
		delete model;
	}
	catch (exception& e)
	{
		cout << e.what() << endl;
	}
}
