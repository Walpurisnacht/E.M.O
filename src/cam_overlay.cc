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

        // Set parameter for saving image
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

//			cv::imshow("ORIGIN",temp);
//			cv::waitKey(0);
//			cv::destroyAllWindows();

//            cout << "Cam res" << endl;
//			cout << temp.cols << " " << temp.rows << endl;

			//cv::Mat layer = cv::imread("sad.png",1);

			//overlayImage(temp, layer, temp, cv::Point(0,0));

			cv_image<bgr_pixel> cimg(temp);

			// Detect faces
            std::vector<dlib::rectangle> faces = detector(cimg);

//            cout << "Cam bounding box" << endl;
//            cout << faces[0] << endl;

            // Find the pose of ONE face.
            std::vector<full_object_detection> shapes;
//            shapes.push_back(pose_model(cimg, faces[0]));
            for (unsigned long i = 0; i < faces.size(); ++i)
                shapes.push_back(pose_model(cimg, faces[i]));

            std::vector<full_object_detection> view = shapes;

			if (shapes.size() == 0 || checkShape(shapes[0]))
			{
				win.clear_overlay();
				win.set_image(cimg);
                printf("No face detected!\n");
				continue;
			}

			//win.clear_overlay();
			//win.set_image(cimg);

			//Record mode, bypass prediction
			if (argv[4][0] == '1' && shapes.size() != 0)
			{
				if (stat(argv[5],&st) == -1) {
                    cout << "rm stat = " << system("rm -r ./save/") << endl;
					mkdir(argv[5], 0700);
				}
				win.clear_overlay();
				win.set_image(cimg);
				imwrite(argv[5] + to_string(static_cast<long long>(cnt)) + ".jpg", temp, compression_params);
				cout << "Writing frame " << cnt << " to " << argv[5] << endl;
				cnt++;

				continue;
			}

			//Preprocess image
			cv::Mat proc = temp.clone();

//			cv::imshow("TEMP",temp);
//			cv::imshow("PROC",proc);
//			cv::waitKey(0);
//			cv::destroyAllWindows();

			dlib::point mid(proc.cols/2, proc.rows/2);
			full_object_detection shape = shapes[0];
			float angle = getAngle(shape.part(31), shape.part(35));
//			cout << "Angle " << angle << endl;

            //Rotate img
			cv::Mat rot_mat = rotateImg(proc, angle);

//			cout << "Rotating..." << endl;

            cv_rotatePoint(angle, shape, rot_mat);

//            cv::imshow("TEMP_ROT",temp);
//			cv::imshow("PROC_ROT",proc);
//			cv::waitKey(0);
//			cv::destroyAllWindows();

            //Calc pts after rotate
//			for (size_t i = 0; i < 68; i++) {
                //shape.part(i) = rotatePoint(mid, -angle, shape.part(i));
//                shape.part(i) = cv_rotatePoint(angle, shape.part(i), rot_mat);
//                cout << "Point " << i << " " << shape.part(i) << endl;
//            }
            shapes[0] = shape;
//            win.clear_overlay();
//			win.set_image(cimg);
//
//			win.add_overlay(render_face_detections(shapes));
//			continue;


            //Crop face landmark
			std::map<std::string,long> data;
			if (!cropFace(proc, shape, data))
                continue;

//			cv::imshow("TEMP_CROP",temp);
//			cv::imshow("PROC_CROP",proc);
//			cv::imshow("FIX_CROP",proc);
//			cv::waitKey(0);
//			cv::destroyAllWindows();

//			imwrite(argv[5] + to_string(static_cast<long long>(cnt)) + "_crop.jpg", fixed, compression_params);

            //Resize image to width 100
			float rat = resizeImg(proc);

			//Calc pts after resize
//			cout << "Resizing..." << endl;
			for (size_t i = 0; i < 68; i++) {
                shape.part(i).x() -= (data["x_min"] - 10);
                shape.part(i).x() *= rat;
                shape.part(i).y() -= (data["y_min"] - 10);
                shape.part(i).y() *= rat;
//                cout << "Point " << i << " " << shape.part(i) << endl;
			}

			cv_render_face_detection(proc, shape);

//			cout << "Processed!" << endl;

//			cv::imshow("SRC_RES",temp);
//			cv::imshow("PROC_RES",proc);
//			cv::imshow("FIX_RES",fixed);
//			cv::waitKey(0);
//			cv::destroyAllWindows();

			win.clear_overlay();
			win.set_image(cimg);

			win.add_overlay(render_face_detections(view));

			//Save img
//			if (stat(argv[5],&st) == -1) {
//                cout << "rm stat = " << system("rm -r ./save/") << endl;
//                mkdir(argv[5], 0700);
//            }


//            imwrite(argv[5] + to_string(static_cast<long long>(cnt)) + "_proc.jpg", fixed, compression_params);
//            cout << "Writing frame " << cnt << " to " << argv[5] << endl;
//            cnt++;
//            continue;


			//Feature calculator
			std::vector<double> feature = feature_calculator(shape,argv[3]);

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
