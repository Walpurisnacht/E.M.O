#include "feature_calculator.h"
#include "svm.h"
#include "img_proc.h"
#include "cam_overlay.h"

int main(int argc, char** argv)
{
    struct stat st;
    cv::setUseOptimized(true);

	try
	{
		int cnt = 0;

		if (argc == 1)
		{
			cout << "Call this program like this:" << endl;
			cout << "[app] [face model] [svm model] [neutral.csv] [record] [save path]" << endl;
			return 0;
		}

        // Set parameter for saving image in recording mode
        std::vector<int> compression_params;
        compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
        compression_params.push_back(100);

        // Init camera + preview window
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

			cv_image<bgr_pixel> cimg(temp);

			// Detect faces
            std::vector<dlib::rectangle> faces = detector(cimg);

            // Find landmark of all face detected
            std::vector<full_object_detection> shapes;
            for (unsigned long i = 0; i < faces.size(); ++i)
                shapes.push_back(pose_model(cimg, faces[i]));

            std::vector<full_object_detection> view = shapes;

			// Only view source without detection
			if (shapes.size() == 0 || checkShape(shapes[0]))
			{
				win.clear_overlay();
				win.set_image(cimg);
                printf("No face detected!\n");
				continue;
			}

			// Record mode, bypass prediction
//			if (argv[4][0] == '1' && shapes.size() != 0)
//			{
//				if (stat(argv[5],&st) == -1) {
//                    cout << "rm stat = " << system("rm -r ./save/") << endl;
//					mkdir(argv[5], 0700);
//				}
//				win.clear_overlay();
//				win.set_image(cimg);
//				imwrite(argv[5] + to_string(static_cast<long long>(cnt)) + ".jpg", temp, compression_params);
//				cout << "Writing frame " << cnt << " to " << argv[5] << endl;
//				cnt++;
//
//				continue;
//			}

			// Preprocess image
            cv::Mat proc;
            temp.copyTo(proc);

			dlib::point mid(proc.cols/2, proc.rows/2);

			// Create a new copy to process for predicting
			full_object_detection shape = shapes[0];
			float angle = getAngle(shape.part(31), shape.part(35));

            // Rotate img with pivot as the center of image
			cv::Mat rot_mat = rotateImg(proc, angle);

            cv_rotatePoint(angle, shape, rot_mat);
//            shapes[0] = shape;


            // Crop face landmark
			std::map<std::string,long> data;
			if (!cropFace(proc, shape, data)) {
                win.clear_overlay();
				win.set_image(cimg);
                printf("No face detected!\n");
				continue;
			}

            // Resize image to 100 px wide
			float rat = resizeImg(proc);

			// Calculate landmark points after resized
			for (size_t i = 0; i < 68; i++) {
                shape.part(i).x() -= (data["x_min"] - 10);
                shape.part(i).x() *= rat;
                shape.part(i).y() -= (data["y_min"] - 10);
                shape.part(i).y() *= rat;
			}

			// Redraw facial landmark on image
			cv_render_face_detection(proc, shape);

			// Feature calculator from processed landmarks
			std::vector<double> feature = feature_calculator(shape,argv[3]);

			size_t n = feature.size()+1;

			// Node preparation following libSVM format
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

			cv_render_face_detection(temp, shapes[0]);
			if (argv[4][0] == '1') {
                cv::VideoWriter outputVid;
				cv::Size S = cv::Size((int) cap.get(CV_CAP_PROP_FRAME_WIDTH),
				(int) cap.get(CV_CAP_PROP_FRAME_HEIGHT));
				int ex = static_cast<int>(cap.get(CV_CAP_PROP_FOURCC));
				outputVid.open(argv[5], ex, cap.get(CV_CAP_PROP_FPS), S, true);
				if (!outputVid.isOpened())
                    continue;
                outputVid << temp;
            }

			if (result == -1)
				overlayImage(temp, cv::imread("sad.png",1), temp, cv::Point(0,0));
			else if (result == 0)
				overlayImage(temp, cv::imread("normal.png",1), temp, cv::Point(0,0));
			else if (result == 1)
				overlayImage(temp, cv::imread("smile.png",1), temp, cv::Point(0,0));

			win.clear_overlay();
			win.set_image(cimg);

//			win.add_overlay(render_face_detections(shapes));
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
